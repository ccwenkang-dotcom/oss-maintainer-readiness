from __future__ import annotations

from .models import Assessment, Evidence, Finding


def _finding(level: str, code: str, message: str) -> Finding:
    return Finding(level=level, code=code, message=message)


def assess_evidence(evidence: Evidence) -> Assessment:
    findings: list[Finding] = []
    score = 0

    if not evidence.repo_exists:
        findings.append(_finding("missing", "repo_not_found", "Repository is not publicly visible."))
        return Assessment(status="red", score=0, evidence=evidence, findings=tuple(findings))

    if evidence.is_public:
        score += 10
        findings.append(_finding("strong", "repo_public", "Repository is publicly visible."))
    elif evidence.source == "local":
        score += 4
        findings.append(
            _finding(
                "weak",
                "local_preflight_not_public",
                "Local preflight can be scored, but public maintainer evidence still requires publication.",
            )
        )
    else:
        findings.append(_finding("missing", "repo_not_public", "Repository is not public."))
        return Assessment(status="red", score=0, evidence=evidence, findings=tuple(findings))

    if evidence.is_fork:
        if evidence.original_commits >= 5:
            score += 8
            findings.append(
                _finding("weak", "fork_some_original_activity", "Fork has some original activity.")
            )
        else:
            score -= 20
            findings.append(
                _finding(
                    "weak",
                    "fork_weak_original_activity",
                    "Repository is mainly a fork with limited original maintainer evidence.",
                )
            )
    else:
        score += 18
        findings.append(_finding("strong", "repo_owned_original_work", "Repository is original owned work."))

    score += _boolean_signal(findings, evidence.has_readme, 10, "readme_present", "missing_readme", "README exists.")
    score += _boolean_signal(findings, evidence.has_license, 10, "license_present", "missing_license", "License exists.")
    score += _boolean_signal(findings, evidence.has_tests, 12, "tests_present", "missing_tests", "Tests are present.")
    score += _boolean_signal(findings, evidence.has_ci, 8, "ci_present", "missing_ci", "CI workflow is present.")
    score += _boolean_signal(
        findings,
        evidence.has_recent_commits,
        8,
        "recent_commits_present",
        "missing_recent_commits",
        "Recent commit activity exists.",
    )
    score += _boolean_signal(findings, evidence.has_releases, 8, "releases_present", "missing_releases", "Releases or tags exist.")
    score += _boolean_signal(
        findings,
        evidence.has_issue_or_pr_activity,
        8,
        "issue_or_pr_activity_present",
        "missing_issue_or_pr_activity",
        "Issue or pull request activity exists.",
    )
    score += _boolean_signal(
        findings,
        evidence.has_contributing,
        5,
        "contributing_present",
        "missing_contributing",
        "Contributing guide exists.",
    )
    score += _boolean_signal(
        findings,
        evidence.has_security_policy,
        5,
        "security_policy_present",
        "missing_security_policy",
        "Security policy exists.",
    )

    if evidence.stars > 0 or evidence.forks > 0:
        score += min(12, evidence.stars // 2 + evidence.forks * 2 + 4)
        findings.append(_finding("strong", "community_signal_present", "Stars or forks provide community signal."))
    else:
        findings.append(_finding("weak", "missing_community_signal", "No stars or forks are visible yet."))

    for warning in evidence.warnings:
        findings.append(_finding("weak", "collector_warning", warning))

    score = max(0, min(100, score))
    missing_codes = {finding.code for finding in findings if finding.level == "missing"}

    if not evidence.has_readme or not evidence.has_license or not evidence.has_tests:
        status = "red"
    elif evidence.is_fork and evidence.original_commits < 5:
        status = "red"
    elif score >= 80 and not missing_codes:
        status = "green"
    elif score >= 55:
        status = "yellow"
    else:
        status = "red"

    return Assessment(status=status, score=score, evidence=evidence, findings=tuple(findings))


def _boolean_signal(
    findings: list[Finding],
    present: bool,
    points: int,
    present_code: str,
    missing_code: str,
    present_message: str,
) -> int:
    if present:
        findings.append(_finding("strong", present_code, present_message))
        return points
    findings.append(_finding("missing", missing_code, present_message.replace("exists", "is missing").replace("are present", "are missing")))
    return 0
