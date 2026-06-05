CivicPlan
=========

CivicPlan is the CivicSuite module for comprehensive-plan policy lookup and cited planning analysis support.

Current state: v0.2.2 corrective demotion state. The previous v1.0.0 release was published in error. This narrow truth-repair release is no functional upgrade; it exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression, with the CivicCore pin aligned to the current city-core platform. This repo contains a local-first cited planning-support runtime aligned to the CivicCore v1.2.0 release wheel, health/root/readiness endpoints, documentation gates, cited plan-policy lookup, staff-only local policy ingestion via CIVICPLAN_POLICY_DB_URL, goal/objective/policy navigation, cited plan Q&A, cross-plan synthesis, amendment history, progress tracking, CivicZone and CivicClerk context contracts, policy-consistency support, staff-analysis outline support, records-ready export checklist, local adversarial integration mocks, schema status checks, and an accessible public UI at /civicplan wired to local CivicPlan APIs.

It does not ship official planning determinations, legal advice, live external vendor calls by default, permitting-system write-back, or elected-body decisions.

Core API:
- GET /
- GET /health
- GET /ready
- GET /api/v1/civicplan/readiness
- GET /civicplan
- POST /api/v1/civicplan/policies/lookup
- POST /api/v1/civicplan/context/zoning
- POST /api/v1/civicplan/consistency/check
- POST /api/v1/civicplan/staff-analysis/draft; persisted records require X-CivicPlan-Role: staff and X-CivicPlan-Staff-Key when CIVICPLAN_POLICY_DB_URL is configured
- GET /api/v1/civicplan/staff-analysis/{analysis_id} when CIVICPLAN_POLICY_DB_URL is configured and both staff headers are present
- POST /api/v1/civicplan/export

Quickstart: install CivicCore first with python -m pip install https://github.com/CivicSuite/civiccore/releases/download/v1.2.0/civiccore-1.2.0-py3-none-any.whl, then run python -m pip install -e ".[dev]".

Set CIVICPLAN_POLICY_DB_URL to enable persistent plan-policy and staff-analysis records. Persisted staff-analysis create/read routes are staff-only and require CIVICPLAN_STAFF_API_KEY, X-CivicPlan-Role: staff, and matching X-CivicPlan-Staff-Key. When unset, CivicPlan continues to use deterministic in-memory sample data. When set, the runtime initializes schema without seeding sample policies; /ready remains not-ready until adopted local policies are loaded.

Use the civicplan-import-policies console script to batch-load local municipal plan-policy CSV exports into CIVICPLAN_POLICY_DB_URL. See docs/local-policy-import.md.

Use the civicplan-db-status console script with the same SQLAlchemy URL to initialize and verify the local CivicPlan schema before pointing the runtime at a policy database.

Code license: Apache 2.0. Documentation license: CC BY 4.0.
