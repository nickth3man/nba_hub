# NBA Hub Implementation Spec (Implementation)

Document Type: Implementation
Last Updated: 2026-01-15

## 1. Scope and Constraints

- Build Basketball-Reference parity pages: Home, Players Directory, Player Profile, Teams Directory, Team Profile, Seasons Index, Season Summary, Leaders, Awards, Draft, Transactions, Glossary.
- Default to the most recent season when a season is not specified.
- Beginner mode is on by default; advanced stats are opt-in per table.
- Data scope: NBA/BAA/ABA (1946-present). No WNBA or international leagues.
- Exclusions: Stathead query builder, user accounts, ads, live game updates, and paywalls.
- Performance targets: LCP < 2.0s on mid-tier laptops; table render under 500ms for 200-row tables.
- Accessibility targets: keyboard nav, skip links, aria labels, sticky table headers, and glossary tooltips for all stat abbreviations.

## 2. Data Model and Schema Alignment

| Entity | Convex Table | Primary Key | UI Usage |
| --- | --- | --- | --- |
| Leagues | `leagues` | `league_id` | League labels on season pages |
| Seasons | `seasons` | `season_id` | Season index + default year |
| Team History | `team_history` | `team_history_id` | Team identity + active flag |
| Player Season Totals | `player_season_totals` | `player_bref_id + season_year + team_abbrev` | Player profiles + leaders |
| Player Season Advanced | `player_season_advanced` | `player_bref_id + season_year + team_abbrev` | Advanced player tables |
| Team Season Totals | `team_season_totals` | `team_abbrev + season_year` | Team profile + season stats |
| Team Season Advanced | `team_season_advanced` | `team_abbrev + season_year` | Season summary + ratings |
| Standings | `standings` | `team_abbrev + season_year` | Season summary standings |
| Drafts | `drafts` | `season_year + pick_overall` | Draft page |
| Awards | `awards` | `award_key` | Awards page |
| Transactions | `transactions` | `transaction_id` | Transactions page |

Data adjustments:
- Add `player_name` (optional) to `player_season_totals` for display names from BRef CSVs.
- Add season indexes for list-by-season queries:
  - `player_season_totals` index `by_season_year` on `season_year`.
  - `player_season_advanced` index `by_season_year` on `season_year`.
  - `team_season_totals` index `by_season_year` on `season_year`.
  - `team_season_advanced` index `by_season_year` on `season_year`.
  - `standings` index `by_season_year` on `season_year`.
  - `awards` index `by_season_year` on `season_year`.
  - `transactions` index `by_season_year` on `season_year`.

### 2-1 Schema Parity Rule

- Update `convex/schema.ts` and `crates/nba_core/src/schema.rs` in the same change set.
- When adding fields, also update `convex/ingest.ts` and `crates/nba_etl/src/seed.rs`.
- Keep Convex functions CRUD-only; derived metrics are calculated in Rust or the frontend.

## 3. Convex API Surface

### 3-1 Modules

- `players.ts`, `teams.ts`, `seasons.ts`, `leaders.ts`, `awards.ts`, `drafts.ts`, `transactions.ts`.

### 3-2 Queries for Frontend

| Query | Args | Returns | Used By |
| --- | --- | --- | --- |
| `players:listPlayerDirectory` | `paginationOpts?` | `[{ player_bref_id, player_name, first_season, last_season, seasons_count, teams_count }]` | Players directory |
| `players:getPlayerProfile` | `{ playerBrefId }` | `{ player, totals, advanced }` | Player profile |
| `teams:listTeams` | `{ activeOnly?, paginationOpts? }` | `team_history[]` | Teams directory |
| `teams:getTeamProfile` | `{ teamAbbrev }` | `{ team, totals, advanced, standings }` | Team profile |
| `seasons:listSeasons` | `{ leagueId? }` | `[{ season_year, league_id }]` | Seasons index + default |
| `seasons:getSeasonSummary` | `{ seasonYear }` | `{ standings, teamTotals, teamAdvanced }` | Season summary |
| `leaders:getSeasonLeaders` | `{ seasonYear }` | `{ points, rebounds, assists, steals, blocks }` | Leaders + season summary |
| `awards:listAwardsBySeason` | `{ seasonYear }` | `award[]` | Awards page |
| `drafts:listDraftBySeason` | `{ seasonYear }` | `draft[]` | Draft page |
| `transactions:listTransactionsBySeason` | `{ seasonYear }` | `transaction[]` | Transactions page |

## 4. Rust ETL CLI (crates/nba_etl)

The Rust CLI seeds CSV archives, backfills missing boxscore metadata, and performs validation.

### 4-1 Commands

| Command | Example | Purpose |
| --- | --- | --- |
| `seed` | `cargo run -p nba_etl -- seed --csv-dir data/raw` | Load CSV archives into Convex |
| `backfill` | `cargo run -p nba_etl -- backfill --date 20240115` | Scrape boxscore metadata for a date |
| `validate` | `cargo run -p nba_etl -- validate --db-path data/nba.duckdb` | Validate totals via DuckDB |

### 4-2 Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `CONVEX_URL` | Convex base URL | `http://localhost:3210` |
| `CONVEX_ADMIN_KEY` | Convex admin key for mutations | None |
| `DUCKDB_PATH` | Override DuckDB path | `data/nba.duckdb` |

## 5. Scraper Parity (crates/nba_scraper)

- Scrape only gaps: awards voting, personnel lists, and boxscore metadata.
- CSV archives remain the source-of-truth for season stats and standings.

### 5-2 Robots and Rate Limits

- Respect robots.txt allow/deny rules for Basketball-Reference.
- Default delay: 3s between requests, concurrency 1 per host.
- Log and skip disallowed pages; no bypass logic.

