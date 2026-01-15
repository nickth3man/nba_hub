# ADR-004: Player Bios and Identity Mapping

Document Type: Strategic (ADR)
Status: Accepted
Date: 2026-01-15

## Context
Season stat CSVs are keyed by Basketball-Reference IDs (`player_bref_id`), while the `players` table is seeded from NBA API IDs. The UI requires human-readable player names on season-based pages.

## Decision
Treat `player_bref_id` as the canonical identifier for all season stat pages. Add an optional `player_name` field to `player_season_totals` during ETL so the frontend can render friendly names. The `players` table remains for NBA API references but is not used for routing on season pages.

## Consequences
- ETL parses the `player` column from season CSVs into `player_name` when available.
- Convex schema and Rust schema both include `player_name` on `player_season_totals`.
- Player profile routes use `player_bref_id` instead of `player_id`.

## References

| Topic | Location | Anchor |
| --- | --- | --- |
| MVP scope | [PRD](../../.plans/PRD.md#0-6-mvp-features) | Section 0.6 |
| Data model | [Implementation Spec](../../.plans/IMPLEMENTATION_SPEC.md#2-data-model-and-schema-alignment) | Section 2 |
| Frontend routes | [Implementation Spec](../../.plans/IMPLEMENTATION_SPEC.md#7-frontend-mvp-leptos) | Section 7 |
