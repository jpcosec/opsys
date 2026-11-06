"""GC01: task types as models with a hierarchy and type-declared closeout evidence.

Covers each Done When line of task-gc01: the seven factory subclasses and their declared
evidence/receipts, `add task --task-type` (registered-only + default + envelope note), the
store family ``model <= TaskCodeDoc``, closeout reading evidence from the type, `--evidence`
as a floor, the desk-local type registration (DC7), the legacy ``task_type`` migration, and
the removal of ``TASK_TYPE_EVIDENCE``.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import yaml

from deskops.models import TaskAggregateDoc
from deskops.models import TaskCodeDoc
from deskops.models import TaskDebugDoc
from deskops.models import TaskDecisionDoc
from deskops.models import TaskDoc
from deskops.models import TaskDocsDoc
from deskops.models import TaskExternalDoc
from deskops.models import TaskRefactorDoc
from deskops.models.task_types import canonical_task_type_name
from deskops.models.task_types import TASK_TYPE_MODELS

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SLDB = [sys.executable, "-m", "sldb"]


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([*CLI, *argv, "--root", str(root)], cwd=root, capture_output=True, text=True)
    if check:
        assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def _init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([*CLI, "init", str(root)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def _sldb(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*SLDB, *argv], cwd=root, capture_output=True, text=True)


def _frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}


def _write_task(root: Path, task_id: str, *, task_type: str, references: list[str] | None = None, files: list[str] | None = None) -> Path:
    path = root / "desk" / "tasks" / f"{task_id}.md"
    path.write_text(
        f"""---
id: {task_id}
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: {references or []}
depends_on: []
pills: []
files: {files or []}
task_type: {task_type}
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# {task_id}

## Rationale

## Goal

Migrate.

## Scope

## Implementation Path

## Validation

## Done When

