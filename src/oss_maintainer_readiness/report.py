from __future__ import annotations

import json

from .models import Assessment, Finding
from .safety import assert_safe_text


SECTION_TITLES = {
    "strong": "Strong Evidence",
    "weak": "Weak Evidence",
    "missing": "Missing Evidence",
    "unsafe": "Unsafe Evidence",
}


def render_markdown(assessment: Assessment, extra_markers: tuple[str, ...] = ()) -> str:
    evidence = assessment.evidence
    lines = [
        "# OSS Maintainer Readiness Report",
        "",
        f"**Repository:** `{evidence.owner}/{evidence.name}`",
        f"**Source:** {evidence.source}",
        f"**Status:** {assessment.status}",
        f"**Score:** {assessment.score}/100",
        "",
    ]
    if evidence.repo_url:
        lines.extend([f"**URL:** {evidence.repo_url}", ""])
    if evidence.warnings:
        lines.extend(["## Collector Warnings", ""])
        for warning in evidence.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    groups = assessment.grouped_findings()
    for level in ("strong", "weak", "missing", "unsafe"):
        findings = groups.get(level, [])
        lines.extend([f"## {SECTION_TITLES[level]}", ""])
        if findings:
            lines.extend(_finding_lines(findings))
        else:
            lines.append("- None.")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    assert_safe_text(text, extra_markers=extra_markers)
    return text


def render_json(assessment: Assessment, extra_markers: tuple[str, ...] = ()) -> str:
    text = json.dumps(assessment.to_dict(), indent=2, sort_keys=True)
    assert_safe_text(text, extra_markers=extra_markers)
    return text + "\n"


def _finding_lines(findings: list[Finding]) -> list[str]:
    return [f"- `{finding.code}`: {finding.message}" for finding in findings]
