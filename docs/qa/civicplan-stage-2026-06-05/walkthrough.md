# CivicPlan Stage Walkthrough
**Date:** 2026-06-05
**Branch:** `stage-civicplan-release-readiness-2026-06-05`
**Mode:** Playwright-driven runtime walkthrough

## Verdict
Pass. The `/civicplan` public UI is wired to real local CivicPlan API endpoints on desktop and mobile, and the runtime readiness/health endpoints return the expected contracts. No console errors, page errors, or failed network requests were observed.

## Product Model
CivicPlan is a local-first cited planning-support module. It helps residents and staff find cited plan-policy context, ask cited plan questions, check consistency support, browse plan structure, and inspect progress targets. It does not make official planning determinations, provide legal advice, call live vendors by default, write to permitting systems, or replace planner/elected-body judgment.

## Runtime Setup
- Server: `python -m uvicorn civicplan.main:app --host 127.0.0.1 --port 18085`
- Browser: Playwright Chromium, headless
- Desktop viewport: 1440 x 1000
- Mobile viewport: 390 x 900

## Screenshots
- Desktop initial: `docs/qa/civicplan-stage-2026-06-05/desktop-initial.png`
- Desktop completed: `docs/qa/civicplan-stage-2026-06-05/desktop-completed.png`
- Mobile initial: `docs/qa/civicplan-stage-2026-06-05/mobile-initial.png`
- Mobile completed: `docs/qa/civicplan-stage-2026-06-05/mobile-completed.png`

## Walked Flows
- Opened `/civicplan` and verified the page title `CivicPlan Public Policy Lookup`.
- Clicked `Look Up Policy` and verified cited Comprehensive Plan policy text rendered.
- Clicked `Ask Cited Question` and verified `Cited Answer` rendered.
- Clicked `Check Consistency Support` and verified `potentially-consistent` rendered.
- Clicked `Load Plans` and verified `transportation-plan-3.4` rendered in the navigator output.
- Clicked `Load Targets` and verified `Progress Targets` rendered.
- Repeated the same full flow at mobile viewport.
- Opened `/ready` and verified unconfigured local DB returns `not-ready` with blockers.
- Opened `/health` and verified CivicPlan `0.2.2` with CivicCore `1.2.0`.

## API/Runtime Results
`/ready` without `CIVICPLAN_POLICY_DB_URL`:

```json
{
  "status": "not-ready",
  "ready": false,
  "policy_database_configured": false,
  "schema_ready": false,
  "schema_version": null,
  "expected_schema_version": null,
  "policy_count": 0,
  "blockers": [
    "Set CIVICPLAN_POLICY_DB_URL to a local policy database.",
    "Load adopted municipal plan policies before public use."
  ]
}
```

`/health`:

```json
{
  "status": "ok",
  "service": "civicplan",
  "version": "0.2.2",
  "civiccore_version": "1.2.0"
}
```

## Console And Network
- Console errors: 0
- Page errors: 0
- Failed network requests: 0

## Findings
None.

## Test Coverage Cross-Check
- `tests/test_planning_foundation.py` covers public UI route wiring strings and the JavaScript quote-escaping regression.
- `tests/test_v1_plan_workflows.py` covers navigator distinct plan types and duplicate-free Q&A source policy IDs.
- `tests/test_production_depth_policy_persistence.py` covers readiness states, no sample seeding for configured DBs, staff auth, persistence, and schema status.

## Follow-Up
No immediate fixes required. If the UI grows beyond this single-page tool, promote the Playwright smoke into a committed automated browser test.
