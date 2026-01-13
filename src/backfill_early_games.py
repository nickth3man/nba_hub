import csv
import os
import time
import requests
from bs4 import BeautifulSoup
import duckdb
from datetime import datetime
import argparse
import sys

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
    url = f"https://www.basketball-reference.com/leagues/{league}_{year}_games.html"
    print(f"Scraping {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "schedule"})

    if not table:
        print("Could not find schedule table.")
        return []

    games = []
    # Iterate over rows in tbody
    tbody = table.find("tbody")
    if not tbody:
        return []

    for tr in tbody.find_all("tr"):
        if "class" in tr.attrs and "thead" in tr.attrs["class"]:
            continue  # Skip header rows repeated in table

        # Date
        date_th = tr.find("th", {"data-stat": "date_game"})
        if not date_th:
            continue
        date_str = date_th.get_text()
        csk = date_th.get("csk")  # e.g. 194611010TRH

        # Visitor
        visitor_td = tr.find("td", {"data-stat": "visitor_team_name"})
        visitor_name = visitor_td.get_text() if visitor_td else ""

        # Home
        home_td = tr.find("td", {"data-stat": "home_team_name"})
        home_name = home_td.get_text() if home_td else ""

        # Scores
        visitor_pts_td = tr.find("td", {"data-stat": "visitor_pts"})
        visitor_pts = visitor_pts_td.get_text() if visitor_pts_td else ""

        home_pts_td = tr.find("td", {"data-stat": "home_pts"})
        home_pts = home_pts_td.get_text() if home_pts_td else ""

        # Attendance
        attend_td = tr.find("td", {"data-stat": "attendance"})
        attendance = attend_td.get_text().replace(",", "") if attend_td else ""

        # Arena
        arena_td = tr.find("td", {"data-stat": "arena_name"})
        arena = arena_td.get_text() if arena_td else ""

        # Parse Date
        dt = None
        try:
            # Format: "Fri, Nov 1, 1946"
            dt = datetime.strptime(date_str, "%a, %b %d, %Y")
            # Set a default time? The existing data has times.
            # I'll just use the date part or set to 00:00:00 or 19:00:00 (7 PM) as a guess?
            # Existing data: 2026-01-09 17:30:00.
            # I'll set it to 19:00:00 EST as a placeholder for historical games.
            game_datetime = dt.strftime("%Y-%m-%d 19:00:00")
        except ValueError:
            game_datetime = date_str  # Keep original if parse fails

        # Map Teams
        home_id = get_team_id(home_name, team_map)
        away_id = get_team_id(visitor_name, team_map)

        # Split City/Name
        # This is tricky. "New York Knicks" -> City="New York", Name="Knicks"
        # "St. Louis Bombers" -> City="St. Louis", Name="Bombers"
        # I'll use a simple heuristic: Last word is name, rest is city.
        # EXCEPT for "Trail Blazers", "SuperSonics" (sometimes one word), "Red Skins".
        # I'll rely on the full name for now, but the CSV schema requires City and Name separately.

        def split_team_name(full_name):
            parts = full_name.split()
            if not parts:
                return "", ""
            if full_name == "Portland Trail Blazers":
                return "Portland", "Trail Blazers"
            if full_name == "Sheboygan Red Skins":
                return "Sheboygan", "Red Skins"
            # Add more exceptions if needed
            return " ".join(parts[:-1]), parts[-1]

        home_city, home_team_name = split_team_name(home_name)
        away_city, away_team_name = split_team_name(visitor_name)

        # Winner
        winner = ""
        try:
            h_score = int(home_pts)
            v_score = int(visitor_pts)
            if h_score > v_score:
                winner = home_id
            else:
                winner = away_id
        except ValueError:
            pass  # Scores might be empty if game hasn't happened (unlikely for 1947) or data missing

        # Game ID
        # Use csk if available, else generate
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
            "gameType": "Regular Season",  # Assumption
            "attendance": attendance,
            "arenaId": "",  # No arena ID mapping
            "gameLabel": "",
            "gameSubLabel": "",
            "seriesGameNumber": "",
        }
        games.append(game_row)

    return games


def update_duckdb():
    print("Refreshing DuckDB...")
    con = duckdb.connect(DB_FILE)
    # Drop and recreate or just append?
    # The prompt says "refreshes DuckDB".
    # Safest is to recreate the table from the CSV.
    con.sql(
        f"CREATE OR REPLACE TABLE games AS SELECT * FROM read_csv_auto('{GAMES_FILE}')"
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
