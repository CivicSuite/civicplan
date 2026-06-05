# CivicPlan Local Policy Import

CivicPlan can load local municipal plan-policy CSV exports into the configured policy database. This is a local-first operator path; it does not call live document stores, planning systems, LLMs, or vendor APIs.

## Database Target

Use the same SQLAlchemy URL that the runtime reads from `CIVICPLAN_POLICY_DB_URL`. The importer creates policy tables if needed and does not seed sample policies.

## CSV Contract

Required columns:

| Column | Purpose |
| --- | --- |
| `topic_key` | Lookup keyword for resident/staff questions, such as `housing`, `climate`, or `transportation`. |
| `policy_id` | Local adopted-policy identifier. |
| `plan_type` | Plan family such as `comprehensive`, `transportation`, `parks`, or `climate`. |
| `title` | Human-readable policy title. |
| `citation` | Public citation to the adopted plan section. |
| `excerpt` | Adopted policy excerpt. |
| `relevance` | Plain-language relevance note. |
| `adoption_status` | Adoption status; non-adopted values are labeled as pending and require staff confirmation. |
| `source_document` | Source document name or export label. |

## Failure Behavior

- Missing required columns fail before any database writes.
- Empty required values fail before any database writes.
- Existing `policy_id` rows are updated, so repeated imports are idempotent.
- Sample policies are not loaded into the target database by the importer.
