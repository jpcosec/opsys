"""A desk whose lifecycle seeds predate CC31 (task.debug: advance y doctor ante semillas anteriores).

A desk migrated before CC31 carries ``desk/lifecycle/execution-task_activates.md`` with
``attributes: {}``: the edge moves the task to ``ritual-testing`` but sets no status, and TaskDoc's
validator (CC37, the package's table) rejects ``draft`` after ``task_activates``. Reproduction
(b2/b3): a clean desk, the edge's ``attributes`` emptied through sldb, a task with its preflight
and bundle receipts recorded by an operator and accepted. Then:

* ``deskops doctor`` reports the seed out of date, with ``deskops desk update --apply`` (d1, b1, b5);
* ``deskops advance`` fails before writing, naming the edge (d2, b5, b6), exit 1, task unchanged;
* after ``deskops desk update --apply`` doctor no longer reports it and advance takes the task to
  ``active``.
"""
from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from deskops.doctor_findings import seed_drift
from deskops.lifecycle import LifecycleSeedOutOfDate
from deskops.lifecycle import Transition
from deskops.lifecycle import _check_against_package
from deskops.operations import DeskopsOperations
from deskops.workspace import desk_seed_text
from sldb.cli import main as sldb_main

GOLDEN_DIR = Path(__file__).resolve().parent / "fixtures" / "golden" / "output"
EDGE = "desk/lifecycle/execution-task_activates.md"
TASK_ID = "task-repro-advance"
DOCTOR_LINE = (
    f"lifecycle seed out of date: {EDGE} differs from the deskops package (attributes). "
    "Fix: deskops desk update --apply"
)
ADVANCE_ERROR = (
    f"Cannot advance {TASK_ID} via task_activates: the edge {EDGE} does not set status active "
    "(attributes.sets.status is missing). The desk's lifecycle seeds are out of date: "
    "run 'deskops desk update --apply'."
)


