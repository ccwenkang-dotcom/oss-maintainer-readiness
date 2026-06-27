from oss_maintainer_readiness.models import Evidence
from oss_maintainer_readiness.rules import assess_evidence


def test_strong_repository_is_green():
    evidence = Evidence(
        owner="example",
        name="maintainer-toolkit",
        source="synthetic",
        repo_url="https://github.com/example/maintainer-toolkit",
        is_fork=False,
        original_commits=30,
        has_readme=True,
        has_license=True,
        has_tests=True,
        has_ci=True,
        has_recent_commits=True,
        has_releases=True,
        has_issue_or_pr_activity=True,
        has_contributing=True,
        has_security_policy=True,
        stars=25,
        forks=4,
    )

    assessment = assess_evidence(evidence)

    assert assessment.status == "green"
    assert assessment.score >= 80
    assert any(finding.code == "repo_owned_original_work" for finding in assessment.findings)


def test_fork_only_repository_with_weak_evidence_is_red():
    evidence = Evidence(
        owner="ccwenkang-dotcom",
        name="kohya_ss",
        source="github",
        repo_url="https://github.com/ccwenkang-dotcom/kohya_ss",
        is_fork=True,
        original_commits=1,
        has_readme=True,
        has_license=True,
        has_tests=False,
        has_ci=False,
        has_recent_commits=False,
        has_releases=False,
        has_issue_or_pr_activity=False,
        stars=0,
        forks=0,
    )

    assessment = assess_evidence(evidence)

    assert assessment.status == "red"
    assert any(finding.code == "fork_weak_original_activity" for finding in assessment.findings)
    assert any(finding.code == "missing_tests" for finding in assessment.findings)


def test_missing_foundational_files_caps_status_at_red():
    evidence = Evidence(
        owner="example",
        name="empty",
        source="synthetic",
        has_readme=False,
        has_license=False,
        has_tests=False,
        has_ci=False,
    )

    assessment = assess_evidence(evidence)

    assert assessment.status == "red"
    codes = {finding.code for finding in assessment.findings}
    assert {"missing_readme", "missing_license", "missing_tests"}.issubset(codes)


def test_not_found_repository_is_red():
    evidence = Evidence(
        owner="missing",
        name="repo",
        source="github",
        repo_exists=False,
        is_public=False,
    )

    assessment = assess_evidence(evidence)

    assert assessment.status == "red"
    assert assessment.score == 0
    assert any(finding.code == "repo_not_found" for finding in assessment.findings)


def test_local_preflight_is_scored_even_before_publication():
    evidence = Evidence(
        owner="local",
        name="oss-maintainer-readiness",
        source="local",
        repo_exists=True,
        is_public=False,
        is_fork=False,
        original_commits=8,
        has_readme=True,
        has_license=True,
        has_tests=True,
        has_ci=True,
        has_recent_commits=True,
        has_releases=True,
        has_contributing=True,
        has_security_policy=True,
    )

    assessment = assess_evidence(evidence)

    assert assessment.status in {"yellow", "green"}
    assert any(finding.code == "local_preflight_not_public" for finding in assessment.findings)
