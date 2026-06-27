from __future__ import annotations

from pathlib import Path

from .models import Evidence


class LocalRepositoryError(ValueError):
    """Raised when a local repository path cannot be inspected."""


def collect_local_evidence(path: str | Path) -> Evidence:
    repo = Path(path).resolve()
    if not repo.exists():
        raise LocalRepositoryError(f"local repository path does not exist: {repo}")
    if not repo.is_dir():
        raise LocalRepositoryError(f"local repository path is not a directory: {repo}")

    return Evidence(
        owner="local",
        name=repo.name,
        source="local",
        repo_url=None,
        repo_exists=True,
        is_public=False,
        is_fork=False,
        original_commits=_count_local_commits(repo),
        has_readme=_has_any(repo, ("README.md", "README.rst", "README.txt")),
        has_license=_has_any(repo, ("LICENSE", "LICENSE.md", "COPYING")),
        has_tests=_has_tests(repo),
        has_ci=_has_ci(repo),
        has_recent_commits=_has_git_directory(repo),
        has_releases=_has_any(repo, ("CHANGELOG.md", "RELEASES.md")) or _has_git_tags(repo),
        has_issue_or_pr_activity=_has_any(repo, (".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE.md")),
        has_contributing=_has_any(repo, ("CONTRIBUTING.md", ".github/CONTRIBUTING.md")),
        has_security_policy=_has_any(repo, ("SECURITY.md", ".github/SECURITY.md")),
    )


def _has_any(repo: Path, relative_paths: tuple[str, ...]) -> bool:
    return any((repo / relative_path).exists() for relative_path in relative_paths)


def _has_tests(repo: Path) -> bool:
    if (repo / "tests").is_dir():
        return any((repo / "tests").rglob("test_*.py"))
    return any(repo.glob("test_*.py"))


def _has_ci(repo: Path) -> bool:
    workflows = repo / ".github" / "workflows"
    return workflows.is_dir() and any(path.suffix.lower() in {".yml", ".yaml"} for path in workflows.iterdir())


def _has_git_directory(repo: Path) -> bool:
    return (repo / ".git").exists()


def _has_git_tags(repo: Path) -> bool:
    tag_dir = repo / ".git" / "refs" / "tags"
    return tag_dir.is_dir() and any(tag_dir.iterdir())


def _count_local_commits(repo: Path) -> int:
    head = repo / ".git" / "HEAD"
    return 1 if head.exists() else 0
