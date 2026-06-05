# Audit Lite - Schema status
**Date:** 2026-06-05
**Scope:** Reviewed the CivicPlan local schema-version ledger, non-destructive migration/status path, console script, docs, and tests.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. CivicPlan now records an explicit local schema version whenever the policy repository initializes, reports table/version readiness without destructive cleanup, and exposes that check through the packaged `civicplan-db-status` command. Focused tests and an installed-script smoke prove the status path works against SQLite, which is the local-first operator path used in this repo.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `civicplan/persistence.py:73` defines a single expected schema version and `civicplan/persistence.py:99` records it through a non-destructive `metadata.create_all()` migration path.
- `civicplan/persistence.py:118` reports readiness, dialect, missing tables, and current schema version for operator checks.
- `civicplan/db_admin.py:8` exposes the same status path through a package console module without seeding sample policies into operator databases.
- `tests/test_production_depth_policy_persistence.py:41` covers repository schema status, and `tests/test_production_depth_policy_persistence.py:56` covers the CLI module behavior.
- Installed console smoke returned `CivicPlan schema ready: version=2026-06-05-001; expected=2026-06-05-001; dialect=sqlite; missing_tables=none.`

## Watch items

This is a local schema ledger, not a full Alembic migration tree. If CivicPlan later changes persisted column shapes, the next slice should add version-to-version upgrade steps instead of only recording the current create-all schema.

## Escalation recommendation

No escalation needed for this slice. The change is scoped to persistence bootstrap/status reporting and does not alter existing table columns or API response contracts.
