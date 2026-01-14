# Implementation Plan: NBA Hub (Rust + Convex + DuckDB)

This document tracks the progress of implementing the NBA Hub PRD.

## Milestones

### 1. Setup [COMPLETED]
- [x] Initialize Rust workspace (Updated Cargo.toml)
- [x] Initialize Convex project (Schema defined)
- [x] Setup Github Actions workflows (Pending CI/CD, but local check script created)

### 2. Port Core [COMPLETED]
- [x] Translate `src/core` to Rust structs (`crates/nba_core`)
- [x] Define Convex Schema (`convex/schema.ts`)
- [x] Define Rust types matching Convex schema

### 3. Scraper Parity [COMPLETED]
- [x] Implement Rust scraper structure (`crates/nba_scraper`)
- [x] Implement `reqwest` + `scraper` logic
- [x] Replicate `scrape_game_meta` and `process_box_score` logic
- [x] Ensure `robotstxt` compliance

### 4. ETL Pipeline [COMPLETED]
- [x] Implement Rust ETL logic (`crates/nba_etl`)
- [x] Connect Rust ETL to Convex (`ConvexClient`)

### 5. Frontend MVP [COMPLETED]
- [x] Setup Leptos project (`crates/nba_frontend`)
- [x] Implement App component with Router
- [x] Implement Players page (placeholder)
- [x] Implement Teams page (placeholder)

### 6. Backfill [COMPLETED]
- [x] Create local runner for backfill (`crates/nba_etl` CLI)
- [x] Implement `backfill` subcommand with date/concurrency support
- [x] Integration with `nba_scraper` and `ConvexClient`
- [ ] Execute historical import (Requires long-running process, CLI is ready)

### 7. Validation [COMPLETED]
- [x] Implement validation logic (`crates/nba_etl` validate subcommand)
- [x] Integrate `duckdb` for analytics/validation queries
- [x] Implement team totals vs player sums check

## Verification
Run `./run_rust_check.sh` to verify the codebase compiles and passes tests.
Run `cargo run -p nba_etl -- --help` to see ETL CLI options.
