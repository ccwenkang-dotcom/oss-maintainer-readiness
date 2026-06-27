import json

import pytest

from oss_maintainer_readiness.models import Assessment, Evidence, Finding
from oss_maintainer_readiness.report import render_json, render_markdown
from oss_maintainer_readiness.safety import SafetyViolation


def _assessment() -> Assessment:
    return Assessment(
        status="yellow",
        score=67,
        evidence=Evidence(
            owner="example",
            name="maintainer-toolkit",
            source="synthetic",
            repo_url="https://github.com/example/maintainer-toolkit",
            has_readme=True,
        ),
        findings=(
            Finding("strong", "readme_present", "README exists."),
            Finding("missing", "missing_tests", "Tests are missing."),
        ),
    )


def test_render_markdown_includes_status_and_sections():
    markdown = render_markdown(_assessment())

    assert "# OSS Maintainer Readiness Report" in markdown
    assert "**Status:** yellow" in markdown
    assert "## Strong Evidence" in markdown
    assert "## Missing Evidence" in markdown
    assert "missing_tests" in markdown


def test_render_json_is_parseable_and_stable():
    payload = json.loads(render_json(_assessment()))

    assert payload["status"] == "yellow"
    assert payload["score"] == 67
    assert payload["evidence"]["owner"] == "example"
    assert payload["findings"][0]["code"] == "readme_present"


def test_render_markdown_blocks_private_markers():
    assessment = Assessment(
        status="red",
        score=0,
        evidence=Evidence(owner="example", name="unsafe", source="synthetic"),
        findings=(Finding("unsafe", "leak", "Contains C:\\PRIVATE_PROJECT marker."),),
    )

    with pytest.raises(SafetyViolation):
        render_markdown(assessment)
