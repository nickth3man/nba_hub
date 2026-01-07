# Phase 1.2 (Part 1) Execution Guide: Acquire 1990s Historical Player Box Scores

## Overview
This guide provides step-by-step instructions to acquire historical NBA player box scores for the Jordan era (1990-1996) using the `acquire_historical_player_boxscores.py` script.

## Current Database Status

**Existing Data:**
- Current player box score data: 1996-11-01 to 2023-06-12 (769,033 records)
- Only season 1996-97 (season_id 21996) has player box scores from the historical period
- 23,757 records for 1996-97 season covering 1,189 games and 441 players

**Target Data to Acquire:**
- 1990-91 season (season_id 21990): 1,107 games
- 1991-92 season (season_id 21991): 1,107 games
- 1992-93 season (season_id 21992): 1,107 games
- 1993-94 season (season_id 21993): 1,107 games
- 1994-95 season (season_id 21994): 1,107 games
- 1995-96 season (season_id 21995): 1,189 games

**Expected Results:**
- Total games: ~6,724 regular season games
- Estimated player-game records: ~160,000-170,000
- Processing time: 3-4 hours (rate-limited at 1.0s per request)

## Prerequisites

**Verified Installed Packages:**
- basketball-reference-web-scraper: 4.15.4 ✓
- cloudscraper: 1.2.71 ✓
- duckdb: 1.4.2 ✓
- pandas: 2.3.3 ✓

**Database:**
- Path: `c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb`
- Size: 232 MB
- Tables verified: `player_game_stats_silver`, `games`, `team`, `common_player_info`

**IMPORTANT BUG FIX:**
A critical bug in the script has been identified and fixed:
- **Issue:** The `min` column was being formatted as string "MM:SS" but database expects BIGINT (integer minutes)
- **Fix Applied:** Line 514-516 now converts seconds to integer minutes
- **Status:** FIXED - Script is ready to use

## Step 1: Test Run (Dry-Run with 1995-96 Season)

Before running the full acquisition, test with a single season to verify:
- Basketball-Reference connection works
- Team abbreviation mapping is correct
- Player name resolution is functional
- Era-specific stats handling (3PT, blocks, steals should all be present for 1990s)
- Checkpoint system works

**Command:**
```bash
cd "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\scripts"

python acquire_historical_player_boxscores.py --start-year 1995 --end-year 1995 --dry-run
```

**What to Verify:**
1. Script successfully connects to database
2. Loads team mappings (should see ~30+ teams)
3. Loads player mappings (should see thousands of players)
4. Downloads box scores for 1995-96 season dates
5. Processes records with all modern stats (3PT, blocks, steals, OREB/DREB)
6. Creates CSV file: `nba_database_documentation/data/historical_boxscores_1995.csv`
7. Reports statistics without inserting to database

**Expected Output:**
- ~1,189 games processed
- ~23,000-24,000 player box score records
- CSV file created with all records
- Minimal unmapped rows (should be < 1%)

## Step 2: Full Acquisition (1990-1996)

Once the dry-run succeeds, run the full acquisition:

**Command:**
```bash
cd "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\scripts"

python acquire_historical_player_boxscores.py --start-year 1990 --end-year 1996
```

**Note:** This will process years 1990, 1991, 1992, 1993, 1994, 1995, AND 1996. Since 1996 already has data, the INSERT statement uses a NOT EXISTS clause to prevent duplicates.

**Alternative (If You Want to Skip 1996):**
```bash
python acquire_historical_player_boxscores.py --start-year 1990 --end-year 1995
```

**Progress Monitoring:**
- Script shows progress every 50 games
- Each season takes approximately 30-40 minutes
- Total time: 3-4 hours for all 6-7 years
- Checkpoint files created after each year completes

**Checkpoint System:**
- Checkpoint file: `nba_database_documentation/data/historical_acquisition_checkpoint.json`
- Contains list of completed years
- If script is interrupted, rerun the same command to resume
- Script will skip already completed years

