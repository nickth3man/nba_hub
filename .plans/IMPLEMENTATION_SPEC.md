# Implementation Spec: NBA Hub (Implementation)

Version: 1.1
Status: Draft
Date: 2026-01-14
Owner: Project Lead
Document Type: Implementation

## 1) Scope and Constraints
- Implement the PRD milestones using the Rust + Convex + DuckDB stack. See [PRD](PRD.md#1-overview).
- Rust-first: TypeScript is limited to Convex schema and thin query/mutation wrappers only.
- Data sources are local CSV archives in `data/raw` plus Basketball-Reference scraping for coaches, referees, awards voting, and game metadata.
- Convex schema is the source of truth for storage; Rust structs must match it exactly.
- Store all dates as `YYYY-MM-DD` strings; no time-of-day persisted.
- Convex document size limit is 1 MiB; batch payloads and row shapes must respect this limit.
- Robots.txt compliance is mandatory for all scraping; enforce crawl-delay and allow/deny rules.

## 2) Data Model and Schema Alignment

### 2.1 Schema Parity Rule
`convex/schema.ts` and `crates/nba_core/src/schema.rs` must define the same tables and fields. Types must match exactly (string, number, boolean, optional).

### 2.2 Table Inventory, Keys, and Indexes

#### Core Reference
| Table | Primary key (unique index) | Required fields (type) | Optional fields (type) | Secondary indexes |
|------|----------------------------|-------------------------|------------------------|-------------------|
| `leagues` | `by_league_id` (`league_id`) | `league_id` (number), `league_code` (string), `league_name` (string) | none | none |
| `seasons` | `by_season_id` (`season_id`) | `season_id` (number), `league_id` (number), `season_year` (number) | `start_date` (string), `end_date` (string) | `by_league_year` (`league_id`, `season_year`) |
| `arenas` | `by_arena_id` (`arena_id`) | `arena_id` (number), `arena_name` (string) | `city` (string) | none |
| `teams` | `by_team_id` (`team_id`) | `team_id` (number), `league_id` (number) | `franchise_code` (string), `nba_api_team_id` (number) | none |
| `team_history` | `by_team_history_id` (`team_history_id`) | `team_history_id` (number), `team_id` (number), `effective_start` (string), `city` (string), `nickname` (string), `is_active` (boolean) | `effective_end` (string), `abbreviation` (string) | `by_team_id` (`team_id`), `by_active` (`is_active`, `team_id`) |
| `players` | `by_player_id` (`player_id`) | `player_id` (number) | `nba_api_person_id` (number), `first_name` (string), `last_name` (string), `display_name` (string), `birth_date` (string), `from_year` (number), `to_year` (number) | `by_last_name` (`last_name`, `first_name`) |
| `coaches` | `by_coach_id` (`coach_id`) | `coach_id` (string), `display_name` (string) | `nba_api_coach_id` (number) | none |
| `referees` | `by_referee_id` (`referee_id`) | `referee_id` (string), `display_name` (string) | `nba_api_ref_id` (number) | none |

#### Games and Boxscores
| Table | Primary key (unique index) | Required fields (type) | Optional fields (type) | Secondary indexes |
|------|----------------------------|-------------------------|------------------------|-------------------|
| `games` | `by_game_id` (`game_id`) | `game_id` (string), `league_id` (number), `season_id` (number), `season_type` (string), `game_date` (string), `home_team_id` (number), `away_team_id` (number) | `home_points` (number), `away_points` (number), `attendance` (number), `arena_id` (number) | `by_season_id` (`season_id`), `by_home_team` (`home_team_id`), `by_away_team` (`away_team_id`) |
| `player_boxscores` | `by_game_player` (`game_id`, `player_id`) | `game_id` (string), `player_id` (number), `team_id` (number) | `minutes` (number), `points` (number), `assists` (number), `rebounds_total` (number), `steals` (number), `blocks` (number), `fgm` (number), `fga` (number), `fg3m` (number), `fg3a` (number), `ftm` (number), `fta` (number), `pf` (number), `turnovers` (number), `plus_minus` (number) | `by_game_id` (`game_id`), `by_player_id` (`player_id`) |
| `team_boxscores` | `by_game_team` (`game_id`, `team_id`) | `game_id` (string), `team_id` (number) | `minutes` (number), `points` (number), `assists` (number), `rebounds_total` (number), `fgm` (number), `fga` (number), `fg3m` (number), `fg3a` (number), `ftm` (number), `fta` (number), `turnovers` (number), `pf` (number) | `by_game_id` (`game_id`), `by_team_id` (`team_id`) |

#### Season Aggregates
| Table | Primary key (unique index) | Required fields (type) | Optional fields (type) | Secondary indexes |
|------|----------------------------|-------------------------|------------------------|-------------------|
| `player_season_totals` | `by_player_season_team` (`player_bref_id`, `season_year`, `team_abbrev`) | `season_year` (number), `player_bref_id` (string), `team_abbrev` (string), `games` (number) | `games_started` (number), `minutes` (number), `points` (number), `assists` (number), `rebounds_total` (number), `steals` (number), `blocks` (number), `fgm` (number), `fga` (number), `fg3m` (number), `fg3a` (number), `ftm` (number), `fta` (number), `turnovers` (number), `pf` (number) | `by_player_season` (`player_bref_id`, `season_year`), `by_season_team` (`season_year`, `team_abbrev`) |
| `player_season_advanced` | `by_player_season_team` (`player_bref_id`, `season_year`, `team_abbrev`) | `season_year` (number), `player_bref_id` (string), `team_abbrev` (string) | `minutes` (number), `per` (number), `ts_percent` (number), `usg_percent` (number), `ows` (number), `dws` (number), `ws` (number), `bpm` (number), `vorp` (number) | `by_player_season` (`player_bref_id`, `season_year`), `by_season_team` (`season_year`, `team_abbrev`) |
| `team_season_totals` | `by_team_season` (`team_abbrev`, `season_year`) | `season_year` (number), `team_abbrev` (string), `games` (number) | `minutes` (number), `points` (number), `assists` (number), `rebounds_total` (number), `fgm` (number), `fga` (number), `fg3m` (number), `fg3a` (number), `ftm` (number), `fta` (number), `turnovers` (number), `pf` (number) | none |
| `team_season_advanced` | `by_team_season` (`team_abbrev`, `season_year`) | `season_year` (number), `team_abbrev` (string), `wins` (number), `losses` (number) | `srs` (number), `pace` (number), `off_rtg` (number), `def_rtg` (number), `net_rtg` (number) | none |
| `standings` | `by_team_season` (`team_abbrev`, `season_year`) | `season_year` (number), `team_abbrev` (string), `wins` (number), `losses` (number), `playoffs` (boolean) | none | none |

#### Other
| Table | Primary key (unique index) | Required fields (type) | Optional fields (type) | Secondary indexes |
|------|----------------------------|-------------------------|------------------------|-------------------|
| `drafts` | `by_season_pick` (`season_year`, `pick_overall`) | `season_year` (number), `pick_overall` (number) | `round_number` (number), `pick_in_round` (number), `team_abbrev` (string), `player_bref_id` (string), `player_name` (string), `college` (string) | `by_team_abbrev` (`team_abbrev`), `by_player_bref_id` (`player_bref_id`) |
| `awards` | `by_award_key` (`award_key`) | `award_key` (string), `award_type` (string), `season_year` (number) | `player_bref_id` (string), `player_name` (string), `team_abbrev` (string), `rank` (number), `points_won` (number), `points_max` (number), `share` (number) | `by_award_season` (`award_type`, `season_year`), `by_player_bref_id` (`player_bref_id`) |
| `transactions` | `by_transaction_id` (`transaction_id`) | `transaction_id` (string), `season_year` (number), `details` (string) | `team_abbrev` (string), `player_bref_id` (string) | `by_player_bref_id` (`player_bref_id`) |

### 2.3 Type Conventions and Derived Fields
- Numeric fields are integers unless noted; floats include `minutes`, `per`, `ts_percent`, `usg_percent`, `ows`, `dws`, `ws`, `bpm`, `vorp`, `srs`, `pace`, `off_rtg`, `def_rtg`, `net_rtg`, `share`.
- Date fields are stored as `YYYY-MM-DD` strings.
- `season_year` from a game date: if month >= 7 then year + 1 else year.
- `season_id` = `league_id * 10000 + season_year`.
- `league_id` mapping: `NBA` -> 1, `BAA` -> 2, `ABA` -> 3; unknown -> 1.
- `team_history_id` is sequential in file order starting at 1.
- `effective_start` = `{seasonFounded}-01-01`; `effective_end` = `{seasonActiveTill}-12-31`.
- `is_active` = `season_active_till >= current_year()`; if missing, treat as active.
- `display_name` = trimmed `first_name + " " + last_name`; if blank, set `display_name` to null.
- `award_key` = `{award_type}|{season_year}|{player_bref_id_or_name}`, where `player_bref_id_or_name` uses `player_bref_id` when present, else normalized `player_name` (trimmed, single spaces). If both are missing, skip the row and log.
- `award_type` values:
  - CSV seed: `ALL_STAR`, `{TYPE}_{TEAM_NUMBER}` from `End of Season Teams.csv` (example: `ALL_NBA_1`).
  - CSV voting: `{TYPE}` uppercased from `End of Season Teams (Voting).csv` (example: `ALL_NBA`).
  - Scraper: `MVP`, `ROY`, `DPOY`, `SMOY`, `MIP`.
- `team_map` key = `{teamCity}|{teamName}` with trimmed fields.

### 2.4 Data Coverage Notes
- `arenas` is not populated by current CSVs; only `arena_id` is stored on `games`.
- `transactions` require a separate source file; skip ingestion when a source is not provided.

## 3) Convex Functions

### 3.1 Ingest Mutations (`convex/ingest.ts`)
Implement the following mutations using validators and `mutation()`:

| Mutation | Payload key | Unique index | Notes |
|---------|-------------|--------------|------|
| `upsertLeagues` | `leagues` | `by_league_id` | Insert only if missing. |
| `upsertSeasons` | `seasons` | `by_season_id` | Insert only if missing. |
| `upsertArenas` | `arenas` | `by_arena_id` | Insert only if missing. |
| `upsertTeams` | `teams` | `by_team_id` | Insert only if missing. |
| `upsertTeamHistory` | `history` | `by_team_history_id` | Insert only if missing. |
| `upsertPlayers` | `players` | `by_player_id` | Insert only if missing. |
| `upsertCoaches` | `coaches` | `by_coach_id` | Insert only if missing. |
| `upsertReferees` | `referees` | `by_referee_id` | Insert only if missing. |
| `upsertGames` | `games` | `by_game_id` | Insert only if missing. |
| `upsertPlayerBoxscores` | `boxscores` | `by_game_player` | Insert only if missing. |
| `upsertTeamBoxscores` | `boxscores` | `by_game_team` | Insert only if missing. |
| `upsertDrafts` | `drafts` | `by_season_pick` | Insert only if missing. |
| `upsertPlayerSeasonTotals` | `totals` | `by_player_season_team` | Use team-aware key to allow multi-team seasons. |
| `upsertPlayerSeasonAdvanced` | `advanced` | `by_player_season_team` | Use team-aware key to allow multi-team seasons. |
| `upsertTeamSeasonTotals` | `totals` | `by_team_season` | Insert only if missing. |
| `upsertTeamSeasonAdvanced` | `advanced` | `by_team_season` | Insert only if missing. |
| `upsertStandings` | `standings` | `by_team_season` | Insert only if missing. |
| `upsertAwards` | `awards` | `by_award_key` | Compute `award_key` before upsert. |
| `upsertTransactions` | `transactions` | `by_transaction_id` | Insert only if missing. |

Upsert rule: use the corresponding unique index and `first()` to detect existing rows. Insert only when missing. Each mutation must accept batches and keep the payload under the 1 MiB Convex document limit. On 413 or limit errors, reduce batch size and retry.

### 3.2 Queries for Frontend
Create query modules:

- `convex/players.ts`:
  - `listPlayers({ paginationOpts })`
  - `paginationOpts` shape: `{ numItems: number, cursor?: string | null }`
  - Order by `by_last_name` index (`last_name`, `first_name`), ascending.
  - Use `paginate(paginationOpts)` and return `page`, `isDone`, `continueCursor`.
  - Default `paginationOpts.numItems` to 200 when not provided.

- `convex/teams.ts`:
  - `listTeams({ activeOnly?: boolean, paginationOpts })`
  - `paginationOpts` shape: `{ numItems: number, cursor?: string | null }`
  - If `activeOnly` is true or omitted, query `team_history` via `by_active` where `is_active = true`.
  - If `activeOnly` is false, paginate by `by_team_history_id` for stable ordering.

## 4) Rust ETL CLI (`crates/nba_etl`)

### 4.1 Commands
| Command | Purpose | Required args | Optional args |
|---------|---------|---------------|---------------|
| `seed` | Load CSV archives and upsert into Convex. | `--csv-dir` | `--batch-size` |
| `backfill` | Scrape Basketball-Reference metadata and insert into Convex. | `--date` OR (`--start-date` + `--end-date`) | `--concurrency`, `--delay-ms`, `--awards-start`, `--awards-end`, `--skip-awards`, `--skip-personnel` |
| `validate` | Run DuckDB validations. | `--csv-dir`, `--db-path` | none |

Date args use `YYYYMMDD`.

### 4.2 Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| `CONVEX_URL` | Convex deployment URL | `http://localhost:3210` |
| `CONVEX_ADMIN_KEY` | Admin auth key for Convex | none |
| `SCRAPER_USER_AGENT` | User-Agent for scraping | `NBA Hub Scraper (nba-hub-bot)` |
| `NBA_HUB_DATA_DIR` | Base data directory | `data` |
| `DUCKDB_PATH` | DuckDB database file | `data/nba.duckdb` |

### 4.3 Seed Pipeline
1) Seed reference data:
   - `leagues`: insert fixed rows (NBA=1, BAA=2, ABA=3).
   - `seasons`: generate per-league seasons.
     - BAA: 1946-1948 (league_id 2)
     - NBA: 1949-current (league_id 1)
     - ABA: 1967-1976 (league_id 3)
     - `season_id` uses `league_id * 10000 + season_year`.
