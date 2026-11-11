"""Tasks with a lifecycle state from desks migrated before CC31 (task.debug of legacy states).

A terminal or drawer status with an empty history at ``ritual-execution`` is a state no
transition produces, so TaskDoc's validator (CC37) rejects it and sldb's store check stops at
the first such document. The seven fixtures are the five tasks of the shared_llm-gateway
reproduction (two superseded, one deferred, two draft after ``task_hands_to_closeout``) plus a
cancelled and a closed one (b6):

* ``deskops desk update`` (dry-run) lists what the table migrates and the tasks it does not
  decide, and writes nothing; ``--apply`` migrates (one ``<file>: <field> <before> -> <after>``
  line per field, b4), reports the rest with exit 1, and a second run migrates nothing (d1);
* ``deskops doctor`` reports each invalid task and goes on with every other check (d2, b9).
"""
from __future__ import annotations

import contextlib
import io
import itertools
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.commands.doctor import DoctorCLI
from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION
from deskops.models.task_lifecycle import legacy_state_migration
from deskops.models.task_lifecycle import lifecycle_errors
from deskops.operations import DeskopsOperations
from sldb.cli import main as sldb_main
from sldb.runtime.validation import extract_model_data

GOLDEN_DIR = Path(__file__).resolve().parent / "fixtures" / "golden" / "output"

