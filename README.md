# NBA Hub

Rust-first NBA/BAA/ABA data pipeline and public stat site using Convex for APIs and DuckDB for validation/analytics.

## Overview

NBA Hub ingests historical data, normalizes it into a unified schema, and serves stateless public pages via a Leptos frontend. The Rust ETL pushes canonical JSON to Convex, while DuckDB is used locally for heavy validation and audits.

## Documentation

- **[Getting Started](docs/getting_started.md)**: Setup for Rust + Convex + DuckDB.
- **[Architecture](docs/architecture.md)**: Component boundaries and data flow.
- **[Configuration](docs/configuration.md)**: Environment variables and paths.
- **[Troubleshooting](docs/troubleshooting.md)**: Common build/runtime issues.

## Quick Start

1. **Install toolchains**:
   ```bash
   rustup update stable
   npm install
   ```

2. **Start Convex locally**:
   ```bash
   npx convex dev
   ```

3. **Build and run ETL**:
   ```bash
   cargo run -p nba_etl -- --help
   ```

4. **Run the frontend (CSR dev)**:
   ```bash
   cargo run -p nba_frontend
   ```

For more detail, see the [Getting Started Guide](docs/getting_started.md).

## Data Sources

- **Basketball-Reference**: Game metadata (boxscores, officials, coaches).
- **Kaggle/CSV archives**: Historical player/team/game tables (local `data/raw`).

## Legacy Note

The Python pipeline under `src/` is legacy and retained for reference only. New development targets the Rust + Convex stack.

## License

[MIT](LICENSE)
