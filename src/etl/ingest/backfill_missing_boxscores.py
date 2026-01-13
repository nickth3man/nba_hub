import random
import re
import time

import requests
from bs4 import BeautifulSoup

from src.core.database import get_db_connection


def get_missing_games():
    con = get_db_connection()
    games = con.execute("""
        SELECT gameId, gameDateTimeEst, hometeamId, awayteamId
        FROM raw_games
        WHERE gameId NOT IN (SELECT CAST(gameId AS VARCHAR) FROM raw_player_box_scores)
        ORDER BY gameDateTimeEst ASC
    """).fetchall()
    con.close()
    return games


def scrape_box_score(game_id):
    url = f"https://www.basketball-reference.com/boxscores/{game_id}.html"
    print(f"Scraping {url}...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print("Rate limited. Sleeping for 60s...")
            time.sleep(60)
            return None
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # 1. Extract Referees
    referees = []
    officials_div = soup.find("div", string=re.compile("Officials:"))
    if not officials_div:
        strong = soup.find("strong", string="Officials:")
        if strong:
            officials_div = strong.parent

    if officials_div:
        for a in officials_div.find_all("a"):
            ref_id = a["href"].split("/")[-1].replace(".html", "")
            ref_name = a.text.strip()
            referees.append((ref_id, ref_name))

    # 2. Extract Players/Stats
    # Find all tables with id starting with box- and ending in -game-basic
    stats = []
    tables = soup.find_all("table", id=re.compile(r"box-.*-game-basic"))
    for table in tables:
        team_abbr = table["id"].split("-")[1]
        tbody = table.find("tbody")
        if not tbody:
            continue

        for tr in tbody.find_all("tr"):
            if "class" in tr.attrs and "thead" in tr.attrs["class"]:
                continue

            player_td = tr.find("td", {"data-stat": "player"})
            if not player_td:
                continue

            player_id = player_td["data-append-csv"]
            name = player_td.text.strip()

            # Helper to get stat
            def get_stat(tr_element, stat_name, default=0):
                td = tr_element.find("td", {"data-stat": stat_name})
                if not td or not td.text.strip():
                    return default
                try:
                    return float(td.text.strip())
                except ValueError:
                    return default

            row = {
                "game_id": game_id,
                "player_id": player_id,
                "team_abbr": team_abbr,
                "name": name,
                "mp": get_stat(tr, "mp", 0),  # Changed default to 0 to match type hint
                "fg": get_stat(tr, "fg"),
                "fga": get_stat(tr, "fga"),
                "fg3": get_stat(tr, "fg3"),
                "fg3a": get_stat(tr, "fg3a"),
                "ft": get_stat(tr, "ft"),
                "fta": get_stat(tr, "fta"),
                "orb": get_stat(tr, "orb"),
                "drb": get_stat(tr, "drb"),
                "trb": get_stat(tr, "trb"),
                "ast": get_stat(tr, "ast"),
                "stl": get_stat(tr, "stl"),
                "blk": get_stat(tr, "blk"),
                "tov": get_stat(tr, "tov"),
                "pf": get_stat(tr, "pf"),
                "pts": get_stat(tr, "pts"),
            }
            stats.append(row)

    return {"stats": stats, "referees": referees}


def save_to_db(data):
    if not data:
        return
    con = get_db_connection()

    # 1. Players
    players = []
    for s in data["stats"]:
        players.append((s["player_id"], s["name"]))
    con.executemany(
        "INSERT OR IGNORE INTO unified_players (player_id, display_name) VALUES (?, ?)",
        players,
    )

    # 2. Boxscores
    boxscores = []
    for s in data["stats"]:
        # We need to map team_abbr to team_id
        # For simplicity in this backfill, we'll try to find it in team_history
        team_id_res = con.execute(
            "SELECT team_id FROM unified_team_history WHERE abbreviation = ? LIMIT 1",
            (s["team_abbr"],),
        ).fetchone()
        team_id = team_id_res[0] if team_id_res else None

        if not team_id:
            # Fallback for old abbreviations
            # Huskies = TRH, Stags = CHS, etc.
            # They should be in our updated TeamHistories.csv
            print(f"Warning: Could not find team_id for {s['team_abbr']}")
            continue

        # Convert MP to double
        mp_str = str(s["mp"])
        if ":" in mp_str:
            parts = mp_str.split(":")
            mp = float(parts[0]) + float(parts[1]) / 60.0
        else:
            mp = float(mp_str)

        boxscores.append(
            (
                s["game_id"],
                s["player_id"],
                team_id,
                mp,
                s["pts"],
                s["ast"],
                s["trb"],
                s["stl"],
                s["blk"],
                s["fg"],
                s["fga"],
                s["fg3"],
                s["fg3a"],
                s["ft"],
                s["fta"],
                s["pf"],
                s["tov"],
                0,  # plus_minus
            )
        )

    con.executemany(
        """
        INSERT OR IGNORE INTO unified_player_boxscores
        (game_id, player_id, team_id, minutes, points, assists, rebounds_total, steals, blocks, fgm, fga, fg3m, fg3a, ftm, fta, pf, turnovers, plus_minus)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        boxscores,
    )

    con.close()


if __name__ == "__main__":
    missing = get_missing_games()
    print(f"Found {len(missing)} missing games.")

    # Process only first 10 for validation
    for game in missing[:10]:
        game_id = game[0]
        data = scrape_box_score(game_id)
        if data:
            save_to_db(data)
            print(f"Saved {len(data['stats'])} player stats for {game_id}")
        time.sleep(random.uniform(5, 8))  # Very slow to avoid block
