import duckdb

con = duckdb.connect('data/nba.duckdb')
csv_path = 'data/PlayerStatistics.csv'

con.execute(f"CREATE OR REPLACE TABLE kaggle_player_stats AS SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=True)")

print("--- COVERAGE ANALYSIS ---")

# 1. Games in Kaggle NOT in DB
# Assuming gameId format matches (both integers or numeric strings)
missing = con.execute("""
    SELECT DISTINCT k.gameId
    FROM kaggle_player_stats k
    WHERE k.gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)
""").fetchall()

print(f"Games in Kaggle missing from DB: {len(missing)}")

# 2. Date Distribution of Missing Games
if len(missing) > 0:
    print("\nAnalyzing missing games date range...")
    dates = con.execute("""
        SELECT MIN(gameDateTimeEst), MAX(gameDateTimeEst)
        FROM kaggle_player_stats
        WHERE gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)
    """).fetchone()
    print(f"Missing Games Date Range: {dates[0]} to {dates[1]}")
    
    # Breakdown by Decade
    print("\nMissing Games by Decade:")
    decades = con.execute("""
        SELECT LEFT(CAST(gameDateTimeEst AS VARCHAR), 3) || '0s', COUNT(DISTINCT gameId)
        FROM kaggle_player_stats
        WHERE gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)
        GROUP BY 1
        ORDER BY 1
    """).fetchall()
    for d in decades:
        print(f"  {d[0]}: {d[1]} games")

# 3. Check if these games exist in 'games' table but just lack player stats
print("\nChecking if missing games exist in 'games' table (metadata only)...")
missing_ids = [m[0] for m in missing]
# Use temp table for join speed
con.execute("CREATE OR REPLACE TABLE missing_ids (game_id BIGINT)")
con.execute(f"INSERT INTO missing_ids SELECT DISTINCT gameId FROM kaggle_player_stats WHERE gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)")

metadata_match = con.execute("""
    SELECT COUNT(*)
    FROM missing_ids m
    JOIN games g ON m.game_id = g.game_id
""").fetchone()[0]

print(f"Of the {len(missing)} missing games, {metadata_match} exist in our 'games' table (metadata) but have no player stats.")

# 4. Value Proposition
print("\n--- CONCLUSION ---")
if len(missing) > 10000:
    print("CRITICAL: Kaggle dataset contains thousands of games missing from your player stats.")
else:
    print("MARGINAL: Kaggle dataset offers minor coverage improvement.")

con.execute("DROP TABLE kaggle_player_stats")
con.execute("DROP TABLE missing_ids")
