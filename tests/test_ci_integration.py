"""scripts/ci-knowledge-check.sh gates a desk on doctor, the store check and graph missing."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ci-knowledge-check.sh"
CLI = [sys.executable, "-m", "deskops"]


def _sandbox_desk(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    result = subprocess.run([*CLI, "init", str(repo)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr or result.stdout
    return repo


def _run_check(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["bash", str(SCRIPT), str(repo)], capture_output=True, text=True)


def test_ci_check_passes_on_a_fresh_desk(tmp_path: Path) -> None:
    result = _run_check(_sandbox_desk(tmp_path))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "No missing graph references found." in result.stdout


def test_ci_check_fails_on_a_dangling_source_atom(tmp_path: Path) -> None:
    repo = _sandbox_desk(tmp_path)
    guide = repo / "docs" / "guide.md"
    guide.parent.mkdir(parents=True)
    guide.write_text("# Guide\n\n```yaml\nsource_atoms:\n  - atom-missing\n```\n", encoding="utf-8")

    result = _run_check(repo)

    assert result.returncode != 0
    assert "dangling_source_atom_reference: doc:docs/guide.md -> atom:atom-missing" in result.stdout
    assert "FAILED: python -m deskops graph missing" in result.stderr
