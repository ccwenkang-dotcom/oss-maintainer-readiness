from __future__ import annotations

from pathlib import Path

BLOCKED_MARKERS: tuple[str, ...] = (
    "C:\\PRIVATE_PROJECT",
    "PRIVATE_PROJECT_MARKER",
    "PRIVATE_KEY",
    "OPENAI_API_KEY",
    "GITHUB_TOKEN",
    "BEGIN RSA PRIVATE KEY",
)


class SafetyViolation(ValueError):
    """Raised when generated output contains private or secret markers."""


def load_blocked_markers_file(path: str | Path) -> tuple[str, ...]:
    marker_path = Path(path)
    if not marker_path.exists():
        return ()
    markers: list[str] = []
    for line in marker_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        markers.append(stripped)
    return tuple(markers)


def find_blocked_markers(text: str, extra_markers: tuple[str, ...] = ()) -> list[str]:
    blocked_markers = BLOCKED_MARKERS + extra_markers
    matches: list[str] = []
    for marker in sorted(blocked_markers, key=len, reverse=True):
        if marker not in text:
            continue
        if any(marker in existing for existing in matches):
            continue
        matches.append(marker)
    return sorted(matches, key=blocked_markers.index)


def assert_safe_text(text: str, extra_markers: tuple[str, ...] = ()) -> None:
    markers = find_blocked_markers(text, extra_markers=extra_markers)
    if markers:
        joined = ", ".join(markers)
        raise SafetyViolation(f"blocked private or secret marker found: {joined}")
