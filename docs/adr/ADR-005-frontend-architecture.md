# ADR-005: Frontend IA and Beginner-First Design System

Document Type: Strategic (ADR)
Status: Accepted
Date: 2026-01-15

## Context
Basketball-Reference pages are data-dense and optimized for power users. The clone must maintain information parity while making navigation and stats approachable for beginners.

## Decision
Adopt a beginner-first information architecture with a global navigation bar, page-level “On this page” anchors, and a default-on beginner stats mode. Implement a small CSS utility system within Leptos to standardize tables, callouts, and glossary tooltips.

## Consequences
- Every detail page includes a jump menu and summary callout.
- Stat tables expose beginner columns by default with an explicit advanced toggle.
- Glossary tooltips are required for all stat abbreviations.

## References

| Topic | Location | Anchor |
| --- | --- | --- |
| UX principles | [PRD](../../.plans/PRD.md#2-ux-principles) | Section 2 |
| Frontend MVP | [Implementation Spec](../../.plans/IMPLEMENTATION_SPEC.md#7-frontend-mvp-leptos) | Section 7 |
| Beginner mode | [Implementation Spec](../../.plans/IMPLEMENTATION_SPEC.md#8-ux-patterns-and-beginner-mode) | Section 8 |
