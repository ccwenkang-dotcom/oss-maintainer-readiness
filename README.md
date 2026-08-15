# OSS Maintainer Readiness Checker

[![CI](https://github.com/ccwenkang-dotcom/oss-maintainer-readiness/actions/workflows/ci.yml/badge.svg)](https://github.com/ccwenkang-dotcom/oss-maintainer-readiness/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ccwenkang-dotcom/oss-maintainer-readiness)](https://github.com/ccwenkang-dotcom/oss-maintainer-readiness/releases/tag/v0.1.0)

A local-first command-line tool and reusable GitHub Action for checking the public evidence that an open-source repository is ready for sustained maintenance.

The checker inspects public GitHub metadata or a local repository, applies a deterministic evidence model, and writes both Markdown and JSON reports. It is intentionally conservative: weak or missing evidence is reported as weak or missing rather than inferred.

## Why This Exists

Maintainers often need a compact, repeatable view of whether a repository has the operational basics expected of a healthy open-source project: documentation, licensing, tests, CI, releases, issue handling, security guidance, and recent maintenance.

This project turns those visible signals into an auditable report. It does **not** decide whether a project qualifies for any grant, sponsorship, accelerator, or maintainer-support program.

## What It Checks

- Public repository visibility
- Original maintainer activity versus fork-only evidence
- README and open-source license
- Tests and continuous integration
- Recent commits and release or tag history
- Issue or pull-request activity
- Contributing and security policy files
- Stars and forks as lightweight community signals

The scoring model is documented in [docs/SCORING.md](docs/SCORING.md).

## Installation

### Install the verified release from GitHub

```bash
python -m pip install "git+https://github.com/ccwenkang-dotcom/oss-maintainer-readiness.git@v0.1.0"
```

### Install for local development

```bash
git clone https://github.com/ccwenkang-dotcom/oss-maintainer-readiness.git
cd oss-maintainer-readiness
python -m pip install -e ".[dev]"
```

Python 3.11 or later is required.

## Command-Line Usage

Check a local repository before publishing:

```bash
oss-readiness check --local . --out reports/self
```

Check a public GitHub repository without credentials:

```bash
oss-readiness check \
  --repo ccwenkang-dotcom/oss-maintainer-readiness \
  --out reports/oss-maintainer-readiness
```

Both commands write:

- `<out>.md` — human-readable findings
- `<out>.json` — machine-readable evidence and findings

A successful command means the reports were generated. It does not mean the repository received a green assessment.

## GitHub Action

The repository includes a composite action that can generate a report inside another repository's workflow.

```yaml
name: OSS readiness

on:
  workflow_dispatch:
  schedule:
    - cron: "0 8 1 * *"

jobs:
  assess:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ccwenkang-dotcom/oss-maintainer-readiness@v0.1.0
        with:
          repository: ${{ github.repository }}
          output: reports/oss-readiness
      - uses: actions/upload-artifact@v4
        with:
          name: oss-readiness-report
          path: reports/oss-readiness.*
```

Use `@main` only when intentionally testing unreleased changes.

## Report Statuses

- **Green** — core repository evidence is present and the score reaches the documented threshold.
- **Yellow** — the repository has a credible foundation but still has material maintenance gaps.
- **Red** — required evidence is missing, the repository is not publicly verifiable, or a hard gate fails.

Scores are evidence summaries, not quality guarantees. Review the individual findings before acting on a status.

## Privacy and Safety Boundaries

- No GitHub login or token is required.
- No private repository access is attempted.
- No form submission or browser automation is performed.
- No stars, downloads, users, issues, or contribution activity are fabricated.
- No external approval or eligibility outcome is guaranteed.
- A local blocklist can stop report generation when sensitive markers are detected.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m build
```

CI tests supported Python versions and verifies that source and wheel distributions can be built.

## Maintenance

The current primary maintainer is listed in [MAINTAINERS.md](MAINTAINERS.md). Planned work and release priorities are tracked in [ROADMAP.md](ROADMAP.md). The release process is documented in [docs/RELEASING.md](docs/RELEASING.md).

Bug reports and focused pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before opening a report.

## License

MIT License. See [LICENSE](LICENSE).
