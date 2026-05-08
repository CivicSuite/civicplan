# CivicPlan Release-Recovery Browser QA

Date: 2026-05-07
Scope: `docs/index.html` release-status copy after the suite-wide release
recovery claim freeze.

## Playwright Walkthrough

| Viewport | Evidence | Result |
| --- | --- | --- |
| Desktop 1440x1000 | `docs/browser-qa-civicplan-release-recovery-desktop.png` | Passed |
| Mobile 390x844 | `docs/browser-qa-civicplan-release-recovery-mobile.png` | Passed |

## Checks

- Page title rendered as `CivicPlan - cited planning policy support for CivicSuite`.
- Primary heading rendered as `Cited planning policy support that keeps humans responsible.`
- Release-recovery wording was visible in both viewports.
- Stale product-release wording was absent from the rendered page.
- Browser console messages: none.
- Page errors: none.
- Horizontal overflow: none.
- Keyboard focus check: first `Tab` reached the `recovery status` link.

## Boundary

This QA pass verifies the changed public documentation surface. It does not
recertify CivicPlan as a product-ready release; that status depends on the full
suite recovery gates and post-merge CI.
