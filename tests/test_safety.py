import pytest

from oss_maintainer_readiness.safety import (
    SafetyViolation,
    assert_safe_text,
    find_blocked_markers,
    load_blocked_markers_file,
)


def test_allows_public_synthetic_text():
    assert_safe_text("public repo report for example/example")


def test_reports_all_blocked_markers_found():
    markers = find_blocked_markers("OPENAI_API_KEY in a C:\\PRIVATE_PROJECT path")

    assert markers == ["C:\\PRIVATE_PROJECT", "OPENAI_API_KEY"]


def test_blocks_private_path_marker():
    with pytest.raises(SafetyViolation) as excinfo:
        assert_safe_text("accidental C:\\PRIVATE_PROJECT path")

    assert "C:\\PRIVATE_PROJECT" in str(excinfo.value)


def test_blocks_private_project_marker():
    with pytest.raises(SafetyViolation):
        assert_safe_text("contains PRIVATE_PROJECT_MARKER marker")


def test_blocks_secret_marker():
    with pytest.raises(SafetyViolation):
        assert_safe_text("OPENAI_API_KEY=secret")


def test_loads_local_blocked_marker_file(tmp_path):
    blocklist = tmp_path / "blocklist.local"
    blocklist.write_text("# local only\nPRIVATE_LOCAL_NAME\n\n", encoding="utf-8")

    assert load_blocked_markers_file(blocklist) == ("PRIVATE_LOCAL_NAME",)