2) Load `TeamHistories.csv`:
   - Build `team_history_id` sequentially starting at 1.
   - Map `league` to `league_id` using the mapping above.
   - Compute `effective_start` and `effective_end` from `seasonFounded` and `seasonActiveTill`.
   - Compute `is_active` from `seasonActiveTill` vs current year.
3) Derive `teams` from `team_history`:
   - Distinct `team_id` rows.
   - `franchise_code` = `teamAbbrev`, `nba_api_team_id` = `team_id`.
4) Load `Players.csv` and merge `all_players.csv`:
   - `display_name` = `firstName + " " + lastName` trimmed.
   - `from_year`/`to_year` from `all_players.csv` when present.
5) Load `Games.csv`:
   - `game_id` = `gameId` as string.
   - `game_date` = date portion of `gameDateTimeEst`.
   - `season_year` from `game_date` using month >= 7 rule.
   - `league_id` derived from `home_team_id` via `team_history.league_id` for the game season; fallback to NBA (1), and use BAA (2) for `season_year < 1949`.
   - `season_id` = `league_id * 10000 + season_year`.
   - `season_type` defaults to `Regular` when blank.
6) Load `PlayerStatistics.csv`:
   - Map `team_id` by `teamCity|teamName` using `team_history`.
   - Skip rows with missing team mapping and log a warning.
