# Architecture

The NBA Data Hub is designed as a modular data lakehouse using DuckDB as the central storage engine.

## Directory Structure

- **`src/`**: Contains the source code.
  - **`core/`**: Core infrastructure code.
    - `config.py`: Configuration settings and file paths.
    - `database.py`: DuckDB connection management.
  - **`etl/`**: Extract, Transform, Load pipelines.
    - `load/`: Scripts to load raw data (CSV, JSON) into DuckDB staging tables.
    - `transform/`: Scripts to clean and normalize data into a unified schema.
    - `ingest/`: Scripts to populate the final analytical tables from staging/transformed data.
  - **`scraping/`**: Web scrapers using Playwright and BeautifulSoup to fetch data from external sources (e.g., Basketball-Reference).
  - **`cli/`**: Command-line entry points for running the pipelines.
- **`data/`**: Data storage.
  - `raw/`: Raw CSV and JSON files.
  - `nba.duckdb`: The main DuckDB database file.
- **`scripts/`**: Utility and maintenance scripts.
- **`tests/`**: Unit and integration tests.

## Data Flow

The data pipeline follows a **Scrape -> Load -> Transform -> Ingest** pattern:

1.  **Scrape/Extract**:
    - Data is scraped from websites or fetched from APIs.
    - Raw HTML or JSON is saved to `data/raw/`.

2.  **Loading**:
    - Raw CSV/JSON files are loaded into DuckDB as **Staging Tables**.
    - These tables mirror the structure of the raw files.

3.  **Transformation**:
    - Data is cleaned, cast to correct types, and normalized.
    - Schema migrations are applied to ensure consistency.

4.  **Ingestion**:
    - Transformed data is inserted into **Unified Tables**.
    - These tables form the core data model for analysis.

## Database Schema

The database uses a relational schema with `unified_` tables serving as the core data model.

- **`unified_players`**: Central registry of all players.
- **`unified_teams`**: Team history and metadata.
- **`unified_games`**: Game results and metadata.
- **`unified_player_boxscores`**: Detailed player stats per game.
- **`unified_seasons`**: Season metadata (start/end dates).
- **`unified_leagues`**: League definitions (NBA, BAA, ABA).
- **`unified_drafts`**: Draft history.
- **`unified_coaches`**: Coach registry.
- **`unified_referees`**: Referee registry.
