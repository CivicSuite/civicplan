# Audit Lite - Readiness gate
**Date:** 2026-06-05
**Scope:** Reviewed the CivicPlan public-use readiness endpoints and configured-database sample-seeding fix.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. CivicPlan now has explicit readiness gates at `/ready` and `/api/v1/civicplan/readiness`, and a configured local policy database no longer gets seeded with sample policies by the runtime. That closes the main false-green risk where an operator could point CivicPlan at an empty customer database and still appear locally populated.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `civicplan/main.py:138` exposes a short readiness endpoint, and `civicplan/main.py:145` exposes the API namespaced readiness endpoint for installers/operators.
- `civicplan/main.py:405` creates configured runtime repositories with `seed_defaults=False`, preventing sample policies from being written into local municipal databases.
- `civicplan/main.py:441` reports `not-ready` when no policy database is configured, and it requires both schema readiness and at least one loaded local policy before returning `ready`.
- `tests/test_production_depth_policy_persistence.py:116` covers unconfigured readiness, `tests/test_production_depth_policy_persistence.py:127` covers the no-sample-seed regression, and `tests/test_production_depth_policy_persistence.py:148` covers a ready local-policy database.
- Runtime root copy and operator docs now direct users to verify `/ready` before public use.

## Escalation recommendation

No escalation needed for this slice. The change is a bounded readiness/status gate and a safer repository-construction default; existing lookup fallback and staff-analysis behavior remain covered by the persistence tests.
