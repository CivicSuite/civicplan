# CivicPlan

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: **v0.1.2 planning policy foundation release plus production-depth policy persistence and CivicZone policy-context contract**. This repo ships a FastAPI package aligned to `civiccore==1.0.0`, health/root endpoints, documentation gates, deterministic sample plan-policy lookup, optional database-backed policy and staff-analysis records via `CIVICPLAN_POLICY_DB_URL`, a CivicZone-facing cited policy-context endpoint, policy-consistency support, staff-analysis outline support, records-ready export checklist, and accessible public sample UI at `/civicplan`. It does **not** ship official planning determinations, legal advice, live GIS, live LLM calls, plan document ingestion, permitting-system integrations, or production staff-review queues.

## What CivicPlan Does

- Looks up sample comprehensive-plan, transportation-plan, and parks-plan policies with citations.
- Returns cited comprehensive-plan context for CivicZone zoning questions while preserving a review-required boundary.
- Flags sample consistency factors while keeping the planner of record responsible for official findings.
- Drafts a cited staff-analysis outline that requires human review.
- Builds records-ready export checklists that preserve proposal, policy, reviewer, and generated-output provenance.
- Demonstrates a public plan-policy lookup UI at `/civicplan`.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Foundation

- `GET /` returns current module status and next roadmap boundary.
- `GET /health` returns package and CivicCore version information.
- `GET /civicplan` returns the accessible public sample UI.
- `POST /api/v1/civicplan/policies/lookup` returns a cited sample plan policy.
- `POST /api/v1/civicplan/context/zoning` returns cited plan-policy context for CivicZone questions.
- `POST /api/v1/civicplan/consistency/check` returns sample consistency-support factors.
- `POST /api/v1/civicplan/staff-analysis/draft` returns a cited staff-analysis outline; persisted records require `X-CivicPlan-Role: staff` when `CIVICPLAN_POLICY_DB_URL` is configured.
- `GET /api/v1/civicplan/staff-analysis/{analysis_id}` retrieves persisted staff-analysis records when `CIVICPLAN_POLICY_DB_URL` is configured and `X-CivicPlan-Role: staff` is present.
- `POST /api/v1/civicplan/export` returns a records-ready plan-policy export checklist.

Set `CIVICPLAN_POLICY_DB_URL` to enable persistent plan-policy and staff-analysis records. Persisted staff-analysis create/read routes are staff-only and require `X-CivicPlan-Role: staff` from a trusted staff or service workflow. When unset, CivicPlan continues to use deterministic in-memory sample data.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