**Expected Console Output:**
```
================================================================================
ACQUIRING HISTORICAL PLAYER BOX SCORES
Years: 1990-1996
================================================================================

--------------------------------------------------------------------------------
Season 1990-91
--------------------------------------------------------------------------------
[1/3] Loading season games from database...
[OK] Loaded 1107 game mappings
[2/3] Downloading player box scores...
  -> Progress: 50/1107 (5%), Records: 1200, Unmapped: 0
  -> Progress: 100/1107 (9%), Records: 2400, Unmapped: 0
  ...
  -> Downloaded 26400 player box scores
[3/3] Loading data...
  -> Saved to CSV: historical_boxscores_1990.csv
  [OK] Inserted 26400 records
  -> Season summary:
     Records: 26400
     Games: 1107
     Players: 420

[OK] Season 1990 complete and checkpointed
```

## Step 3: Validation After Completion

Run these SQL queries to validate the acquired data:

### Query 1: Overall Record Count
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    COUNT(*) as total_records,
    COUNT(DISTINCT g.game_id) as unique_games,
    COUNT(DISTINCT pgs.player_id) as unique_players
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997;
"
```

**Expected Result:**
- total_records: ~160,000-170,000
- unique_games: ~6,700
- unique_players: ~450-500

### Query 2: Records by Season
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    g.season_id,
    COUNT(*) as records,
    COUNT(DISTINCT pgs.game_id) as games,
    COUNT(DISTINCT pgs.player_id) as players,
    ROUND(AVG(pgs.pts), 1) as avg_pts_per_player
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY g.season_id
ORDER BY g.season_id;
"
```

**Expected Result:** Each season should have ~23,000-26,000 records

