# Maintainers

## Primary Maintainer

- [@ccwenkang-dotcom](https://github.com/ccwenkang-dotcom)

The primary maintainer currently owns repository direction, issue triage, pull-request review, release management, security coordination, and compatibility decisions.

## Maintenance Principles

- Public claims must be supported by public evidence.
- Missing evidence is reported conservatively rather than inferred.
- Scoring changes require tests and documentation.
- Security-sensitive reports follow `SECURITY.md` rather than public issue discussion.
- Releases follow `docs/RELEASING.md` and include user-visible changelog entries.
- Automation must not fabricate stars, downloads, users, issues, pull requests, or adoption signals.

## Decision Process

Small fixes may be merged after tests and review. Changes to scoring semantics, report schemas, safety boundaries, or command-line compatibility should be proposed in an issue or pull request with:

1. the maintenance problem being solved;
2. the evidence source and its limitations;
3. expected user impact;
4. tests for changed behavior; and
5. migration notes when compatibility changes.

Additional maintainers may be added after sustained, reviewable contributions and agreement on the project's evidence-first principles.
