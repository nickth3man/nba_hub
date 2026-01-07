# Phase 1.3 System Architecture

## Overview

This document describes the architecture and data flow for the Advanced Metrics Scraper implementation.

## System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Source Layer                           │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                  Basketball-Reference.com
                  /leagues/NBA_{year}_advanced.html
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Acquisition Layer                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  acquire_advanced_metrics.py                                │   │
│  │  ├── cloudscraper (Cloudflare bypass)                       │   │
│  │  ├── pandas.read_html (HTML parsing)                        │   │
│  │  ├── Rate limiting (1s delay)                               │   │
│  │  ├── Retry logic (3 attempts)                               │   │
│  │  └── CSV export                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Processing Layer                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Data Processing Pipeline                                   │   │
│  │  ├── Remove TOT rows (multi-team players)                   │   │
│  │  ├── Fuzzy player name matching (85% threshold)             │   │
│  │  ├── Team abbreviation mapping                              │   │
│  │  ├── Data type conversion (safe_float, safe_int)            │   │
│  │  ├── NULL handling                                          │   │
│  │  └── Season ID calculation                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Storage Layer                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  DuckDB Database (nba.duckdb)                               │   │
│  │  ┌────────────────────────────────────────────────────┐     │   │
│  │  │  player_season_advanced_stats                      │     │   │
│  │  │  ├── Primary Key: (player_id, season_id, team_id) │     │   │
│  │  │  ├── 24 metric columns                             │     │   │
│  │  │  ├── 6 indexes                                     │     │   │
│  │  │  └── INSERT OR IGNORE (duplicate prevention)       │     │   │
│  │  └────────────────────────────────────────────────────┘     │   │
│  │  ┌────────────────────────────────────────────────────┐     │   │
│  │  │  Reference Tables                                   │     │   │
│  │  │  ├── common_player_info (player mapping)           │     │   │
│  │  │  └── team (team mapping)                           │     │   │
│  │  └────────────────────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Validation Layer                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  validate_advanced_metrics.py                               │   │
│  │  ├── Record counts                                          │   │
│  │  ├── Known player benchmarks                               │   │
│  │  ├── Data completeness                                      │   │
│  │  ├── Multi-team player verification                         │   │
│  │  └── Duplicate detection                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────────┐
│  Basketball-     │
│  Reference.com   │
│                  │
│  Advanced Stats  │
│  HTML Tables     │
└────────┬─────────┘
         │
         │ HTTP GET (cloudscraper)
         │
         ▼
┌─────────────────────────────────────────┐
│  Raw HTML Response                      │
│  • ~500 player rows per season          │
│  • Includes TOT rows for traded players │
│  • String data types                    │
└────────┬────────────────────────────────┘
         │
         │ pandas.read_html()
         │
         ▼
┌─────────────────────────────────────────┐
│  DataFrame (Raw)                        │
│  • Player names (BR format)             │
│  • Team abbreviations (BR format)       │
│  • 24+ stat columns                     │
│  • TOT rows present                     │
└────────┬────────────────────────────────┘
         │
         │ process_advanced_stats()
         │
         ▼
┌─────────────────────────────────────────┐
│  Processing Steps:                      │
│  1. Filter out TOT rows                 │
│  2. Fuzzy match player names            │
│  3. Map team abbreviations              │
│  4. Convert data types                  │
│  5. Calculate season_id                 │
│  6. Handle NULL values                  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  DataFrame (Processed)                  │
│  • player_id (mapped to database)       │
│  • team_id (mapped to database)         │
│  • season_id (calculated)               │
│  • Typed columns (DOUBLE, INTEGER)      │
│  • No TOT rows                          │
└────────┬────────────────────────────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌────────────────┐  ┌──────────────────────┐
│  CSV Export    │  │  Database Insert     │
│  data/         │  │  INSERT OR IGNORE    │
│  advanced_     │  │  player_season_      │
│  metrics_      │  │  advanced_stats      │
│  {year}.csv    │  │                      │
└────────────────┘  └──────────────────────┘
```

## Component Interactions

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interaction Layer                       │
└─────────────────────────────────────────────────────────────────┘
        │                    │                     │
        │                    │                     │
   ┌────▼────┐        ┌──────▼──────┐      ┌──────▼──────┐
   │  test_  │        │   create_   │      │  acquire_   │
   │  env    │        │   table     │      │  advanced   │
   │  .py    │        │   .py       │      │  _metrics   │
   └────┬────┘        └──────┬──────┘      │  .py        │
        │                    │             └──────┬──────┘
        │                    │                    │
        ▼                    ▼                    │
   ┌─────────────────────────────────────┐       │
   │         DuckDB Database             │       │
   │         (nba.duckdb)                │◄──────┘
   └─────────────────┬───────────────────┘
                     │
                     │
              ┌──────▼──────┐
              │  validate_  │
              │  advanced   │
              │  _metrics   │
              │  .py        │
              └─────────────┘
```

