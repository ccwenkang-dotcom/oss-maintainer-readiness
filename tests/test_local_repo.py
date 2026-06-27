from pathlib import Path

import pytest

from oss_maintainer_readiness.local_repo import LocalRepositoryError, collect_local_evidence


def test_collects_foundational_local_repo_signals(tmp_path: Path):
    repo = tmp_path / "maintainer-toolkit"
    repo.mkdir()
    (repo / "README.md").write_text("# Maintainer Toolkit\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (repo / "CONTRIBUTING.md").write_text("Contribute here.\n", encoding="utf-8")
    (repo / "SECURITY.md").write_text("Report issues.\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_example.py").write_text("def test_example():\n    assert True\n", encoding="utf-8")
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text("## 0.1.0\n", encoding="utf-8")

    evidence = collect_local_evidence(repo)

    assert evidence.owner == "local"
    assert evidence.name == "maintainer-toolkit"
    assert evidence.source == "local"
    assert evidence.has_readme is True
    assert evidence.has_license is True
    assert evidence.has_tests is True
    assert evidence.has_ci is True
    assert evidence.has_contributing is True
    assert evidence.has_security_policy is True
    assert evidence.has_releases is True


def test_missing_local_path_raises_clear_error(tmp_path: Path):
    with pytest.raises(LocalRepositoryError) as excinfo:
        collect_local_evidence(tmp_path / "missing")

    assert "does not exist" in str(excinfo.value)
