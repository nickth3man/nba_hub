# Configuration

NBA Hub uses environment variables for Convex access and local paths for CSV/DuckDB.

## Environment Variables

Create a `.env` or `.env.local` at the repo root:

- **`CONVEX_URL`**: Base URL for Convex (default `http://localhost:3210`).
- **`CONVEX_ADMIN_KEY`**: Admin key for mutations (required for writes).
- **`DUCKDB_PATH`**: Override DuckDB path (default `data/nba.duckdb`).

## Data Paths

Rust configuration lives in `crates/nba_core/src/config.rs`:

- `data/` for local artifacts.
- `data/raw/` for CSV/JSON sources used during seed/backfill.
- `data/nba.duckdb` for validation queries.

## Convex Configuration

Convex schema and functions live in `convex/`. Use `npx convex dev` for local dev and `npx convex deploy` for production.

## Legacy Python

Python configuration under `src/core/config.py` is legacy and not used by the Rust pipeline.
