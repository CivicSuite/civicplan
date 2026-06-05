# CivicPlan v1.0.0 Careful-Coding Evidence

Date: 2026-05-21
Scope: release-truth promotion from demoted v0.2.0 to v1.0.0.

## Step 1 - Callers / Consumers

- Runtime version consumers: `civicplan/__init__.py`, `civicplan/main.py`, `/health`, FastAPI app metadata.
- Packaging consumers: `pyproject.toml`, `scripts/verify-release.sh`, GitHub `verify.yml`, GitHub `release.yml`.
- Docs consumers: README, text README, user manual, security note, docs index, implementation plan, reconciliation, release status, changelog.
- Test consumers: runtime foundation tests, planning foundation public UI test, release verifier.
- UX consumers: `/civicplan` public page and `/docs` generated FastAPI docs.

## Step 2 - Runtime Context

The changed version and dependency strings are read during import, FastAPI route handling, CI workflow setup, shell release verification, package build, and browser-rendered static HTML. No async/sync contract changed.

## Step 3 - Pattern Fan-Out

Searched current-facing surfaces for `0.2.0`, `v0.2.0`, stale CivicCore/CivicZone references, and release-candidate wording. Remaining `0.2.0` hits are limited to docs verifier banlist and tests that assert the banlist remains present.

## Step 4 - Data Contract

The release contract changes from demoted recovery label to `1.0.0`; the API schema and endpoint shapes do not change. CivicCore dependency truth remains a direct v1.2.0 release wheel.

## Step 5 - Blast Radius

This changes release truth across code, docs, tests, workflows, release verifier, and public UI. If only one layer moved, CivicPlan could produce a false v1 artifact or stale CI proof; the fix moved all mirrored surfaces together.

## Step 6 - File Re-Read

Re-read changed runtime, verifier, docs, workflow, and test files through diff and targeted grep after edits.

## Step 7 - Full Path

Operator installs CivicPlan -> package imports `__version__` -> `/health` reports CivicPlan `0.2.2` and CivicCore `1.2.0` -> resident opens `/civicplan` -> page shows v0.2.2 corrective demotion support and planning boundary copy -> release verifier builds `civicplan-0.2.2` artifacts and SHA256SUMS.

## Step 8 - New State Consumption

The `0.2.2` value is consumed by package metadata, `/health`, root status copy, public UI copy, docs, release verifier artifact names, and tests. The CivicCore v1.2.0 dependency is consumed by `pyproject.toml`, workflow install steps, README/manual quickstarts, and tests.

## Step 9 - Five-Lens Self-Audit

- Principal engineer: no API shape changed; CI dependency pin drift was found and fixed.
- UX: browser screenshots show v1 visible, no console/page errors, no overflow, skip-link focus works.
- QA: tests, docs, Ruff, release verifier, action-budget, and diff check pass.
- Tests: added workflow dependency truth regression coverage.
- Docs: current-facing docs now align to v1.0.0 and avoid official-determination/legal/live-vendor/suite-ready overclaims.
