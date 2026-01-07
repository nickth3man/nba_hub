# Phase 1.3 Quick Start Guide

## Overview

This guide provides the fastest path to implement the Advanced Metrics Scraper.

## Prerequisites

1. Python 3.8+ installed
2. Access to `nba.duckdb` database
3. Internet connection

## Installation (5 minutes)

```bash
# Install required packages
pip install duckdb pandas cloudscraper thefuzz

# Navigate to scripts directory
cd nba_database_documentation/scripts
```

## Option A: Automated Execution (Recommended)

Run the complete implementation with one command:

```bash
python run_phase_1_3.py
```

This will:
1. ✅ Test environment and dependencies
2. ✅ Create database table
3. ✅ Test scraper with 2023-24 season (dry run)
4. ✅ Load 2023-24 season data
5. ✅ Test with 1980 historical data
6. ✅ Display validation instructions

**Duration**: ~10 minutes

## Option B: Manual Step-by-Step

### Step 1: Test Environment (1 minute)

```bash
python test_environment.py
```

Expected: All checks pass ✅

### Step 2: Create Table (1 minute)

```bash
python create_advanced_stats_table.py
```

Expected: Table created with 24 columns ✅

### Step 3: Test Scraper (2 minutes)

```bash
python acquire_advanced_metrics.py --start-year 2024 --end-year 2024 --dry-run
```

Expected: Downloads ~500 records, no database insert ✅

### Step 4: Load 2023-24 Season (2 minutes)

```bash
python acquire_advanced_metrics.py --start-year 2024 --end-year 2024
```

Expected: Inserts ~500 records to database ✅

### Step 5: Validate Data (1 minute)

```bash
python validate_advanced_metrics.py
```

Expected: All validation checks pass ✅

### Step 6: Load Historical Test (2 minutes)

```bash
python acquire_advanced_metrics.py --start-year 1980 --end-year 1980
```

Expected: Inserts ~350 records for 1980 season ✅

## Full Historical Backfill (Optional)

After successful testing, load all available data:

```bash
python acquire_advanced_metrics.py --start-year 1974 --end-year 2023
```

- **Duration**: 2-3 hours
- **Records**: ~22,500
- **Seasons**: 50 (1973-74 through 2022-23)
- **Can be interrupted**: Uses INSERT OR IGNORE, safe to restart

## Verification Queries

### Check Record Count

```bash
python -c "import duckdb; conn = duckdb.connect('../../nba.duckdb'); print(f'Total records: {conn.execute(\"SELECT COUNT(*) FROM player_season_advanced_stats\").fetchone()[0]:,}'); conn.close()"
```

### View Nikola Jokic Stats

```sql
SELECT
    p.display_first_last,
    a.season_id,
    a.per,
    a.vorp,
    a.ws,
    a.bpm
FROM player_season_advanced_stats a
JOIN common_player_info p ON a.player_id = p.person_id
WHERE p.display_first_last = 'Nikola Jokic'
  AND a.season_id = 22023;
```

Expected values:
- PER: ~31.5
- VORP: ~8.5-9.0
- WS: ~13.0-15.0

## Troubleshooting

### Missing packages?

```bash
pip install duckdb pandas cloudscraper thefuzz
```

### Database not found?

Ensure you're running from the correct directory:
```bash
cd c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\scripts
```

### Rate limited (429 errors)?

Wait a few minutes and retry. The script handles this automatically with exponential backoff.

### Player names not matching?

This is normal for ~5% of players (edge cases, name variations). The script logs these for review.

## Success Criteria

After running the automated script, you should have:

- ✅ New table: `player_season_advanced_stats`
- ✅ ~500 records for 2023-24 season
- ✅ ~350 records for 1980 season
- ✅ CSV exports in `data/` directory
- ✅ No duplicate records
- ✅ Nikola Jokic's stats match expected values

## Next Steps

1. **Run validation** to confirm data quality
2. **Load full history** (1974-2023) if desired
3. **Explore the data** with analytical queries
4. **Integrate** with other database tables

## Time Estimate

| Task | Duration |
|------|----------|
| Installation | 5 minutes |
| Automated execution | 10 minutes |
| Validation | 5 minutes |
| **Total** | **20 minutes** |
| Full backfill (optional) | 2-3 hours |

## Help

For detailed information, see:
- `PHASE_1_3_ADVANCED_METRICS.md` - Complete documentation
- `scripts/acquire_advanced_metrics.py` - Script comments
- `sql_queries/create_advanced_stats_table.sql` - Table schema

## Common Commands

```bash
# Test everything
python run_phase_1_3.py

# Load single season
python acquire_advanced_metrics.py --start-year 2024 --end-year 2024

# Load decade
python acquire_advanced_metrics.py --start-year 2010 --end-year 2019

# Validate data
python validate_advanced_metrics.py

# Full backfill
python acquire_advanced_metrics.py --start-year 1974 --end-year 2023
```