7) Load `TeamStatistics.csv`:
   - Map to `team_boxscores` by `gameId` and `teamId`.
8) Load `Draft Pick History.csv`:
   - `pick_in_round` remains null unless a source field is added.
9) Load `Player Totals.csv` and `Advanced.csv` into player season aggregates.
10) Load `Team Totals.csv` and `Team Summaries.csv` into team season aggregates and standings.
11) Load awards from CSVs:
   - `All-Star Selections.csv` -> `award_type = ALL_STAR`.
   - `End of Season Teams.csv` -> `award_type = {TYPE}_{TEAM_NUMBER}`.
   - `End of Season Teams (Voting).csv` -> `award_type = {TYPE}` and populate `rank`, `points_won`, `points_max`, `share`.
12) Coaches and referees are ingested by `backfill` (not `seed`).

### 4.4 CSV Mapping
| CSV | Target table | Field notes |
|-----|--------------|------------|
| `Players.csv` | `players` | `player_id = personId`, `display_name = first + last`, `birth_date = birthdate` |
| `all_players.csv` | `players` | optional file; `person_id` fills `from_year`, `to_year` |
| `TeamHistories.csv` | `team_history` + `teams` | `team_history_id` sequential; `league` maps to `league_id`; `teams` deduped by `teamId` |
| `Games.csv` | `games` | `game_id` string; `game_date` from `gameDateTimeEst` |
| `PlayerStatistics.csv` | `player_boxscores` | `team_id` via `(playerteamCity, playerteamName)` map |
| `TeamStatistics.csv` | `team_boxscores` | `team_id = teamId`; `points = teamScore`; `minutes = numMinutes` |
| `Draft Pick History.csv` | `drafts` | `player_bref_id` from `player_id`, `team_abbrev` from `tm` |
| `Player Totals.csv` | `player_season_totals` | `player_bref_id` from `player_id`, `team_abbrev` from `team` |
| `Advanced.csv` | `player_season_advanced` | `player_bref_id` from `player_id`, `team_abbrev` from `team` |
| `Team Totals.csv` | `team_season_totals` | `team_abbrev` from `abbreviation` |
| `Team Summaries.csv` | `team_season_advanced` + `standings` | `wins/losses` -> standings; ratings -> advanced |
| `All-Star Selections.csv` | `awards` | optional file; `award_type = ALL_STAR`, `player_bref_id` from `player_id` |
| `End of Season Teams.csv` | `awards` | optional file; `award_type = {type}_{number_tm}` |
| `End of Season Teams (Voting).csv` | `awards` | optional file; `award_type = {type}`, with voting fields |

