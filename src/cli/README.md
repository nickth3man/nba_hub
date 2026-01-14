# Command Line Interface

This directory contains the entry points for running the NBA Data Hub pipelines.

## Scripts

- **`main.py`**: General entry point (if applicable).
- **`run_all.py`**: The master script that executes the full end-to-end pipeline.
  - Initializes the database.
  - Runs backfill scrapers.
  - Loads raw data.
  - Performs transformations.
  - Ingests data into unified tables.
- **`run_init.py`**: Initializes the database schema and loads static reference data (referees, coaches, awards).

## Usage

To run the full pipeline:
```bash
python src/cli/run_all.py
```

To initialize the database only:
```bash
python src/cli/run_init.py
```
