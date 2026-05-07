CivicPlan
=========

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: v0.1.2 planning policy foundation release plus production-depth policy persistence and CivicZone policy-context contract. This repo ships a FastAPI package aligned to civiccore==1.0.0, health/root endpoints, documentation gates, deterministic sample plan-policy lookup, optional database-backed policy and staff-analysis records via CIVICPLAN_POLICY_DB_URL, a CivicZone-facing cited policy-context endpoint, policy-consistency support, staff-analysis outline support, records-ready export checklist, and accessible public sample UI at /civicplan.

It does not ship official planning determinations, legal advice, live GIS, live LLM calls, plan document ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicplan
- POST /api/v1/civicplan/policies/lookup
- POST /api/v1/civicplan/context/zoning
- POST /api/v1/civicplan/consistency/check
- POST /api/v1/civicplan/staff-analysis/draft; persisted records require X-CivicPlan-Role: staff when CIVICPLAN_POLICY_DB_URL is configured
- GET /api/v1/civicplan/staff-analysis/{analysis_id} when CIVICPLAN_POLICY_DB_URL is configured and X-CivicPlan-Role: staff is present
- POST /api/v1/civicplan/export

Quickstart: install CivicCore first with python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0-py3-none-any.whl, then run python -m pip install -e ".[dev]".

Set CIVICPLAN_POLICY_DB_URL to enable persistent plan-policy and staff-analysis records. Persisted staff-analysis create/read routes are staff-only and require X-CivicPlan-Role: staff from a trusted staff or service workflow. When unset, CivicPlan continues to use deterministic in-memory sample data.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
