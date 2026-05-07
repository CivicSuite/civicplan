# Changelog

All notable changes to CivicPlan will be documented in this file.

The format follows Keep a Changelog, and this project follows Semantic Versioning.

## [Unreleased]

## [0.1.2] - 2026-05-07

### Added

- Production-depth policy persistence slice with `CIVICPLAN_POLICY_DB_URL`, persisted plan-policy records, persisted staff-analysis outlines, and retrieval by `analysis_id`.
- CivicZone-facing `POST /api/v1/civicplan/context/zoning` contract that returns cited, review-required plan-policy context without making zoning determinations.

### Changed

- Aligned CivicPlan's release gate, CI install path, docs, and health-contract test with the published `civiccore==1.0.0` wheel before the CivicZone policy-context contract sprint.
- Updated public UI copy to v0.1.2 and removed the static no-op lookup button.

## [0.1.1] - 2026-04-28

### Changed

- Aligned CivicPlan to `civiccore==0.3.0` while preserving the v0.1 planning policy foundation behavior.
- Updated release gates, CI wheel install, docs, tests, and browser-visible version copy for the v0.1.1 compatibility release.

## [0.1.0] - 2026-04-27

### Added

- Professional repository scaffold, documentation, issue templates, PR template, and release gates.
- FastAPI runtime foundation with root, health, and public UI endpoints.
- Deterministic cited plan-policy lookup helper.
- Policy-consistency support helper with planner-review boundary.
- Staff-analysis outline helper with citations and human-review requirement.
- Records-ready plan-policy export checklist.
- Accessible public sample UI at `/civicplan` with browser QA coverage.
