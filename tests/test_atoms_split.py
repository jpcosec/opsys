from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main


SECTIONED_ATOM = """---
id: atom-splittable-guidance
title: Splittable Guidance
five_wh_one_plus: how
tags:
- system:deskops
- topic:atoms
provenance: docs/source-guidance.md
---

# Splittable Guidance

## Answer

### Rerouting

Preserve downstream resolution by keeping a redirect stub.

### Validation

Block mutation when inbound references are still present.
"""


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def _write_sectioned_atom(root: Path) -> Path:
    source = root / "docs" / "source-guidance.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("Source guidance.\n", encoding="utf-8")

    atom_path = root / "desk" / "atoms" / "atom-splittable-guidance.md"
    atom_path.write_text(SECTIONED_ATOM, encoding="utf-8")
    return atom_path


def test_atoms_split_supports_explicit_section_assignment_and_keeps_redirect_stub(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    source_path = _write_sectioned_atom(tmp_path)

    result = main(
        [
            "atoms",
            "split",
            "atom-splittable-guidance",
            "--into",
            "atom-validation-guidance",
            "atom-rerouting-guidance",
            "--section",
            "atom-rerouting-guidance:Rerouting",
            "--section",
            "atom-validation-guidance:Validation",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 0
    assert "Split atom atom-splittable-guidance" in captured.out
    assert "Original kept as redirect stub: yes" in captured.out

    rerouting = (tmp_path / "desk" / "atoms" / "atom-rerouting-guidance.md").read_text(encoding="utf-8")
    validation = (tmp_path / "desk" / "atoms" / "atom-validation-guidance.md").read_text(encoding="utf-8")
    redirect = source_path.read_text(encoding="utf-8")

    assert "title: Splittable Guidance — Rerouting" in rerouting
    assert "Preserve downstream resolution by keeping a redirect stub." in rerouting
    assert "provenance: docs/source-guidance.md" in rerouting
    assert "### Rerouting" not in rerouting

    assert "title: Splittable Guidance — Validation" in validation
    assert "Block mutation when inbound references are still present." in validation
    assert "provenance: docs/source-guidance.md" in validation
    assert "### Validation" not in validation

    assert "This atom has been split." in redirect
    assert "atom:atom-rerouting-guidance" in redirect
    assert "atom:atom-validation-guidance" in redirect
    assert "The original atom is intentionally kept as a redirect stub" in redirect


def test_atoms_split_blocks_when_inbound_references_exist_without_force(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    source_path = _write_sectioned_atom(tmp_path)
    original_text = source_path.read_text(encoding="utf-8")

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nDepends on atom:atom-splittable-guidance today.\n",
        encoding="utf-8",
    )

    result = main(
        [
            "atoms",
            "split",
            "atom-splittable-guidance",
            "--into",
            "atom-rerouting-guidance",
            "atom-validation-guidance",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 1
    assert "Refusing to split atom-splittable-guidance" in captured.out
    assert "desk/tasks/task-ref.md:3" in captured.out
    assert source_path.read_text(encoding="utf-8") == original_text
    assert not (tmp_path / "desk" / "atoms" / "atom-rerouting-guidance.md").exists()
    assert not (tmp_path / "desk" / "atoms" / "atom-validation-guidance.md").exists()


def test_atoms_split_force_uses_heading_order_defaults_and_reports_acknowledged_refs(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _write_sectioned_atom(tmp_path)

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nDepends on atom:atom-splittable-guidance today.\n",
        encoding="utf-8",
    )

    result = main(
        [
            "atoms",
            "split",
            "atom-splittable-guidance",
            "--into",
            "atom-rerouting-guidance",
            "atom-validation-guidance",
            "--force",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 0
    assert "Inbound references acknowledged:" in captured.out
    assert "desk/tasks/task-ref.md:3" in captured.out

    rerouting = (tmp_path / "desk" / "atoms" / "atom-rerouting-guidance.md").read_text(encoding="utf-8")
    validation = (tmp_path / "desk" / "atoms" / "atom-validation-guidance.md").read_text(encoding="utf-8")

    assert "title: Splittable Guidance — Rerouting" in rerouting
    assert "title: Splittable Guidance — Validation" in validation
    assert "atom:atom-splittable-guidance" in task_path.read_text(encoding="utf-8")
