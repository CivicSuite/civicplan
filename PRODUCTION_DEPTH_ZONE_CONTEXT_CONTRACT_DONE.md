# CivicPlan Production Depth - Zone Context Contract

Date: 2026-05-07

Status: done for the v0.1.2 production-depth sprint.

Implemented:

- Added `POST /api/v1/civicplan/context/zoning`.
- Returns cited plan-policy context with `policy_id`, `plan_type`, `citation`, `excerpt`, `relevance`, `disclaimer`, `review_required`, `source`, `civiczone_context_id`, and a boundary statement.
- Uses deterministic sample policy lookup when `CIVICPLAN_POLICY_DB_URL` is unset.
- Uses persisted policy records when `CIVICPLAN_POLICY_DB_URL` is configured.
- Returns actionable validation guidance when the required `topic` field is missing or invalid.
- Keeps existing endpoint validation guidance endpoint-neutral while preserving zoning-specific help on the zoning context endpoint.
- Scopes persisted policy lookup by `plan_type` and topic/policy match so a configured database cannot return an unrelated policy solely because it shares a plan type.
- Updated public UI copy to v0.1.2 and removed the static no-op lookup button.

Boundary:

- CivicPlan provides cited comprehensive-plan context only.
- CivicPlan does not make zoning determinations, planning approvals, legal advice, GIS lookups, or staff-report approvals.

Verification:

- `python -m pytest tests\test_planning_foundation.py tests\test_production_depth_policy_persistence.py -q`: 15 passed.
- `bash scripts/verify-release.sh`: 18 passed, docs gate passed, placeholder import gate passed, Ruff passed, and v0.1.2 artifacts built.
- `python -m ruff check .`: all checks passed.
- `bash scripts/verify-docs.sh`: `VERIFY-DOCS: PASSED`.
- Playwright browser QA covered `docs/index.html` and `/civicplan` at 1366x900 and 390x844 with no console errors, no page errors, no horizontal overflow, and no public UI buttons.
