# Production-Depth Policy Persistence Done

Date: 2026-04-28

## Scope

This slice adds optional database-backed plan-policy and staff-analysis records while preserving deterministic sample behavior when no database URL is configured.

## Shipped

- `CIVICPLAN_POLICY_DB_URL` enables persistent plan-policy and staff-analysis records.
- `PlanPolicyRepository` stores seeded sample policies and generated staff-analysis outlines.
- `POST /api/v1/civicplan/staff-analysis/draft` returns an `analysis_id` when persistence is configured.
- `GET /api/v1/civicplan/staff-analysis/{analysis_id}` retrieves persisted staff-analysis records when persistence is configured.

## Still Not Shipped

- Official planning determinations.
- Legal advice.
- Live GIS.
- Live LLM calls.
- Plan document ingestion.
- Permitting-system integrations.
- Production staff-review queues.

## Verification

- Repository persistence tests must pass.
- API persistence and retrieval tests must pass.
- Full release verification must pass before push/merge.
- Browser QA evidence must confirm `docs/index.html` renders the updated persistence status at desktop and mobile widths with zero console errors.
