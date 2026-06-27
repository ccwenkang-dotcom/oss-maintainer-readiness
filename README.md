# OSS Maintainer Readiness Checker

A local-first command-line checker for open-source maintainer application evidence.

The tool inspects public GitHub repository metadata or a local repository path, scores the visible maintainer evidence, and writes Markdown plus JSON reports. It is designed for honest readiness checks before applying to maintainer-support programs.

## What It Checks

- Public repository visibility
- Original maintainer activity versus fork-only evidence
- README, license, tests, CI, releases, and recent maintenance
- Issue or pull request activity
- Contributing and security policy files
- Stars and forks as lightweight community signals

The checker is intentionally conservative: weak evidence is reported as weak.

## Boundaries

- No login
- No tokens
- No private repository access
- No form submission
- No browser automation
- No guarantee of external approval

## Install For Local Development

```bash
python -m pip install -e .[dev]
```

## Usage

Check a local repository before publishing:

```bash
python -m oss_maintainer_readiness.cli check --local . --out reports/self
```

Check a public GitHub repository without credentials:

```bash
python -m oss_maintainer_readiness.cli check --repo ccwenkang-dotcom/kohya_ss --out reports/kohya_ss
```

Both commands write:

- `<out>.md`
- `<out>.json`

## Development

```bash
python -m pytest -q
```

## Status

Version 0.1 is a local/no-live readiness tool. Publishing the repository or submitting any external application must be a separate operator decision.
