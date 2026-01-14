# Getting Started

This guide will help you set up the NBA Data Hub on your local machine.

## Prerequisites

- **Python 3.13+**: Ensure you have Python installed. You can check with `python --version`.
- **Git**: To clone the repository.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/nba_hub.git
   cd nba_hub
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   The project uses Playwright for web scraping. You need to install the necessary browser binaries.
   ```bash
   playwright install
   ```

## Initialization

Before running the full pipeline, you need to initialize the database and load some static data (referees, coaches, etc.).

```bash
python src/cli/run_init.py
```

## Running the Pipeline

To run the full data pipeline, which includes scraping, loading, transforming, and ingesting data into DuckDB:

```bash
python src/cli/run_all.py
```

This script performs the following steps:
1.  **Initialization**: Sets up referees, coaches, and awards tables.
2.  **Backfill Scraping**: Scrapes historical data (coaches, awards, drafts) if missing.
3.  **Load Raw Data**: Loads raw CSVs into the system.
4.  **Transform**: Migrates data to the unified schema.
5.  **Ingestion**: Ingests players, stats, awards, and transactions into the database.

## Running Tests

To ensure everything is working correctly, you can run the tests:

```bash
pytest
```
