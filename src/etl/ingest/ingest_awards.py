import io

import pandas as pd
import requests

from src.core.database import get_db_connection


def ingest_awards():
    url = "https://raw.githubusercontent.com/sumitrodatta/bball-reference-datasets/master/Data/End%20of%20Season%20Teams.csv"
    print(f"Fetching awards from {url}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        print(f"Loaded {len(df)} team records.")
    except Exception as e:
        print(f"Error fetching/parsing CSV: {e}")
        return

    con = get_db_connection()

    con.execute(
        "CREATE TABLE IF NOT EXISTS unified_awards (award_id INTEGER PRIMARY KEY, award_code VARCHAR NOT NULL UNIQUE, award_name VARCHAR NOT NULL)"
    )
    awards_data = [
        (1, "MVP", "Most Valuable Player"),
        (2, "ROY", "Rookie of the Year"),
        (3, "DPOY", "Defensive Player of the Year"),
        (4, "SMOY", "Sixth Man of the Year"),
        (5, "MIP", "Most Improved Player"),
        (6, "ALL-NBA", "All-NBA Team"),
        (7, "ALL-DEF", "All-Defensive Team"),
        (8, "ALL-ROOK", "All-Rookie Team"),
        (9, "FINALS-MVP", "Finals MVP"),
    ]
    con.executemany(
        "INSERT OR IGNORE INTO unified_awards (award_id, award_code, award_name) VALUES (?, ?, ?)",
        awards_data,
    )

    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_season_awards (
      season_award_id    INTEGER PRIMARY KEY,
      season_id          INTEGER NOT NULL REFERENCES unified_seasons(season_id),
      award_id           INTEGER NOT NULL REFERENCES unified_awards(award_id),
      season_type        VARCHAR NOT NULL,
      UNIQUE (season_id, award_id, season_type)
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_award_results (
      season_award_id    INTEGER NOT NULL REFERENCES unified_season_awards(season_award_id),
      rank               INTEGER,
      is_winner          BOOLEAN NOT NULL DEFAULT FALSE,
      player_id          BIGINT,
      PRIMARY KEY (season_award_id, player_id)
    )
    """)

    con.register("raw_teams", df)

    print("Mapping and ingesting All-NBA/Defense/Rookie teams...")
    con.execute("""
    INSERT OR IGNORE INTO unified_season_awards (season_award_id, season_id, award_id, season_type)
    SELECT
        row_number() over() + 20000,
        s.season_id,
        a.award_id,
        'REG'
    FROM (SELECT DISTINCT season, type FROM raw_teams) ra
    JOIN unified_seasons s ON ra.season = s.season_year
    JOIN unified_awards a ON (
        CASE
            WHEN ra.type = 'All-NBA' THEN 'ALL-NBA'
            WHEN ra.type = 'All-Defense' THEN 'ALL-DEF'
            WHEN ra.type = 'All-Rookie' THEN 'ALL-ROOK'
            ELSE 'OTHER'
        END
    ) = a.award_code
    WHERE a.award_code != 'OTHER'
    """)

    con.execute("""
    INSERT OR IGNORE INTO unified_award_results (season_award_id, rank, is_winner, player_id)
    SELECT
        sa.season_award_id,
        (CASE
            WHEN ra.number_tm = '1st' THEN 1
            WHEN ra.number_tm = '2nd' THEN 2
            WHEN ra.number_tm = '3rd' THEN 3
            ELSE 1
        END) as rank,
        TRUE as is_winner,
        p.player_id
    FROM raw_teams ra
    JOIN unified_seasons s ON ra.season = s.season_year
    JOIN unified_awards a ON (
        CASE
            WHEN ra.type = 'All-NBA' THEN 'ALL-NBA'
            WHEN ra.type = 'All-Defense' THEN 'ALL-DEF'
            WHEN ra.type = 'All-Rookie' THEN 'ALL-ROOK'
            ELSE 'OTHER'
        END
    ) = a.award_code
    JOIN unified_season_awards sa ON sa.season_id = s.season_id AND sa.award_id = a.award_id
    JOIN unified_players p ON LOWER(p.display_name) = LOWER(ra.player)
    """)

    count = con.execute("SELECT count(*) FROM unified_award_results").fetchone()[0]
    print(f"Total award results: {count}")
    con.close()


if __name__ == "__main__":
    ingest_awards()
