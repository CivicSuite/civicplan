# CivicPlan

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: **v1.0.0 product release**. This repo ships a FastAPI package aligned to `civiccore==1.0.0`, health/root endpoints, documentation gates, cited plan-policy lookup, staff-only local policy ingestion via `CIVICPLAN_POLICY_DB_URL`, goal/objective/policy navigation, cited plan Q&A, cross-plan synthesis, amendment history, progress tracking, CivicZone and CivicClerk context contracts, policy-consistency support, staff-analysis outline support, records-ready export checklist, local adversarial integration mocks, and accessible public UI at `/civicplan`. It does **not** ship official planning determinations, legal advice, live external vendor calls by default, permitting-system write-back, or elected-body decisions.

## What CivicPlan Does

- Looks up sample comprehensive-plan, transportation-plan, and parks-plan policies with citations.
- Ingests local adopted, pending, or superseded plan policies into the configured database.
- Lets residents and staff browse plan structure and ask cited plan-policy questions.
- Synthesizes cross-plan context with citations and review-required boundaries.
- Returns cited comprehensive-plan context for CivicZone zoning questions while preserving a review-required boundary.
- Returns CivicClerk staff-report context without making the staff report official.
- Flags sample consistency factors while keeping the planner of record responsible for official findings.
- Tracks amendment status and progress-target evidence for staff review.
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
- `POST /api/v1/civicplan/policies/ingest` stores a staff-only local plan policy when `CIVICPLAN_POLICY_DB_URL` is configured.
- `GET /api/v1/civicplan/plans/navigator` returns cited plan structure grouped by plan type.
- `POST /api/v1/civicplan/questions/answer` returns a cited, review-required plan-policy answer.
- `POST /api/v1/civicplan/plans/synthesis` returns cited cross-plan synthesis for a topic.
- `GET /api/v1/civicplan/amendments/history` distinguishes adopted, pending, and superseded plan language.
- `GET /api/v1/civicplan/progress/targets` returns measurable target status and evidence.
- `POST /api/v1/civicplan/context/zoning` returns cited plan-policy context for CivicZone questions.
- `POST /api/v1/civicplan/context/civicclerk` returns cited staff-report context for CivicClerk.
- `POST /api/v1/civicplan/integrations/mock` validates local integration fixtures and rejects live endpoints.
- `POST /api/v1/civicplan/consistency/check` returns sample consistency-support factors.
- `POST /api/v1/civicplan/staff-analysis/draft` returns a cited staff-analysis outline; persisted records require `X-CivicPlan-Role: staff` when `CIVICPLAN_POLICY_DB_URL` is configured.
- `GET /api/v1/civicplan/staff-analysis/{analysis_id}` retrieves persisted staff-analysis records when `CIVICPLAN_POLICY_DB_URL` is configured and `X-CivicPlan-Role: staff` is present.
- `POST /api/v1/civicplan/export` returns a records-ready plan-policy export checklist.

Set `CIVICPLAN_POLICY_DB_URL` to enable persistent plan-policy and staff-analysis records. Persisted staff-analysis and policy-ingestion routes are staff-only and require `X-CivicPlan-Role: staff` from a trusted staff or service workflow. When unset, CivicPlan continues to use deterministic in-memory sample data.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
