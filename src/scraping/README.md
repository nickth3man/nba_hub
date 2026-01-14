# Web Scraping

This directory contains scripts to scrape historical NBA data from various websites (primarily Basketball-Reference).

## Subdirectories

- **`backfill/`**: Scripts designed to run once or periodically to fetch historical data that is missing.
  - `scrape_coaches_history.py`
  - `scrape_awards_voting.py`
  - `scrape_draft_history.py`

- **`sites/`**: Site-specific scraping logic and parsers.
  - `basketball_reference_*.py`: Modules for scraping specific sections of Basketball-Reference (games, awards, personnel).

## Files

- **`scrape_boxscore.js`**: A JavaScript/Node.js script (likely using Playwright) to scrape detailed box scores.
- **`README_BACKFILL.md`**: Specific instructions for backfilling early historical data.

## Usage

Most scrapers are invoked via the `src/cli/run_all.py` pipeline, but they can be run individually.

```bash
python src/scraping/backfill/scrape_coaches_history.py
```
