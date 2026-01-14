import os

import pandas as pd

from src.core.config import TEAM_HISTORIES_CSV
from src.core.database import get_db_connection


def init_dimensions():
    if not os.path.exists(TEAM_HISTORIES_CSV):
        print(f"Error: {TEAM_HISTORIES_CSV} not found.")
        return

    con = get_db_connection()

    print("Initializing raw_dim_teams...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw_dim_teams AS
        SELECT
            CAST(teamId AS VARCHAR) as team_id,
            teamCity as city,
            teamName as nickname,
            teamAbbrev as abbreviation,
            seasonFounded as year_founded,
            seasonActiveTill as year_active_till,
            league
        FROM read_csv_auto('{TEAM_HISTORIES_CSV}')
    """)

    team_count = con.execute("SELECT COUNT(*) FROM raw_dim_teams").fetchone()[0]
    print(f"Loaded {team_count} rows into raw_dim_teams.")

    print("Initializing raw_dim_seasons...")
    seasons = []
    for year in range(1946, 2026):
        season_id = f"{year}-{str(year + 1)[2:]}"
        league = "BAA" if year < 1949 else "NBA"
        seasons.append((season_id, year, year + 1, league))

    df_seasons = pd.DataFrame(
        seasons, columns=["season_id", "start_year", "end_year", "league"]
    )
    con.execute("CREATE OR REPLACE TABLE raw_dim_seasons AS SELECT * FROM df_seasons")

    season_count = con.execute("SELECT COUNT(*) FROM raw_dim_seasons").fetchone()[0]
    print(f"Loaded {season_count} rows into raw_dim_seasons.")

    con.close()
    print("Dimensions initialized successfully.")


if __name__ == "__main__":
    init_dimensions()
