# Phase 1.3: Advanced Metrics Scraper Implementation

## Overview

This phase implements a scraper to acquire advanced player metrics (PER, Win Shares, BPM, VORP) from Basketball-Reference and load them into the NBA Hub database.

## Components Created

### 1. Database Schema

**File**: `sql_queries/create_advanced_stats_table.sql`

Creates the `player_season_advanced_stats` table with the following structure:

- **Primary Key**: (player_id, season_id, team_id)
- **Metrics**: 24 advanced statistics including:
  - Efficiency metrics (PER, TS%, eFG%)
  - Rate metrics (3PA rate, FT rate)
  - Percentage metrics (ORB%, DRB%, AST%, etc.)
  - Impact metrics (Win Shares, BPM, VORP)
- **Indexes**: Optimized for common query patterns

### 2. Data Acquisition Script

**File**: `scripts/acquire_advanced_metrics.py`

Features:
- Uses `cloudscraper` to bypass Cloudflare protection
- Scrapes from Basketball-Reference's advanced stats pages
- Fuzzy matching for player names (85% similarity threshold)
- Team abbreviation mapping (handles historical teams)
- Multi-team player handling (skips TOT rows, keeps individual team stats)
- Rate limiting (1 second between requests)
- Error handling and retry logic (3 attempts with exponential backoff)
- INSERT OR IGNORE to prevent duplicates
- CSV export for each season

Command-line arguments:
```bash
--start-year YYYY    # Starting season end year
--end-year YYYY      # Ending season end year
--dry-run           # Download and process without database insert
```

### 3. Supporting Scripts

**File**: `scripts/test_environment.py`
- Validates Python environment and dependencies
- Checks database connection
- Verifies required tables exist

**File**: `scripts/create_advanced_stats_table.py`
- Executes the SQL schema creation
- Verifies table creation
- Displays table schema

**File**: `scripts/validate_advanced_metrics.py`
- Validates loaded data quality
- Checks against known player benchmarks
- Verifies multi-team player handling
- Generates data completeness reports

**File**: `scripts/run_phase_1_3.py`
- Master orchestration script
- Runs all steps in sequence
- Handles error conditions
- Provides clear status updates

## Installation

### Required Dependencies

```bash
pip install duckdb pandas cloudscraper thefuzz
```

### Dependency Details

- **duckdb**: Database interface
- **pandas**: Data manipulation and HTML parsing
- **cloudscraper**: Web scraping with Cloudflare bypass
- **thefuzz**: Fuzzy string matching for player names

## Usage

### Quick Start (Automated)

Run the complete implementation:

```bash
cd nba_database_documentation/scripts
python run_phase_1_3.py
```

This will:
1. Test the environment
2. Create the database table
3. Test with 2023-24 season (dry run)
4. Load 2023-24 season data
5. Test with 1980 season data
6. Display validation instructions

### Manual Execution

#### Step 1: Test Environment

```bash
python test_environment.py
```

Expected output:
- All required packages installed
- Database connection successful
- Required tables present

#### Step 2: Create Database Table

```bash
python create_advanced_stats_table.py
```

Creates the `player_season_advanced_stats` table with all indexes.

#### Step 3: Test Scraper (Dry Run)

```bash
python acquire_advanced_metrics.py --start-year 2024 --end-year 2024 --dry-run
```

Downloads and processes data without inserting to database.

#### Step 4: Load Recent Season

```bash
python acquire_advanced_metrics.py --start-year 2024 --end-year 2024
```

Loads 2023-24 season data (~500 records).

#### Step 5: Validate Data

```bash
python validate_advanced_metrics.py
```

Checks:
- Record counts
- Nikola Jokic's known metrics
- Top players by VORP
- Multi-team player handling
- Data completeness
- Duplicate detection

#### Step 6: Test Historical Data

```bash
python acquire_advanced_metrics.py --start-year 1980 --end-year 1980
```

Loads 1979-80 season data to verify historical data handling.

