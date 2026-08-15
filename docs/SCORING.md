# Scoring Model

The checker summarizes visible repository evidence. The score is deterministic and intentionally conservative; it is not an endorsement, security audit, or eligibility decision for any external program.

## Evidence Weights

For a public, original repository, the current model can award:

| Signal | Points |
| --- | ---: |
| Public repository | 10 |
| Original owned work | 18 |
| README | 10 |
| Open-source license | 10 |
| Tests | 12 |
| CI workflow | 8 |
| Recent commits | 8 |
| Releases or tags | 8 |
| Issue or pull-request activity | 8 |
| Contributing guide | 5 |
| Security policy | 5 |
| Community signals | Up to 12 |

The final score is clamped to the range 0–100.

Community points are deliberately lightweight. Stars and forks are useful context, but they are not treated as proof of code quality, security, or sustainable maintenance.

## Fork Handling

A fork with at least five original commits receives limited credit for original activity. A fork with fewer than five original commits receives a penalty and cannot receive a green status. This reduces the risk of presenting upstream popularity as evidence of the fork owner's maintenance work.

## Status Gates

### Green

A repository can be green only when:

- the score is at least 80;
- no required signal is missing; and
- no hard gate fails.

### Yellow

A repository is yellow when it has a credible foundation and a score of at least 55, but still has material gaps.

### Red

A repository is red when any of the following applies:

- it is not publicly verifiable;
- README, license, or tests are missing;
- it is primarily a fork with insufficient original activity;
- the score is below 55; or
- evidence collection fails closed.

## Collection Limits

Public GitHub checks use unauthenticated public endpoints. Rate limits, API availability, renamed files, nonstandard repository layouts, and incomplete metadata can produce warnings or conservative findings.

Local checks can inspect repository files but cannot prove public adoption, public issue handling, release history, or community usage. A local report should therefore be treated as preflight evidence only.

## Interpretation

Use the report to identify concrete maintenance work, not to optimize a number in isolation. A healthy next step is usually to fix the underlying gap—for example, publish a real release, document a real security process, or respond to genuine user issues—rather than manufacture a signal.
