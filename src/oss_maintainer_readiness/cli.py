from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .github_public import GitHubPublicError, collect_public_github_evidence
from .local_repo import LocalRepositoryError, collect_local_evidence
from .report import render_json, render_markdown
from .rules import assess_evidence
from .safety import SafetyViolation, load_blocked_markers_file

DEFAULT_BLOCKLIST = ".oss-readiness-blocklist.local"


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    if args.command == "check":
        return _check(args)
    parser.print_help()
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="oss-readiness")
    subparsers = parser.add_subparsers(dest="command")
    check = subparsers.add_parser("check", help="Check OSS maintainer readiness evidence.")
    source = check.add_mutually_exclusive_group(required=True)
    source.add_argument("--repo", help="Public GitHub repository as owner/repo or URL.")
    source.add_argument("--local", help="Local repository path to inspect.")
    check.add_argument("--out", required=True, help="Output path stem. Writes .md and .json.")
    return parser


def _check(args: argparse.Namespace) -> int:
    try:
        if args.local:
            evidence = collect_local_evidence(args.local)
        else:
            evidence = collect_public_github_evidence(args.repo)
        assessment = assess_evidence(evidence)
        extra_markers = load_blocked_markers_file(DEFAULT_BLOCKLIST)
        markdown = render_markdown(assessment, extra_markers=extra_markers)
        json_payload = render_json(assessment, extra_markers=extra_markers)
        _write_reports(Path(args.out), markdown, json_payload)
    except (GitHubPublicError, LocalRepositoryError, SafetyViolation) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


def _write_reports(out_stem: Path, markdown: str, json_payload: str) -> None:
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    out_stem.with_suffix(".md").write_text(markdown, encoding="utf-8", newline="\n")
    out_stem.with_suffix(".json").write_text(json_payload, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    raise SystemExit(main())