Files are optional when noted; missing files should log and be skipped.

### 4.5 Batch Sizes and Limits
Default batch size is 200 rows per mutation. Batch payloads must remain under the 1 MiB Convex document size limit. If a batch fails with 413 or size errors, halve the batch size and retry.

## 5) Scraper Parity (`crates/nba_scraper`)

### 5.1 Required Scrapers and Rules
- `scrape_games_for_date(date: YYYYMMDD)`:
  - URL: `https://www.basketball-reference.com/boxscores/?month=MM&day=DD&year=YYYY`
  - Parse `div.game_summary a[href*='boxscores']` where link text is `Final`.
  - Return absolute boxscore URLs.

- `scrape_boxscore(url)`:
  - Parse officials block for `/referees/` links, extract `referee_id` and display name.
  - Parse coach links via `a[href*='/coaches/']`, exclude `NBA_stats.html`.
  - Return `BoxscoreMeta { referees, coaches }`.

- `scrape_coaches()`:
  - URL: `https://www.basketball-reference.com/coaches/NBA_stats.html`
  - Parse `table#coaches tbody tr`, skip header rows.
  - Extract `coach_id` from href and display name from link text.

- `scrape_referees()`:
  - URL: `https://www.basketball-reference.com/referees/`
  - Parse `table#referees tbody tr`, skip header rows.
  - Extract `referee_id` from href and display name from link text.

