CivicPlan
=========

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: v0.1.1 planning policy foundation release. This repo ships a FastAPI package aligned to civiccore==0.3.0, health/root endpoints, documentation gates, deterministic sample plan-policy lookup, policy-consistency support, staff-analysis outline support, records-ready export checklist, and accessible public sample UI at /civicplan.

It does not ship official planning determinations, legal advice, live GIS, live LLM calls, plan document ingestion, permitting-system integrations, or production staff-review queues.

Core API:
- GET /
- GET /health
- GET /civicplan
- POST /api/v1/civicplan/policies/lookup
- POST /api/v1/civicplan/consistency/check
- POST /api/v1/civicplan/staff-analysis/draft
- POST /api/v1/civicplan/export

Code license: Apache 2.0. Documentation license: CC BY 4.0.
