# PRD: NBA Hub (Rust + Convex + DuckDB) Basketball-Reference Clone (Strategic)

Version: 1.1
Status: Finalized
Date: 2026-01-14
Owner: Project Lead

## 1) Overview
Build a public-facing, 1:1 clone of basketball-reference.com for NBA/BAA/ABA with a Rust-only implementation wherever possible. Convex will be the application database and backend platform, and DuckDB will remain for local analytics, derivations, and validation. The system must preserve full feature parity with the existing Python pipeline, maintain strict data validation against authoritative sources (Basketball-Reference, NBA.com, etc.), and be modular, readable, and approachable for new contributors.

## 2) Goals
- 1:1 page and table parity with Basketball-Reference for NBA/BAA/ABA.
- Rust-first codebase (Rust only where possible).
- Convex + DuckDB hybrid: Convex for application data and APIs, DuckDB for heavy analytics and validation.
- Maximal data integrity and auditability: every number derives from underlying games and boxscores.
- Public stateless read experience; internal admin-only ingestion and tooling.
- Nightly updates at 12:00 AM local time.
- No paid services; open-source tooling only (Convex deployment allowed).
- Modular architecture with clear boundaries, beginner-friendly structure, and strong docs.

## 3) Non-Goals
- WNBA, NCAA, international leagues, or post-project expansions.
- Betting, gambling, or monetized data usage.
- Paid infrastructure or closed-source dependencies.
- Mobile native apps (web only).

## 4) Users and Use Cases
- Public users browsing stats, standings, rosters, game logs, and historical data.
- Internal admin workflows for ingestion, validation, and backfills.

## 5) Success Criteria
- All pages and tables match Basketball-Reference for NBA/BAA/ABA in content and structure.
- All derived stats (per-game, per-36, per-100, advanced) match source values within defined tolerances (Integers as source of truth, float comparisons with epsilon).
- Full Python feature parity achieved in Rust.
- Convex-backed API responds quickly for public page views.
- Nightly updates complete reliably without bans or robots.txt violations.

## 6) Scope
### 6.1 Pages (Public)
- Players: bio, career totals, season totals, per-game, advanced, game logs, splits.
- Teams: seasons, rosters, standings, stats, drafts, records.
- Seasons: league standings, leaders, awards, playoffs, schedules.
- Games: boxscores, summaries, play-by-play where available.
- Drafts, awards, transactions, coaches, referees.

### 6.2 Data Coverage
- NBA, BAA, ABA (all seasons).
- Every single page that can be derived from the database.
- All source pages mirrored by database-backed views.

## 7) Architecture
### 7.1 High-Level Components
- Rust Scraper/ETL: Extracts and normalizes data from source sites.
- Convex: Primary application database and API surface.
- DuckDB: Local analytics, validation, derivation, and backups.
- Frontend: Leptos (SSR + hydration) public site.
- Hosting: Github Actions for nightly scrapes (Cron).

### 7.2 Rust-Only Constraint
Convex server functions and schema are authored in TypeScript. To maintain the Rust-first goal:
- **Schema as Infrastructure**: Treat `convex/schema.ts` as the Database Definition Layer (DDL). It is the source of truth for storage structure.
- **Minimal TS Logic**: Convex functions are restricted to simple CRUD and subscription handling.
- **Heavy Logic in Rust**: All scraping, ETL, statistical derivation, and complex validation reside in Rust services.
- **Data Flow**: Rust calculates final states and pushes JSON to Convex.

## 8) Data Flow
1) **Trigger**: Github Actions Cron triggers Rust binary nightly.
2) **Fetch**: Rust scraper fetches source pages (respecting robots.txt).
3) **Extract**: Raw tables parsed into JSON (HTML discarded to save space).
4) **Normalize**: JSON records normalized into canonical types (Integers for counts).
5) **Validate**: Rust validation layer checks consistency (e.g., Team Pts = Sum Player Pts).
6) **Write**: Clean data written to Convex tables via Rust Client.
7) **Sync**: Convex exports changes to local DuckDB for heavy analytics (optional/dev).
8) **Serve**: Public users query Convex via Leptos frontend.

## 9) Data Model (Core Tables)
Use existing `unified_*` schema as baseline. Key entities:
- leagues
- seasons
- teams
- players
- games
- player_boxscores
- team_boxscores
- player_season_totals
- player_season_advanced
- team_season_totals
- team_season_advanced
- standings
- awards
- drafts
- transactions
- coaches
- referees

