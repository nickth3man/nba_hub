# Architecture

NBA Hub uses Rust for ETL and validation, Convex for serving application data, and DuckDB for local analytics and audits.

## Directory Structure

- **`crates/`**: Rust workspace.
  - **`nba_core`**: Shared schema types and configuration.
  - **`nba_scraper`**: HTTP scraping + parsing utilities.
  - **`nba_etl`**: ETL CLI (backfill, seed, validation).
  - **`nba_frontend`**: Leptos frontend (SSR/CSR).
- **`convex/`**: Convex schema + functions.
- **`data/`**: Local datasets and DuckDB.
  - `raw/`: Source CSV/JSON used for ingestion.
  - `nba.duckdb`: Validation/analytics DB.
- **`docs/`**: Project documentation.
- **`src/`**: Legacy Python pipeline (reference only).

## Data Flow

1. **Scrape/Extract**:
   - Rust scrapers fetch Basketball-Reference pages and parse tables.
   - Raw HTML is discarded after parsing; JSON records are retained.

2. **Seed/Load**:
   - CSV archives in `data/raw` are parsed into canonical Rust structs.
   - Canonical records are pushed to Convex via mutations.

3. **Validation**:
   - DuckDB ingests subsets of Convex or CSV data for integrity checks.
   - Validation reports discrepancies (totals vs sums, derived stats).

4. **Serve**:
   - Leptos renders public pages using Convex queries.
   - Convex serves read-only API responses for page rendering.

## Core Schema

The core schema mirrors `convex/schema.ts` and Rust types in `crates/nba_core/src/schema.rs`:

- `leagues`, `seasons`, `teams`, `team_history`
- `players`, `games`
- `player_boxscores`, `team_boxscores`
- `player_season_totals`, `player_season_advanced`
- `team_season_totals`, `team_season_advanced`
- `standings`, `awards`, `drafts`, `transactions`, `coaches`, `referees`
