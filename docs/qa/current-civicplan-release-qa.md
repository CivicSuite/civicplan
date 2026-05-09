# CivicPlan Current Release QA

Date: 2026-05-09
Scope: live local CivicPlan runtime at `http://127.0.0.1:18153`

## Summary

Live browser QA passed for the current CivicPlan recovery pass.

| Scenario | Viewport | Path | Status | Overflow | Console | Page errors | Focus evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| resident-desktop | 1440x1000 | `/civicplan` | 200 | no | 0 | 0 | Skip to main content |
| resident-mobile | 390x844 | `/civicplan` | 200 | no | 0 | 0 | Skip to main content |
| docs-desktop | 1440x1000 | `/docs` | 200 | no | 0 | 0 | `/openapi.json` |
| health-json | 800x600 | `/health` | 200 | no | 0 | 0 | response content rendered |

## Evidence Files

- `docs/qa/current-civicplan-release-qa/resident-desktop.png`
- `docs/qa/current-civicplan-release-qa/resident-mobile.png`
- `docs/qa/current-civicplan-release-qa/docs-desktop.png`
- `docs/qa/current-civicplan-release-qa/health-json.png`
- `docs/qa/current-civicplan-release-qa/summary.json`

## Boundaries Checked

- Resident UI shows cited plan-policy lookup, consistency support, staff analysis, export, plan navigator, progress tracking, and planning boundary copy.
- The page keeps the no-official-determination, no-legal-advice, and human-review boundaries visible.
- No browser console messages or page errors were observed.
- No horizontal overflow was observed at desktop or mobile widths.
- Keyboard focus reached the skip link or expected rendered browser content.
