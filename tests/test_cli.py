import json
from pathlib import Path

from oss_maintainer_readiness.cli import main


def test_cli_writes_local_markdown_and_json_reports(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Repo\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_repo.py").write_text("def test_repo():\n    assert True\n", encoding="utf-8")
    out = tmp_path / "reports" / "repo"

    code = main(["check", "--local", str(repo), "--out", str(out)])

    assert code == 0
    assert (tmp_path / "reports" / "repo.md").exists()
    assert (tmp_path / "reports" / "repo.json").exists()
    payload = json.loads((tmp_path / "reports" / "repo.json").read_text(encoding="utf-8"))
    assert payload["evidence"]["name"] == "repo"


def test_cli_requires_one_input_source(tmp_path: Path):
    code = main(["check", "--out", str(tmp_path / "report")])

    assert code == 2


def test_cli_returns_nonzero_for_missing_local_path(tmp_path: Path):
    code = main(["check", "--local", str(tmp_path / "missing"), "--out", str(tmp_path / "report")])

    assert code == 1


def test_cli_uses_ignored_local_blocklist(tmp_path: Path, monkeypatch):
    repo = tmp_path / "PRIVATE_LOCAL_NAME"
    repo.mkdir()
    (repo / "README.md").write_text("# Repo\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_repo.py").write_text("def test_repo():\n    assert True\n", encoding="utf-8")
    (tmp_path / ".oss-readiness-blocklist.local").write_text("PRIVATE_LOCAL_NAME\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    code = main(["check", "--local", str(repo), "--out", str(tmp_path / "report")])

    assert code == 1
    assert not (tmp_path / "report.md").exists()