## Mapping Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Player Name Mapping                          │
└─────────────────────────────────────────────────────────────────┘

Basketball-Reference Name          Fuzzy Match          Database
┌─────────────────────┐           (85% similarity)    ┌──────────────┐
│  "LeBron James"     │  ────────────────────────────>│  person_id   │
│  "Nikola Jokić"     │                               │  203999      │
│  "Giannis           │                               │  ....        │
│   Antetokounmpo"    │                               │              │
└─────────────────────┘                               └──────────────┘
         │                                                     │
         │  1. Try exact match                                │
         │  2. Try fuzzy match                                │
         │  3. Log unmapped (<5%)                             │
         │                                                     │
┌─────────────────────────────────────────────────────────────────┐
│  player_name_to_id_map (dictionary)                             │
│  • display_first_last → person_id                               │
│  • first_name + last_name → person_id                           │
│  • Loaded from common_player_info table                         │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    Team Abbreviation Mapping                    │
└─────────────────────────────────────────────────────────────────┘

Basketball-Reference          Mapping Dictionary       Database
┌─────────────────┐          ┌──────────────────┐    ┌──────────┐
│  PHO            │  ──────> │  PHO → PHX       │ ─> │  team_id │
│  BRK            │          │  BRK → BKN       │    │  1610612738│
│  CHO            │          │  CHO → CHA       │    │  ....    │
│  SEA (historic) │          │  SEA → OKC       │    │          │
└─────────────────┘          └──────────────────┘    └──────────┘

                             BREF_TO_NBA_TEAM_MAP
                             • 30+ current teams
                             • Historical variations
                             • Defunct team mapping
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      HTTP Request                               │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Try request    │
                    │  (Attempt 1)    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                Success           Failure
                    │                 │
                    ▼                 ▼
            ┌──────────────┐   ┌──────────────┐
            │  Continue    │   │  429 Error?  │
            └──────────────┘   └──────┬───────┘
                                      │
                              ┌───────┴───────┐
                              │               │
                            Yes              No
                              │               │
                              ▼               ▼
                      ┌───────────────┐  ┌────────────┐
                      │  Wait 5s      │  │  Retry     │
                      │  Retry        │  │  or Fail   │
                      │  (Attempt 2)  │  └────────────┘
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │  Attempt 3    │
                      │  (Wait 10s)   │
                      └───────┬───────┘
                              │
                      ┌───────┴───────┐
                      │               │
                  Success         Failure
                      │               │
                      ▼               ▼
              ┌──────────────┐  ┌────────────┐
              │  Continue    │  │  Log error │
              │              │  │  Skip year │
              └──────────────┘  └────────────┘
```

## Database Schema Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    Database Schema                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│  common_player_info      │
│  ┌────────────────────┐  │
│  │ person_id (PK)     │◄─┼─────────┐
│  │ display_first_last │  │         │
│  │ first_name         │  │         │
│  │ last_name          │  │         │
│  └────────────────────┘  │         │
└──────────────────────────┘         │
                                     │
                                     │  Foreign Key
┌──────────────────────────┐         │  (not enforced)
│  team                    │         │
│  ┌────────────────────┐  │         │
│  │ id (PK)            │◄─┼────┐    │
│  │ abbreviation       │  │    │    │
│  │ full_name          │  │    │    │
│  └────────────────────┘  │    │    │
└──────────────────────────┘    │    │
                                │    │
                                │    │
┌───────────────────────────────┼────┼────────────────────────────┐
│  player_season_advanced_stats │    │                            │
│  ┌────────────────────────────┼────┼───────────────────┐        │
│  │ player_id ─────────────────┘    │                   │        │
│  │ season_id                       │                   │        │
│  │ team_id ────────────────────────┘                   │        │
│  │ games_played                                        │        │
│  │ minutes_played                                      │        │
│  │ per, ts_pct, efg_pct, ...                          │        │
│  │ ows, dws, ws, ws_48                                 │        │
│  │ obpm, dbpm, bpm, vorp                               │        │
│  │                                                     │        │
│  │ PRIMARY KEY (player_id, season_id, team_id)        │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                  │
│  INDEXES:                                                        │
│  • idx_advanced_stats_player (player_id)                        │
│  • idx_advanced_stats_season (season_id)                        │
│  • idx_advanced_stats_team (team_id)                            │
│  • idx_advanced_stats_vorp (vorp DESC)                          │
│  • idx_advanced_stats_per (per DESC)                            │
│  • idx_advanced_stats_ws (ws DESC)                              │
└──────────────────────────────────────────────────────────────────┘
```

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  Option A: Automated (run_phase_1_3.py)                        │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─► Step 1: test_environment.py
    │   └─► Check dependencies, database, tables
    │
    ├─► Step 2: create_advanced_stats_table.py
    │   └─► Execute SQL schema, verify creation
    │
    ├─► Step 3: acquire_advanced_metrics.py --dry-run
    │   └─► Test 2024 season (no DB insert)
    │
    ├─► Step 4: acquire_advanced_metrics.py (2024)
    │   └─► Load 2024 season data
    │
    ├─► Step 5: acquire_advanced_metrics.py (1980)
    │   └─► Load 1980 historical data
    │
    └─► Step 6: Display validation instructions


