import os
import subprocess
import sys

from src.core.config import GAMES_CSV
from src.core.database import get_db_connection


def init_db():
    print("Initializing DB schema...")
    # Update path to use the new location
    subprocess.run(
        [sys.executable, "src/etl/load/init_referees_coaches.py"], check=True
    )


def refresh_games_table():
    print("Refreshing games table from CSV...")
    if not os.path.exists(GAMES_CSV):
        print(f"Warning: {GAMES_CSV} not found. Skipping games table refresh.")
        return

    con = get_db_connection()
    con.execute(
        f"CREATE OR REPLACE TABLE games AS SELECT * FROM read_csv_auto('{str(GAMES_CSV)}')"
    )
    con.close()
    print("Games table refreshed.")


def run_scraper():
    print("Running scraper for 2023-10-24...")
    # Oct 24, 2023 has 2 games: LAL vs DEN, PHX vs GSW
    subprocess.run(
        [
            sys.executable,
            "src/scraping/sites/basketball_reference_games.py",
            "--date",
            "20231024",
        ],
        check=True,
    )


def verify_data():
    print("Verifying data...")
    con = get_db_connection()

    print("Referees:")
    try:
        refs = con.execute("SELECT * FROM unified_referees LIMIT 5").fetchall()
        for r in refs:
            print(r)
    except Exception as e:
        print(f"Error querying referees: {e}")

    con.close()


if __name__ == "__main__":
    init_db()
    refresh_games_table()
    run_scraper()
    verify_data()
