"""Closeout link evidence for changed skill files covered by guard tests.

Skill Markdown files are deliberately not graph nodes. A changed skill file is
linked only when a test that reads its skill tree is itself linked to an atom
or a valid materialization contract.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
import yaml

from deskops.operations import DeskopsOperations


CHANGED_SKILL = ".pi/skills/use-deskops/SKILL.md"
GUARD_TEST = "tests/test_skill_cli_drift.py"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_atom(root: Path, atom_id: str) -> None:
    _write(
        root / "desk" / "atoms" / f"{atom_id}.md",
        f"""---
id: {atom_id}
title: Skill guard atom
five_wh_one_plus: what
tags: []
---

# Skill guard atom

## Answer

Guard the skill trees.
""",
    )


def _write_materialization(root: Path, atom_id: str) -> None:
    _write(
        root / "desk" / "materializations" / "materialization-skill-drift-guards.md",
        f"""---
id: materialization-skill-drift-guards
title: Skill drift guard tests
source_atoms:
- {atom_id}
target_kind: test_file
target_identity: {GUARD_TEST}
validation:
- python -m pytest {GUARD_TEST} -q
tags: []
---

# Skill drift guard tests

## Intent

Guard the skill trees with a tracked test.
""",
    )


def _write_guard_test(root: Path) -> None:
    _write(
        root / GUARD_TEST,
        'SKILL_TREES = (".pi/skills", ".agents/skills", ".opencode/skills")\n'
        'SKILL_FILE = "SKILL.md"\n\n\n'
        "def test_skills_exist() -> None:\n"
        "    assert SKILL_TREES and SKILL_FILE\n",
    )


def _write_changed_skill(root: Path) -> None:
    _write(root / CHANGED_SKILL, "# Use deskops\n")


def _write_task(root: Path, changed_files: list[str]) -> None:
    references = yaml.safe_dump([GUARD_TEST], sort_keys=False).rstrip()
    files = yaml.safe_dump(changed_files, sort_keys=False).rstrip()
    _write(
        root / "desk" / "tasks" / "task-x.md",
        f"""---
id: task-x
status: active
references:
{references}
depends_on: []
pills: []
files:
{files}
checklists: []
tags: []
---

# Task X

## Rationale

Not provided.

## Goal

Verify closeout.

## Scope

Stay scoped.

## Implementation Path

Implement verify.

## Validation

- pytest

## Done When

Verified.
""",
    )


def _link_gate(tmp_path: Path, changed_files: list[str] | None = None) -> dict:
    root = tmp_path / "repo"
    root.mkdir()
    _write_atom(root, "atom-skill-guard")
    _write_materialization(root, "atom-skill-guard")
    _write_guard_test(root)
    _write_changed_skill(root)
    _write_task(root, changed_files or [CHANGED_SKILL])
    report = DeskopsOperations(root).verify_task_closeout("task-x")
    return report["gates"]["atom_or_materialization_link"]


def test_atom_linked_guard_test_covers_a_changed_skill_file(tmp_path: Path) -> None:
    gate = _link_gate(tmp_path)

    assert gate["ok"] is True
    assert gate["findings"] == []
    assert gate["evidence"] == [f"guard-test:{GUARD_TEST} -> {CHANGED_SKILL}"]


def test_guard_test_without_materialization_link_is_not_evidence(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _write_atom(root, "atom-skill-guard")
    _write_guard_test(root)
    _write_changed_skill(root)
    _write_task(root, [CHANGED_SKILL])

    report = DeskopsOperations(root).verify_task_closeout("task-x")
    gate = report["gates"]["atom_or_materialization_link"]

    assert gate["ok"] is False
    assert gate["evidence"] == []
    assert [finding["code"] for finding in gate["findings"]] == ["missing_changed_file_link"]


def test_non_skill_changed_file_keeps_the_existing_gate_behavior(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _write_atom(root, "atom-skill-guard")
    _write_materialization(root, "atom-skill-guard")
    _write_guard_test(root)
    _write_changed_skill(root)
    _write(root / "deskops" / "module.py", "X = 1\n")
    _write_task(root, ["deskops/module.py"])

    report = DeskopsOperations(root).verify_task_closeout("task-x")
    gate = report["gates"]["atom_or_materialization_link"]

    assert gate["ok"] is False
    assert not any(item.startswith("guard-test:") for item in gate["evidence"])
    assert [finding["code"] for finding in gate["findings"]] == ["missing_changed_file_link"]
