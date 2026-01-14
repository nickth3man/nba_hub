# ETL Pipeline

This directory handles the Extract, Transform, and Load processes.

## Subdirectories

- **`ingest/`**: Scripts that populate the final analytical tables (`unified_*`) from staging or transformed data.
  - `ingest_all_players.py`: Populates `unified_players`.
  - `ingest_advanced_stats.py`: Ingests advanced metrics.
  - `ingest_awards.py`: Ingests historical awards.
  - `ingest_transactions.py`: Ingests player transactions.

- **`load/`**: Scripts that load raw data from CSV/JSON files into DuckDB staging tables.
  - `load_games.py`: Loads `Games.csv`.
  - `load_box_scores.py`: Loads box score data.
  - `init_*.py`: Initializes reference tables (awards, referees, coaches).

- **`transform/`**: Scripts that clean, normalize, and migrate data.
  - `migrate_unified_schema.py`: The main script for creating and populating the unified schema.
  - `fix_*.py`: One-off scripts to fix specific data issues (e.g., schema mismatches, early BAA games).
