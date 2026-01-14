import os

from src.core.database import get_db_connection

CSV_PATH = "data/raw/PlayerStatistics.csv"


def load_box_scores():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    con = get_db_connection()

    print("Creating raw_player_box_scores table...")
    # We use read_csv_auto to infer types, but we can enforce some if needed.
    # We'll create the table directly from the CSV.
    query = f"""
        CREATE OR REPLACE TABLE raw_player_box_scores AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')
    """
    con.execute(query)

    res = con.execute("SELECT COUNT(*) FROM raw_player_box_scores")
    row = res.fetchone()
    count = row[0] if row else 0
    print(f"Loaded {count} rows into raw_player_box_scores.")

    # Verify range
    min_res = con.execute("SELECT MIN(gameDateTimeEst) FROM raw_player_box_scores")
    min_row = min_res.fetchone()
    min_date = min_row[0] if min_row else "N/A"

    max_res = con.execute("SELECT MAX(gameDateTimeEst) FROM raw_player_box_scores")
    max_row = max_res.fetchone()
    max_date = max_row[0] if max_row else "N/A"

    print(f"Date Range: {min_date} to {max_date}")

    con.close()


if __name__ == "__main__":
    load_box_scores()