- `scrape_awards_for_year(year)`:
  - URL: `https://www.basketball-reference.com/awards/awards_{year}.html`
  - Parse tables `mvp`, `roy`, `dpoy`, `smoy`, `mip`.
  - Skip `thead` rows and require a non-empty rank.
  - Extract `player_bref_id` from `data-append-csv` or player link href.

### 5.2 Robots and Rate Limits
- Basketball-Reference robots.txt sets `Crawl-delay: 3` for `User-agent: *` and disallows:
  - `/play-index/*.cgi?*`, `/play-index/plus/*.cgi?*`
  - `*/gamelog/`, `*/splits/`, `*/on-off/`, `*/lineups/`, `*/shooting/`
  - `/req/`, `/short/`, `/dump/`, `/nocdn/`
- Fetch `robots.txt` once per host and enforce allow/deny using `robotstxt::DefaultMatcher`.
- Enforce per-host single-flight requests and apply crawl-delay (default 3000ms).
- Default concurrency is 1 per host.

## 6) Validation (DuckDB)

Validation uses DuckDB `read_csv_auto` for CSVs and creates temporary tables if missing.

### 6.1 Required Checks
| Check ID | Input | Calculation | Expected |
|---------|-------|-------------|----------|
| V-001 | `PlayerStatistics.csv` + `TeamStatistics.csv` | Sum player points by `gameId` and `teamId` and compare to `teamScore` | Exact match |
| V-002 | `PlayerStatistics.csv` + `Games.csv` | Per-game stats (`stat_total / games`) vs `Player Per Game.csv` | Epsilon 0.0001 |
| V-003 | `Player Totals.csv` | Per-36 stats (`stat_total * 36 / minutes`) vs `Per 36 Minutes.csv` | Epsilon 0.0001 |
| V-004 | `PlayerStatistics.csv` + `TeamStatistics.csv` | Per-100 stats using possessions formula vs `Per 100 Poss.csv` | Epsilon 0.0001 |
| V-005 | `Advanced.csv` | Compare advanced fields vs stored `player_season_advanced` values | Epsilon 0.0001 |