def _run(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
    return int(code or 0), out.getvalue(), err.getvalue()


def _sldb(argv: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        try:
            return int(sldb_main(argv) or 0)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1


def _check_golden(name: str, actual: str, request: pytest.FixtureRequest) -> None:
    path = GOLDEN_DIR / name
    if request.config.getoption("--update-golden"):
        path.write_text(actual, encoding="utf-8")
        return
    assert path.exists(), f"missing golden {path}; run pytest --update-golden"
    assert actual == path.read_text(encoding="utf-8"), f"golden mismatch: {name}"


@pytest.fixture
def pre_cc31_desk(lifecycle_desk: Path) -> Path:
    """b2/b3: the clean desk, the edge without ``attributes`` (through sldb, not by hand) and a
    task.code task with its activation receipts accepted."""
    root = lifecycle_desk
    task = DeskopsOperations(root).create_task_bundle(
        {
            "title": "Repro advance",
            "goal": "g",
            "scope": "s",
            "implementation_path": "i",
            "done_when": "d",
            "validation": ["pytest"],
            "task_type": "task.code",
        }
    )
    assert task.task_id == TASK_ID
    store = str(root / ".sldb")
    assert _sldb(["fields", "update", "docs/RelationDoc/execution-task_activates/attributes", "{}", "--store", store]) == 0
    assert "attributes: {}" in (root / EDGE).read_text(encoding="utf-8")
    evidence = root / "notes" / "evidence.txt"
    evidence.parent.mkdir()
    evidence.write_text("contract read\n", encoding="utf-8")
    for kind in ("preflight", "bundle"):
        code, out, err = _run(
            ["review", "record", TASK_ID, "--kind", kind, "--operator", "coord2", "--evidence", "notes/evidence.txt",
             "--reason", "contract read", "--root", str(root)]
        )
        assert code == 0, out + err
        code, out, err = _run(
            ["review", "dispose", f"review-{TASK_ID}-{kind}-1", "--verdict", "accepted", "--reason", "ok", "--root", str(root)]
        )
        assert code == 0, out + err
    return root


def test_pre_cc31_edge_doctor_reports_it_advance_refuses_and_desk_update_fixes_both(
    pre_cc31_desk: Path, request: pytest.FixtureRequest
) -> None:
    root = pre_cc31_desk
    task_path = root / "desk" / "tasks" / f"{TASK_ID}.md"

    code, doctor_out, _ = _run(["doctor", "--root", str(root)])
    assert f"- {DOCTOR_LINE}" in doctor_out.splitlines(), doctor_out
    assert "Desk is healthy" not in doctor_out
    assert code == 1  # the edge governs a transition: an error (b1)
    _check_golden("doctor_lifecycle_seed_out_of_date.text", doctor_out.replace(str(root), "<root>"), request)

    before = task_path.read_bytes()
    code, out, err = _run(["advance", "task", TASK_ID, "--root", str(root)])
    assert code == 1
    assert err == f"Error: {ADVANCE_ERROR}\n", err
    assert "Validation error" not in out + err and "pydantic" not in out + err
    assert task_path.read_bytes() == before
    _check_golden("advance_lifecycle_seed_out_of_date.text", err, request)

    code, out, err = _run(["desk", "update", "--apply", "--root", str(root)])
    assert code == 0, out + err
    assert f"rewrote {EDGE}" in out
    assert (root / EDGE).read_text(encoding="utf-8") == desk_seed_text(root.name, EDGE)

    code, doctor_out, _ = _run(["doctor", "--root", str(root)])
    assert "lifecycle seed out of date" not in doctor_out, doctor_out

    code, out, err = _run(["advance", "task", TASK_ID, "--root", str(root)])
    assert code == 0, out + err
    assert "Status: active" in out and "via task_activates" in out
    text = task_path.read_text(encoding="utf-8")
    assert "status: active\n" in text and "current_node: ritual-testing\n" in text


# ---------------------------------------------------------------- severity and comparison (b1)
def test_seed_drift_of_a_transition_field_is_an_error_and_lists_the_sorted_keys() -> None:
    package = desk_seed_text("repo", EDGE)
    desk = package.replace("relation_type: task_activates", "relation_type: task_activates\nextra: 1").replace(
        "condition: ''", "condition: status = \"draft\""
    )
    drift = seed_drift(EDGE, package, desk)
    assert drift.fields == ("condition", "extra")
    assert drift.governs_transition
    assert drift.line == (
        f"lifecycle seed out of date: {EDGE} differs from the deskops package (condition, extra). "
        "Fix: deskops desk update --apply"
    )


def test_seed_drift_in_the_body_only_is_an_alert() -> None:
    package = desk_seed_text("repo", EDGE)
    drift = seed_drift(EDGE, package, package.replace("## Notes", "## Notes\n\nA desk's own note."))
    assert drift.fields == ("body",) and not drift.governs_transition
    assert drift.line.endswith("differs from the deskops package (body). Fix: deskops desk update --apply")


def test_sldb_provenance_is_not_a_differing_field() -> None:
    package = desk_seed_text("repo", EDGE)
    provenance = "---\nsldb:\n  by: agent\n  via: fields_update\n"
    desk = package.replace("---\n", provenance, 1)
    assert seed_drift(EDGE, package, desk.replace("status: active", "status: draft")).fields == ("attributes",)
    assert seed_drift(EDGE, package, desk).fields == ("sldb",)


def test_seed_drift_of_a_rule_is_an_alert() -> None:
    rule = "desk/lifecycle/rule-activation-task-code.md"
    package = desk_seed_text("repo", rule)
    drift = seed_drift(rule, package, package.replace("---\n", "---\nnotes: x\n", 1))
    assert drift.fields == ("notes",) and not drift.governs_transition


# ---------------------------------------------------------------- the check before applying (b6)
def _transition(**overrides) -> Transition:
    values = dict(relation_type="task_activates", source="ritual-execution", target="ritual-testing", condition="",
                  sets={"status": "active"}, relation_doc="execution-task_activates")
    values.update(overrides)
    return Transition(**values)


def test_an_edge_like_the_package_passes() -> None:
    _check_against_package({"id": "task-x"}, _transition(), "ritual-testing")


def test_an_edge_setting_another_status_names_it() -> None:
    with pytest.raises(LifecycleSeedOutOfDate) as exc:
        _check_against_package({"id": "task-x"}, _transition(sets={"status": "draft"}), "ritual-testing")
    assert "does not set status active (attributes.sets.status is draft)" in str(exc.value)


def test_an_edge_leading_elsewhere_names_it() -> None:
    with pytest.raises(LifecycleSeedOutOfDate) as exc:
        _check_against_package({"id": "task-x"}, _transition(target="ritual-closeout"), "ritual-closeout")
    assert str(exc.value).startswith(f"Cannot advance task-x via task_activates: the edge {EDGE} does not lead to ritual-testing")