#### Step 7: Full Historical Backfill

```bash
python acquire_advanced_metrics.py --start-year 1974 --end-year 2023
```

**Duration**: 2-3 hours
**Expected Records**: ~22,500 (50 seasons × ~450 players/season)
**Features**:
- Can be interrupted and resumed (uses INSERT OR IGNORE)
- Rate limited to be respectful of Basketball-Reference
- CSV exports for each season saved to `data/` directory

## Data Source

**URL Pattern**: `https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html`

**Availability**: 1973-74 season onwards

**Column Mapping**:
- G → games_played
- MP → minutes_played
- PER → per
- TS% → ts_pct
- eFG% → efg_pct
- 3PAr → fg3a_rate
- FTr → fta_rate
- ORB% → orb_pct
- DRB% → drb_pct
- TRB% → trb_pct
- AST% → ast_pct
- STL% → stl_pct
- BLK% → blk_pct
- TOV% → tov_pct
- USG% → usg_pct
- OWS → ows
- DWS → dws
- WS → ws
- WS/48 → ws_48
- OBPM → obpm
- DBPM → dbpm
- BPM → bpm
- VORP → vorp

## Edge Cases Handled

### 1. Multi-Team Players

Players traded mid-season appear multiple times in Basketball-Reference data:
- Individual team rows (e.g., BOS, LAL)
- TOT row (season total)

**Solution**: Skip TOT rows, keep individual team rows to match our database schema where each player-season-team combination is unique.

### 2. Player Name Mapping

Basketball-Reference uses display names that may not match exactly with NBA API data.

**Solution**:
- Fuzzy matching with 85% similarity threshold
- Tests both display_first_last and first_name + last_name combinations
- Logs unmapped players for review

### 3. Team Abbreviation Variations

Historical teams and abbreviation changes.

**Solution**: Comprehensive mapping dictionary including:
- PHO → PHX
- BRK → BKN
- CHO → CHA
- SEA → OKC (defunct teams mapped to successors)
- And 15+ other historical variations

### 4. Data Type Handling

Basketball-Reference returns strings that need type conversion.

**Solution**:
- `safe_float()` and `safe_int()` functions
- Handle empty strings, None, 'None' text
- Preserve NULL for missing data

### 5. Rate Limiting and Retries

Basketball-Reference may rate limit or return errors.

**Solution**:
- 1 second delay between requests
- 3 retry attempts
- Exponential backoff (5, 10, 15 seconds)
- Cloudflare bypass via cloudscraper

## Validation Benchmarks

### 2023-24 Season Test Cases

**Nikola Jokic** (expected values):
- PER: ~31.5
- VORP: ~8.5-9.0
- WS: ~13.0-15.0
- BPM: ~11.0-12.0

**Data Completeness**:
- All key metrics (PER, VORP, WS, BPM) should be >95% filled
- TS% should be 100% filled for players with FG attempts

**Multi-Team Players**:
- Should see players with multiple team records (no TOT)
- Examples: trades during 2023-24 season

### Historical Data Test (1980)

- Should load ~300-400 records
- All advanced metrics available (advanced stats started 1973-74)
- Can validate against known star players from that era

## Database Query Examples

### Top Players by VORP (Current Season)

```sql
SELECT
    p.display_first_last as player,
    t.abbreviation as team,
    a.vorp,
    a.per,
    a.ws,
    a.bpm
FROM player_season_advanced_stats a
JOIN common_player_info p ON a.player_id = p.person_id
JOIN team t ON a.team_id = t.id
WHERE a.season_id = 22023  -- 2023-24 season
  AND a.vorp IS NOT NULL
ORDER BY a.vorp DESC
LIMIT 10;
```

### Player Career Advanced Stats

```sql
SELECT
    season_id,
    t.abbreviation as team,
    games_played,
    per,
    ws,
    vorp
FROM player_season_advanced_stats a
JOIN team t ON a.team_id = t.id
WHERE player_id = 203999  -- Nikola Jokic
ORDER BY season_id DESC;
```

