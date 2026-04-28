CivicPlan
=========

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: v0.1.1 planning policy foundation release plus production-depth policy persistence slice. This repo ships a FastAPI package aligned to civiccore==0.3.0, health/root endpoints, documentation gates, deterministic sample plan-policy lookup, optional database-backed policy and staff-analysis records via CIVICPLAN_POLICY_DB_URL, policy-consistency support, staff-analysis outline support, records-ready export checklist, and accessible public sample UI at /civicplan.

It does not ship official planning determinations, legal advice, live GIS, live LLM calls, plan document ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicplan
- POST /api/v1/civicplan/policies/lookup
- POST /api/v1/civicplan/consistency/check
- POST /api/v1/civicplan/staff-analysis/draft
- GET /api/v1/civicplan/staff-analysis/{analysis_id} when CIVICPLAN_POLICY_DB_URL is configured
- POST /api/v1/civicplan/export

Set CIVICPLAN_POLICY_DB_URL to enable persistent plan-policy and staff-analysis records. When unset, CivicPlan continues to use deterministic in-memory sample data.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