┌─────────────────────────────────────────────────────────────────┐
│  Option B: Manual Execution                                    │
└─────────────────────────────────────────────────────────────────┘
    │
    └─► User runs individual scripts as needed
        • Test environment
        • Create table
        • Run scraper (with custom parameters)
        • Validate data
        • Full backfill
```

## Performance Characteristics

```
┌─────────────────────────────────────────────────────────────────┐
│                    Performance Profile                          │
└─────────────────────────────────────────────────────────────────┘

Single Season (e.g., 2024):
    HTTP Request:           ~2 seconds
    HTML Parsing:           ~0.5 seconds
    Data Processing:        ~1 second
    Database Insert:        ~0.5 seconds
    Rate Limit Delay:       1 second
    ────────────────────────────────────
    Total per season:       ~5 seconds

Full Backfill (1974-2023):
    50 seasons × 5 seconds = 250 seconds (ideal)
    With retries and delays = ~2-3 hours (realistic)

Database Operations:
    Table creation:         <1 second
    Index creation:         <1 second per index
    INSERT performance:     ~1000 rows/second
    Query performance:      <100ms (with indexes)
```

## Security Considerations

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Architecture                        │
└─────────────────────────────────────────────────────────────────┘

1. Web Scraping:
   • Uses cloudscraper (respects robots.txt)
   • Rate limiting (1 second delay)
   • No authentication required
   • Read-only operations

2. Database:
   • Local DuckDB file (no network exposure)
   • INSERT OR IGNORE (prevents duplicates)
   • No SQL injection risk (parameterized queries)
   • No credentials required

3. Data Validation:
   • Type checking (safe_float, safe_int)
   • NULL handling
   • Range validation (implicit via data types)
   • Duplicate prevention (primary key)

4. File System:
   • CSV exports to local directory
   • No sensitive data exposure
   • Read-only source data
```

## Extensibility Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    Extension Architecture                       │
└─────────────────────────────────────────────────────────────────┘

1. New Metrics:
   • Add columns to SQL schema
   • Update scraper column mapping
   • Add to safe_float() processing
   • Update validation checks

2. New Data Sources:
   • Create new scraper class
   • Implement same interface
   • Use same database table
   • Merge data by primary key

3. Custom Mappings:
   • Extend BREF_TO_NBA_TEAM_MAP
   • Add manual player mappings
   • Override fuzzy match threshold
   • Add custom validation rules

4. Additional Seasons:
   • Run with new year range
   • INSERT OR IGNORE handles duplicates
   • Automatic CSV export
   • Incremental updates supported
```

## Monitoring and Logging

```
┌─────────────────────────────────────────────────────────────────┐
│                    Logging Architecture                         │
└─────────────────────────────────────────────────────────────────┘

Console Output:
    [OK]      - Successful operation
    [INFO]    - Informational message
    [WARNING] - Non-fatal issue (e.g., unmapped player)
    [ERROR]   - Fatal error

Progress Reporting:
    • Seasons processed
    • Records downloaded
    • Records inserted
    • Unmapped counts
    • Error counts

CSV Exports:
    • One file per season
    • Complete data snapshot
    • Can be used for debugging
    • Enables data recovery

Validation Output:
    • Record counts by season
    • Known player benchmarks
    • Data completeness percentages
    • Duplicate detection results
```

## Deployment Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                    Deployment Architecture                      │
└─────────────────────────────────────────────────────────────────┘

Development Environment:
    Windows 10/11
    Python 3.8+
    Local DuckDB file
    Command-line execution

Production Considerations:
    • Can run on any OS (cross-platform)
    • Cron job for annual updates
    • Docker containerization possible
    • Cloud deployment supported
    • Horizontal scaling not required (sequential processing)

File Locations:
    Database:    c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb
    Scripts:     nba_database_documentation\scripts\
    SQL:         nba_database_documentation\sql_queries\
    CSV Output:  nba_database_documentation\data\
    Docs:        nba_database_documentation\*.md
```

---

**Architecture Version**: 1.0
**Last Updated**: 2026-01-06
**Status**: Production Ready
