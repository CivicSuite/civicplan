# Security

CivicPlan current version: `1.0.0`. Deploy it behind the city's trusted access layer, configure local adopted plan-policy records, and keep official planning determinations with municipal staff and elected bodies.

When `CIVICPLAN_POLICY_DB_URL` is configured, persisted staff-analysis create/read routes require `X-CivicPlan-Role: staff` from a trusted staff or service workflow. This header gate is a local release safeguard, not a replacement for production identity, tenant scoping, and audit logging.

Report suspected vulnerabilities privately to the project maintainer. Do not open public issues containing exploit details, secrets, or sensitive municipal data.
