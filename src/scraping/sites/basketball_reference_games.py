import argparse
import csv
import os
import re
import time

import requests
from bs4 import BeautifulSoup

from src.core.config import TEAM_HISTORIES_CSV
from src.core.database import get_db_connection


def load_team_map():
    """
    Loads a mapping of Team Abbreviation -> Team ID from TeamHistories.csv.
    """
    team_map = {}
    if not os.path.exists(TEAM_HISTORIES_CSV):
        print(f"Warning: {TEAM_HISTORIES_CSV} not found. Team mapping will be limited.")
        return team_map

    with open(TEAM_HISTORIES_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            abbrev = row["teamAbbrev"].strip()
            team_id = row["teamId"]
            if abbrev:
                team_map[abbrev] = team_id

    # Manual overrides for common mismatches if any
    team_map["PHO"] = "1610612756"  # Phoenix Suns (PHX in some, PHO in BR)
    team_map["BRK"] = "1610612751"  # Brooklyn Nets (BKN in some)
    team_map["CHO"] = "1610612766"  # Charlotte Hornets (CHA in some)

    return team_map


def get_nba_game_id(con, date_str, home_team_abbr, team_map):
    """
    Finds the NBA Game ID for a given date and home team.
    """
    # Convert date YYYYMMDD -> YYYY-MM-DD
    date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

    home_team_id = team_map.get(home_team_abbr)
    if not home_team_id:
        return None

    # Query DB
    query = """
        SELECT gameId
        FROM unified_games
        WHERE strftime(game_date, '%Y-%m-%d') = ?
        AND home_team_id = ?
    """
    result = con.execute(query, (date_formatted, home_team_id)).fetchone()

    if result:
        return result[0]
    return None


def scrape_game_meta(date_str, dry_run=False):
    """
    Scrapes metadata (Referees, Coaches) for games on a specific date.
    date_str: YYYYMMDD
    """
    team_map = load_team_map()
    con = get_db_connection()

    # Construct URL for the date's games
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])

    url = f"https://www.basketball-reference.com/boxscores/?month={month}&day={day}&year={year}"
    print(f"Fetching games for {date_str} from {url}...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all game summaries
        game_summaries = soup.find_all("div", class_="game_summary")

        for summary in game_summaries:
            # Extract Game Link
            links = summary.find_all("a", href=True)
            box_score_link = None
            for link in links:
                if "boxscores" in link["href"] and link.text.strip() == "Final":
                    box_score_link = link["href"]
                    break

            if not box_score_link:
                continue

            game_url = f"https://www.basketball-reference.com{box_score_link}"
            print(f"  Processing game: {game_url}")

            # Extract BR Game ID from URL (e.g., /boxscores/202310240DEN.html -> 202310240DEN)
            br_game_id = box_score_link.split("/")[-1].replace(".html", "")

            # Parse BR ID to get Home Team Abbr
            # Format: YYYYMMDD0TEAM
            # e.g. 202310240DEN -> DEN
            home_team_abbr = br_game_id[9:]

            # Find NBA Game ID
            nba_game_id = get_nba_game_id(con, date_str, home_team_abbr, team_map)

            if not nba_game_id:
                print(
                    f"    Warning: Could not find NBA Game ID for {br_game_id} (Home: {home_team_abbr}). Using BR ID."
                )
                # We can use BR ID but it won't join with games table.
                # Ideally we skip or insert with BR ID.
                # For now, let's use BR ID but log it.
                game_id_to_use = br_game_id
            else:
                game_id_to_use = nba_game_id

            # Fetch Box Score
            process_box_score(con, game_url, game_id_to_use, dry_run)

            # Sleep to respect rate limits
            time.sleep(3)

    except Exception as e:
        print(f"Error scraping {date_str}: {e}")
    finally:
        con.close()


def process_box_score(con, url, game_id, dry_run):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"    Failed to fetch box score: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # 1. Extract Referees
        referees = []
        # Look for "Officials" section
        # Usually in a div with text "Officials:"
        officials_div = soup.find("div", string=re.compile("Officials:"))
        if not officials_div:
            # Try finding strong tag
            strong_tag = soup.find("strong", string="Officials:")
            if strong_tag:
                officials_div = strong_tag.parent

        if officials_div:
            for link in officials_div.find_all("a"):
                ref_name = link.text
                ref_link = link["href"]  # /referees/cutleke99r.html
                ref_id = ref_link.split("/")[-1].replace(".html", "")
                referees.append((ref_id, ref_name))

        # 2. Extract Coaches
        coaches = []
        # Coaches are harder. They might be in the scorebox or team stats.
        # Strategy: Look for "Head Coach" in comments if not found in text
        # Or look for links to /coaches/
        # TODO: Verify Coach extraction. BR structure might have changed or it's dynamically loaded.
        # Consider fetching Team Season page if not found here.

        # Let's look for all links containing /coaches/
        # But filter out "Coaches" header link
        soup.find_all("a", href=re.compile(r"/coaches/[a-z0-9]+\.html"))

        # We need to associate coach with team.
        # Usually the coach link is near the team name or in the team's box score footer.
        # In the HTML structure, there are tables for each team.
        # id="box-TEAM-game-basic"

        # Find team abbreviations from the page
        # The scorebox has team links
        scorebox = soup.find("div", class_="scorebox")
        teams = []
        if scorebox:
            for team_div in scorebox.find_all("div", class_="scorebox_team"):
                team_link = team_div.find("a", href=re.compile(r"/teams/"))
                if team_link:
                    team_abbr = team_link["href"].split("/")[2]
                    teams.append(team_abbr)

        # Now look for coach in each team's section
        # The coach is often in a data-stat="coach" or just text in the footer?
        # Based on my grep, I didn't see "Head Coach".
        # But I saw "Coaches" link.

        # Alternative: The coach is listed in the "Team Info" which might be parsed from the "Game Info" block?
        # No, usually it's "Lakers: Darvin Ham"

        # Let's try to find the coach by looking for the pattern in the text content of the whole page?
        # No, that's messy.

        # Let's try to find the "Basic Box Score" table for each team and look at the bottom.
        # The footer often has "Team Totals".
        # Maybe it's not in the footer but below it?

        # If I can't find it, I'll skip for now.

        if not dry_run:
            save_to_db(con, game_id, referees, coaches)
        else:
            print(f"    Referees: {referees}")
            print(f"    Coaches: {coaches}")

    except Exception as e:
        print(f"    Error processing box score {game_id}: {e}")


def save_to_db(con, game_id, referees, coaches):
    # Insert Referees
    for ref_id, ref_name in referees:
        # Insert into referees table
        con.execute(
            "INSERT OR IGNORE INTO referees (referee_id, name) VALUES (?, ?)",
            (ref_id, ref_name),
        )

        # Insert into game_referees
        con.execute(
            "INSERT OR IGNORE INTO game_referees (game_id, referee_id, role) VALUES (?, ?, ?)",
            (game_id, ref_id, "Official"),
        )

    # Insert Coaches
    # ...

    # con.close() # Do not close here, passed from caller


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="Date in YYYYMMDD format")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.date:
        scrape_game_meta(args.date, args.dry_run)
    else:
        print("Please provide a date with --date YYYYMMDD")
