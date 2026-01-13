import csv
import os
import time
import requests
from bs4 import BeautifulSoup
import duckdb
from datetime import datetime
import argparse
import sys
import random

# Configuration
DATA_DIR = "data/raw"
GAMES_FILE = os.path.join(DATA_DIR, "Games.csv")
TEAM_HISTORIES_FILE = os.path.join(DATA_DIR, "TeamHistories.csv")
DB_FILE = "data/nba.duckdb"

# Manual overrides for team mapping if simple string matching fails
TEAM_OVERRIDES = {
    "Fort Wayne Pistons": 1610612765,  # Ft. Wayne Zollner Pistons
    "Tri-Cities Blackhawks": 1610612737,
    "Minneapolis Lakers": 1610612747,
    "Rochester Royals": 1610612758,
    "Syracuse Nationals": 1610612755,
    "Indianapolis Olympians": 9058,
    "Washington Capitols": 9015,  # Or 1610612764? TeamHistories has multiple entries. 9015 is BAA/NBA 1946-1949.
    "Anderson Packers": 9028,
    "Sheboygan Red Skins": 9063,  # Check spelling "Redskins" vs "Red Skins"
    "Waterloo Hawks": 9002,
    "Denver Nuggets": 9070,  # Old Denver Nuggets (1949-50)
    "Baltimore Bullets": 9071,  # Old Baltimore Bullets (1944-1954)
}