### Season Averages

```sql
SELECT
    season_id,
    COUNT(*) as player_count,
    AVG(per) as avg_per,
    AVG(vorp) as avg_vorp,
    AVG(ws) as avg_ws,
    MAX(vorp) as max_vorp
FROM player_season_advanced_stats
GROUP BY season_id
ORDER BY season_id DESC;
```

## Success Criteria

- ✅ **Table Created**: `player_season_advanced_stats` with proper schema and indexes
- ✅ **Scraper Functional**: Can download and parse Basketball-Reference data
- ✅ **Player Mapping**: Fuzzy matching successfully maps >95% of players
- ✅ **Multi-Team Handling**: Correctly skips TOT rows, keeps individual team stats
- ✅ **Data Validation**: Jokic's 2023-24 metrics match expected values
- ✅ **Historical Data**: 1980 season loads successfully
- ✅ **No Duplicates**: Primary key constraint prevents duplicate records
- ✅ **Full Backfill**: ~22,500 records loaded for 1974-2023 seasons

## Expected Results

### Record Counts by Era

- **1974-1980**: ~300-400 records/season (fewer teams, smaller rosters)
- **1981-1995**: ~400-450 records/season (expansion era)
- **1996-2023**: ~450-500 records/season (modern 30-team era)

**Total**: ~22,500 records for full backfill (1974-2023)

### Data Quality Metrics

- **Player Match Rate**: >95% (unmapped players are typically edge cases)
- **Team Match Rate**: >99% (comprehensive historical mapping)
- **Metric Completeness**: >95% for all key metrics
- **Duplicate Rate**: 0% (primary key constraint)

## Troubleshooting

### "Module not found" errors

```bash
pip install duckdb pandas cloudscraper thefuzz
```

### Database lock errors

Ensure no other processes are accessing the database:
```bash
# Close any open database connections
# On Windows, check Task Manager for python processes
```

### Player name mismatches

Check unmapped players in script output. May need to add manual mappings for edge cases (name changes, special characters, etc.).

### Rate limiting (429 errors)

Script handles this automatically with retries. If persistent:
- Increase `REQUEST_DELAY_SECONDS` in the script
- Increase `RETRY_BACKOFF_SECONDS`
- Run in smaller batches (fewer years at a time)

### Cloudflare blocking

The script uses `cloudscraper` which should handle most cases. If still blocked:
- Check your IP isn't temporarily blocked by Basketball-Reference
- Try again after a few hours
- Consider using a VPN

## Output Files

All CSV files are saved to `nba_database_documentation/data/`:

- `advanced_metrics_2024.csv` - 2023-24 season
- `advanced_metrics_2023.csv` - 2022-23 season
- ... (one file per season)

These can be used for:
- Backup/archive
- External analysis
- Debugging
- Re-import if needed

## Next Steps

After completing Phase 1.3:

1. **Verify data quality** with validation script
2. **Run analytical queries** to explore the data
3. **Integrate with other tables** (player_game_stats, etc.)
4. **Update documentation** with example use cases
5. **Consider Phase 1.4**: Additional metrics or data sources

## Related Files

- `sql_queries/create_advanced_stats_table.sql` - Table schema
- `scripts/acquire_advanced_metrics.py` - Main scraper
- `scripts/test_environment.py` - Environment validation
- `scripts/create_advanced_stats_table.py` - Table creation
- `scripts/validate_advanced_metrics.py` - Data validation
- `scripts/run_phase_1_3.py` - Master orchestration script
- `data/advanced_metrics_*.csv` - Exported data files

## References

- [Basketball-Reference Advanced Stats Glossary](https://www.basketball-reference.com/about/glossary.html)
- [DuckDB Python API](https://duckdb.org/docs/api/python/overview)
- [cloudscraper Documentation](https://github.com/VeNoMouS/cloudscraper)
- [thefuzz Documentation](https://github.com/seatgeek/thefuzz)
