import duckdb
import os

db_path = 'data/nba.duckdb'
csv_path = 'data/PlayerStatistics.csv'

print(f"Analyzing Kaggle Dataset: {csv_path}")
print(f"Comparing against: {db_path}")

con = duckdb.connect(db_path)

# 1. Load Kaggle CSV into a temporary table
print("\nLoading CSV into DuckDB (this might take a moment)...")
con.execute(f"""
    CREATE OR REPLACE TABLE kaggle_player_stats AS 
    SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=True)
""")

# 2. General Stats
print("\n--- KAGGLE DATASET STATS ---")
row_count = con.execute("SELECT COUNT(*) FROM kaggle_player_stats").fetchone()[0]
print(f"Row Count: {row_count}")

columns = con.execute("DESCRIBE kaggle_player_stats").fetchall()
col_names = [c[0] for c in columns]
print(f"Columns ({len(columns)}): {', '.join(col_names[:10])}...")

# 3. Date Range
try:
    # Assuming 'Date' column exists based on typical file structure, otherwise check 'GAME_DATE'
    date_col = 'Date' if 'Date' in col_names else 'GAME_DATE'
    if date_col not in col_names:
        # Fallback to finding a date-like column
        for c in col_names:
            if 'date' in c.lower():
                date_col = c
                break
    
    print(f"Using date column: {date_col}")
    min_date, max_date = con.execute(f"SELECT MIN({date_col}), MAX({date_col}) FROM kaggle_player_stats").fetchone()
    print(f"Date Range: {min_date} to {max_date}")
except Exception as e:
    print(f"Could not determine date range: {e}")

# 4. Duplicate Analysis
print("\n--- INTEGRITY CHECK ---")
# Check for duplicates (Player + Game + Team)
# Need to identify correct columns for Player and Game
# Usually: Player, GameID or Date+Team
p_col = 'Player' if 'Player' in col_names else 'PLAYER_NAME'
g_col = 'GameID' if 'GameID' in col_names else 'GAME_ID'
if g_col not in col_names: g_col = date_col # Fallback

if p_col in col_names:
    dupes = con.execute(f"""
        SELECT COUNT(*) 
        FROM (
            SELECT {p_col}, {g_col}, COUNT(*) 
            FROM kaggle_player_stats 
            GROUP BY {p_col}, {g_col} 
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    print(f"Duplicate Player-Game Entries: {dupes}")
else:
    print("Could not identify Player column for duplicate check.")

# 5. Comparison with Silver Table
print("\n--- COMPARISON WITH player_game_stats_silver ---")
silver_count = con.execute("SELECT COUNT(*) FROM player_game_stats_silver").fetchone()[0]
print(f"My DB Row Count: {silver_count}")
print(f"Kaggle vs DB Diff: {row_count - silver_count} rows")

# Check coverage overlap
# Check a random recent game
print("\nChecking a sample game (2022-12-13, GameID 0022200411)...")
# Verify if Kaggle has GameID
has_game_id = 'GameID' in col_names or 'GAME_ID' in col_names
if has_game_id:
    gid_col = 'GameID' if 'GameID' in col_names else 'GAME_ID'
    kaggle_sample = con.execute(f"SELECT COUNT(*) FROM kaggle_player_stats WHERE CAST({gid_col} AS VARCHAR) LIKE '%22200411'").fetchone()[0]
    db_sample = con.execute("SELECT COUNT(*) FROM player_game_stats_silver WHERE game_id = 22200411").fetchone()[0]
    print(f"Rows for Game 22200411 -> Kaggle: {kaggle_sample}, My DB: {db_sample}")
else:
    print("Kaggle dataset does not appear to have a standard GameID column for easy direct comparison.")

# 6. Schema Difference
print("\n--- SCHEMA DIFFERENCES ---")
db_cols = set([c[0] for c in con.execute("DESCRIBE player_game_stats_silver").fetchall()])
kag_cols = set(col_names)

only_in_kaggle = kag_cols - db_cols
only_in_db = db_cols - kag_cols

print(f"Columns only in Kaggle ({len(only_in_kaggle)}): {list(only_in_kaggle)[:5]}...")
print(f"Columns only in DB ({len(only_in_db)}): {list(only_in_db)[:5]}...")

con.execute("DROP TABLE kaggle_player_stats")
print("\nDone.")
