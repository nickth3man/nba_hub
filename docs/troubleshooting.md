# Troubleshooting

Common issues and fixes for the Rust + Convex pipeline.

## Convex Issues

### `401 Unauthorized` on mutations
**Cause**: Missing or invalid `CONVEX_ADMIN_KEY`.
**Fix**: Set `CONVEX_ADMIN_KEY` in `.env.local` and restart the ETL.

### `ECONNREFUSED` to Convex
**Cause**: Convex dev server not running.
**Fix**: Run `npx convex dev` and retry.

## ETL Issues

### CSV file not found
**Cause**: `--csv-dir` points to the wrong path.
**Fix**: Ensure `data/raw` exists and pass the correct directory.

### Validation fails with missing tables
**Cause**: DuckDB not populated.
**Fix**: Run `seed` and `backfill` first, or point to the correct DuckDB file.

## Scraper Issues

### 429/5xx errors
**Cause**: Rate limits.
**Fix**: Increase `--delay-ms` or lower `--concurrency`.
