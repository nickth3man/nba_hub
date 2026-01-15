# Getting Started

This guide sets up the Rust + Convex pipeline for NBA Hub.

## Prerequisites

- **Rust**: `rustup update stable`
- **Node.js**: required for the Convex CLI
- **DuckDB**: optional (used for local validation)

## Install Dependencies

```bash
npm install
cargo build --workspace
```

## Configure Environment

Create `.env.local` with:

```bash
CONVEX_URL=http://localhost:3210
CONVEX_ADMIN_KEY=your-admin-key
```

## Start Convex

```bash
npx convex dev
```

## Seed Core Data

```bash
cargo run -p nba_etl -- seed --csv-dir data/raw
```

## Run a Backfill (Single Date)

```bash
cargo run -p nba_etl -- backfill --date 20240115
```

## Run Validation

```bash
cargo run -p nba_etl -- validate --db-path data/nba.duckdb
```

## Run the Frontend

```bash
cargo run -p nba_frontend
```
