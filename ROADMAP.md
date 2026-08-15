# Roadmap

This roadmap records intended maintenance work. It is not a promise of dates or adoption, and priorities may change in response to real user reports.

## v0.1 — Public Foundation

- [x] Inspect local repositories and public GitHub repositories.
- [x] Generate Markdown and JSON reports.
- [x] Apply deterministic red/yellow/green assessment rules.
- [x] Distinguish original repositories from weak fork-only evidence.
- [x] Add safety boundaries and blocked-marker handling.
- [x] Test Python 3.11, 3.12, and 3.13 in CI.
- [x] Provide a reusable composite GitHub Action.
- [x] Document scoring and release procedures.
- [x] Publish the first tagged GitHub Release.
- [x] Validate tagged installation in a clean environment.

## v0.2 — Better Evidence Transparency

- [ ] Add a versioned JSON report schema.
- [ ] Include the collection timestamp and collector version in reports.
- [ ] Explain the source of every evidence field in report output.
- [ ] Add fixtures for renamed default branches and nonstandard policy paths.
- [ ] Add optional strict mode for CI enforcement without changing default behavior.

## v0.3 — Maintainer Workflow Integration

- [ ] Add machine-readable GitHub Action outputs for status and score.
- [ ] Add a documented workflow for periodic repository health checks.
- [ ] Add comparison reports that show evidence changes between two runs.
- [ ] Evaluate SARIF output only if it maps cleanly to actionable findings.

## Packaging and Distribution

- [ ] Publish to PyPI after the tagged GitHub release is verified.
- [ ] Add trusted publishing rather than long-lived package tokens.
- [ ] Publish provenance for release artifacts.
- [ ] Add installation and upgrade compatibility tests.

## Non-Goals

- Predicting acceptance into grants, sponsorships, or support programs.
- Fabricating or purchasing community signals.
- Accessing private repositories without an explicit future design and security review.
- Replacing human review of project importance, governance, or ecosystem impact.