def load_team_map():
    team_map = {}
    with open(TEAM_HISTORIES_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            full_name = f"{row['teamCity']} {row['teamName']}"
            team_id = row["teamId"]
            team_map[full_name] = team_id

            # Also map just the city if unique? No, dangerous.
            # Map "City Name" -> ID

    # Add overrides
    team_map.update(TEAM_OVERRIDES)

    # Add specific fixes based on known BAA/early NBA teams
    team_map["St. Louis Bombers"] = "9012"
    team_map["Chicago Stags"] = "9059"
    team_map["Detroit Falcons"] = "9020"
    team_map["Toronto Huskies"] = "9042"
    team_map["Washington Capitols"] = "9015"
    team_map["Cleveland Rebels"] = "9017"
    team_map["Pittsburgh Ironmen"] = "9001"
    team_map["Providence Steamrollers"] = "9056"
    team_map["Indianapolis Jets"] = "9008"
    team_map["Sheboygan Red Skins"] = "9063"  # Website might use space
    team_map["Sheboygan Redskins"] = "9063"
    team_map["Waterloo Hawks"] = "9002"
    team_map["Denver Nuggets"] = "9070"
    team_map["Baltimore Bullets"] = "9071"

    return team_map


def get_team_id(team_name, team_map):
    if team_name in team_map:
        return team_map[team_name]
    # Try fuzzy match or partials?
    # For now, return None and log warning
    print(f"Warning: Could not find ID for team '{team_name}'")
    return None


def scrape_season(year, team_map, dry_run=False):
    league = "BAA" if year < 1950 else "NBA"
    base_url = "https://www.basketball-reference.com"
    main_url = f"{base_url}/leagues/{league}_{year}_games.html"
    print(f"Scraping {main_url}...")

    # Try to read from local file first
    local_main_file = os.path.join("data/raw/html", f"{league}_{year}_games.html")
    content = None
    if os.path.exists(local_main_file):
        print(f"Reading from local file: {local_main_file}")
        with open(local_main_file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = fetch_url(main_url, local_main_file)

    if not content:
        return []

    soup = BeautifulSoup(content, "html.parser")

    # Find all month links
    month_links = []
    filter_div = soup.find("div", class_="filter")
    if filter_div:
        for a in filter_div.find_all("a"):
            if "_games-" in a["href"]:
                month_links.append(base_url + a["href"])

    # If no month links found, maybe they are all on one page or it's a different structure
    if not month_links:
        month_links = [main_url]

    all_games = []
    for url in month_links:
        # Generate local filename for month
        month_filename = url.split("/")[-1]
        local_month_file = os.path.join("data/raw/html", month_filename)

        month_content = None
        if os.path.exists(local_month_file):
            print(f"Reading from local file: {local_month_file}")
            with open(local_month_file, "r", encoding="utf-8") as f:
                month_content = f.read()
        else:
            print(f"Fetching {url}...")
            month_content = fetch_url(url, local_month_file)
            if month_content:
                time.sleep(random.uniform(3, 5))  # Be nice

        if month_content:
            all_games.extend(parse_games_table(month_content, team_map))

    return all_games


def fetch_url(url, local_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content
        # Save to local file for future use
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(content)
        return content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_games_table(content, team_map):
    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", {"id": "schedule"})

    if not table:
        print("Could not find schedule table.")
        return []

    games = []
    tbody = table.find("tbody")
    if not tbody:
        return []

    for tr in tbody.find_all("tr"):
        if "class" in tr.attrs and "thead" in tr.attrs["class"]:
            continue

        date_th = tr.find("th", {"data-stat": "date_game"})
        if not date_th:
            continue
        date_str = date_th.get_text()
        csk = date_th.get("csk")

        visitor_td = tr.find("td", {"data-stat": "visitor_team_name"})
        visitor_name = visitor_td.get_text() if visitor_td else ""

        home_td = tr.find("td", {"data-stat": "home_team_name"})
        home_name = home_td.get_text() if home_td else ""

        visitor_pts_td = tr.find("td", {"data-stat": "visitor_pts"})
        visitor_pts = visitor_pts_td.get_text() if visitor_pts_td else ""

        home_pts_td = tr.find("td", {"data-stat": "home_pts"})
        home_pts = home_pts_td.get_text() if home_pts_td else ""

        attend_td = tr.find("td", {"data-stat": "attendance"})
        attendance = attend_td.get_text().replace(",", "") if attend_td else ""

        arena_td = tr.find("td", {"data-stat": "arena_name"})
        arena = arena_td.get_text() if arena_td else ""

        dt = None
        try:
            dt = datetime.strptime(date_str, "%a, %b %d, %Y")
            game_datetime = dt.strftime("%Y-%m-%d 19:00:00")
        except ValueError:
            game_datetime = date_str

        home_id = get_team_id(home_name, team_map)
        away_id = get_team_id(visitor_name, team_map)

        def split_team_name(full_name):
            parts = full_name.split()
            if not parts:
                return "", ""
            if full_name == "Portland Trail Blazers":
                return "Portland", "Trail Blazers"
            if full_name == "Sheboygan Red Skins":
                return "Sheboygan", "Red Skins"
            return " ".join(parts[:-1]), parts[-1]

        home_city, home_team_name = split_team_name(home_name)
        away_city, away_team_name = split_team_name(visitor_name)

        winner = ""
        try:
            h_score = int(home_pts)
            v_score = int(visitor_pts)
            if h_score > v_score:
                winner = home_id
            else:
                winner = away_id
        except ValueError:
            pass

        if csk:
            game_id = csk
        elif dt:
            game_id = f"{dt.strftime('%Y%m%d')}0{home_id}"
        else:
            game_id = f"UNKNOWN_{hash(date_str)}_{home_id}"

        game_row = {
            "gameId": game_id,
            "gameDateTimeEst": game_datetime,
            "hometeamCity": home_city,
            "hometeamName": home_team_name,
            "hometeamId": home_id,
            "awayteamCity": away_city,
            "awayteamName": away_team_name,
            "awayteamId": away_id,
            "homeScore": home_pts,
            "awayScore": visitor_pts,
            "winner": winner,
            "gameType": "Regular Season",
            "attendance": attendance,
            "arenaId": "",
            "gameLabel": "",
            "gameSubLabel": "",
            "seriesGameNumber": "",
        }
        games.append(game_row)

    return games


def update_duckdb():
    print("Refreshing DuckDB...")
    con = duckdb.connect(DB_FILE)
    # Explicitly cast gameId as VARCHAR to handle historical alphanumeric IDs
    con.sql(
        f"CREATE OR REPLACE TABLE games AS SELECT * FROM read_csv('{GAMES_FILE}', types={{'gameId': 'VARCHAR', 'hometeamId': 'VARCHAR', 'awayteamId': 'VARCHAR', 'winner': 'VARCHAR', 'arenaId': 'VARCHAR'}})"
    )
    print("DuckDB refreshed.")
    con.close()


def main():
    parser = argparse.ArgumentParser(description="Backfill early NBA games.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Run for 1947 only and do not save."
    )
    args = parser.parse_args()

    team_map = load_team_map()

    years_to_process = [1947] if args.dry_run else range(1947, 1956)

    all_new_games = []

    for year in years_to_process:
        print(f"Processing {year}...")
        games = scrape_season(year, team_map, args.dry_run)
        print(f"Found {len(games)} games for {year}.")
        all_new_games.extend(games)
        time.sleep(1)  # Be nice to the server

    if args.dry_run:
        print("Dry run complete. No data saved.")
        print(f"Total games found: {len(all_new_games)}")
        if len(all_new_games) > 0:
            print("Sample game:")
            print(all_new_games[0])
    else:
        # Append to CSV
        # First, check existing game IDs to avoid duplicates
        existing_ids = set()
        if os.path.exists(GAMES_FILE):
            with open(GAMES_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row["gameId"])

        new_games_count = 0
        with open(GAMES_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "gameId",
                    "gameDateTimeEst",
                    "hometeamCity",
                    "hometeamName",
                    "hometeamId",
                    "awayteamCity",
                    "awayteamName",
                    "awayteamId",
                    "homeScore",
                    "awayScore",
                    "winner",
                    "gameType",
                    "attendance",
                    "arenaId",
                    "gameLabel",
                    "gameSubLabel",
                    "seriesGameNumber",
                ],
            )
            # If file was empty (unlikely), write header. But we are appending.

            for game in all_new_games:
                if game["gameId"] not in existing_ids:
                    writer.writerow(game)
                    new_games_count += 1
                    existing_ids.add(game["gameId"])

        print(f"Added {new_games_count} new games to {GAMES_FILE}.")
        update_duckdb()


if __name__ == "__main__":
    main()