Possessions formula for V-004:
- `team_poss = FGA + 0.4*FTA - 1.07*(ORB/(ORB+oppDRB))*(FGA-FGM) + TOV`
- `opp_poss` computed from opponent row.
- `game_poss = 0.5 * (team_poss + opp_poss)`
- `player_poss = game_poss * (player_minutes / team_minutes)` using `numMinutes` from `TeamStatistics.csv`.

Validation must exit non-zero if any check fails and print a summary of mismatches.

## 7) Frontend MVP (Leptos)
- Use `create_resource` to fetch lists from Convex HTTP API via `CONVEX_URL/api/query`.
- Pages:
  - `/players` list: show `display_name`, `from_year`, `to_year`.
  - `/teams` list: show `city`, `nickname`, `abbreviation`, `is_active`.
- Provide loading, empty, and error states.

## 8) Nightly Scheduling
Update `nightly.yml` to run:
1) `nba_etl seed --csv-dir data/raw --batch-size 200`
2) `nba_etl backfill --start-date YYYYMMDD --end-date YYYYMMDD --concurrency 1 --delay-ms 3000`

Date window: yesterday in UTC (`date -u -d "yesterday" +%Y%m%d`). Use `SCRAPER_USER_AGENT`, `CONVEX_URL`, and `CONVEX_ADMIN_KEY` in the workflow env.

## 9) ANTI-PATTERNS (DO NOT)

| DO NOT | DO INSTEAD | WHY |
|--------|------------|-----|
| Deduplicate awards by `award_type + season_year` only | Use `award_key` to ensure per-player uniqueness | Avoid dropping award rows |
| Deduplicate player season rows without `team_abbrev` | Use team-aware keys for season totals/advanced | Preserve multi-team seasons |
| Fetch all `team_history` rows and filter in memory | Use `by_active` index with `paginate` | Prevent full-table scans |
| Ignore robots.txt crawl-delay | Enforce `Crawl-delay` and per-host single-flight | Avoid bans |
| Use floating-point equality for validations | Compare with epsilon (0.0001) | Avoid false negatives |
| Send unbounded batches to Convex | Chunk to <= 1 MiB payload size | Convex limits |
| Parse dates inconsistently across tables | Normalize to `YYYY-MM-DD` at ingest | Consistent joins |
| Infer missing IDs without logging | Log and skip missing mappings | Auditability |

## 10) TEST CASE SPECIFICATIONS

### Unit Tests Required (Scraper)
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| SC-001 | `scrape_games_for_date` | HTML with 2 summaries and 1 `Final` link | 1 absolute URL | no `Final` text |
| SC-002 | `scrape_boxscore` | officials block + coach links | 3 refs + 2 coaches | missing officials |
| SC-003 | `scrape_coaches` | table with header rows | header rows skipped | empty tbody |
| SC-004 | `scrape_referees` | table with 2 refs | 2 refs parsed | missing href |
| SC-005 | `scrape_awards_for_year` | awards table with `data-append-csv` | award rows parsed | `thead` rows |

### Unit Tests Required (ETL)
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| ETL-001 | Team history load | `TeamHistories.csv` row | `team_history_id` sequential | `seasonActiveTill` empty |
| ETL-002 | Team map | city/name pair | correct `team_id` | duplicate city/name |
| ETL-003 | Game date parse | `gameDateTimeEst` | `YYYY-MM-DD` | missing time |
| ETL-004 | Season calc | `2025-10-01` | `season_year = 2026` | `2025-05-01` |
| ETL-005 | Team boxscores | `TeamStatistics.csv` row | `team_boxscores` mapping | empty numeric fields |
| ETL-006 | Award key | awards row | `award_key` stable | missing `player_bref_id` |

