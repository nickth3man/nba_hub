# Awards Scraper

This directory contains scripts to scrape NBA awards voting data from Basketball-Reference.

## Setup

Ensure you have the required dependencies installed:
```bash
pip install requests beautifulsoup4 duckdb
```

## Usage

1. **Initialize the Database Table**
   Run the initialization script to create the `awards_voting` table in `data/nba.duckdb`.
   ```bash
   python src/db/init_awards_table.py
   ```

2. **Run the Scraper**
   Run the scraper script to fetch data and populate the database.
   ```bash
   python src/scraping/scrape_awards.py
   ```
   By default, it scrapes data from 2020 to 2024 for testing purposes. You can modify the `years` range in the `main()` function to scrape more history.

## Notes
- The scraper respects rate limits by sleeping 3-5 seconds between requests.
- It handles MVP, ROY, DPOY, SMOY, and MIP awards.
- Data is upserted, so running it multiple times for the same year is safe.
