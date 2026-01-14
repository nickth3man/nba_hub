import pandas as pd

from src.core.database import get_db_connection


def ingest_players():
    print("Ingesting players from common_player_info table...")
    con = get_db_connection()

    con.execute("""
        INSERT INTO unified_players (player_id, nba_api_person_id, display_name, from_year, to_year)
        SELECT 
            CAST(person_id AS BIGINT), 
            CAST(person_id AS BIGINT), 
            display_first_last, 
            CAST(from_year AS INTEGER), 
            CAST(to_year AS INTEGER)
        FROM common_player_info
        WHERE CAST(person_id AS BIGINT) NOT IN (SELECT player_id FROM unified_players)
    """)

    con.execute("""
        UPDATE unified_players
        SET from_year = CAST(cpi.from_year AS INTEGER),
            to_year = CAST(cpi.to_year AS INTEGER)
        FROM common_player_info cpi
        WHERE unified_players.player_id = CAST(cpi.person_id AS BIGINT)
        AND unified_players.from_year IS NULL
    """)

    res = con.execute("SELECT count(*) FROM unified_players")
    row = res.fetchone()
    count = row[0] if row else 0
    print(f"Total players in unified_players: {count}")
    con.close()


if __name__ == "__main__":
    ingest_players()