### Unit Tests Required (Convex)
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| CVX-001 | `upsertPlayers` | 2 players, one existing | inserts 1 | duplicate id |
| CVX-002 | `upsertPlayerSeasonTotals` | two rows same player/year different team | inserts 2 | `team_abbrev = TOT` |
| CVX-003 | `upsertAwards` | two players same season/type | inserts 2 | missing `player_bref_id` |
| CVX-004 | `listPlayers` | paginationOpts 50 | 50 sorted results | empty table |
| CVX-005 | `listTeams` | activeOnly=true | only active teams | no active teams |

### Unit Tests Required (Validation)
| Test ID | Component | Input | Expected Output | Edge Cases |
|---------|-----------|-------|-----------------|------------|
| VAL-001 | Team totals | game with 2 players | points sum equals teamScore | missing player rows |
| VAL-002 | Per-game | season totals | matches `Player Per Game.csv` | zero games |
| VAL-003 | Per-36 | minutes > 0 | matches `Per 36 Minutes.csv` | minutes = 0 |
| VAL-004 | Per-100 | known fixture | matches `Per 100 Poss.csv` | missing opp DRB |
| VAL-005 | Advanced parity | `Advanced.csv` rows | matches stored values | NaN values |

### Integration Tests Required
| Test ID | Flow | Setup | Verification | Teardown |
|---------|------|-------|--------------|----------|
| IT-001 | Seed + Query | run `seed` on fixture CSVs | `listPlayers` returns fixtures | delete tables |
| IT-002 | Backfill date | scrape date with 1 game | referees/coaches inserted | cleanup inserted rows |
| IT-003 | Validation | run `validate` on fixture CSVs | zero discrepancies | remove temp tables |

## 11) ERROR HANDLING MATRIX

### External Service Errors
| Error Type | Detection | Response | Fallback | Logging | Alert |
|------------|-----------|----------|----------|---------|-------|
| robots.txt blocked | matcher returns false | skip URL | none | WARN | if >10/day |
| HTTP 429/5xx | status code | backoff, retry 3x | skip after retries | WARN | if retry exhausted |
| Convex 401/403 | response body | abort batch | none | ERROR | immediate |
| Convex 413/limits | response body | reduce batch size and retry | none | WARN | if >5/hour |
| DuckDB open error | exception | abort validation | none | ERROR | immediate |
| CSV missing | file not found | skip optional files, abort required | none | ERROR | immediate |
| CSV parse error | serde error | abort seed/backfill | none | ERROR | immediate |

### User-Facing Errors
| Error Type | User Message | Code | Recovery Action |
|------------|--------------|------|-----------------|
| Convex unavailable | "Data service unavailable." | 503 | show retry button |
| Empty data | "No results yet." | 204 | show refresh |
| Invalid route | "Page not found." | 404 | link to home |

## 12) References

### Schema References
| Topic | Location | Anchor |
|-------|----------|--------|
| Convex schema | [convex/schema.ts](../convex/schema.ts) | `defineSchema` |
| Rust schema | [crates/nba_core/src/schema.rs](../crates/nba_core/src/schema.rs) | `pub struct` |

### Implementation References
| Topic | Location | Section |
|-------|----------|---------|
| PRD | [PRD.md](PRD.md#1-overview) | Section 1 |
| Convex ingest | [convex/ingest.ts](../convex/ingest.ts) | `upsert*` |
| Players query | [convex/players.ts](../convex/players.ts) | `listPlayers` |
| Teams query | [convex/teams.ts](../convex/teams.ts) | `listTeams` |
| ETL seed | [crates/nba_etl/src/seed.rs](../crates/nba_etl/src/seed.rs) | `run_seed` |
| ETL backfill | [crates/nba_etl/src/backfill.rs](../crates/nba_etl/src/backfill.rs) | `run_backfill` |
| Scraper client | [crates/nba_scraper/src/client.rs](../crates/nba_scraper/src/client.rs) | `ScraperClient` |
| Scraper B-Ref | [crates/nba_scraper/src/sites/basketball_reference.rs](../crates/nba_scraper/src/sites/basketball_reference.rs) | `scrape_*` |
| Awards scraper | [crates/nba_scraper/src/sites/awards.rs](../crates/nba_scraper/src/sites/awards.rs) | `scrape_awards_for_year` |
| Personnel scraper | [crates/nba_scraper/src/sites/personnel.rs](../crates/nba_scraper/src/sites/personnel.rs) | `scrape_coaches`, `scrape_referees` |
| Nightly workflow | [nightly.yml](../.github/workflows/nightly.yml#L1) | `Run ETL` |
