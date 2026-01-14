import os
from src.core.database import get_db_connection
from src.core.config import GAMES_CSV


def load_games():
    if not os.path.exists(GAMES_CSV):
        print(f"Error: {GAMES_CSV} not found.")
        return

    con = get_db_connection()

    print("Creating raw_games table...")
    # Force gameId to be VARCHAR to handle historical IDs like '194611010TRH'
    query = f"""
        CREATE OR REPLACE TABLE raw_games AS
        SELECT * FROM read_csv_auto('{str(GAMES_CSV)}', types={{'gameId': 'VARCHAR'}})
    """
    con.execute(query)

    res = con.execute("SELECT COUNT(*) FROM raw_games")
    row = res.fetchone()
    count = row[0] if row else 0
    print(f"Loaded {count} rows into raw_games.")
    con.close()


if __name__ == "__main__":
    load_games()
