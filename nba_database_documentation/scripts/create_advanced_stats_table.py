"""
Create the player_season_advanced_stats table in the DuckDB database
"""

import sys
from pathlib import Path
import duckdb

DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")
SQL_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\sql_queries\create_advanced_stats_table.sql")

def main():
    print("Creating player_season_advanced_stats table...")
    print(f"Database: {DB_PATH}")
    print(f"SQL Script: {SQL_PATH}")
    print()

    # Read SQL script
    with open(SQL_PATH, 'r') as f:
        sql_script = f.read()

    # Connect to database
    try:
        conn = duckdb.connect(str(DB_PATH))
        print("[OK] Connected to database")

        # Execute SQL script
        conn.execute(sql_script)
        print("[OK] Table created successfully")

        # Verify table exists
        result = conn.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = 'player_season_advanced_stats'
        """).fetchall()

        if result:
            print(f"[OK] Verified table exists: {result[0][0]}")

            # Show table schema
            schema = conn.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'player_season_advanced_stats'
                ORDER BY ordinal_position
            """).fetchdf()

            print(f"\nTable schema ({len(schema)} columns):")
            for _, row in schema.iterrows():
                print(f"  {row['column_name']}: {row['data_type']}")

        else:
            print("[ERROR] Table was not created")
            sys.exit(1)

        conn.close()
        print("\n[OK] Table creation complete!")

    except Exception as e:
        print(f"[ERROR] Failed to create table: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
