# Audit Lite - CivicCore 1.2 Alignment
**Date:** 2026-06-05
**Scope:** Reviewed CivicPlan dependency, workflow, docs, and runtime-test alignment to the published CivicCore v1.2.0 wheel.
**Reviewer:** Codex (audit-lite)

## TL;DR
Ship this slice. CivicPlan now pins the current CivicCore v1.2.0 release wheel, GitHub workflow install steps match the source dependency, `/health` asserts the imported runtime version, and stale CivicCore pin text has been removed from current-facing and QA docs.

## Severity rollup
- Blocker: 0
- Critical: 0
- Major: 0
- Minor: 0
- Nit: 0

## Findings

None.

## What's working
- `pyproject.toml`, workflow install steps, runtime tests, README/manual quickstarts, and docs verifier now agree on CivicCore v1.2.0.
- The stale-pin scan has no remaining matches for the previous CivicCore URL/hash/version strings.
- The release gate passed after the alignment change.

## Verification

- Stale pin scan: no matches for previous CivicCore wheel URL/hash/version strings.
- Release gate: `VERIFY-RELEASE: PASSED`
- Test suite inside release gate: `34 passed, 1 warning`

## Escalation recommendation

No escalation needed. This is a scoped release-contract alignment with direct tests and a passing release gate.
