# Changelog

All notable changes to this project are documented here.

## 0.1.1 - 2026-08-15

- Fixed public GitHub evidence collection so closed issues and merged pull requests count as maintenance activity.
- Added regression coverage for historical issue and pull-request activity.
- Updated release automation to publish when the package version changes on `main`.

## 0.1.0 - 2026-08-15

- Added local repository and public GitHub evidence collection.
- Added deterministic red/yellow/green scoring with documented hard gates.
- Added Markdown and JSON report generation.
- Added explicit fork handling and original-maintainer activity checks.
- Added fail-closed blocked-marker safety handling.
- Added tests across Python 3.11, 3.12, and 3.13.
- Added CI validation for source and wheel distributions.
- Added a reusable composite GitHub Action.
- Added maintainer ownership, roadmap, scoring, contribution, security, and release documentation.
