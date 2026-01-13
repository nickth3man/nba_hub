import pandas as pd

from src.core.database import get_db_connection


def ingest_transactions():
    url = "https://raw.githubusercontent.com/rossgraham/NBA-Transaction-History/main/DB/Player_Trans.csv"
    print(f"Fetching transactions from {url}...")

    try:
        df = pd.read_csv(url, header=None, names=["date", "type", "team", "player"])
        print(f"Loaded {len(df)} transactions.")
    except Exception as e:
        print(f"Error: {e}")
        return

    con = get_db_connection()

    # Create unified_transactions table
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_transactions (
        transaction_id INTEGER PRIMARY KEY,
        transaction_date DATE NOT NULL,
        transaction_type VARCHAR NOT NULL,
        team_id BIGINT,
        player_id BIGINT,
        raw_team VARCHAR,
        raw_player VARCHAR
    )
    """)

    # Pre-process: Map team abbreviations and player names
    # This is a heuristic mapping

    # Register temp table
    con.register("raw_trans", df)

    print("Mapping and ingesting transactions...")
    con.execute("""
    INSERT INTO unified_transactions (transaction_id, transaction_date, transaction_type, team_id, player_id, raw_team, raw_player)
    SELECT
        row_number() over() as transaction_id,
        CAST(rt.date AS DATE),
        rt.type,
        (SELECT team_id FROM unified_team_history WHERE abbreviation = rt.team LIMIT 1) as team_id,
        (SELECT player_id FROM unified_players WHERE display_name = rt.player LIMIT 1) as player_id,
        rt.team,
        rt.player
    FROM raw_trans rt
    """)

    count = con.execute("SELECT count(*) FROM unified_transactions").fetchone()[0]
    print(f"Total transactions ingested: {count}")
    con.close()


if __name__ == "__main__":
    ingest_transactions()
