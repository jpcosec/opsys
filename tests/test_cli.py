from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import CLI
from deskops.cli.main import main


ATOM_PAYLOAD_ARGS = [
    "--title",
    "Trackable atom",
    "--five-wh-one-plus",
    "what",
    "--answer",
    "Created atoms should be visible through deskops and sldb.",
]


def test_cli_help_uses_deskops_name(capsys) -> None:
    result = main(["--help"])

    captured = capsys.readouterr()
    assert result == 0
    assert "usage: deskops" in captured.out
    assert "{inbox,about,faq,repo,desk,bootstrap,init,atoms,graph,add,list,show,advance}" in captured.out


def test_about_prints_first_use_summary(capsys) -> None:
    result = main(["about"])

    captured = capsys.readouterr()
    assert result == 0
    assert "Workflow-domain CLI built on top of sldb." in captured.out
    assert "deskops bootstrap" in captured.out
    assert "deskops init ." in captured.out


def test_faq_lists_deskops_questions(capsys) -> None:
    result = main(["faq"])

    captured = capsys.readouterr()
    assert result == 0
    assert "deskops FAQ questions:" in captured.out
    assert "How do I run the CLI correctly?" in captured.out


def test_desk_install_scaffolds_expected_surface(tmp_path: Path, capsys) -> None:
    result = main(["desk", "install", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert "Scaffold complete." in captured.out
    assert "Register the repo separately" in captured.out

    expected_paths = [
        tmp_path / "desk" / "tasks" / "Board.md",
        tmp_path / "desk" / "contexts" / "pills.md",
        tmp_path / "desk" / "rituals" / "execution.md",
        tmp_path / "desk" / "rituals" / "testing.md",
        tmp_path / "desk" / "rituals" / "closeout.md",
        tmp_path / "desk" / "inbox",
        tmp_path / "desk" / "drawer" / "README.md",
        tmp_path / "desk" / "atoms",
        tmp_path / "desk" / "atoms" / "tag-namespaces.yaml",
    ]
    for path in expected_paths:
        assert path.exists()

    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "rituals:\n- desk/rituals/execution.md" in board_text
    assert "desk/contexts/pills.md" in board_text


def test_desk_install_is_idempotent(tmp_path: Path, capsys) -> None:
    first = main(["desk", "install", str(tmp_path)])
    first_output = capsys.readouterr()

    second = main(["desk", "install", str(tmp_path)])
    second_output = capsys.readouterr()

    assert first == 0
    assert second == 0
    assert "Wrote" in first_output.out
    assert "Wrote" not in second_output.out


def test_desk_install_rejects_non_directory_target(tmp_path: Path, capsys) -> None:
    target = tmp_path / "not-a-directory.txt"
    target.write_text("placeholder", encoding="utf-8")

    result = main(["desk", "install", str(target)])

    captured = capsys.readouterr()
    assert result == 1
    assert "is not a directory" in captured.out


def test_repo_register_fails_without_store(tmp_path: Path, monkeypatch, capsys) -> None:
    """repo register should fail preflight when no store is available."""
    monkeypatch.setattr(
        "deskops.cli.main.SLDBBootstrap.ensure_machine_ready", lambda self: 0
    )
    monkeypatch.chdir(tmp_path)
    result = main(["repo", "register", "test-repo", str(tmp_path)])
    captured = capsys.readouterr()
    assert result == 1
    assert "Error:" in captured.out


def test_repo_register_fails_with_nonexistent_store(tmp_path: Path, monkeypatch, capsys) -> None:
    """repo register should fail preflight when --store points nowhere."""
    monkeypatch.setattr(
        "deskops.cli.main.SLDBBootstrap.ensure_machine_ready", lambda self: 0
    )
    bad_store = str(tmp_path / "nonexistent" / "store")
    result = main(["repo", "register", "test-repo", str(tmp_path), "--store", bad_store])
    captured = capsys.readouterr()
    assert result == 1
    assert "Error:" in captured.out


def test_init_bootstraps_local_store_and_desk(tmp_path: Path, monkeypatch, capsys) -> None:
    calls: list[Path] = []

    def fake_machine_ready(self) -> int:
        return 0

    def fake_init_local_store(self, target_path: Path) -> int:
        calls.append(target_path)
        (target_path / ".sldb").mkdir()
        print(f"Initialized store at {target_path / '.sldb'}")
        return 0

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", fake_machine_ready)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.init_local_store", fake_init_local_store)

    result = main(["init", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert calls == [tmp_path]
    assert (tmp_path / ".sldb").exists()
    assert (tmp_path / "desk" / "tasks" / "Board.md").exists()
    assert "Initialization complete." in captured.out


def test_bootstrap_command_runs_machine_setup(monkeypatch) -> None:
    called = {"count": 0}

    def fake_machine_ready(self) -> int:
        called["count"] += 1
        return 0

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", fake_machine_ready)

    assert main(["bootstrap"]) == 0
    assert called["count"] == 1


def test_atoms_add_namespace_updates_registry(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "atoms",
            "add-namespace",
            "pattern",
            "--root",
            str(tmp_path),
            "--meaning",
            "Reusable solution shape.",
            "--use-when",
            "The atom describes a repeatable solution.",
            "--do-not-use-when",
            "The atom only mentions a topic.",
            "--example",
            "pattern:roundtrip-validation",
        ]
    )

    captured = capsys.readouterr()
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    assert result == 0
    assert "Added atom tag namespace pattern" in captured.out
    assert registry.exists()
    assert "pattern:" in registry.read_text(encoding="utf-8")


def test_add_atom_does_not_create_orphan_field_instances(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "add",
            "atom",
            "--root",
            str(tmp_path),
            "--title",
            "Atoms stay small",
            "--five-wh-one-plus",
            "what",
            "--answer",
            "An atom answers one raw question.",
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Created atom atom-atoms-stay-small" in captured.out
    assert (tmp_path / "desk" / "atoms" / "atom-atoms-stay-small.md").exists()
    assert not list((tmp_path / "desk" / "fields").glob("field-instance-*.md"))


def test_inbox_uses_local_pythonpath_without_global_bootstrap(monkeypatch) -> None:
    called = {"sldb": 0, "machine": 0}

    class FakeInboxCLI:
        def run(self, args: SimpleNamespace) -> int:
            assert args.pythonpath == str(ROOT)
            called["sldb"] += 1
            return 0

    def fake_sldb_available(self) -> int:
        called["sldb"] += 1
        return 0

    def fake_machine_ready(self) -> int:
        called["machine"] += 1
        return 0

    monkeypatch.setattr("deskops.cli.commands.inbox.InboxCLI", FakeInboxCLI)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", fake_sldb_available)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", fake_machine_ready)

    assert CLI().run(["inbox", "--list"]) == 0
    assert called["machine"] == 0
    assert called["sldb"] == 2


def test_cli_delegates_desk_command_without_bootstrap(monkeypatch) -> None:
    called = {"desk": 0, "bootstrap": 0}

    class FakeDeskCLI:
        def run(self, args: SimpleNamespace) -> int:
            called["desk"] += 1
            assert args.command == "desk"
            return 0

    def fake_machine_ready(self) -> int:
        called["bootstrap"] += 1
        return 0

    monkeypatch.setattr("deskops.cli.commands.desk.DeskCLI", FakeDeskCLI)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", fake_machine_ready)

    assert CLI().run(["desk", "install", str(ROOT)]) == 0
    assert called["desk"] == 1
    assert called["bootstrap"] == 0


def test_add_task_creates_actionable_bundle(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Ship semantic CLI",
            "--goal",
            "Expose semantic task commands through deskops.",
            "--scope",
            "Task management only.",
            "--implementation-path",
            "Create semantic commands over the operational runtime.",
            "--done-when",
            "Task management flows through the new runtime.",
            "--validation",
            "pytest tests/test_cli.py",
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Created task bundle task-ship-semantic-cli" in captured.out
    assert (tmp_path / "desk" / "tasks" / "task-ship-semantic-cli.md").exists()
    assert (tmp_path / "desk" / "routines" / "routine-task-ship-semantic-cli.md").exists()
    assert (
        tmp_path
        / "desk"
        / "primitives"
        / "checklists"
        / "checklist-task-ship-semantic-cli-execution-ready.md"
    ).exists()
    assert (
        tmp_path
        / "desk"
        / "primitives"
        / "operators"
        / "operator-task-ship-semantic-cli-activate.md"
    ).exists()

    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-ship-semantic-cli.md" in board_text


def test_add_task_accepts_json_payload(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "add",
            "task",
            '{"title":"JSON task","goal":"Drive creation from payload.","scope":"Operational runtime only.","implementation_path":"Build from an inline JSON payload.","done_when":"The task bundle can be created from JSON.","validation":["pytest"]}',
            "--root",
            str(tmp_path),
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Created task bundle task-json-task" in captured.out
    assert (tmp_path / "desk" / "tasks" / "task-json-task.md").exists()


def test_show_list_and_advance_task_uses_operational_runtime(tmp_path: Path, capsys) -> None:
    add_result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Advance task runtime",
            "--goal",
            "Operate task state through routines.",
            "--scope",
            "Task state machine only.",
            "--implementation-path",
            "Advance through checklist and operator nodes.",
            "--done-when",
            "The task reaches closed via the runtime.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert add_result == 0

    list_result = main(["list", "tasks", "--root", str(tmp_path)])
    listed = capsys.readouterr()
    assert list_result == 0
    assert "task-advance-task-runtime | draft | checklist-task-advance-task-runtime-execution-ready" in listed.out

    show_result = main(["show", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    shown = capsys.readouterr()
    assert show_result == 0
    assert "Status: draft" in shown.out
    assert "Current node: checklist-task-advance-task-runtime-execution-ready" in shown.out

    first_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    first = capsys.readouterr()
    assert first_advance == 0
    assert "Status: active" in first.out
    assert "Current node: checklist-task-advance-task-runtime-testing-ready" in first.out

    second_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    second = capsys.readouterr()
    assert second_advance == 0
    assert "Status: ready_for_testing" in second.out
    assert "Current node: checklist-task-advance-task-runtime-closeout-ready" in second.out

    third_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    third = capsys.readouterr()
    assert third_advance == 0
    assert "Status: closed" in third.out
    assert "Current node: complete" in third.out


def test_add_and_show_condition_as_first_class_primitive(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "add",
            "condition",
            "--root",
            str(tmp_path),
            "--title",
            "Has goal",
            "--subject",
            "goal",
            "--predicate",
            "truthy",
            "--summary",
            "Goal must exist before activation.",
        ]
    )

    created = capsys.readouterr()
    assert result == 0
    assert "Created condition" in created.out
    assert (tmp_path / "desk" / "primitives" / "conditions" / "condition-has-goal.md").exists()

    show = main(["show", "condition", "condition-has-goal", "--root", str(tmp_path)])
    shown = capsys.readouterr()
    assert show == 0
    assert "Condition: condition-has-goal" in shown.out
    assert "Predicate: truthy" in shown.out


def test_add_list_and_show_routine_from_yaml(tmp_path: Path, capsys) -> None:
    routine_yaml = tmp_path / "routine.yaml"
    routine_yaml.write_text(
        """
title: Release routine
summary: Release workflow.
entrypoint: checklist-release-ready
decomposition:
  - checklist-release-ready
  - operator-release
edges:
  - edge-release-ready-to-operator
terminal_nodes:
  - complete
""".strip()
        + "\n",
        encoding="utf-8",
    )

    create_condition = main(
        [
            "add",
            "condition",
            "--root",
            str(tmp_path),
            "--title",
            "Release approved",
            "--subject",
            "approved",
            "--predicate",
            "truthy",
        ]
    )
    capsys.readouterr()
    assert create_condition == 0

    create_checklist = main(
        [
            "add",
            "checklist",
            "--root",
            str(tmp_path),
            "--title",
            "Release ready",
            "--item",
            "Approval exists",
            "--condition-ref",
            "condition-release-approved",
        ]
    )
    capsys.readouterr()
    assert create_checklist == 0

    create_operator = main(
        [
            "add",
            "operator",
            "--root",
            str(tmp_path),
            "--title",
            "Release",
            "--action",
            "set_field",
            "--target",
            "status",
            "--value",
            "released",
        ]
    )
    capsys.readouterr()
    assert create_operator == 0

    create_edge = main(
        [
            "add",
            "edge",
            "--root",
            str(tmp_path),
            "--title",
            "Release ready to operator",
            "--source",
            "checklist-release-ready",
            "--target-node",
            "operator-release",
        ]
    )
    capsys.readouterr()
    assert create_edge == 0

    create_routine = main(
        [
            "add",
            "routine",
            "--root",
            str(tmp_path),
            "--from-yaml",
            str(routine_yaml),
        ]
    )
    created = capsys.readouterr()
    assert create_routine == 0
    assert "Created routine routine-release-routine" in created.out

    listed = main(["list", "routines", "--root", str(tmp_path)])
    list_output = capsys.readouterr()
    assert listed == 0
    assert "routine-release-routine | active | checklist-release-ready" in list_output.out

    shown = main(["show", "routine", "routine-release-routine", "--root", str(tmp_path)])
    show_output = capsys.readouterr()
    assert shown == 0
    assert "Routine: routine-release-routine" in show_output.out
    assert "Entrypoint: checklist-release-ready" in show_output.out
    assert "edge-release-ready-to-operator" in show_output.out


def test_add_list_and_show_pill_from_specs(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "pill",
            "--root",
            str(tmp_path),
            "--title",
            "Guardrail: Keep layers clean",
            "--what",
            "Separate infra from workflow semantics.",
            "--why",
            "Avoid architectural drift.",
            "--when",
            "When changing workflow code.",
            "--where",
            "Runtime and compiled specs.",
            "--how",
            "Keep opsys logic out of sldb.",
            "--how-not",
            "Do not mix persistence and workflow behavior.",
        ]
    )
    add_out = capsys.readouterr()
    assert created == 0
    assert "Created pill pill-guardrail-keep-layers-clean" in add_out.out
    assert (tmp_path / "desk" / "contexts" / "pill-guardrail-keep-layers-clean.md").exists()
    assert not list((tmp_path / "desk" / "fields").glob("field-instance-*.md"))

    listed = main(["list", "pills", "--root", str(tmp_path)])
    list_out = capsys.readouterr()
    assert listed == 0
    assert "pill-guardrail-keep-layers-clean | Guardrail: Keep layers clean" in list_out.out

    shown = main(["show", "pill", "pill-guardrail-keep-layers-clean", "--root", str(tmp_path)])
    show_out = capsys.readouterr()
    assert shown == 0
    assert "Pill: pill-guardrail-keep-layers-clean" in show_out.out
    assert "what: Separate infra from workflow semantics." in show_out.out


def test_add_list_and_show_ritual_from_specs(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "ritual",
            "--root",
            str(tmp_path),
            "--title",
            "Testing ritual",
            "--purpose",
            "Drive explicit proof before closeout.",
            "--trigger",
            "Execution handoff complete.",
            "--preconditions",
            "Task is active",
            "--steps",
            "Review tests",
            "--steps",
            "Run validation",
            "--validation",
            "pytest",
            "--failure-modes",
            "Skipping validation",
            "--completion",
            "Evidence is ready for closeout.",
        ]
    )
    add_out = capsys.readouterr()
    assert created == 0
    assert "Created ritual ritual-testing-ritual" in add_out.out

    listed = main(["list", "rituals", "--root", str(tmp_path)])
    list_out = capsys.readouterr()
    assert listed == 0
    assert "ritual-testing-ritual | Testing ritual" in list_out.out

    shown = main(["show", "ritual", "ritual-testing-ritual", "--root", str(tmp_path)])
    show_out = capsys.readouterr()
    assert shown == 0
    assert "Ritual: ritual-testing-ritual" in show_out.out
    assert "steps: Review tests, Run validation" in show_out.out


def test_show_atom_finds_nested_atom(tmp_path: Path, capsys) -> None:
    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    capsys.readouterr()
    assert created == 0

    atom_path = tmp_path / "desk" / "atoms" / "atom-trackable-atom.md"
    nested_path = tmp_path / "desk" / "atoms" / "topic" / "atom-trackable-atom.md"
    nested_path.parent.mkdir(parents=True)
    atom_path.rename(nested_path)

    shown = main(["show", "atom", "atom-trackable-atom", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 0
    assert "Atom: atom-trackable-atom" in show_out.out
    assert "Created atoms should be visible through deskops and sldb." in show_out.out


def test_add_atom_tracks_local_sldb_store_when_atomdoc_registered(tmp_path: Path, capsys) -> None:
    from sldb.cli.main import main as sldb_main

    store = tmp_path / ".sldb"
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(
        [
            "models",
            "add",
            "deskops.models:AtomDoc",
            "--store",
            str(store),
            "--pythonpath",
            str(ROOT),
        ]
    ) == 0
    capsys.readouterr()

    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    create_out = capsys.readouterr()
    assert created == 0
    assert "Created atom atom-trackable-atom" in create_out.out

    shown = sldb_main(
        [
            "docs",
            "show",
            "atom-trackable-atom",
            "--store",
            str(store),
            "--pythonpath",
            str(ROOT),
        ]
    )
    sldb_out = capsys.readouterr()

    assert shown == 0
    assert '"name": "atom-trackable-atom"' in sldb_out.out
    assert '"model": "AtomDoc"' in sldb_out.out


def test_add_list_and_show_board_from_specs(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "board",
            "--root",
            str(tmp_path),
            "--title",
            "Main Board",
            "--scope",
            "desk",
            "--purpose",
            "Route active work.",
            "--tasks",
            "desk/tasks/task-a.md",
            "--pills",
            "desk/contexts/pill-a.md",
            "--rituals",
            "desk/rituals/ritual-a.md",
            "--notes",
            "No additional notes.",
        ]
    )
    add_out = capsys.readouterr()
    assert created == 0
    assert "Created board board-main-board" in add_out.out

    listed = main(["list", "boards", "--root", str(tmp_path)])
    list_out = capsys.readouterr()
    assert listed == 0
    assert "board-main-board | Main Board" in list_out.out

    shown = main(["show", "board", "board-main-board", "--root", str(tmp_path)])
    show_out = capsys.readouterr()
    assert shown == 0
    assert "Board: board-main-board" in show_out.out
    assert "scope: desk" in show_out.out


def test_add_list_and_show_repository_from_specs(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "repository",
            "--root",
            str(tmp_path),
            "--name",
            "Opsys",
            "--path",
            "tools/deskops",
            "--status",
            "active",
            "--description",
            "Workflow-domain repository.",
        ]
    )
    add_out = capsys.readouterr()
    assert created == 0
    assert "Created repository repo-opsys" in add_out.out

    listed = main(["list", "repositories", "--root", str(tmp_path)])
    list_out = capsys.readouterr()
    assert listed == 0
    assert "repo-opsys | Opsys" in list_out.out

    shown = main(["show", "repository", "repo-opsys", "--root", str(tmp_path)])
    show_out = capsys.readouterr()
    assert shown == 0
    assert "Repository: repo-opsys" in show_out.out
    assert "name: Opsys" in show_out.out


def test_add_list_and_show_step_from_specs(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "step",
            "--root",
            str(tmp_path),
            "--title",
            "Validate draft",
            "--action",
            "Run validation",
            "--outcome",
            "Promotable draft.",
        ]
    )
    add_out = capsys.readouterr()
    assert created == 0
    assert "Created step step-validate-draft" in add_out.out

    listed = main(["list", "steps", "--root", str(tmp_path)])
    list_out = capsys.readouterr()
    assert listed == 0
    assert "step-validate-draft | Validate draft" in list_out.out

    shown = main(["show", "step", "step-validate-draft", "--root", str(tmp_path)])
    show_out = capsys.readouterr()
    assert shown == 0
    assert "Step: step-validate-draft" in show_out.out
    assert "action: Run validation" in show_out.out
