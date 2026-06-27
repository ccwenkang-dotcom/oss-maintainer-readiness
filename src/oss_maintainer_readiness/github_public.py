from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .models import Evidence

API_ROOT = "https://api.github.com"


class GitHubPublicError(ValueError):
    """Raised when a public GitHub repository reference is invalid."""


def parse_github_repo(value: str) -> tuple[str, str]:
    candidate = value.strip().rstrip("/")
    if candidate.startswith("https://github.com/"):
        parsed = urlparse(candidate)
        parts = [part for part in parsed.path.split("/") if part]
    else:
        parts = [part for part in candidate.split("/") if part]
    if len(parts) < 2:
        raise GitHubPublicError(f"expected GitHub repository as owner/repo or URL, got: {value}")
    owner, repo = parts[0], parts[1]
    if not owner or not repo or repo.endswith(".git"):
        repo = repo.removesuffix(".git")
    if not owner or not repo:
        raise GitHubPublicError(f"invalid GitHub repository reference: {value}")
    return owner, repo


def collect_public_github_evidence(repo_ref: str, timeout: float = 10.0) -> Evidence:
    owner, repo = parse_github_repo(repo_ref)
    repo_url = f"{API_ROOT}/repos/{owner}/{repo}"
    try:
        payload = _json_get(repo_url, timeout=timeout)
    except HTTPError as exc:
        if exc.code == 404:
            return Evidence(
                owner=owner,
                name=repo,
                source="github",
                repo_url=f"https://github.com/{owner}/{repo}",
                repo_exists=False,
                is_public=False,
                warnings=("GitHub returned 404 for the repository.",),
            )
        if exc.code in {403, 429}:
            return Evidence(
                owner=owner,
                name=repo,
                source="github",
                repo_url=f"https://github.com/{owner}/{repo}",
                warnings=(f"GitHub API rate limit or access response: HTTP {exc.code}.",),
            )
        raise
    except URLError as exc:
        return Evidence(
            owner=owner,
            name=repo,
            source="github",
            repo_url=f"https://github.com/{owner}/{repo}",
            warnings=(f"GitHub API request failed: {exc.reason}.",),
        )

    readme_exists = _exists(f"{repo_url}/readme", timeout)
    ci_exists = _exists(f"{repo_url}/contents/.github/workflows", timeout)
    release_count = _count_list(f"{repo_url}/releases?per_page=1", timeout)
    original_commits = _count_list(f"{repo_url}/commits?author={owner}&per_page=100", timeout)
    return evidence_from_repo_payload(
        payload,
        readme_exists=readme_exists,
        ci_exists=ci_exists,
        release_count=release_count,
        original_commits=original_commits,
    )


def evidence_from_repo_payload(
    payload: dict[str, Any],
    *,
    readme_exists: bool,
    ci_exists: bool,
    release_count: int,
    original_commits: int = 0,
) -> Evidence:
    full_name = str(payload.get("full_name", "unknown/unknown"))
    owner, name = full_name.split("/", 1) if "/" in full_name else ("unknown", str(payload.get("name", "unknown")))
    license_payload = payload.get("license")
    pushed_at = payload.get("pushed_at")
    open_issues = int(payload.get("open_issues_count") or 0)
    stars = int(payload.get("stargazers_count") or 0)
    forks = int(payload.get("forks_count") or 0)
    return Evidence(
        owner=owner,
        name=name,
        source="github",
        repo_url=str(payload.get("html_url") or f"https://github.com/{owner}/{name}"),
        repo_exists=True,
        is_public=not bool(payload.get("private")),
        is_fork=bool(payload.get("fork")),
        original_commits=original_commits,
        has_readme=readme_exists,
        has_license=bool(license_payload),
        has_tests=False,
        has_ci=ci_exists,
        has_recent_commits=_is_recent_iso8601(pushed_at),
        has_releases=release_count > 0,
        has_issue_or_pr_activity=open_issues > 0,
        has_contributing=False,
        has_security_policy=False,
        stars=stars,
        forks=forks,
    )


def _json_get(url: str, timeout: float = 10.0) -> Any:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "oss-maintainer-readiness/0.1",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _exists(url: str, timeout: float) -> bool:
    try:
        _json_get(url, timeout)
        return True
    except HTTPError as exc:
        if exc.code == 404:
            return False
        return False
    except URLError:
        return False


def _count_list(url: str, timeout: float) -> int:
    try:
        payload = _json_get(url, timeout)
    except (HTTPError, URLError):
        return 0
    if isinstance(payload, list):
        return len(payload)
    return 0


def _is_recent_iso8601(value: Any) -> bool:
    if not value:
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    age_days = (datetime.now(timezone.utc) - parsed).days
    return age_days <= 365
