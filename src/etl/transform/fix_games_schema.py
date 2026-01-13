from src.core.database import get_db_connection


def fix_games_schema():
    csv_path = "data/raw/Games.csv"

    print("Connecting to database...")
    con = get_db_connection()

    print("Dropping existing 'games' table...")
    con.execute("DROP TABLE IF EXISTS games")

    print(f"Recreating 'games' table from {csv_path} with gameId as VARCHAR...")
    # We use read_csv with types parameter to force gameId to be VARCHAR
    # auto_detect=True is default, but we override gameId
    query = f"""
        CREATE TABLE games AS
        SELECT * FROM read_csv('{csv_path}',
            types={{'gameId': 'VARCHAR'}},
            auto_detect=TRUE
        )
    """
    con.execute(query)

    print("Verifying row count...")
    count = con.execute("SELECT COUNT(*) FROM games").fetchone()[0]
    print(f"Total games: {count}")

    print("Checking for 1947 season games (games in 1946 or 1947)...")
    # Assuming 1947 season includes games from late 1946 to 1947.
    # We can check gameDateTimeEst.
    count_1947 = con.execute("""
        SELECT COUNT(*) FROM games
        WHERE gameDateTimeEst LIKE '1946%' OR gameDateTimeEst LIKE '1947%'
    """).fetchone()[0]
    print(f"Games in 1946/1947: {count_1947}")

    # Also checking by gameId format just in case
    count_hist_ids = con.execute("""
        SELECT COUNT(*) FROM games
        WHERE gameId LIKE '%TRH%' OR gameId LIKE '%CHS%' OR gameId LIKE '%DTF%'
    """).fetchone()[0]
    print(f"Games with historical ID format (sample check): {count_hist_ids}")

    con.close()
    print("Done.")


if __name__ == "__main__":
    fix_games_schema()