""",
        encoding="utf-8",
    )
    return path


def _write_legacy_task(root: Path, task_id: str, task_type: str) -> Path:
    return _write_task(root, task_id, task_type=task_type)


# ------------------------------------------------------------------ models
def test_factory_type_declarations_match_the_normative_table() -> None:
    assert TaskCodeDoc.model_fields["task_type"].default == "task.code"
    assert TaskCodeDoc.__closeout_evidence__ == ("tests", "commit", "atom", "materialization")
    assert TaskCodeDoc.__activation_receipts__ == ("preflight", "bundle")

    assert TaskDocsDoc.model_fields["task_type"].default == "task.docs"
    assert TaskDocsDoc.__closeout_evidence__ == ("commit", "document")
    assert TaskDocsDoc.__activation_receipts__ == ("preflight",)

    assert TaskDebugDoc.model_fields["task_type"].default == "task.debug"
    assert TaskDebugDoc.__closeout_evidence__ == ("tests", "commit", "atom", "materialization")
    assert TaskDebugDoc.__activation_receipts__ == ("preflight", "reproduction")

    assert TaskRefactorDoc.model_fields["task_type"].default == "task.refactor"
    assert TaskRefactorDoc.__closeout_evidence__ == ("tests", "commit", "atom", "materialization", "goldens")
    assert TaskRefactorDoc.__activation_receipts__ == ("preflight", "bundle", "goldens")

    assert TaskDecisionDoc.model_fields["task_type"].default == "task.decision"
    assert TaskDecisionDoc.__closeout_evidence__ == ("commit", "document")
    assert TaskDecisionDoc.__activation_receipts__ == ("owner",)

    assert TaskAggregateDoc.model_fields["task_type"].default == "task.aggregate"
    assert TaskAggregateDoc.__closeout_evidence__ == ("children", "commit")
    assert TaskAggregateDoc.__activation_receipts__ == ()

    assert TaskExternalDoc.model_fields["task_type"].default == "task.external"
    assert TaskExternalDoc.__closeout_evidence__ == ("external",)
    assert TaskExternalDoc.__activation_receipts__ == ("preflight",)


def test_type_hierarchy_keeps_refactor_in_code_and_debug_out_of_it() -> None:
    assert issubclass(TaskRefactorDoc, TaskCodeDoc)
    assert not issubclass(TaskDebugDoc, TaskCodeDoc)
    assert issubclass(TaskDebugDoc, TaskDoc)
    assert issubclass(TaskDocsDoc, TaskDoc)


def test_taskdoc_declares_the_contract_fields() -> None:
    assert TaskDoc.__contract__ == [
        "title",
        "goal",
        "scope",
        "implementation_path",
        "files",
        "validation",
        "done_when",
    ]


def test_legacy_task_type_map_matches_the_migration() -> None:
    assert canonical_task_type_name("code") == "task.code"
    assert canonical_task_type_name("implementation") == "task.code"
    assert canonical_task_type_name("test") == "task.code"
    assert canonical_task_type_name("docs") == "task.docs"
    assert canonical_task_type_name("spec") == "task.docs"
    assert canonical_task_type_name("design") == "task.docs"
    assert canonical_task_type_name("external") == "task.external"
    assert canonical_task_type_name("") == "task.code"
    assert canonical_task_type_name("task.code") == "task.code"
    assert canonical_task_type_name("reflection") == "task.code"


# ------------------------------------------------------------------ add task
def test_add_task_with_task_type_tracks_under_the_type_model(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Typed", "--goal", "g", "--scope", "s", "--task-type", "task.code")
    assert "Created task bundle task-typed" in result.stdout
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-typed.md")
    assert frontmatter["task_type"] == "task.code"

    found = _sldb(lifecycle_desk, "find", "task-typed", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    results = json.loads(found.stdout)["results"]
    assert [(r["name"], r["model"]) for r in results] == [("task-typed", "TaskCodeDoc")]


def test_add_task_without_task_type_defaults_to_code_with_a_note(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Defaulted", "--goal", "g", "--scope", "s")
    assert "no --task-type given; defaulting to task.code" in result.stdout
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-defaulted.md")
    assert frontmatter["task_type"] == "task.code"
    assert frontmatter.get("closeout_evidence") is None


def test_add_task_with_an_unregistered_type_lists_the_types(lifecycle_desk: Path) -> None:
    result = _cli(lifecycle_desk, "add", "task", "--title", "Bad", "--goal", "g", "--scope", "s", "--task-type", "foo", check=False)
    assert result.returncode == 1
    assert "'foo' is not a registered task type" in result.stdout
    for name in TASK_TYPE_MODELS:
        assert name in result.stdout
    assert not (lifecycle_desk / "desk" / "tasks" / "task-bad.md").exists()


# ------------------------------------------------------------------ evidence floor
def test_add_task_evidence_can_add_but_not_remove_a_type_kind(lifecycle_desk: Path) -> None:
    removed = _cli(
        lifecycle_desk,
        "add", "task", "--title", "Removed", "--goal", "g", "--scope", "s",
        "--task-type", "task.code", "--evidence", "commit", "document",
        check=False,
    )
    assert removed.returncode == 1
    assert "--evidence removes closeout evidence the task type requires" in removed.stdout

    added = _cli(
        lifecycle_desk,
        "add", "task", "--title", "Added", "--goal", "g", "--scope", "s",
        "--task-type", "task.code",
        "--evidence", "tests", "commit", "atom", "materialization", "document",
    )
    assert added.returncode == 0
    frontmatter = _frontmatter(lifecycle_desk / "desk" / "tasks" / "task-added.md")
    assert frontmatter["closeout_evidence"] == ["tests", "commit", "atom", "materialization", "document"]


# ------------------------------------------------------------------ family query
def test_model_family_query_includes_refactor_and_not_debug_or_docs(lifecycle_desk: Path) -> None:
    for title in ("Code", "Refactor", "Debug", "Docs"):
        _cli(lifecycle_desk, "add", "task", "--title", title, "--goal", "g", "--scope", "s", "--task-type", f"task.{title.lower()}")

    found = _sldb(lifecycle_desk, "find", "task-", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    names = {r["name"] for r in json.loads(found.stdout)["results"]}
    assert "task-code" in names
    assert "task-refactor" in names
    assert "task-debug" not in names
    assert "task-docs" not in names


# ------------------------------------------------------------------ closeout reads the type
def test_closeout_verify_reads_evidence_from_the_type(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "api.md").write_text("# API\n", encoding="utf-8")
    _git(root, "add", "docs")
    _git(root, "commit", "-q", "-m", "docs")
    commit = _git(root, "rev-parse", "HEAD")

    _write_task(root, "task-doc-task", task_type="task.docs", references=[commit, "docs/api.md"])

    result = _cli(root, "closeout", "verify", "--task", "task-doc-task")
    report = json.loads(result.stdout)
    assert report["ok"], report
    assert report["declared"] == ["commit", "document"]
    assert report["found"] == ["commit", "document"]
    assert report["implicit_code"] is False


def test_closeout_verify_fails_naming_children_and_goldens_as_not_verifiable(lifecycle_desk: Path) -> None:
    _cli(lifecycle_desk, "add", "task", "--title", "Aggregate", "--goal", "g", "--scope", "s", "--task-type", "task.aggregate")
    result = _cli(lifecycle_desk, "closeout", "verify", "--task", "task-aggregate", check=False)
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert not report["ok"]
    codes = {item["code"] for item in report["findings"]}
    assert "closeout_evidence_not_verifiable" in codes
    assert any("children" in item["message"] for item in report["findings"])


# ------------------------------------------------------------------ local types (DC7)
def test_desk_update_apply_registers_a_local_type_and_add_task_uses_it(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    models_dir = root / "desk" / "models"
    models_dir.mkdir()
    (models_dir / "local_types.py").write_text(
        """from typing import Literal
