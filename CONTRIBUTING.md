# Contributing

Contributions should keep the project local-first, credential-free, and conservative.

## Development Flow

1. Write or update a focused test first.
2. Run the test and confirm it fails for the expected reason.
3. Implement the smallest change that makes the test pass.
4. Run `python -m pytest -q`.
5. Keep reports honest: weak evidence must stay weak.

## Scope Rules

- Do not add login, token, OAuth, or private repository access without a separate security design.
- Do not add automatic application submission.
- Do not claim external approval is guaranteed.
- Do not include private project material in examples or reports.
