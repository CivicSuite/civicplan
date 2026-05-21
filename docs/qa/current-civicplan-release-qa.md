# CivicPlan v1.0.0 Browser QA Evidence

Base URL: `http://127.0.0.1:18080`

| Surface | Viewport | Status | Screenshot | Console | Focus | Overflow |
|---|---:|---:|---|---:|---|---:|
| resident-desktop `/civicplan` | 1440x1000 | 200 | `docs\qa\current-civicplan-release-qa\resident-desktop.png` | 0 | Skip to main content | False |
| resident-mobile `/civicplan` | 390x844 | 200 | `docs\qa\current-civicplan-release-qa\resident-mobile.png` | 0 | Skip to main content | False |
| docs-desktop `/docs` | 1440x1000 | 200 | `docs\qa\current-civicplan-release-qa\docs-desktop.png` | 0 | /openapi.json | False |
| health-json `/health` | 900x600 | 200 | `docs\qa\current-civicplan-release-qa\health-json.png` | 0 | n/a | False |

## UI State Matrix

- success: browser-rendered at desktop and mobile widths.
- loading: not applicable to the static public UI; no async loading state is exposed.
- empty: not applicable to the static public UI; API empty/no-match behavior is covered by deterministic fallback tests.
- error: API validation and auth error states are covered by tests with actionable fix copy.
- partial_degraded: not applicable to the static public UI; optional persistence disabled state is covered by 503 API tests.

## Copy And Boundary Review

Visible copy states CivicPlan is cited support only and does not make official planning determinations, provide legal advice, call live external systems by default, or replace staff/elected judgment.

## Keyboard / Focus

First Tab reaches the skip link on desktop and mobile.
