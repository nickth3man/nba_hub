# NBA Data Lakehouse

This project maintains a comprehensive NBA database using DuckDB, integrating data from multiple sources including Basketball-Reference.com and the official NBA Stats API.

## Directory Structure

```
webapp/
├── data/               # Database storage
│   └── nba.duckdb      # Main DuckDB database
├── src/
│   ├── scrapers/       # Data ingestion scripts
│   │   ├── scrape_contracts.py         # B-Ref contracts parser
│   │   ├── reference_shot_chart_scraper.py # B-Ref shot chart logic (Reference)
│   │   └── ...
│   └── analysis/       # Analysis scripts
├── tests/              # Verification and testing
│   ├── audit_consistency.py
│   └── test_nba_api.py
└── docs/               # Documentation
```

## Data Sources & Methods

1.  **Basketball-Reference.com**:
    *   **Contracts**: Parsed from `/contracts/players.html` (Use `src/scrapers/scrape_contracts.py`).
    *   **Shot Charts**: Can be parsed from HTML comments (Logic in `src/scrapers/reference_shot_chart_scraper.py`).
    *   **Note**: Direct scraping requires a proxy/browser environment due to anti-bot protections.

2.  **Official NBA Stats API (`nba_api`)**:
    *   **Play-by-Play**: Use `playbyplayv3` endpoint.
    *   **Shot Charts**: Use `shotchartdetail` endpoint.
    *   **Usage**: See `tests/test_nba_api.py` for examples.

## Database Schema

The `nba.duckdb` file contains over 70 tables including:
*   `player_game_stats_silver`: Box scores (Verified 99.99% accurate).
*   `games`: Schedule and results.
*   `player_contracts`: Salary data (Schema ready).
*   `play_by_play`: Possession-level data (Schema ready).

## Setup

1.  Install dependencies:
    ```bash
    pip install duckdb pandas requests beautifulsoup4 lxml nba_api
    ```

2.  Run analysis:
    ```bash
    python3 src/analysis/your_script.py
    ```