## 6. Validation (DuckDB)

- Validate season totals, team summaries, and standings parity against CSVs.
- Store validation DB at `data/nba.duckdb` with repeatable audit queries.

## 7. Frontend MVP (Leptos)

### Route Map

| Route | Page | Queries | Notes |
| --- | --- | --- | --- |
| `/` | Home | `seasons:listSeasons`, `leaders:getSeasonLeaders` | Quick nav + beginner callouts |
| `/players` | Players Directory | `players:listPlayerDirectory` | Search + filters |
| `/players/:player_bref_id` | Player Profile | `players:getPlayerProfile` | Totals + advanced tables |
| `/teams` | Teams Directory | `teams:listTeams` | Active teams list |
| `/teams/:team_abbrev` | Team Profile | `teams:getTeamProfile` | Season summaries |
| `/seasons` | Seasons Index | `seasons:listSeasons` | Year list |
| `/seasons/:year` | Season Summary | `seasons:getSeasonSummary`, `leaders:getSeasonLeaders` | Standings + leaders |
| `/leaders/:year?` | Leaders | `leaders:getSeasonLeaders` | Season leaders |
| `/awards/:year?` | Awards | `awards:listAwardsBySeason` | Award lists |
| `/draft/:year?` | Draft | `drafts:listDraftBySeason` | Draft history |
| `/transactions/:year?` | Transactions | `transactions:listTransactionsBySeason` | Transactions log |
| `/glossary` | Glossary | Static map | Stat definitions |

Layout requirements:
- Global nav with categories (Home, Players, Teams, Seasons, Leaders, Awards, Draft, Transactions, Glossary).
- Page header with title, summary blurb, and “What am I looking at?” callout.
- “On this page” anchor list for sections on detail pages.
- Table sections grouped by Overview, Performance, Advanced, Records.

## 8. UX Patterns and Beginner Mode

Beginner mode:
- Default ON for all stat tables.
- Toggle persists per page session.
- Beginner columns for player seasons: Season, Team, G, PTS, REB, AST, FG%, 3P%, FT%.
- Advanced columns add: PER, TS%, USG%, WS, BPM, VORP.

Glossary:
- Static map of stat abbreviations to long-form labels + definitions.
- Every stat header uses a tooltip with the glossary definition.

Accessibility:
- Skip links to main content and tables.
- Table headers use `<th scope="col">` and sticky header rows.
- Hover/Focus row highlighting for scanability.

## 9. Anti-Patterns (DO NOT)

| ❌ Don’t | ✅ Do Instead | Why |
| --- | --- | --- |
| Mix NBA API IDs with BRef IDs in routing | Route by `player_bref_id` only | Prevents broken links |
| Hide advanced stats without explanation | Use “Beginner mode” toggle with helper text | Reduces confusion |
| Compute derived stats in Convex | Compute in frontend or Rust | Convex stays CRUD-only |
| Render tables without headers/aria | Use scoped headers + tooltips | Accessibility compliance |
| Hardcode season year in routes | Default to latest season from `seasons` | Future-proof navigation |

## 10. Test Case Specifications

### Unit Tests Required

| Test ID | Component | Input | Expected Output | Edge Cases |
| --- | --- | --- | --- | --- |
| TC-001 | Leaders reducer | Season totals list | Top 10 sorted by points | Ties, missing points |
| TC-002 | Player directory aggregator | Totals list | First/last season + counts | Multi-team seasons |
| TC-003 | Beginner toggle | Toggle on/off | Columns hidden/shown | No advanced stats |
| TC-004 | Stat formatter | Optional numbers | `-` for missing values | Null/NaN |
| TC-005 | Season default | Seasons list | Latest season picked | Empty list |

### Integration Tests Required

| Test ID | Flow | Setup | Verification | Teardown |
| --- | --- | --- | --- | --- |
| IT-001 | Home → Player profile | Load app | Player table links resolve | None |
| IT-002 | Season summary load | Load season page | Standings + leaders render | None |
| IT-003 | Glossary tooltips | Hover stat header | Tooltip text appears | None |

## 11. Error Handling Matrix

### External Service Errors

| Error Type | Detection | Response | Fallback | Logging | Alert |
| --- | --- | --- | --- | --- | --- |
| Convex unavailable | Network error | Show error banner | Retry button | ERROR | If >3 in 5 min |
| Convex empty page | Empty payload | Show empty state | Suggested links | WARN | None |
| Scraper 429 | HTTP 429 | Backoff + retry | Skip batch | WARN | If 5/min |

### User-Facing Errors

| Error Type | User Message | Code | Recovery Action |
| --- | --- | --- | --- |
| Season not found | “Season not found.” | 404 | Link to seasons index |
| Player not found | “Player data unavailable.” | 404 | Back to players |
| Team not found | “Team data unavailable.” | 404 | Back to teams |

## 12. References

| Topic | Location | Anchor |
| --- | --- | --- |
| Strategic blueprint | [PRD](PRD.md#0-strategic-blueprint-7-questions) | Section 0 |
| Architecture overview | [Architecture](../docs/architecture.md#data-flow) | Data Flow |
| Convex schema | [convex/schema.ts](../convex/schema.ts) | `defineSchema` |
| Frontend routes | [nba_frontend/src/lib.rs](../crates/nba_frontend/src/lib.rs) | `Routes` |
| Players page | [nba_frontend/src/pages/players.rs](../crates/nba_frontend/src/pages/players.rs) | `Players` |
| Teams page | [nba_frontend/src/pages/teams.rs](../crates/nba_frontend/src/pages/teams.rs) | `Teams` |