### Query 3: Check for Missing Stats
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN pgs.pts IS NULL THEN 1 ELSE 0 END) as missing_pts,
    SUM(CASE WHEN pgs.reb IS NULL THEN 1 ELSE 0 END) as missing_reb,
    SUM(CASE WHEN pgs.ast IS NULL THEN 1 ELSE 0 END) as missing_ast,
    SUM(CASE WHEN pgs.fg3m IS NULL THEN 1 ELSE 0 END) as missing_3pt,
    SUM(CASE WHEN pgs.stl IS NULL THEN 1 ELSE 0 END) as missing_stl,
    SUM(CASE WHEN pgs.blk IS NULL THEN 1 ELSE 0 END) as missing_blk,
    ROUND(100.0 * SUM(CASE WHEN pgs.pts IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as pct_missing_pts
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
  AND pgs.min > 0;
"
```

**Expected Result:** Missing stats should be < 1% for all categories (3PT, blocks, steals, rebounds all tracked in 1990s)

### Query 4: Verify Michael Jordan's Games
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    p.display_first_last as player,
    g.game_date,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.stl,
    pgs.blk,
    pgs.fg3m
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN common_player_info p ON pgs.player_id = p.person_id
WHERE p.display_first_last LIKE '%Jordan%'
  AND g.season_id >= 21990 AND g.season_id < 21997
ORDER BY pgs.pts DESC
LIMIT 10;
"
```

**Expected Result:** Should see Michael Jordan's top games with high point totals (50+, 60+ point games)

### Query 5: Team Distribution
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    t.abbreviation,
    t.full_name,
    COUNT(*) as player_game_records
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN team t ON pgs.team_id = t.id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY t.abbreviation, t.full_name
ORDER BY player_game_records DESC
LIMIT 10;
"
```

**Expected Result:** All teams should have similar counts (~5,000-6,000 records each)

### Query 6: Date Range Verification
```bash
duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb -c "
SELECT
    g.season_id,
    MIN(g.game_date) as first_game,
    MAX(g.game_date) as last_game,
    COUNT(DISTINCT g.game_id) as games_with_boxscores
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY g.season_id
ORDER BY g.season_id;
"
```

**Expected Result:** Date ranges should match the game table dates shown earlier

## Step 4: Post-Acquisition Cleanup

After successful validation:

1. **Remove Checkpoint File:**
```bash
del "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data\historical_acquisition_checkpoint.json"
```

2. **Optional: Archive CSV Files:**
The script creates CSV files for each year. You can either:
- Keep them for backup: Move to an archive folder
- Delete them: They're redundant once data is in database

```bash
mkdir "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data\archive_1990s"
move "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data\historical_boxscores_*.csv" "c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data\archive_1990s\"
```

## Troubleshooting

### Rate Limiting (HTTP 429 Errors)
If you see rate limit errors:
- Script automatically retries with exponential backoff
- Default delay: 1.0 seconds between requests
- Backoff: 10s, 20s, 30s on retries
- If persistent, increase `REQUEST_DELAY_SECONDS` in script from 1.0 to 2.0

### Script Interruption
If script is interrupted (Ctrl+C, connection loss):
1. Check checkpoint file exists: `historical_acquisition_checkpoint.json`
2. Rerun the same command
3. Script will skip completed years and resume

### Unmapped Rows
If you see many unmapped rows (> 5%):
- Check team abbreviation mapping in script (lines 225-242)
- Historical teams (SEA, VAN, CHH) may need additional mappings
- Review unmapped samples in console output

### Missing Player IDs
If many players can't be mapped:
- Check `common_player_info` table has sufficient historical players
- May need to acquire historical player info first
- Script will still insert records with NULL player_id and use player_name

### Database Lock Errors
If you get "database is locked" errors:
- Close any other connections to `nba.duckdb`
- Close DuckDB CLI if open
- Only run one instance of the script at a time

## Script Features

**Rate Limiting:**
- 1.0 second delay between requests (conservative)
- Basketball-Reference limit: ~20 requests/minute
- Retry logic with exponential backoff on 429 errors

**Checkpoint System:**
- Saves progress after each season completes
- JSON file: `historical_acquisition_checkpoint.json`
- Resume capability with `--resume-from-checkpoint` (automatic)

**Team Abbreviation Mapping:**
- Handles historical teams:
  - SEA (Seattle SuperSonics) → OKC
  - VAN (Vancouver Grizzlies) → MEM
  - CHH (Charlotte Hornets) → CHA
  - WSB (Washington Bullets) → WAS
- Full list in script lines 225-242

**Era-Specific Stats:**
- 1990-1996 has ALL modern stats:
  - 3-pointers: Available (introduced 1979-80)
  - Blocks/Steals: Available (tracked since 1973-74)
  - OREB/DREB: Available (split since 1973-74)
- Script automatically handles stat availability by year

**Duplicate Prevention:**
- INSERT uses NOT EXISTS clause
- Safe to rerun for same years
- Won't create duplicate records

## Success Criteria

- ✅ ~160,000+ records inserted for 1990-1996 period
- ✅ All 6 seasons have data (21990-21995, plus existing 21996)
- ✅ < 1% missing stats (NULL values) for core stats
- ✅ Michael Jordan's games present and validated
- ✅ All validation queries pass
- ✅ No checkpoint files remaining

## Next Steps

After successful acquisition:
1. Proceed to Phase 1.2 (Part 2): Acquire 1980s data
2. Or proceed to Phase 1.3: Acquire historical team box scores
3. Update documentation with new data coverage

## Notes

**Why Start with 1990s:**
- Highest value: Michael Jordan's championship years (1991-1993, 1996-1998)
- Complete stats: All modern metrics available
- Well-documented era: Easy to validate
- Smaller dataset: Faster acquisition and validation

**Data Quality:**
- Basketball-Reference is authoritative source
- 1990s data is highly reliable
- Expect minimal missing or incorrect data

**Performance:**
- Total processing time: 3-4 hours
- Network dependent: Slower on poor connections
- CPU usage: Low (mostly I/O bound)
- Memory usage: ~200-300 MB

**Storage:**
- CSV files: ~50-100 MB total
- Database growth: ~30-40 MB
- Total space needed: ~150 MB
