import csv
from datetime import datetime

import requests

from src.core.database import get_db_connection


def fetch_octonion_games(year):
    url = f"https://raw.githubusercontent.com/octonion/basketball/master/bbref/csv/games_BAA_{year}.csv"
    print(f"Fetching {url}...")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {year} data.")
        return []

    games = []
    lines = response.text.strip().split("\n")
    reader = csv.reader(lines)
    for row in reader:
        if len(row) < 11:
            continue

        # Parse date
        date_str = row[1]  # "Fri, Nov 1, 1946"
        dt = datetime.strptime(date_str, "%a, %b %d, %Y")

        # Game ID from URL
        box_link = row[4]  # /boxscores/194611010TRH.html
        game_id = box_link.split("/")[-1].replace(".html", "")

        home_team = row[8]
        away_team = row[5]
        home_score = row[10]
        away_score = row[7]

        games.append(
            {
                "game_id": game_id,
                "game_date": dt.strftime("%Y-%m-%d"),
                "home_team_name": home_team,
                "away_team_name": away_team,
                "home_score": home_score,
                "away_score": away_score,
                "season_year": int(row[0]) - 1,
            }
        )
    return games


def update_db(games):
    if not games:
        return
    con = get_db_connection()

    mapped_games = []
    for g in games:
        # Try to map teams using nickname or city nickname
        h_id_res = con.execute(
            "SELECT team_id FROM unified_team_history WHERE nickname = ? OR (city || ' ' || nickname) = ? LIMIT 1",
            (g["home_team_name"], g["home_team_name"]),
        ).fetchone()
        a_id_res = con.execute(
            "SELECT team_id FROM unified_team_history WHERE nickname = ? OR (city || ' ' || nickname) = ? LIMIT 1",
            (g["away_team_name"], g["away_team_name"]),
        ).fetchone()

        h_id = h_id_res[0] if h_id_res else None
        a_id = a_id_res[0] if a_id_res else None

        if not h_id or not a_id:
            # Comprehensive Manual Mapping for early BAA/NBA teams
            overrides = {
                "Toronto Huskies": 9042,
                "Chicago Stags": 9059,
                "Detroit Falcons": 9020,
                "Pittsburgh Ironmen": 9001,
                "Providence Steam Rollers": 9056,
                "Cleveland Rebels": 9017,
                "Washington Capitols": 9015,
                "St. Louis Bombers": 9012,
                "Philadelphia Warriors": 1610612755,
                "New York Knicks": 1610612752,
                "Baltimore Bullets": 9071,
                "Boston Celtics": 1610612738,
                "Minneapolis Lakers": 1610612747,
                "Rochester Royals": 1610612758,
                "Fort Wayne Pistons": 1610612765,
                "Indianapolis Jets": 9008,
            }
            if not h_id:
                h_id = overrides.get(g["home_team_name"])
            if not a_id:
                a_id = overrides.get(g["away_team_name"])

        if not h_id or not a_id:
            print(
                f"Warning: Could not map teams for {g['game_id']} ({g['home_team_name']} vs {g['away_team_name']})"
            )
            continue

        season_id_res = con.execute(
            "SELECT season_id FROM unified_seasons WHERE season_year = ? LIMIT 1",
            (g["season_year"],),
        ).fetchone()
        if not season_id_res:
            print(f"Warning: Season {g['season_year']} not found.")
            continue

        mapped_games.append(
            (
                g["game_id"],
                2,
                season_id_res[0],
                "REG",
                g["game_date"],
                h_id,
                a_id,
                g["home_score"],
                g["away_score"],
            )
        )

    con.executemany(
        """
        INSERT OR IGNORE INTO unified_games (game_id, league_id, season_id, season_type, game_date, home_team_id, away_team_id, home_points, away_points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        mapped_games,
    )

    con.close()
    print(f"Inserted {len(mapped_games)} games.")


if __name__ == "__main__":
    for year in [1947, 1948, 1949]:
        games = fetch_octonion_games(year)
        update_db(games)
