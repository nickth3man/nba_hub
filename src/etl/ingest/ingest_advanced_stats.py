import io

import pandas as pd
import requests

from src.core.database import get_db_connection


def ingest_advanced_stats():
    # The librarian provided a blob link, converting to raw
    url = "https://raw.githubusercontent.com/peasant98/TheNBACSV/master/nbaNew.csv"
    print(f"Fetching advanced stats from {url}...")

    try:
        # This is a large file (~24K rows, but 5MB+)
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        print(f"Loaded {len(df)} player-season records.")
    except Exception as e:
        print(f"Error fetching/parsing CSV: {e}")
        return

    con = get_db_connection()

    # Create table for seasonal advanced stats
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_player_season_advanced (
        season_id INTEGER REFERENCES unified_seasons(season_id),
        player_id BIGINT REFERENCES unified_players(player_id),
        team_id BIGINT REFERENCES unified_teams(team_id),
        per DOUBLE,
        ts_pct DOUBLE,
        usg_pct DOUBLE,
        ows DOUBLE,
        dws DOUBLE,
        ws DOUBLE,
        ws_48 DOUBLE,
        obpm DOUBLE,
        dbpm DOUBLE,
        bpm DOUBLE,
        vorp DOUBLE,
        PRIMARY KEY (season_id, player_id, team_id)
    )
    """)

    # Register temp table
    con.register("raw_adv", df)

    print("Mapping and ingesting advanced stats...")
    # Map SeasonStart to Season, PlayerName to ID, Tm to ID
    # Fix: TS% and USG% contain '%' signs, strip them
    con.execute("""
    INSERT OR IGNORE INTO unified_player_season_advanced
    (season_id, player_id, team_id, per, ts_pct, usg_pct, ows, dws, ws, ws_48, obpm, dbpm, bpm, vorp)
    SELECT
        s.season_id,
        p.player_id,
        t.team_id,
        CAST(ra.PER AS DOUBLE),
        CAST(replace(CAST(ra."TS%" AS VARCHAR), '%', '') AS DOUBLE) / 100.0,
        CAST(replace(CAST(ra."USG%" AS VARCHAR), '%', '') AS DOUBLE) / 100.0,
        CAST(ra.OWS AS DOUBLE),
        CAST(ra.DWS AS DOUBLE),
        CAST(ra.WS AS DOUBLE),
        CAST(ra."WS/48" AS DOUBLE),
        CAST(ra.OBPM AS DOUBLE),
        CAST(ra.DBPM AS DOUBLE),
        CAST(ra.BPM AS DOUBLE),
        CAST(ra.VORP AS DOUBLE)
    FROM raw_adv ra
    JOIN unified_seasons s ON CAST(ra.SeasonStart AS INTEGER) = s.season_year
    JOIN unified_players p ON LOWER(p.display_name) = LOWER(ra.PlayerName)
    JOIN unified_team_history t ON ra.Tm = t.abbreviation
    """)

    count = con.execute(
        "SELECT count(*) FROM unified_player_season_advanced"
    ).fetchone()[0]
    print(f"Total advanced records ingested: {count}")
    con.close()


if __name__ == "__main__":
    ingest_advanced_stats()