**Precision Strategy**:
- Source of Truth: **Integers** (FGM, FGA, Minutes, Seconds).
- Derived Stats: Calculated on read or stored as `f64` for sorting, but strictly rounded at display layer.
- Comparison: Use epsilon (`0.0001`) for float parity checks against reference sites.

## 10) Convex + DuckDB Integration
- Convex: Operational datastore, real-time API.
- DuckDB: Analytical engine, complex SQL joins for validation, local dev environment.
- **Data Retention**:
    - Raw HTML: **Discarded** after parsing.
    - Raw JSON: **Retained** in DuckDB/Convex for auditability and re-parsing.

## 11) Scraping and Politeness Strategy
Requirements:
- Respect robots.txt (strict).
- Use crawl-delay directives when provided.
- Concurrency limits per-host.
- Backoff on 429/5xx with exponential delay + jitter.
- Cache responses and use conditional requests when possible.

Recommended Rust approach:
- HTTP: reqwest + tokio.
- HTML parsing: scraper.
- robots.txt parsing: robotstxt crate (Apache-2.0).
- Rate limiting: per-domain semaphore + configurable crawl delay.

Target behavior:
- Default crawl delay: 3s if not specified.
- 1-2 concurrent requests per host.
- Respect crawl-delay and request-rate directives.

## 12) Validation and Integrity
- Schema validation on ingest with strict types.
- Cross-check totals vs per-game sums.
- Team total points must match sum of players for every game.
- Season totals derived from games and compared to scraped summary tables.
- Mark historical seasons as immutable once validated.
- Audit tables for discrepancies and remediation workflows.

## 13) API Requirements
- Public, stateless read access for page rendering.
- Internal-only admin endpoints for ingestion, re-scrapes, and validation.
- Typed query layer via Convex functions.
- Page view analytics only (no user tracking).

## 14) Frontend (Leptos)
- Server-side rendered for SEO and fast initial load.
- Rust-only UI code.
- Cache-friendly HTML responses.
- Public pages match Basketball-Reference layout/content.

## 15) Scheduling
- **Primary**: Github Actions Cron (`0 9 * * *` UTC / 4 AM ET) for nightly updates.
- **Secondary**: Local admin triggers for full backfills or ad-hoc repairs.

## 16) Hosting and Deployment
- **Backend**: Convex (Managed).
- **Frontend**: Vercel/Netlify (Leptos output) or Convex Hosting.
- **ETL/Scraper**: Github Actions (Ephemeral Runners).
- **Cost**: $0 (Free Tier for all services).

## 17) Performance Targets
- Page render latency under 200ms for common pages.
- Avoid heavy joins in Convex; rely on precomputed tables.
- Cache hot pages where possible.

## 18) Risks
- Rust-only constraint conflicts with Convex TypeScript requirement (Mitigated by "Schema-only TS" pattern).
- Scraping rate limits or bans if politeness not carefully enforced.
- Data volume and validation time for full historical backfill.
- Convex limits for large historical datasets.

## 19) Milestones
1) **Setup**: Initialize Rust workspace, Convex project, and Github Actions workflows.
2) **Port Core**: Translate `src/core` and `unified_*` schema to Rust structs and Convex Schema.
3) **Scraper Parity**: Port Python scrapers to Rust (`reqwest` + `scraper`), ensuring 1:1 data match.
4) **ETL Pipeline**: Implement Rust ETL to write to Convex.
5) **Frontend MVP**: Leptos pages for Players and Teams.
6) **Backfill**: Execute full historical import via local runner.
7) **Validation**: Verify all derived stats against Basketball-Reference.

## 20) Implementation Decisions (Finalized)
- **TS Usage**: Limited to `convex/schema.ts` and minimal `convex/*.ts` for mutations/queries. No complex logic in TS.
- **Hosting**: Github Actions for nightly jobs. No VPS.
- **Retention**: Raw JSON stored. Raw HTML deleted.
- **Precision**: Integer storage for counts. Floats for averages with display rounding.

## 21) References

### Implementation Details Location
| Content Type | Location |
|--------------|----------|
| Anti-patterns | [Implementation Spec, Section 9](IMPLEMENTATION_SPEC.md#9-anti-patterns-do-not) |
| Test Cases | [Implementation Spec, Section 10](IMPLEMENTATION_SPEC.md#10-test-case-specifications) |
| Error Handling | [Implementation Spec, Section 11](IMPLEMENTATION_SPEC.md#11-error-handling-matrix) |

### Schema References
| Topic | Location | Anchor |
|-------|----------|--------|
| Convex schema | [convex/schema.ts](../convex/schema.ts) | `defineSchema` |
