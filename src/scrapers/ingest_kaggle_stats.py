import duckdb

con = duckdb.connect('data/nba.duckdb')
csv_path = 'data/PlayerStatistics.csv'

print("Starting Kaggle Data Ingestion...")

# 1. Load CSV
con.execute(f"CREATE OR REPLACE TABLE kaggle_source AS SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=True)")

# 2. Identify Missing Games
print("Identifying missing games...")
# We only want games NOT already in player_game_stats_silver
missing_games_query = """
    SELECT DISTINCT gameId 
    FROM kaggle_source 
    WHERE gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)
"""
missing_ids = [r[0] for r in con.execute(missing_games_query).fetchall()]
print(f"Found {len(missing_ids)} games to ingest.")

if len(missing_ids) == 0:
    print("No new games to ingest.")
    exit()

# 3. Map and Insert
# Schema mapping:
# Kaggle -> DB
# gameId -> game_id
# personId -> player_id
# teamId -> team_id
# points -> pts
# totalRebounds -> reb
# assists -> ast
# steals -> stl
# blocks -> blk
# turnovers -> tov
# personalFouls -> pf
# fieldGoalsMade -> fgm
# fieldGoalsAttempted -> fga
# threePointersMade -> fg3m
# threePointersAttempted -> fg3a
# freeThrowsMade -> ftm
# freeThrowsAttempted -> fta
# minutes -> min (needs parsing? Kaggle min is usually string 'PT36M' or float. Let's check)

# Check minutes format
min_sample = con.execute("SELECT minutes FROM kaggle_source LIMIT 1").fetchone()[0]
print(f"Sample minutes format: {min_sample}")

# If minutes is like 'PT12M00.00S', we need to parse. If it's number, cast.
# Based on error earlier, 'minutes' exists.

print("Inserting records...")
# We insert into player_game_stats_silver. 
# Note: We need to handle 'player_name'. Kaggle has firstName, lastName.
# We explicitly cast to BIGINT for IDs to match schema.

# Use a temporary table for the clean data
con.execute("""
    CREATE OR REPLACE TABLE kaggle_clean AS 
    SELECT 
        CAST(gameId AS BIGINT) as game_id,
        CAST(teamId AS BIGINT) as team_id,
        CAST(personId AS BIGINT) as player_id,
        firstName || ' ' || lastName as player_name,
        NULL as start_position,
        NULL as comment,
        minutes as min, 
        CAST(fieldGoalsMade AS INTEGER) as fgm,
        CAST(fieldGoalsAttempted AS INTEGER) as fga,
        CAST(fieldGoalsPercentage AS DOUBLE) as fg_pct,
        CAST(threePointersMade AS INTEGER) as fg3m,
        CAST(threePointersAttempted AS INTEGER) as fg3a,
        CAST(threePointersPercentage AS DOUBLE) as fg3_pct,
        CAST(freeThrowsMade AS INTEGER) as ftm,
        CAST(freeThrowsAttempted AS INTEGER) as fta,
        CAST(freeThrowsPercentage AS DOUBLE) as ft_pct,
        CAST(offensiveRebounds AS INTEGER) as oreb,
        CAST(defensiveRebounds AS INTEGER) as dreb,
        CAST(totalRebounds AS INTEGER) as reb,
        CAST(assists AS INTEGER) as ast,
        CAST(steals AS INTEGER) as stl,
        CAST(blocks AS INTEGER) as blk,
        CAST(turnovers AS INTEGER) as tov,
        CAST(personalFouls AS INTEGER) as pf,
        CAST(points AS INTEGER) as pts,
        CAST(plusMinusPoints AS DOUBLE) as plus_minus,
        NULL as season_id -- We could infer this from game date if needed
    FROM kaggle_source
    WHERE gameId NOT IN (SELECT DISTINCT game_id FROM player_game_stats_silver)
""")

# Insert
con.execute("""
    INSERT INTO player_game_stats_silver 
    SELECT * FROM kaggle_clean
""")

print("Ingestion complete.")

# 4. Verify
new_count = con.execute("SELECT COUNT(*) FROM player_game_stats_silver").fetchone()[0]
print(f"New Table Row Count: {new_count}")

con.execute("DROP TABLE kaggle_source")
con.execute("DROP TABLE kaggle_clean")
