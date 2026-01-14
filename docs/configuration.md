# Configuration

Currently, the NBA Data Hub is configured primarily through Python files.

## File Paths

File paths and directory structures are defined in `src/core/config.py`.

- **`BASE_DIR`**: The root directory of the project.
- **`DATA_DIR`**: `data/` - Root for all data files.
- **`RAW_DATA_DIR`**: `data/raw/` - Location for CSV and JSON files.
- **`DB_PATH`**: `data/nba.duckdb` - The DuckDB database file.
- **`SCRAPER_DATA_DIR`**: `data/raw/html` - Directory for scraped HTML files.
- **`GAMES_CSV`**: `data/raw/Games.csv` - Path to the raw games CSV.
- **`TEAM_HISTORIES_CSV`**: `data/raw/TeamHistories.csv` - Path to team history data.
- **`PLAYERS_CSV`**: `data/raw/Players.csv` - Path to raw player data.
- **`PLAYER_STATISTICS_CSV`**: `data/raw/PlayerStatistics.csv` - Path to player stats.

If you need to change where data is stored, modify `src/core/config.py`.

## Database

The database connection is managed in `src/core/database.py`. It uses the `DB_PATH` from the config file.

## Environment Variables

The project includes `python-dotenv` in `requirements.txt`, but currently, no environment variables are strictly required for the core pipeline. Future updates may add support for API keys (e.g., for NBA API) via `.env` files.

## Dependencies

Python dependencies are managed in `requirements.txt`.
Playwright browsers are managed via the `playwright` CLI.
