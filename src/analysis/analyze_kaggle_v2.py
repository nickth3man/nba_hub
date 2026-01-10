import duckdb

db_path = 'data/nba.duckdb'
csv_path = 'data/PlayerStatistics.csv'

print(f"Deep Analysis of Kaggle Dataset: {csv_path}")
con = duckdb.connect(db_path)

con.execute(f"CREATE OR REPLACE TABLE kaggle_player_stats AS SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=True)")

# 1. Duplicate Analysis (personId + gameId)
print("\n--- DUPLICATE ANALYSIS ---")
dupes = con.execute("""
    SELECT COUNT(*) 
    FROM (
        SELECT personId, gameId, COUNT(*) 
        FROM kaggle_player_stats 
        GROUP BY personId, gameId 
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]
print(f"Duplicate Player-Games (personId + gameId): {dupes}")

# 2. Game Types Analysis
print("\n--- GAME TYPES ---")
try:
    types = con.execute("SELECT gameType, COUNT(*) FROM kaggle_player_stats GROUP BY gameType").fetchall()
    print("Row counts by Game Type:")
    for t in types:
        print(f"  {t[0]}: {t[1]}")
except:
    print("Could not analyze gameType (column missing?)")

# 3. Game ID Overlap
print("\n--- GAME ID OVERLAP ---")
kaggle_games = con.execute("SELECT COUNT(DISTINCT gameId) FROM kaggle_player_stats").fetchone()[0]
db_games = con.execute("SELECT COUNT(DISTINCT game_id) FROM player_game_stats_silver").fetchone()[0]
print(f"Unique Games -> Kaggle: {kaggle_games}, My DB: {db_games}")

# Intersection
overlap = con.execute("""
    SELECT COUNT(*) 
    FROM (
        SELECT DISTINCT gameId FROM kaggle_player_stats
    ) k
    JOIN (
        SELECT DISTINCT game_id FROM player_game_stats_silver
    ) d ON k.gameId = d.game_id
""").fetchone()[0]
print(f"Overlapping Games: {overlap}")

# 4. Specific Game Check (22200411)
print("\n--- GAME 22200411 CHECK ---")
# Try exact match (assuming integer)
k_rows = con.execute("SELECT COUNT(*) FROM kaggle_player_stats WHERE gameId = 22200411").fetchone()[0]
print(f"Kaggle Rows for 22200411: {k_rows}")

if k_rows > 0:
    print("Sample Kaggle Row for this game:")
    print(con.execute("SELECT firstName, lastName, points, minutes FROM kaggle_player_stats WHERE gameId = 22200411 LIMIT 1").fetchall())

con.execute("DROP TABLE kaggle_player_stats")
