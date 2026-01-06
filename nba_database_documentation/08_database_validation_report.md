# NBA Database Validation Report

**Generated**: 2026-01-05 17:24:33
**Database**: nba.duckdb

## Summary

- Total validation checks: 6
- Passed: 2
- Failed: 3
- Warnings: 1
- Success rate: 33.3%

## Detailed Results

| Check | Status | Severity | Details |
|-------|--------|----------|----------|
| Season Coverage | [ERROR] FAIL | CRITICAL | Missing 80 seasons: 1946-47, 1947-48, 1948-49, 1949-50, 1950-51... |
| Season Coverage | [ERROR] FAIL | CRITICAL | Error: boolean value of NA is ambiguous |
| Player Coverage | [OK] PASS | INFO | 4171 players found |
| Statistical Integrity | [ERROR] FAIL | HIGH | Error: Binder Error: Referenced column "field_goals_made" not found in FROM clause!
Candidate bindings: "fga", "fg3a", "game_date", "game_id", "fgm"

LINE 4:                 WHERE field_goals_made > field_goals_attempted
                              ^ |
| Referential Integrity - Teams | [WARNING] WARNING | MEDIUM | 2520 orphaned team_id references (98.21% integrity) |
| Referential Integrity - Games | [OK] PASS | INFO | 100% integrity |

## Critical Issues

- **Season Coverage**: Missing 80 seasons: 1946-47, 1947-48, 1948-49, 1949-50, 1950-51...
- **Season Coverage**: Error: boolean value of NA is ambiguous

## Recommendations

1. Address all CRITICAL and HIGH severity issues immediately
2. Review MEDIUM severity issues for data quality improvements
3. Acquire missing seasons (2023-24, 2024-25, 2025-26)
4. Re-run validation after fixes
