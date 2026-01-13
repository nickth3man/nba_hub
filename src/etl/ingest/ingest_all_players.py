import pandas as pd

from src.core.database import get_db_connection

CSV_PATH = "all_players.csv"


def ingest_players():
    print(f"Reading {CSV_PATH}...")
    # Fix: Ted, Hound Dog McClain has an extra comma in the raw file.
    # We should use quotechar if available, but the sample didn't show quotes.
    # Manual fix for known problematic lines or use regex.
    try:
        df = pd.read_csv(CSV_PATH)
    except pd.errors.ParserError:
        print(
            "Standard CSV parsing failed. Attempting manual fix for problematic lines..."
        )

        rows = []
        with open(CSV_PATH, encoding="utf-8") as f:
            header = f.readline().strip().split(",")
            for line in f:
                parts = line.strip().split(",")
                if len(parts) > 4:
                    # Likely "ID, Name Part 1, Name Part 2, From, To"
                    # Merge middle parts into display_name
                    pid = parts[0]
                    from_yr = parts[-2]
                    to_yr = parts[-1]
                    name = ",".join(parts[1:-2])
                    rows.append([pid, name, from_yr, to_yr])
                else:
                    rows.append(parts)
        df = pd.DataFrame(rows, columns=header)

    print(f"Loaded {len(df)} players.")

    con = get_db_connection()

    # We want to insert or ignore/update
    # Columns: person_id, display_name, from_year, to_year
    # Table: unified_players(player_id, nba_api_person_id, display_name, from_year, to_year)

    # Map CSV to Table
    df["player_id"] = df["person_id"]
    df["nba_api_person_id"] = df["person_id"]

    # Register dataframe with duckdb
    con.register("df_players", df)

    print("Inserting/Updating players in unified_players...")
    # Use a temp table to handle the merge safely
    con.execute("CREATE TEMPORARY TABLE new_players AS SELECT * FROM df_players")

    # 1. Insert new players
    con.execute("""
        INSERT INTO unified_players (player_id, nba_api_person_id, display_name, from_year, to_year)
        SELECT CAST(person_id AS BIGINT), CAST(person_id AS BIGINT), display_name, CAST(from_year AS INTEGER), CAST(to_year AS INTEGER)
        FROM new_players
        WHERE CAST(person_id AS BIGINT) NOT IN (SELECT player_id FROM unified_players)
    """)

    # 2. Update existing players (only those missing career info)
    # We avoid updating player_id to keep FKs happy
    con.execute("""
        UPDATE unified_players
        SET from_year = CAST(np.from_year AS INTEGER),
            to_year = CAST(np.to_year AS INTEGER)
        FROM new_players np
        WHERE unified_players.player_id = CAST(np.person_id AS BIGINT)
        AND unified_players.from_year IS NULL
    """)

    count = con.execute("SELECT count(*) FROM unified_players").fetchone()[0]
    print(f"Total players in unified_players: {count}")
    con.close()


if __name__ == "__main__":
    ingest_players()
