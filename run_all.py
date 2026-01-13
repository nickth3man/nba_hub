import subprocess
import sys
import duckdb
import os

DB_PATH = "data/nba.duckdb"
GAMES_CSV = "data/raw/Games.csv"


def init_db():
    print("Initializing DB schema...")
    subprocess.run([sys.executable, "src/db/init_referees_coaches.py"], check=True)


def refresh_games_table():
    print("Refreshing games table from CSV...")
    if not os.path.exists(GAMES_CSV):
        print(f"Warning: {GAMES_CSV} not found. Skipping games table refresh.")
        return

    con = duckdb.connect(DB_PATH)
    con.execute(
        f"CREATE OR REPLACE TABLE games AS SELECT * FROM read_csv_auto('{GAMES_CSV}')"
    )
    con.close()
    print("Games table refreshed.")


def run_scraper():
    print("Running scraper for 2023-10-24...")
    # Oct 24, 2023 has 2 games: LAL vs DEN, PHX vs GSW
    subprocess.run(
        [sys.executable, "src/scraping/scrape_game_meta.py", "--date", "20231024"],
        check=True,
    )


def verify_data():
    print("Verifying data...")
    con = duckdb.connect(DB_PATH)

    print("Referees:")
    refs = con.execute("SELECT * FROM referees LIMIT 5").fetchall()
    for r in refs:
        print(r)

    print("Game Referees:")
    game_refs = con.execute("SELECT * FROM game_referees LIMIT 5").fetchall()
    for r in game_refs:
        print(r)

    con.close()


if __name__ == "__main__":
    init_db()
    refresh_games_table()
    run_scraper()
    verify_data()