from pydantic import Field
from deskops.models import TaskCodeDoc


class TaskCliDoc(TaskCodeDoc):
    task_type: Literal["task.code.cli"] = Field(default="task.code.cli", description="CLI subtype.")
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization", "document")
    __activation_receipts__ = ("preflight", "bundle")
""",
        encoding="utf-8",
    )

    _cli(root, "desk", "update", "--apply")

    registered = _sldb(root, "models", "list", "--store", ".sldb", "--format", "json")
    assert "TaskCliDoc" in {m["name"] for m in json.loads(registered.stdout)["models"]}

    result = _cli(root, "add", "task", "--title", "CLI", "--goal", "g", "--scope", "s", "--task-type", "task.code.cli")
    assert "Created task bundle task-cli" in result.stdout
    frontmatter = _frontmatter(root / "desk" / "tasks" / "task-cli.md")
    assert frontmatter["task_type"] == "task.code.cli"

    found = _sldb(root, "find", "task-cli", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--pythonpath", str(root / "desk"), "--format", "json")
    results = json.loads(found.stdout)["results"]
    assert [(r["name"], r["model"]) for r in results] == [("task-cli", "TaskCliDoc")]

    # The local subtype adds `document`: closeout reads the subtype's evidence, not task.code's.
    verify = _cli(root, "closeout", "verify", "--task", "task-cli", check=False)
    assert json.loads(verify.stdout)["declared"] == ["tests", "commit", "atom", "materialization", "document"]


def test_desk_update_apply_declares_the_types_it_registers_so_a_clean_clone_rebuilds(tmp_path: Path) -> None:
    """`desk update --apply` registered GC01's task types in sldb's index but not in its
    store.yaml, and the CI rebuild said `Model 'TaskCodeDoc' not registered.` (sldb 8b60e889).
    A declared desk that gains a type keeps rebuilding from its declaration."""
    root = tmp_path / "repo"
    _init(root)
    _git(root, "init", "-q")
    declared = _sldb(root, "stores", "declare", "--write", "--store", ".sldb")
    assert declared.returncode == 0, declared.stdout + declared.stderr
    models_dir = root / "desk" / "models"
    models_dir.mkdir()
    (models_dir / "local_types.py").write_text(
        """from typing import Literal
from pydantic import Field
from deskops.models import TaskCodeDoc


class TaskCliDoc(TaskCodeDoc):
    task_type: Literal["task.code.cli"] = Field(default="task.code.cli", description="CLI subtype.")
    __closeout_evidence__ = ("tests", "commit")
""",
        encoding="utf-8",
    )

    _cli(root, "desk", "update", "--apply")
    _cli(root, "add", "task", "--title", "CLI", "--goal", "g", "--scope", "s", "--task-type", "task.code.cli")

    declaration = yaml.safe_load((root / ".sldb" / "store.yaml").read_text(encoding="utf-8"))
    assert "TaskCliDoc" in {m["name"] for m in declaration["models"]}
    check = _sldb(root, "stores", "build", "--check", "--store", ".sldb")
    assert check.returncode == 0, check.stdout + check.stderr


# ------------------------------------------------------------------ migration
def test_legacy_task_type_migrates_idempotently(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    path = _write_legacy_task(root, "task-legacy", "implementation")

    _cli(root, "desk", "update", "--apply")
    assert _frontmatter(path)["task_type"] == "task.code"

    found = _sldb(root, "find", "task-legacy", "--in", "physical", "--type", "doc", "--where", "model <= TaskCodeDoc", "--store", ".sldb", "--format", "json")
    assert [r["model"] for r in json.loads(found.stdout)["results"]] == ["TaskCodeDoc"]

    before = path.read_bytes()
    second = _cli(root, "desk", "update", "--apply")
    assert "Desk is up to date." in second.stdout
    assert path.read_bytes() == before


def test_unknown_legacy_task_type_migrates_to_code_with_a_report(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    path = _write_legacy_task(root, "task-weird", "reflection")

    result = _cli(root, "desk", "update", "--apply")
    assert _frontmatter(path)["task_type"] == "task.code"
    assert "unknown legacy task_type 'reflection'" in result.stdout
    assert "migrated to task.code" in result.stdout


# ------------------------------------------------------------------ no flat mapping left
def test_task_type_evidence_mapping_is_gone() -> None:
    for path in (ROOT / "deskops").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "TASK_TYPE_EVIDENCE" not in text, path
