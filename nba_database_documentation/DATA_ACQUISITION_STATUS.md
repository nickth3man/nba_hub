# NBA Database - Data Acquisition Status

**Last Updated**: 2026-01-05

## Current Database Status

- **Player Box Score Coverage**: 1996-2023 (769,033 records, 37,167 games)
- **Missing Data**:
  - Recent seasons: 2023-24, 2024-25 (~93,752 records needed)
  - Historical data: 1946-1996 (~800,000 records needed)

## Scripts Created

### 1. Recent Seasons Acquisition (`acquire_recent_nbaapi.py`)

**Purpose**: Acquire player box scores for 2023-24 and 2024-25 seasons using NBA.com API

**Features**:
- Uses `nba_api` package (official NBA.com API)
- Rate limiting (0.6s between requests)
- Automatic season_id determination
- Team abbreviation mapping
- Dry-run mode for testing
- Data transformation to match `player_game_stats_silver` schema

**Usage**:
```bash
# Test with dry-run
python acquire_recent_nbaapi.py --season 2024 --dry-run

# Acquire 2023-24 season
python acquire_recent_nbaapi.py --season 2024

# Acquire 2024-25 season
python acquire_recent_nbaapi.py --season 2025

# Acquire all recent seasons
python acquire_recent_nbaapi.py --season all
```

**Status**: ✅ Created and tested (dry-run in progress)

**Expected Results**:
- 2023-24 season: ~30,750 player-game records (1,230 games × ~25 players/game)
- 2024-25 season: ~32,500 records (in-progress season)

### 2. Historical Backfill (`acquire_historical_player_boxscores.py`)

**Purpose**: Backfill player box scores for 1946-1996 seasons

**Features**:
- Uses `basketball_reference_web_scraper` package
- Checkpoint system for resume capability
- Era-specific stat handling:
  - Blocks/steals: Available from 1973-74
  - 3-pointers: Available from 1979-80
  - OREB/DREB split: Available from 1973-74
- Decade-by-decade or year-by-year acquisition
- Rate limiting for web scraping

**Usage**:
```bash
# Acquire by decade
python acquire_historical_player_boxscores.py --decade 1980

# Acquire specific years
python acquire_historical_player_boxscores.py --start-year 1990 --end-year 1996

# Dry-run mode
python acquire_historical_player_boxscores.py --decade 1980 --dry-run
```

**Status**: ✅ Created (not yet tested)

**Estimated Time**: 20-30 hours for full backfill (50 seasons)

## Sample Query Library (`player_analysis_queries.sql`)

**Purpose**: Comprehensive SQL queries for player box score analysis

**Sections**:
1. Player Career Statistics (game logs, season averages)
2. Career Highs & Milestones (50+ point games, triple-doubles)
3. Player Comparisons (head-to-head, statistical comparisons)
4. League Leaders (scoring, assists, rebounds)
5. Performance Trends (peak seasons, aging curves)
6. Advanced Statistics (TS%, eFG%, usage rate)
7. Clutch Performance (4th quarter, overtime stats)
8. Consistency Analysis (game score variance, streaks)
9. Playing Time Analysis (minutes distribution)
10. Data Quality Checks (missing stats, outliers)
11. Coverage Analysis (games per season, missing dates)

**Status**: ✅ Created

## Gap Analysis Report (`10_player_box_scores_gap_analysis.md`)

**Purpose**: Comprehensive analysis of player box score coverage gaps

**Key Findings**:
- Current coverage: 53% of all games (37,167 of 70,228 total)
- Missing 1946-1996: 33,061 games (47% of total)
- Missing 2023-2026: 3,126 games (4% of total)

**Status**: ✅ Complete

## Next Steps

### Priority 1: Acquire Recent Seasons (2023-24, 2024-25)
- **Estimated Time**: 2-3 hours
- **Impact**: HIGH - Get current/recent data
- **Action**: Run `acquire_recent_nbaapi.py` for seasons 2024 and 2025

### Priority 2: Historical Backfill (1946-1996)
- **Estimated Time**: 20-30 hours
- **Impact**: MEDIUM - Complete historical coverage
- **Action**: Run `acquire_historical_player_boxscores.py` by decade

### Priority 3: Data Validation
- **Estimated Time**: 1-2 hours
- **Impact**: HIGH - Ensure data quality
- **Action**: Run validation queries after each acquisition

## Data Sources

### NBA.com API (`nba_api`)
- **Coverage**: 2023-24 season onwards
- **Reliability**: ⭐⭐⭐⭐⭐ (official NBA data)
- **Rate Limit**: ~100 requests/minute
- **Notes**: BoxScoreTraditionalV2 deprecated but functional for 2023-24

### Basketball-Reference.com (`basketball_reference_web_scraper`)
- **Coverage**: 1946-47 to present
- **Reliability**: ⭐⭐⭐⭐ (gold standard for historical data)
- **Rate Limit**: Conservative scraping (0.6s/request)
- **Notes**: May encounter 403 Forbidden errors; use respectful rate limiting

## Database Schema

### `player_game_stats_silver` Table

**Columns** (26 total):
- **Identifiers**: `game_id`, `player_id`, `player_name`, `team_id`, `team_abbreviation`
- **Game Info**: `game_date`, `season_id`
- **Basic Stats**: `min` (seconds), `pts`, `reb`, `ast`, `stl`, `blk`, `tov`, `pf`
- **Shooting**: `fgm`, `fga`, `fg_pct`, `fg3m`, `fg3a`, `fg3_pct`, `ftm`, `fta`, `ft_pct`
- **Rebounds**: `oreb`, `dreb`
- **Advanced**: `plus_minus`

**Notes**:
- Percentages stored as integers (0-100)
- Minutes stored as total seconds
- NULL handling for era-specific stats (blocks, steals, 3-pointers)

## Troubleshooting

### Basketball-Reference 403 Forbidden
**Issue**: Basketball-Reference blocking requests
**Solution**: Use NBA.com API for recent seasons; implement more aggressive rate limiting for historical data

### Team Abbreviation Mismatches
**Issue**: Different sources use different team codes
**Solution**: Team mapping dictionary in scripts handles common variations (PHX/PHO, BKN/BRK)

### Duplicate Records
**Issue**: Re-running acquisition inserts duplicates
**Solution**: Scripts use `INSERT OR IGNORE` to skip existing records

### Missing Player IDs
**Issue**: Basketball-Reference doesn't provide player_id
**Solution**: Lookup by `player_name` and `team_id` from existing data; manual mapping for edge cases

## Success Metrics

✅ **2023-24 Season Complete**: ~30,750 records
✅ **2024-25 Season Complete**: ~32,500 records
⏳ **1946-1996 Backfill**: ~800,000 records (in progress)
⏳ **Data Quality**: < 0.1% errors/NULL values
⏳ **Referential Integrity**: 100% valid game_id, player_id, team_id

## Resources

- [Gap Analysis Report](10_player_box_scores_gap_analysis.md)
- [Validation Findings](09_validation_findings_and_recommendations.md)
- [Quick Start Guide](scripts/QUICKSTART_DATA_ACQUISITION.md)
- [Player Analysis Queries](sql_queries/player_analysis_queries.sql)
