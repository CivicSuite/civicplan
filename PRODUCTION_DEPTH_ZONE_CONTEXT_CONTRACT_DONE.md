# CivicPlan Production Depth - Zone Context Contract

Date: 2026-05-07

Status: done for the v0.1.2 production-depth sprint.

Implemented:

- Added `POST /api/v1/civicplan/context/zoning`.
- Returns cited plan-policy context with `policy_id`, `plan_type`, `citation`, `excerpt`, `relevance`, `disclaimer`, `review_required`, `source`, `civiczone_context_id`, and a boundary statement.
- Uses deterministic sample policy lookup when `CIVICPLAN_POLICY_DB_URL` is unset.
- Uses persisted policy records when `CIVICPLAN_POLICY_DB_URL` is configured.
- Returns actionable validation guidance when the required `topic` field is missing or invalid.
- Adds bounded request-field lengths across public API request models.
- Keeps existing endpoint validation guidance endpoint-neutral while preserving zoning-specific help on the zoning context endpoint.
- Scopes persisted policy lookup by `plan_type` and topic/policy match so a configured database cannot return an unrelated policy solely because it shares a plan type.
- Requires `X-CivicPlan-Role: staff` for persisted staff-analysis create/read routes when policy persistence is configured.
- Updated public UI copy to v0.1.2 and removed static no-op/editable controls from the sample lookup.

Boundary:

- CivicPlan provides cited comprehensive-plan context only.
- CivicPlan does not make zoning determinations, planning approvals, legal advice, GIS lookups, or staff-report approvals.

Verification:

- `python -m pytest tests\test_planning_foundation.py tests\test_production_depth_policy_persistence.py -q`: 18 passed.
- `bash scripts/verify-release.sh`: 21 passed, docs gate passed, placeholder import gate passed, Ruff passed, and v0.1.2 artifacts built.
- `python -m ruff check .`: all checks passed.
- `bash scripts/verify-docs.sh`: `VERIFY-DOCS: PASSED`.
- Clean Windows venv install with the documented CivicCore wheel prerequisite followed by `python -m pip install -e ".[dev]"`: imported CivicPlan `0.1.2` and CivicCore `1.0.0`.
- Playwright browser QA covered `docs/index.html` and `/civicplan` at 1366x900 and 390x844 with no console errors, no page errors, no horizontal overflow, no public UI buttons, and no editable static sample fields.
