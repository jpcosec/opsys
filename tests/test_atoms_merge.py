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


SOURCE_ATOM = """---
id: atom-source-guidance
title: Source Guidance
five_wh_one_plus: how
tags:
- system:deskops
- topic:merge
- topic:source
provenance: docs/source-guidance.md
---

# Source Guidance

## Answer

Prefer explicit redirects during knowledge refactors.
"""


TARGET_ATOM = """---
id: atom-target-guidance
title: Target Guidance
five_wh_one_plus: how
tags:
- system:deskops
- topic:merge
- topic:target
provenance: docs/target-guidance.md
---

# Target Guidance

## Answer

Keep canonical guidance on the surviving atom.
"""


MISMATCHED_TARGET_ATOM = """---
id: atom-target-guidance
title: Target Guidance
five_wh_one_plus: why
tags:
- system:deskops
- topic:merge
provenance: docs/target-guidance.md
---

# Target Guidance

## Answer

Why this guidance exists matters.
"""


DEDUPE_TARGET_ATOM = """---
id: atom-target-guidance
title: Target Guidance
five_wh_one_plus: how
tags:
- system:deskops
- topic:merge
provenance: docs/target-guidance.md
---

# Target Guidance

## Answer

Keep canonical guidance on the surviving atom.

Prefer explicit redirects during knowledge refactors.
"""


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def _write_atoms(root: Path, *, source_text: str = SOURCE_ATOM, target_text: str = TARGET_ATOM) -> tuple[Path, Path]:
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "source-guidance.md").write_text("Source guidance.\n", encoding="utf-8")
    (docs_dir / "target-guidance.md").write_text("Target guidance.\n", encoding="utf-8")

    source_path = root / "desk" / "atoms" / "atom-source-guidance.md"
    source_path.write_text(source_text, encoding="utf-8")

    target_path = root / "desk" / "atoms" / "atom-target-guidance.md"
    target_path.write_text(target_text, encoding="utf-8")
    return source_path, target_path


def test_atoms_merge_rewrites_inbound_refs_and_preserves_traceability(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    source_path, target_path = _write_atoms(tmp_path)

    task_path = tmp_path / "desk" / "tasks" / "task-ref.md"
    task_path.write_text(
        "# Ref\n\nDepends on atom:atom-source-guidance today.\n",
        encoding="utf-8",
    )

    result = main(
        [
            "atoms",
            "merge",
            "atom-source-guidance",
            "--into",
            "atom-target-guidance",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 0
    assert "Merged atom atom-source-guidance into atom-target-guidance" in captured.out
    assert "Source kept as redirect stub: yes" in captured.out
    assert "Inbound references rewritten: 1" in captured.out
    assert "desk/tasks/task-ref.md:3" in captured.out

    source_text = source_path.read_text(encoding="utf-8")
    target_text = target_path.read_text(encoding="utf-8")
    task_text = task_path.read_text(encoding="utf-8")

    assert "atom:atom-target-guidance" in task_text
    assert "atom:atom-source-guidance" not in task_text

    assert "topic:target" in target_text
    assert "topic:source" in target_text
    assert target_text.count("topic:merge") == 1
    assert "Keep canonical guidance on the surviving atom." in target_text
    assert "### Merged from atom:atom-source-guidance" in target_text
    assert "Original provenance: `docs/source-guidance.md`" in target_text
    assert "Prefer explicit redirects during knowledge refactors." in target_text

    assert "This atom has been merged into atom:atom-target-guidance." in source_text
    assert "redirect stub" in source_text


def test_atoms_merge_blocks_question_conflicts_without_force(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    source_path, target_path = _write_atoms(tmp_path, target_text=MISMATCHED_TARGET_ATOM)
    original_source = source_path.read_text(encoding="utf-8")
    original_target = target_path.read_text(encoding="utf-8")

    result = main(
        [
            "atoms",
            "merge",
            "atom-source-guidance",
            "--into",
            "atom-target-guidance",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 1
    assert "Refusing to merge atom-source-guidance into atom-target-guidance" in captured.out
    assert "five_wh_one_plus conflict (how vs why)" in captured.out
    assert source_path.read_text(encoding="utf-8") == original_source
    assert target_path.read_text(encoding="utf-8") == original_target


def test_atoms_merge_force_allows_conflict_and_records_acknowledged_ambiguity(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    source_path, target_path = _write_atoms(tmp_path, target_text=MISMATCHED_TARGET_ATOM)

    result = main(
        [
            "atoms",
            "merge",
            "atom-source-guidance",
            "--into",
            "atom-target-guidance",
            "--force",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 0
    assert "Merge ambiguities acknowledged:" in captured.out
    assert "five_wh_one_plus conflict (how vs why)" in captured.out
    assert "### Merged from atom:atom-source-guidance" in target_path.read_text(encoding="utf-8")
    assert "This atom has been merged into atom:atom-target-guidance." in source_path.read_text(encoding="utf-8")


def test_atoms_merge_dedupes_source_answer_when_target_already_contains_it(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _write_atoms(tmp_path, target_text=DEDUPE_TARGET_ATOM)

    result = main(
        [
            "atoms",
            "merge",
            "atom-source-guidance",
            "--into",
            "atom-target-guidance",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert result == 0
    target_text = (tmp_path / "desk" / "atoms" / "atom-target-guidance.md").read_text(encoding="utf-8")
    assert target_text.count("Prefer explicit redirects during knowledge refactors.") == 1
    assert "### Merged from atom:atom-source-guidance" not in target_text
    assert "Inbound references rewritten: 0" in captured.out