#: (title, status, current_node, history): the b6 fixtures. The task id is the title's slug.
LEGACY = [
    ("Ci propio del gateway", "superseded", "ritual-execution", []),
    ("Workflow check obligatorio del gateway", "superseded", "ritual-execution", []),
    ("Tope por tipo y pedidos bloqueados", "deferred", "ritual-execution", []),
    ("Linea base de lint del gateway", "draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
    ("Logs de llm gateway servir sin pii", "draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
    ("Cancelada heredada", "cancelled", "ritual-execution", []),
    ("Cerrada heredada", "closed", "ritual-execution", []),
]
MIGRATION_LINES = [
    "desk/tasks/task-cancelada-heredada.md: current_node ritual-execution -> ''",
    "desk/tasks/task-cerrada-heredada.md: current_node ritual-execution -> ''",
    "desk/tasks/task-ci-propio-del-gateway.md: history [] -> [superseded]",
    "desk/tasks/task-tope-por-tipo-y-pedidos-bloqueados.md: current_node ritual-execution -> ''",
    "desk/tasks/task-workflow-check-obligatorio-del-gateway.md: history [] -> [superseded]",
]
UNMIGRATABLE = ["desk/tasks/task-linea-base-de-lint-del-gateway.md", "desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md"]
DRAFT_ERROR = "status: 'draft' does not follow history 'task_hands_to_closeout'; expected 'ready_for_testing'"


def _legacy_text(text: str, status: str, node: str, history: list[str]) -> str:
    """The task as a pre-CC31 desk left it: the three fields written by hand, nothing else."""
    history_text = "history: []" if not history else "history:\n" + "\n".join(f"- {h}" for h in history)
    assert text.count("status: draft\n") == 1 and text.count("current_node: ritual-execution\n") == 1
    assert text.count("history: []\n") == 1
    return (
        text.replace("status: draft\n", f"status: {status}\n")
        .replace("current_node: ritual-execution\n", f"current_node: {node}\n")
        .replace("history: []\n", history_text + "\n")
    )


def _make_tasks(root: Path, rows: list[tuple[str, str, str, list[str]]]) -> dict[str, Path]:
    """Create each task tracked (as ``deskops add task`` does), then give it its legacy state."""
    paths: dict[str, Path] = {}
    operations = DeskopsOperations(root)
    for title, status, node, history in rows:
        payload = {
            "title": title,
            "goal": "g",
            "scope": "s",
            "implementation_path": "i",
            "done_when": "d",
            "validation": ["pytest"],
            "task_type": "task.code",
        }
        task_id = operations.create_task_bundle(payload).task_id
        path = root / "desk" / "tasks" / f"{task_id}.md"
        path.write_text(_legacy_text(path.read_text(encoding="utf-8"), status, node, history), encoding="utf-8")
        paths[path.relative_to(root).as_posix()] = path
    return paths


@pytest.fixture
def legacy_desk(lifecycle_desk: Path) -> tuple[Path, dict[str, Path]]:
    return lifecycle_desk, _make_tasks(lifecycle_desk, LEGACY)


@pytest.fixture
def migratable_desk(lifecycle_desk: Path) -> tuple[Path, dict[str, Path]]:
    rows = [row for row in LEGACY if row[1] != "draft"]
    return lifecycle_desk, _make_tasks(lifecycle_desk, rows)


def _sldb_check(root: Path) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            return int(sldb_main(["stores", "check", "--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]) or 0)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1


def _texts(paths: dict[str, Path]) -> dict[str, str]:
    return {rel: path.read_text(encoding="utf-8") for rel, path in paths.items()}


def _golden(name: str) -> str:
    return (GOLDEN_DIR / name).read_text(encoding="utf-8")


# ------------------------------------------------------------------ the table (d1, b7)
@pytest.mark.parametrize(
    ("status", "node", "expected"),
    [
        ("superseded", "ritual-execution", {"history": ([], ["superseded"])}),
        ("superseded", "", {"history": ([], ["superseded"])}),  # b7: an empty node gets it too
        ("superseded", "ritual-testing", {"history": ([], ["superseded"])}),
        *[(s, "ritual-execution", {"current_node": ("ritual-execution", "")}) for s in ("closed", "resolved", "done", "complete", "cancelled")],
        *[(s, "ritual-execution", {"current_node": ("ritual-execution", "")}) for s in ("deferred", "candidate")],
    ],
)
def test_the_table_migrates_each_legacy_status(status: str, node: str, expected: dict) -> None:
    assert lifecycle_errors(status, node, [])
    changes = legacy_state_migration(status, node, [])
    assert changes == expected
    after_node = changes.get("current_node", (node, node))[1]
    after_history = changes.get("history", ([], []))[1]
    assert lifecycle_errors(status, after_node, after_history) == []


@pytest.mark.parametrize("status", ["cancelled", "closed", "deferred", "candidate", "draft"])
def test_a_coherent_task_outside_the_lifecycle_is_not_touched(status: str) -> None:
    """b7: an empty node with a status of OUTSIDE_LIFECYCLE_STATUSES (cancelled added) is coherent."""
    assert legacy_state_migration(status, "", []) == {}
    payload = {"title": "T", "id": "task-t", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d"}
    assert TaskDoc(**payload, status=status, current_node="", history=[]).status == status


@pytest.mark.parametrize(
    ("status", "node", "history"),
    [
        ("active", "ritual-execution", []),
        ("draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"]),
        ("draft", "ritual-testing", []),
        ("closed", "ritual-testing", ["task_activates"]),
    ],
)
def test_any_other_incoherent_state_is_left_to_its_owner(status: str, node: str, history: list[str]) -> None:
    assert lifecycle_errors(status, node, history)
    assert legacy_state_migration(status, node, history) is None


# ------------------------------------------------------------------ desk update (d1, d2)
def test_desk_update_dry_run_lists_the_migration_and_the_undecided_tasks_and_writes_nothing(legacy_desk, capsys) -> None:
    root, paths = legacy_desk
    before = _texts(paths)
    assert _sldb_check(root) != 0  # sldb stops at the first invalid task: the reproduction
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "- Legacy task states to migrate: 5 task(s)" in out
    for line in MIGRATION_LINES:
        assert f"  - {line}\n" in out
    assert "- Invalid task documents (not written): 2 task(s)" in out
    for rel in UNMIGRATABLE:
        assert f"  - {rel}: {DRAFT_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}.\n" in out
    assert "- Store check failed ('sldb stores check' exit code 1" in out
    assert "Migrating legacy task states" not in out
    assert _texts(paths) == before


def test_desk_update_apply_migrates_by_the_table_reports_the_rest_and_a_second_run_changes_nothing(legacy_desk, capsys) -> None:
    root, paths = legacy_desk
    before = _texts(paths)
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    out = capsys.readouterr().out
    assert out.startswith("Migrating legacy task states...\n" + "".join(f"- {line}\n" for line in MIGRATION_LINES))
    assert "- Invalid task documents (not written): 2 task(s)" in out
    assert "Skipped the store repairs" in out
    after = _texts(paths)
    for rel in UNMIGRATABLE:
        assert after[rel] == before[rel]
    for line in MIGRATION_LINES:
        rel = line.split(":", 1)[0]
        assert after[rel] != before[rel]
        extract_model_data(TaskDoc, after[rel])  # the model reads it now
        # Only the table's field moved.
        changed = [a for a, b in zip(after[rel].splitlines(), before[rel].splitlines()) if a != b]
        assert len(changed) == 1 and changed[0].startswith(("current_node: ''", "history:"))

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    second = capsys.readouterr().out
    assert "Migrating legacy task states" not in second
    assert "Legacy task states to migrate" not in second
    assert not any(line in second for line in MIGRATION_LINES)
    for rel in UNMIGRATABLE:
        assert f"  - {rel}: {DRAFT_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}.\n" in second
    assert _texts(paths) == after


def test_desk_update_apply_on_a_fully_migratable_desk_leaves_a_store_that_checks(migratable_desk, capsys) -> None:
    root, paths = migratable_desk
    assert _sldb_check(root) != 0
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    out = capsys.readouterr().out
    lines = out.splitlines(keepends=True)
    block = lines[0] + "".join(itertools.takewhile(lambda line: line.startswith("- desk/tasks/"), lines[1:]))
    assert block == _golden("desk_update_legacy_migration.text")
    assert "Invalid task documents" not in out
    assert _sldb_check(root) == 0

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    assert "Migrating legacy task states" not in capsys.readouterr().out


# ------------------------------------------------------------------ doctor (d2, b9)
def test_doctor_reports_each_invalid_task_and_runs_every_other_check(legacy_desk, capsys, monkeypatch) -> None:
    root, _paths = legacy_desk
    ran: list[str] = []
    original = DoctorCLI._check_models

    def _check_models(self, *args, **kwargs):
        ran.append("models")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(DoctorCLI, "_check_models", _check_models)
    capsys.readouterr()

    assert main(["doctor", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("Errors (the desk is broken):\n")
    findings = [line for line in out.splitlines() if line.startswith("- Invalid task document: ")]
    assert len(findings) == 7
    for line in MIGRATION_LINES:
        assert any(f.startswith(f"- Invalid task document: {line.split(':', 1)[0]}: ") and f.endswith("Migrate it with deskops desk update --apply.") for f in findings)
    unmigratable = [f for f in findings if UNMIGRATABLE_SUGGESTION in f]
    assert "\n".join(unmigratable) + "\n" == _golden("doctor_invalid_task.text")
    assert "SLDB store check crashed" in out  # the store check still runs after the task findings
    assert ran == ["models"]


# ------------------------------------------------------------------ closeout retire with a store (d3)
def _git(root: Path, *argv: str) -> str:
    import subprocess

    return subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def test_retire_waits_while_another_task_is_invalid_then_retires_the_migrated_task(migratable_desk, capsys) -> None:
    """sldb rebuilds every task of the store when one is untracked, so retire refuses up front
    (nothing written) while another task is invalid; after desk update --apply it retires the
    migrated superseded task, and the store still checks."""
    root, _paths = migratable_desk
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "legacy desk")
    head = _git(root, "rev-parse", "HEAD")
    retire = ["closeout", "retire", "--root", str(root), "--task", "task-ci-propio-del-gateway", "--reason", "pre-CC31", "--ref", head]
    capsys.readouterr()

    assert main(retire) == 1
    out = capsys.readouterr().out
    assert "Cannot retire task-ci-propio-del-gateway yet" in out
    assert "desk/tasks/task-cerrada-heredada.md" in out
    assert _git(root, "status", "--porcelain") == ""
    assert _git(root, "rev-parse", "HEAD") == head

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "migrated")
    capsys.readouterr()
    assert main(retire) == 0, capsys.readouterr().out
    assert "Closeout-Mode: legacy-resolved" in _git(root, "log", "-1", "--format=%B")
    assert not (root / "desk" / "tasks" / "task-ci-propio-del-gateway.md").exists()
    assert _sldb_check(root) == 0
