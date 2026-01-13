# NBA Data Hub

A comprehensive NBA/BAA/ABA historical data lakehouse (1946-2026).

## Structure

- `data/`: DuckDB database and raw CSV/JSON data.
- `src/`: Core source code.
  - `core/`: Database connections and configuration.
  - `etl/`: Ingestion, loading, and transformation logic.
  - `scraping/`: Web scrapers for historical data.
  - `cli/`: Command-line interface scripts.
- `scripts/`: Maintenance and one-off scripts.
- `tests/`: Data integrity and schema tests.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python src/cli/run_init.py
   ```

3. Run the full pipeline:
   ```bash
   python src/cli/run_all.py
   ```

## Data Sources

- Kaggle (various datasets)
- NBA API
- Basketball-Reference (scraped)
- Octonion GitHub (BAA archives)
