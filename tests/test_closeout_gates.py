"""The closeout graph read from sldb's index gives what the full repository scan gave.

`build_closeout_graph_context` used to extract every document and source file of the
repository, ask `doc_status` once per document and read the declared edges of every
document; `lifecycle.transitions_from` read the edge index composed with every linked
store. Both now read less (the sldb index once, the documents the gate asks about, the
desk's own store). `tests/closeout_graph_oracle.py` keeps the old path frozen; these
tests run both over temporary desks and require the same answers: the same
`verify_task_closeout` report, the same declared-edge extraction, the same source nodes
and the same lifecycle transitions.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

from deskops import lifecycle
from deskops.graph.desk_graph import extract_declared_edges
from deskops.graph.desk_graph import extract_doc_nodes
from deskops.graph.desk_graph import extract_source_file_nodes
from deskops.operations import DeskopsOperations
from deskops.services.desk_view import DeskView

from tests.closeout_graph_oracle import FullScanCloseoutGraph
from tests.closeout_graph_oracle import closeout_graph_context_v1
from tests.closeout_graph_oracle import extract_declared_edges_v1
from tests.closeout_graph_oracle import extract_doc_nodes_v1
from tests.closeout_graph_oracle import extract_source_file_nodes_v1
from tests.closeout_graph_oracle import transitions_from_v1


ATOM = "atom-closeout-graph-equivalence"
GUARD_TEST = "tests/test_skill_cli_drift.py"
CHANGED_SKILL = ".pi/skills/use-deskops/SKILL.md"

# task id -> changed files. Together they cover: a file covered by a valid
# materialization (source and test targets), a file whose only materialization is
# invalid, a file with no materialization, a changed document that declares atoms, a
# changed atom, a skill file covered through a guard test, and a path outside the repo.
TASKS: dict[str, list[str]] = {
    "task-valid-materialization": ["deskops/covered.py", "tests/test_covered.py"],
    "task-invalid-materialization": ["deskops/covered_by_invalid.py"],
    "task-no-materialization": ["deskops/uncovered.py", "docs/notes.md"],
    "task-changed-documents": [
        "desk/tasks/task-valid-materialization.md",
        f"desk/atoms/{ATOM}.md",
        "docs/design.md",
    ],
    "task-skill-guard": [CHANGED_SKILL],
    "task-mixed": ["deskops/covered.py", "deskops/uncovered.py", "../outside.py", "config/app-config.yaml"],
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _materialization(name: str, atoms: list[str], target_kind: str, target: str) -> str:
    return (
        "---\n"
        + yaml.safe_dump(
            {
                "id": name,
                "title": name.replace("-", " "),
                "source_atoms": atoms,
                "target_kind": target_kind,
                "target_identity": target,
                "validation": [f"python -m pytest {GUARD_TEST} -q"],
                "tags": [],
            },
            sort_keys=False,
        )
        + f"---\n\n# {name}\n\n## Intent\n\nCover {target}.\n"
    )


def _task(task_id: str, files: list[str], atoms: list[str]) -> str:
    front = {
        "id": task_id,
        "status": "active",
        "current_node": "ritual-testing",
        "history": ["task_activates"],
        "references": [GUARD_TEST],
        "depends_on": [],
        "pills": [],
        "atoms": atoms,
        "files": files,
        "task_type": "code",
        "closeout_evidence": ["tests", "commit", "atom", "materialization"],
        "tags": [],
    }
    return (
        "---\n"
        + yaml.safe_dump(front, sort_keys=False)
        + f"---\n\n# {task_id}\n\n## Rationale\n\nEquivalence.\n\n## Goal\n\nSame answers.\n\n"
        "## Related atoms\n\n"
        f"- {ATOM}\n- atom-that-does-not-exist\n\n"
        "## Implementation Path\n\nTouch deskops/covered.py and tests/test_covered.py.\n\n"
        "## Validation\n\n- pytest\n\n## Done When\n\nDone.\n"
    )


def _populate(root: Path) -> None:
    """The shared desk content: atom, materializations (valid and invalid), sources, tasks."""
    _write(
        root / "desk" / "atoms" / f"{ATOM}.md",
        f"---\nid: {ATOM}\ntitle: Equivalence atom\nfive_wh_one_plus: what\ntags: []\n---\n\n"
        "# Equivalence atom\n\n## Answer\n\nThe closeout graph reads what it needs.\n",
    )
    _write(root / "deskops" / "covered.py", "COVERED = 1\n")
    _write(root / "deskops" / "covered_by_invalid.py", "INVALID = 1\n")
    _write(root / "deskops" / "uncovered.py", "UNCOVERED = 1\n")
    _write(root / "tests" / "test_covered.py", "def test_covered() -> None:\n    assert True\n")
    _write(
        root / GUARD_TEST,
        'SKILL_TREES = (".pi/skills", ".agents/skills", ".opencode/skills")\nSKILL_FILE = "SKILL.md"\n',
    )
    _write(root / CHANGED_SKILL, "# Use deskops\n")
    _write(root / "config" / "app-config.yaml", "key: value\n")
    _write(root / "runs" / "subagents" / "run-1" / "registry.json", "{}\n")
    _write(root / "runs" / "subagents" / "run-1" / "summary.md", "# Run\n")
    _write(root / "docs" / "notes.md", "# Notes\n\nPlain notes.\n")
    _write(
        root / "docs" / "design.md",
        f"---\ntitle: Design\natoms:\n- {ATOM}\n---\n\n# Design\n\n## Related atoms\n\n- {ATOM}\n",
    )
    materializations = root / "desk" / "materializations"
    _write(
        materializations / "materialization-covered-source.md",
        _materialization("materialization-covered-source", [ATOM], "source_file", "deskops/covered.py"),
    )
    _write(
        materializations / "materialization-covered-test.md",
        _materialization("materialization-covered-test", [ATOM], "test_file", "tests/test_covered.py"),
    )
    _write(
        materializations / "materialization-guard-test.md",
        _materialization("materialization-guard-test", [ATOM], "test_file", GUARD_TEST),
    )
    # Invalid: one of its source atoms does not exist.
    _write(
        materializations / "materialization-broken-atom.md",
        _materialization(
            "materialization-broken-atom",
            [ATOM, "atom-missing-from-the-desk"],
            "source_file",
            "deskops/covered_by_invalid.py",
        ),
    )
    # Invalid: its target is not a file of the repository.
    _write(
        materializations / "materialization-missing-target.md",
        _materialization("materialization-missing-target", [ATOM], "source_file", "deskops/gone.py"),
    )
    for task_id, files in TASKS.items():
        _write(root / "desk" / "tasks" / f"{task_id}.md", _task(task_id, files, [ATOM]))


def _commit(root: Path) -> None:
    _git(root, "add", "--", "deskops", "tests", "docs", "config", ".pi")
    _git(root, "commit", "-q", "-m", "work")
    sha = _git(root, "rev-parse", "--short", "HEAD")
    for task_id, files in TASKS.items():
        path = root / "desk" / "tasks" / f"{task_id}.md"
        text = path.read_text(encoding="utf-8").replace(f"- {GUARD_TEST}\n", f"- {GUARD_TEST}\n- '{sha}'\n", 1)
        path.write_text(text, encoding="utf-8")


@pytest.fixture
def bare_desk(tmp_path: Path) -> Path:
    """A repository with a desk and no sldb store: every document is read locally."""
    root = tmp_path / "bare"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    _populate(root)
    _commit(root)
    return root


@pytest.fixture
def store_desk(lifecycle_desk: Path) -> Path:
    """An initialized desk whose store tracks the atom, the tasks and the materializations."""
    from sldb.api import track_document_file

    root = lifecycle_desk
    _populate(root)
    _commit(root)
    pythonpath = str(Path(__file__).resolve().parents[1])
    track_document_file(root / ".sldb", "AtomDoc", root / "desk" / "atoms" / f"{ATOM}.md", name=ATOM, pythonpath=pythonpath, force=True)
    for path in sorted((root / "desk" / "materializations").glob("materialization-*.md")):
        track_document_file(root / ".sldb", "MaterializationContractDoc", path, name=path.stem, pythonpath=pythonpath, force=True)
    for task_id in TASKS:
        track_document_file(root / ".sldb", "TaskDoc", root / "desk" / "tasks" / f"{task_id}.md", name=task_id, pythonpath=pythonpath, force=True)
    return root


def _verify_both(root: Path, monkeypatch: pytest.MonkeyPatch, task_id: str) -> tuple[dict, dict]:
    live = DeskopsOperations(root).verify_task_closeout(task_id)
    with monkeypatch.context() as patch:
        oracle_ops = DeskopsOperations(root)
        patch.setattr(
            oracle_ops.closure,
            "build_closeout_graph_context",
            lambda: FullScanCloseoutGraph(closeout_graph_context_v1(root)),
        )
        old = oracle_ops.verify_task_closeout(task_id)
    return live, old


@pytest.mark.parametrize("desk", ["bare_desk", "store_desk"])
def test_closeout_reports_match_the_full_scan(desk: str, request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> None:
    root: Path = request.getfixturevalue(desk)
    reports = {}
    for task_id in TASKS:
        live, old = _verify_both(root, monkeypatch, task_id)
        assert live == old, task_id
        reports[task_id] = live["gates"]["atom_or_materialization_link"]

    # The desk exercises each case the gate distinguishes.
    valid = reports["task-valid-materialization"]
    assert valid["ok"] is True
    assert "materialization:materialization:materialization-covered-source->deskops/covered.py" in valid["evidence"]
    invalid = reports["task-invalid-materialization"]
    assert invalid["ok"] is False
    assert [f["code"] for f in invalid["findings"]] == ["missing_changed_file_link"]
    absent = reports["task-no-materialization"]
    assert {f["path"] for f in absent["findings"]} == {"deskops/uncovered.py", "docs/notes.md"}
    assert any(item.startswith("graph:") for item in reports["task-changed-documents"]["evidence"])
    assert reports["task-skill-guard"]["evidence"] == [f"guard-test:{GUARD_TEST} -> {CHANGED_SKILL}"]
    assert any(f["code"] == "changed_file_missing" for f in reports["task-mixed"]["findings"])

    context = DeskopsOperations(root).closeout_gates.build_closeout_graph_context()
    assert context.invalid_materializations == closeout_graph_context_v1(root)["invalid_materializations"]
    assert context.invalid_materializations == {
        "materialization:materialization-broken-atom",
        "materialization:materialization-missing-target",
    }


@pytest.mark.parametrize("desk", ["bare_desk", "store_desk"])
def test_declared_edges_and_source_nodes_match_the_full_scan(desk: str, request: pytest.FixtureRequest) -> None:
    root: Path = request.getfixturevalue(desk)
    _assert_graph_matches_the_full_scan(root)


def test_the_repository_itself_matches_the_full_scan() -> None:
    """The real desk of this repository: hundreds of documents, a tracked store, runs/."""
    root = Path(__file__).resolve().parents[1]
    _assert_graph_matches_the_full_scan(root)


def test_the_board_matches_the_full_scan(store_desk: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    live = DeskView(store_desk).board()
    with monkeypatch.context() as patch:
        view = DeskView(store_desk)
        patch.setattr(
            view.ops.closure,
            "build_closeout_graph_context",
            lambda: FullScanCloseoutGraph(closeout_graph_context_v1(store_desk)),
        )
        patch.setattr(
            lifecycle,
            "transitions_from",
            lambda root, node, *, snapshot=None: transitions_from_v1(store_desk, node),
        )
        old = view.board()
    assert live == old


def _lifecycle_nodes() -> list[str]:
    return sorted(set(lifecycle.load_lifecycle_spec().rituals) | {"ritual-unknown"})


def test_transitions_match_the_linked_index(lifecycle_desk: Path, tmp_path: Path) -> None:
    """Reading the desk's own store gives the transitions the linked composition gave,
    also when the desk links another store that carries a lifecycle graph of its own."""
    from sldb.api import link_store

    for node in _lifecycle_nodes():
        assert lifecycle.transitions_from(lifecycle_desk, node) == transitions_from_v1(lifecycle_desk, node), node

    other = tmp_path / "other"
    shutil.copytree(lifecycle_desk, other)
    with contextlib.redirect_stdout(io.StringIO()):
        link_store(lifecycle_desk / ".sldb", other / ".sldb", name="other")
    for node in _lifecycle_nodes():
        assert lifecycle.transitions_from(lifecycle_desk, node) == transitions_from_v1(lifecycle_desk, node), node
    assert lifecycle.transitions_from(lifecycle_desk, "ritual-testing")


def _assert_graph_matches_the_full_scan(root: Path) -> None:
    """sldb's project graph with the desk configuration gives the frozen extractors' output."""
    assert _dicts(extract_doc_nodes(root)) == _dicts(extract_doc_nodes_v1(root))
    assert _dicts(extract_source_file_nodes(root)) == _dicts(extract_source_file_nodes_v1(root))
    live, old = extract_declared_edges(root), extract_declared_edges_v1(root)
    assert _dicts(live.edges) == _dicts(old.edges)
    assert _dicts(live.missing_targets) == _dicts(old.missing_targets)


def _dicts(items: list) -> list[dict]:
    return [item.to_dict() for item in items]
