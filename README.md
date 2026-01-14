# NBA Data Hub

A comprehensive NBA/BAA/ABA historical data lakehouse (1946-2026), built with Python and DuckDB.

## Overview

This project provides a robust pipeline to scrape, ingest, transform, and analyze historical NBA data. It leverages **DuckDB** for high-performance analytics and **Playwright** for reliable web scraping.

## Documentation

- **[Getting Started](docs/getting_started.md)**: Installation, setup, and running your first pipeline.
- **[Architecture](docs/architecture.md)**: Understanding the project structure, data flow, and schema.
- **[Configuration](docs/configuration.md)**: Configuring paths and settings.
- **[Troubleshooting](docs/troubleshooting.md)**: Common issues and fixes.

## Quick Start

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

2.  **Initialize the database**:
    ```bash
    python src/cli/run_init.py
    ```

3.  **Run the pipeline**:
    ```bash
    python src/cli/run_all.py
    ```

For more details, see the [Getting Started Guide](docs/getting_started.md).

## Data Sources

- **Kaggle**: Historical game and player data.
- **NBA API**: Official stats and live data.
- **Basketball-Reference**: Scraped historical awards and voting data.
- **Octonion GitHub**: BAA archives.

## License

[MIT](LICENSE)
