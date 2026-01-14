# Backfill Early Games (1946-1955)

This script scrapes game data for the BAA/NBA seasons from 1947 to 1955 from Basketball Reference and adds it to the `games` table in DuckDB.

## Prerequisites

- Python 3.x
- `requests`
- `beautifulsoup4`
- `duckdb`

## Usage

1.  **Run the script:**

    ```bash
    python src/etl/ingest/backfill_early_games.py
    ```

    This will:
    - Scrape schedule pages for seasons 1947-1955.
    - Map team names to IDs (using `data/raw/TeamHistories.csv` and manual overrides).
    - Append new games to `data/raw/Games.csv`.
    - Refresh the `games` table in `data/nba.duckdb`.

2.  **Dry Run (Optional):**

    To test the scraping for 1947 without saving data:

    ```bash
    python src/etl/ingest/backfill_early_games.py --dry-run
    ```

## Verification

After running the script, you can verify the data using the provided check script:

```bash
python scripts/check_games.py
```

Expected output should show game counts for years 1946-1955 (approx 300-500 per season).

## Notes

- **Team Mapping:** Historical teams like "St. Louis Bombers", "Chicago Stags", etc., are mapped to their IDs found in `TeamHistories.csv`.
- **Missing IDs:** Teams not found in `TeamHistories.csv` (e.g., old Denver Nuggets 1949-50, old Baltimore Bullets) are assigned placeholder IDs (9070, 9071) to avoid conflict with modern franchises.
- **Date/Time:** Game times are estimated as 19:00:00 EST if not available.
