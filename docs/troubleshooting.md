# Troubleshooting

Common issues and solutions for the NBA Data Hub.

## Installation Issues

### `ModuleNotFoundError`
**Issue**: Python cannot find a module (e.g., `ModuleNotFoundError: No module named 'duckdb'`).
**Solution**: Ensure you have installed the dependencies in your active virtual environment.
```bash
pip install -r requirements.txt
```

### Playwright Errors
**Issue**: `playwright._impl._api_types.Error: Executable doesn't exist at ...`
**Solution**: You need to install the browser binaries for Playwright.
```bash
playwright install
```

## Runtime Issues

### Database Locked
**Issue**: `duckdb.IOException: IO Error: Cannot open file ".../nba.duckdb": The process cannot access the file because it is being used by another process.`
**Solution**: DuckDB allows only one writer at a time. Ensure no other scripts or DBeaver/DataGrip connections are holding a write lock on the database file. Close other connections and try again.

### Scraping Failures
**Issue**: Scrapers fail with timeouts or 403 errors.
**Solution**:
- Check your internet connection.
- Some sites may rate-limit scraping. The scrapers use Playwright to mimic a real browser, but aggressive scraping can still trigger blocks.
- Try running the specific scraper script individually to debug.

### Missing Data
**Issue**: Tables are empty after running `run_all.py`.
**Solution**:
- Check the logs for `[FAIL]` messages.
- Ensure `run_init.py` was run first.
- Verify that `data/raw` contains the expected CSV files.
