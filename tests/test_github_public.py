import json
from urllib.error import HTTPError

import pytest

from oss_maintainer_readiness.github_public import (
    GitHubPublicError,
    collect_public_github_evidence,
    evidence_from_repo_payload,
    parse_github_repo,
)


def test_parse_owner_repo_slug():
    assert parse_github_repo("example/maintainer-toolkit") == ("example", "maintainer-toolkit")


def test_parse_github_url():
    assert parse_github_repo("https://github.com/example/maintainer-toolkit") == (
        "example",
        "maintainer-toolkit",
    )


def test_rejects_invalid_repo_slug():
    with pytest.raises(GitHubPublicError):
        parse_github_repo("not-a-repo")


def test_maps_repo_payload_to_evidence():
    payload = {
        "name": "maintainer-toolkit",
        "full_name": "example/maintainer-toolkit",
        "html_url": "https://github.com/example/maintainer-toolkit",
        "private": False,
        "fork": False,
        "stargazers_count": 12,
        "forks_count": 3,
        "open_issues_count": 0,
        "pushed_at": "2026-06-20T00:00:00Z",
        "license": {"spdx_id": "MIT"},
    }

    evidence = evidence_from_repo_payload(
        payload,
        readme_exists=True,
        tests_exist=True,
        ci_exists=True,
        contributing_exists=True,
        security_policy_exists=True,
        release_count=1,
        issue_or_pr_activity_count=1,
    )

    assert evidence.owner == "example"
    assert evidence.name == "maintainer-toolkit"
    assert evidence.source == "github"
    assert evidence.has_readme is True
    assert evidence.has_license is True
    assert evidence.has_tests is True
    assert evidence.has_ci is True
    assert evidence.has_contributing is True
    assert evidence.has_security_policy is True
    assert evidence.has_releases is True
    assert evidence.has_issue_or_pr_activity is True
    assert evidence.stars == 12
    assert evidence.forks == 3


def test_repo_payload_falls_back_to_open_issue_count():
    payload = {
        "name": "maintainer-toolkit",
        "full_name": "example/maintainer-toolkit",
        "private": False,
        "open_issues_count": 1,
    }

    evidence = evidence_from_repo_payload(
        payload,
        readme_exists=False,
        ci_exists=False,
        release_count=0,
    )

    assert evidence.has_issue_or_pr_activity is True


def test_collect_public_github_evidence_maps_404(monkeypatch):
    def fake_json_get(url: str, timeout: float = 10.0):
        raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr("oss_maintainer_readiness.github_public._json_get", fake_json_get)

    evidence = collect_public_github_evidence("missing/repo")

    assert evidence.repo_exists is False
    assert evidence.is_public is False
    assert evidence.owner == "missing"
    assert evidence.name == "repo"


def test_collect_public_github_evidence_uses_public_api(monkeypatch):
    calls: list[str] = []

    def fake_json_get(url: str, timeout: float = 10.0):
        calls.append(url)
        if url.endswith("/repos/example/maintainer-toolkit"):
            return {
                "name": "maintainer-toolkit",
                "full_name": "example/maintainer-toolkit",
                "html_url": "https://github.com/example/maintainer-toolkit",
                "private": False,
                "fork": True,
                "stargazers_count": 0,
                "forks_count": 0,
                "open_issues_count": 0,
                "pushed_at": None,
                "license": None,
            }
        if url.endswith("/readme"):
            return {"name": "README.md"}
        if url.endswith("/contents/.github/workflows"):
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/contents/tests"):
            return [{"name": "test_example.py"}]
        if url.endswith("/contents/CONTRIBUTING.md"):
            return {"name": "CONTRIBUTING.md"}
        if url.endswith("/contents/.github/CONTRIBUTING.md"):
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/contents/SECURITY.md"):
            return {"name": "SECURITY.md"}
        if url.endswith("/contents/.github/SECURITY.md"):
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
        if url.endswith("/releases?per_page=1"):
            return []
        if url.endswith("/tags?per_page=1"):
            return [{"name": "v0.1.0"}]
        if url.endswith("/issues?state=all&per_page=1"):
            return [{"number": 7, "state": "closed", "pull_request": {}}]
        if url.endswith("/commits?author=example&per_page=100"):
            return [{"sha": "abc"}]
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr("oss_maintainer_readiness.github_public._json_get", fake_json_get)

    evidence = collect_public_github_evidence("example/maintainer-toolkit")

    assert evidence.has_readme is True
    assert evidence.has_tests is True
    assert evidence.is_fork is True
    assert evidence.original_commits == 1
    assert evidence.has_contributing is True
    assert evidence.has_security_policy is True
    assert evidence.has_releases is True
    assert evidence.has_issue_or_pr_activity is True
    assert all("token" not in json.dumps(call).lower() for call in calls)
