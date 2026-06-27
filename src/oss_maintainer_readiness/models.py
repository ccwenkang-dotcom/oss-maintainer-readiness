from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Evidence:
    owner: str
    name: str
    source: str
    repo_url: str | None = None
    repo_exists: bool = True
    is_public: bool = True
    is_fork: bool = False
    original_commits: int = 0
    has_readme: bool = False
    has_license: bool = False
    has_tests: bool = False
    has_ci: bool = False
    has_recent_commits: bool = False
    has_releases: bool = False
    has_issue_or_pr_activity: bool = False
    has_contributing: bool = False
    has_security_policy: bool = False
    stars: int = 0
    forks: int = 0
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class Assessment:
    status: str
    score: int
    evidence: Evidence
    findings: tuple[Finding, ...] = field(default_factory=tuple)

    def grouped_findings(self) -> dict[str, list[Finding]]:
        groups: dict[str, list[Finding]] = {"strong": [], "weak": [], "missing": [], "unsafe": []}
        for finding in self.findings:
            groups.setdefault(finding.level, []).append(finding)
        return groups

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "score": self.score,
            "evidence": self.evidence.to_dict(),
            "findings": [finding.to_dict() for finding in self.findings],
        }
