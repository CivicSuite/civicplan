# Audit Lite - Live public UI
**Date:** 2026-06-05
**Scope:** Reviewed the CivicPlan public UI conversion from static sample copy to live API-backed controls, plus the sample policy-list duplicate fix.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. The page now exposes usable lookup, question, consistency, navigator, and progress controls backed by existing CivicPlan endpoints, and the browser smoke proves the controls execute without console errors. The sample no-DB policy list now reads canonical sample records directly, eliminating duplicate housing-policy answers in Q&A and navigator flows.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `civicplan/public_ui.py:129` now renders a real lookup form, with Q&A, consistency, navigator, and progress controls wired to local API endpoints at `civicplan/public_ui.py:203`.
- `civicplan/public_ui.py:211` escapes API-rendered text before inserting it into result panels.
- `civicplan/main.py:418` uses canonical sample `POLICIES` for no-DB list operations, so navigator, Q&A, and synthesis no longer receive duplicate housing records.
- `tests/test_planning_foundation.py:148` rejects the old static/no-control UI contract and checks the endpoint wiring plus the JavaScript quote-escaping regression.
- `tests/test_v1_plan_workflows.py:18` covers distinct sample plan types and duplicate-free source policy IDs.
- Runtime smoke opened `/civicplan` in Chromium, clicked lookup, cited question, consistency, navigator, and progress controls, and observed zero console/page errors with one housing citation rendered in the Q&A result.

## Escalation recommendation

No escalation needed for this slice. This is scoped UI/API wiring plus a local sample-data bug fix, with focused tests and browser runtime coverage.
