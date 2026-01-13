import os

from src.core.database import get_db_connection

CSV_PATH = "data/raw/PlayerStatistics.csv"


def load_box_scores():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    con = get_db_connection()

    print("Creating player_box_scores table...")
    # We use read_csv_auto to infer types, but we can enforce some if needed.
    # We'll create the table directly from the CSV.
    query = f"""
        CREATE OR REPLACE TABLE player_box_scores AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')
    """
    con.execute(query)

    count = con.execute("SELECT COUNT(*) FROM player_box_scores").fetchone()[0]
    print(f"Loaded {count} rows into player_box_scores.")

    # Verify range
    min_date = con.execute(
        "SELECT MIN(gameDateTimeEst) FROM player_box_scores"
    ).fetchone()[0]
    max_date = con.execute(
        "SELECT MAX(gameDateTimeEst) FROM player_box_scores"
    ).fetchone()[0]
    print(f"Date Range: {min_date} to {max_date}")

    con.close()


if __name__ == "__main__":
    load_box_scores()
