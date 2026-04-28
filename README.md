# CivicPlan

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: **v0.1.1 planning policy foundation release**. This repo ships a FastAPI package aligned to `civiccore==0.3.0`, health/root endpoints, documentation gates, deterministic sample plan-policy lookup, policy-consistency support, staff-analysis outline support, records-ready export checklist, and accessible public sample UI at `/civicplan`. It does **not** ship official planning determinations, legal advice, live GIS, live LLM calls, plan document ingestion, permitting-system integrations, or production staff-review queues.

## What CivicPlan Does

- Looks up sample comprehensive-plan, transportation-plan, and parks-plan policies with citations.
- Flags sample consistency factors while keeping the planner of record responsible for official findings.
- Drafts a cited staff-analysis outline that requires human review.
- Builds records-ready export checklists that preserve proposal, policy, reviewer, and generated-output provenance.
- Demonstrates a public plan-policy lookup UI at `/civicplan`.

## Developer Quickstart

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
bash scripts/verify-release.sh
```

## API Foundation

- `GET /` returns current module status and next roadmap boundary.
- `GET /health` returns package and CivicCore version information.
- `GET /civicplan` returns the accessible public sample UI.
- `POST /api/v1/civicplan/policies/lookup` returns a cited sample plan policy.
- `POST /api/v1/civicplan/consistency/check` returns sample consistency-support factors.
- `POST /api/v1/civicplan/staff-analysis/draft` returns a cited staff-analysis outline.
- `POST /api/v1/civicplan/export` returns a records-ready plan-policy export checklist.

## License

Code is Apache 2.0. Documentation is CC BY 4.0.
