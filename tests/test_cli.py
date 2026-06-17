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
    assert "{about,faq,bootstrap,init,inbox,promote,add,edit,list,show,advance,repo,desk,atoms,graph}" in captured.out
    assert "Typical flow:" in captured.out
    assert "deskops add task --root ." in captured.out
    assert "Use docs/quickstart.md" in captured.out


def test_core_help_documents_examples_and_selectors(capsys) -> None:
    inbox_help = main(["inbox", "--help"])
    inbox_output = " ".join(capsys.readouterr().out.split())
    assert inbox_help == 0
    assert "deskops inbox" in inbox_output
    assert "--show selector" in inbox_output

    promote_help = main(["promote", "--help"])
    promote_output = " ".join(capsys.readouterr().out.split())
    assert promote_help == 0
    assert "inbox-to-drawer-task" in promote_output
    assert "drawer-task-to-active-task" in promote_output

    show_help = main(["show", "task", "--help"])
    show_output = " ".join(capsys.readouterr().out.split())
    assert show_help == 0
    assert "deskops show task task-fix-thing" in show_output
    assert "exact id, filename, stem, or unique slug fragment" in show_output

    advance_help = main(["advance", "task", "--help"])
    advance_output = " ".join(capsys.readouterr().out.split())
    assert advance_help == 0
    assert "deskops advance task task-fix-thing" in advance_output
    assert "execution, testing, and closeout gates" in advance_output


def test_generated_artifact_help_uses_value_descriptions(capsys) -> None:
    result = main(["add", "pill", "--help"])
    output = capsys.readouterr().out
    assert result == 0
    assert "Title Field" not in output
    assert "Human-readable title." in output
    assert "What this context explains." in output


def test_repository_help_distinguishes_canonical_registration(capsys) -> None:
    repo_help = main(["repo", "register", "--help"])
    repo_output = capsys.readouterr()
    repo_help_text = " ".join(repo_output.out.split())
    assert repo_help == 0
    assert "Canonically register a repository" in repo_help_text
    assert "track it in SLDB" in repo_help_text

    add_help = main(["add", "repository", "--help"])
    add_output = capsys.readouterr()
    add_help_text = " ".join(add_output.out.split())
    assert add_help == 0
    assert "local repository artifact doc" in add_help_text
    assert "canonical ecosystem registration" in add_help_text


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


def test_inbox_writes_sender_project_from_current_directory(tmp_path: Path, monkeypatch, capsys) -> None:
    from deskops.cli.commands.inbox import InboxCLI

    monkeypatch.chdir(tmp_path)
    args = SimpleNamespace(
        list=False,
        show=None,
        message="A message to this project.",
        title="Self message",
        kind="suggestion",
        desk_root=str(tmp_path / "desk"),
        repo=None,
        store=None,
        pythonpath=None,
        limit=20,
        format="text",
    )

    result = InboxCLI().run(args)

    captured = capsys.readouterr()
    notes = list((tmp_path / "desk" / "inbox").glob("*.md"))
    assert result == 0
    assert "Wrote" in captured.out
    assert len(notes) == 1
    assert f"sender_project: {tmp_path.name}" in notes[0].read_text(encoding="utf-8")


def test_inbox_resolves_sender_project_from_repo_store(tmp_path: Path, monkeypatch) -> None:
    from deskops.cli.commands.inbox import InboxCLI

    sender_root = tmp_path / "sender-repo" / "subdir"
    sender_root.mkdir(parents=True)
    monkeypatch.chdir(sender_root)

    def fake_documents(*_args):
        return [
            SimpleNamespace(
                model_name="RepositoryDoc",
                payload={"id": "sender-repo", "name": "Sender Repo", "path": "sender-repo"},
            )
        ]

    monkeypatch.setattr(
        InboxCLI,
        "_store_context",
        lambda self, args: (tmp_path / ".sldb", tmp_path),
    )
    monkeypatch.setattr("sldb.store.query.load_runtime_documents", fake_documents)

    args = SimpleNamespace(store=str(tmp_path / ".sldb"), pythonpath=None)

    assert InboxCLI()._sender_project(args) == "sender-repo"


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


def test_promote_inbox_to_drawer_task_creates_candidate(tmp_path: Path, capsys) -> None:
    inbox_dir = tmp_path / "desk" / "inbox"
    inbox_dir.mkdir(parents=True)
    note = inbox_dir / "20260613-000000-suggestion-need-cli-promotion.md"
    note.write_text(
        "---\nkind: suggestion\nsender_project: sibling\ncreated_at: 2026-06-13T00:00:00\nstatus: open\n---\n\n"
        "# Need CLI promotion\n\nMake promotion explicit.\n",
        encoding="utf-8",
    )

    result = main([
        "promote",
        "inbox-to-drawer-task",
        "need-cli-promotion",
        "--root",
        str(tmp_path),
    ])

    captured = capsys.readouterr()
    drawer_task = tmp_path / "desk" / "drawer" / "tasks" / "task-need-cli-promotion.md"
    assert result == 0
    assert "Created drawer task candidate task-need-cli-promotion" in captured.out
    assert drawer_task.exists()
    text = drawer_task.read_text(encoding="utf-8")
    assert "Make promotion explicit." in text
    assert "desk/inbox/20260613-000000-suggestion-need-cli-promotion.md" in text
    assert not note.exists()


def test_promote_drawer_task_to_active_task_creates_bundle(tmp_path: Path, capsys) -> None:
    drawer_dir = tmp_path / "desk" / "drawer" / "tasks"
    drawer_dir.mkdir(parents=True)
    source = drawer_dir / "task-promote-demo.md"
    source.write_text(
        "# Promote Demo\n\n"
        "ID: task-promote-demo\nStatus: deferred\n\n"
        "## Goal\n\nMake promotion runnable.\n\n"
        "## Scope\n\nPromotion CLI only.\n",
        encoding="utf-8",
    )

    result = main([
        "promote",
        "drawer-task-to-active-task",
        "promote-demo",
        "--root",
        str(tmp_path),
    ])

    captured = capsys.readouterr()
    active_task = tmp_path / "desk" / "tasks" / "task-promote-demo.md"
    assert result == 0
    assert "Created active task bundle task-promote-demo" in captured.out
    assert active_task.exists()
    assert (tmp_path / "desk" / "routines" / "routine-task-promote-demo.md").exists()
    board = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-promote-demo.md" in board
    assert not source.exists()


def test_promote_rejects_ambiguous_inbox_selector(tmp_path: Path, capsys) -> None:
    inbox_dir = tmp_path / "desk" / "inbox"
    inbox_dir.mkdir(parents=True)
    for name in ["20260613-a-suggestion-shared.md", "20260613-b-suggestion-shared.md"]:
        (inbox_dir / name).write_text(f"# {name}\n\nBody.\n", encoding="utf-8")

    result = main(["promote", "inbox-to-drawer-task", "shared", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Ambiguous inbox note selector shared" in captured.out


def test_add_task_creates_actionable_bundle(tmp_path: Path, capsys) -> None:
    result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Ship semantic CLI",
            "--why",
            "Operators need explicit task intent.",
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
    task_text = (tmp_path / "desk" / "tasks" / "task-ship-semantic-cli.md").read_text(
        encoding="utf-8"
    )
    assert "## Rationale" in task_text
    assert "Operators need explicit task intent." in task_text

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


def test_edit_task_updates_modeled_field_from_cli(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Editable task",
            "--goal",
            "Original goal.",
            "--scope",
            "Original scope.",
            "--implementation-path",
            "Original path.",
            "--done-when",
            "Original done when.",
        ]
    )
    capsys.readouterr()
    assert created == 0

    edited = main([
        "edit",
        "task",
        "task-editable-task",
        "implementation-path",
        "Use the modeled edit command.",
        "--root",
        str(tmp_path),
    ])
    edit_out = capsys.readouterr()

    assert edited == 0
    assert "Updated task task-editable-task field implementation_path" in edit_out.out
    task_text = (tmp_path / "desk" / "tasks" / "task-editable-task.md").read_text(encoding="utf-8")
    assert "## Implementation Path" in task_text
    assert "Use the modeled edit command." in task_text
    assert "Original scope." in task_text
    assert not list((tmp_path / "desk" / "fields").glob("field-instance-*.md"))


def test_edit_pill_updates_modeled_field_from_cli(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "pill",
            "--root",
            str(tmp_path),
            "--title",
            "Guardrail: Editable pill",
            "--what",
            "Original what.",
            "--why",
            "Original why.",
            "--when",
            "Original when.",
            "--where",
            "Original where.",
            "--how",
            "Original how.",
            "--how-not",
            "Original how not.",
        ]
    )
    capsys.readouterr()
    assert created == 0

    edited = main([
        "edit",
        "pill",
        "pill-guardrail-editable-pill",
        "how-not",
        "Do not edit raw Markdown for modeled fields.",
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()

    assert edited == 0
    pill_text = (tmp_path / "desk" / "contexts" / "pill-guardrail-editable-pill.md").read_text(encoding="utf-8")
    assert "## How Not" in pill_text
    assert "Do not edit raw Markdown for modeled fields." in pill_text
    assert "Original how." in pill_text


def test_edit_rejects_unknown_task_field(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Unknown field task",
            "--goal",
            "Goal.",
            "--scope",
            "Scope.",
            "--implementation-path",
            "Path.",
            "--done-when",
            "Done.",
        ]
    )
    capsys.readouterr()
    assert created == 0

    edited = main([
        "edit",
        "task",
        "task-unknown-field-task",
        "not-a-field",
        "value",
        "--root",
        str(tmp_path),
    ])
    edit_out = capsys.readouterr()

    assert edited == 1
    assert "Unknown field 'not_a_field' for task" in edit_out.out


def test_edit_rejects_immutable_id_field(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Immutable id task",
            "--goal",
            "Goal.",
            "--scope",
            "Scope.",
            "--implementation-path",
            "Path.",
            "--done-when",
            "Done.",
        ]
    )
    capsys.readouterr()
    assert created == 0

    edited = main(["edit", "task", "task-immutable-id-task", "id", "task-renamed", "--root", str(tmp_path)])
    edit_out = capsys.readouterr()

    assert edited == 1
    assert "Cannot edit immutable field 'id'" in edit_out.out


def test_edit_rejects_ambiguous_task_selector(tmp_path: Path, capsys) -> None:
    tasks_dir = tmp_path / "desk" / "tasks"
    tasks_dir.mkdir(parents=True)
    for task_id in ["task-shared-alpha", "task-shared-beta"]:
        (tasks_dir / f"{task_id}.md").write_text(
            f"---\nid: {task_id}\nstatus: active\nreferences: []\ndepends_on: []\npills: []\nfiles: []\nroutine: \"\"\n"
            "checklists: []\ncurrent_node: \"\"\nhistory: []\ntags: []\n---\n\n"
            f"# {task_id}\n\n## Rationale\n\nWhy.\n\n## Goal\n\nGoal.\n\n## Scope\n\nScope.\n\n"
            "## Implementation Path\n\nPath.\n\n## Validation\n\n- pytest\n\n## Done When\n\nDone.\n",
            encoding="utf-8",
        )

    edited = main(["edit", "task", "task-shared", "goal", "Updated.", "--root", str(tmp_path)])
    edit_out = capsys.readouterr()

    assert edited == 1
    assert "Ambiguous artifact.task selector 'task-shared'" in edit_out.out


def test_edit_rejects_ambiguous_artifact_selector(tmp_path: Path, capsys) -> None:
    atoms_dir = tmp_path / "desk" / "atoms"
    atoms_dir.mkdir(parents=True)
    for atom_id in ["atom-shared-alpha", "atom-shared-beta"]:
        (atoms_dir / f"{atom_id}.md").write_text(
            f"---\nid: {atom_id}\ntitle: {atom_id}\nfive_wh_one_plus: what\ntags: []\n---\n\n"
            f"# {atom_id}\n\n## Answer\n\nAnswer.\n",
            encoding="utf-8",
        )

    edited = main(["edit", "atom", "atom-shared", "answer", "Updated.", "--root", str(tmp_path)])
    edit_out = capsys.readouterr()

    assert edited == 1
    assert "Ambiguous artifact.atom selector 'atom-shared'" in edit_out.out


def test_add_task_reports_invalid_yaml_without_creating_artifacts(tmp_path: Path, capsys) -> None:
    payload = tmp_path / "bad-task.yaml"
    payload.write_text("title: [unterminated\n", encoding="utf-8")

    result = main(["add", "task", "--from-yaml", str(payload), "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Invalid value: Invalid YAML payload" in captured.err
    assert not list((tmp_path / "desk" / "tasks").glob("task-*.md"))
    assert not (tmp_path / "desk" / "routines").exists()


def test_add_task_reports_invalid_json_without_creating_artifacts(tmp_path: Path, capsys) -> None:
    result = main(["add", "task", '{"title": ', "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Invalid value: Invalid JSON payload" in captured.err
    assert not list((tmp_path / "desk" / "tasks").glob("task-*.md"))


def test_add_routine_rejects_non_mapping_yaml_without_creating_artifacts(tmp_path: Path, capsys) -> None:
    payload = tmp_path / "routine.yaml"
    payload.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    result = main(["add", "routine", "--from-yaml", str(payload), "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "must be a mapping/object, got list" in captured.err
    assert not list((tmp_path / "desk" / "routines").glob("routine-*.md"))


@pytest.mark.parametrize(
    ("args", "created_glob"),
    [
        (["add", "condition", "--from-yaml"], "desk/primitives/conditions/*.md"),
        (["add", "pill", "--from-yaml"], "desk/contexts/*.md"),
    ],
)
def test_add_surfaces_reject_non_mapping_yaml(tmp_path: Path, capsys, args: list[str], created_glob: str) -> None:
    payload = tmp_path / "payload.yaml"
    payload.write_text("scalar payload\n", encoding="utf-8")

    result = main([*args, str(payload), "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "must be a mapping/object, got str" in captured.err
    assert not list(tmp_path.glob(created_glob))


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


def test_advance_task_allows_empty_implementation_path(tmp_path: Path, capsys) -> None:
    add_result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Advance without path",
            "--goal",
            "Keep task progression usable.",
            "--scope",
            "Task state machine only.",
            "--done-when",
            "The task can enter active execution.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert add_result == 0

    first_advance = main(["advance", "task", "task-advance-without-path", "--root", str(tmp_path)])
    first = capsys.readouterr()

    assert first_advance == 0
    assert "Status: active" in first.out
    assert "Current node: checklist-task-advance-without-path-testing-ready" in first.out


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


def test_show_atom_accepts_filename_selector(tmp_path: Path, capsys) -> None:
    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    capsys.readouterr()
    assert created == 0

    shown = main(["show", "atom", "atom-trackable-atom.md", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 0
    assert "Atom: atom-trackable-atom" in show_out.out


def test_show_atom_exact_selector_wins_over_prefix(tmp_path: Path, capsys) -> None:
    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    capsys.readouterr()
    assert created == 0
    extra = tmp_path / "desk" / "atoms" / "atom-trackable-atom-extra.md"
    extra.write_text(
        "---\nid: atom-trackable-atom-extra\ntitle: Extra\nfive_wh_one_plus: what\ntags: []\n---\n\n"
        "# Extra\n\n## Answer\n\nExtra atom.\n",
        encoding="utf-8",
    )

    shown = main(["show", "atom", "atom-trackable-atom", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 0
    assert "Atom: atom-trackable-atom" in show_out.out
    assert "Extra atom" not in show_out.out


def test_show_atom_prefix_fallback_finds_single_match(tmp_path: Path, capsys) -> None:
    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    capsys.readouterr()
    assert created == 0

    shown = main(["show", "atom", "atom-trackable", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 0
    assert "Atom: atom-trackable-atom" in show_out.out


def test_show_atom_rejects_duplicate_nested_exact_matches(tmp_path: Path, capsys) -> None:
    created = main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS])
    capsys.readouterr()
    assert created == 0
    atom_path = tmp_path / "desk" / "atoms" / "atom-trackable-atom.md"
    nested_path = tmp_path / "desk" / "atoms" / "topic" / "atom-trackable-atom.md"
    nested_path.parent.mkdir(parents=True)
    nested_path.write_text(atom_path.read_text(encoding="utf-8"), encoding="utf-8")

    shown = main(["show", "atom", "atom-trackable-atom", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 1
    assert "Ambiguous artifact.atom selector 'atom-trackable-atom'" in show_out.out
    assert "atom-trackable-atom.md" in show_out.out
    assert "topic/atom-trackable-atom.md" in show_out.out


def test_show_atom_rejects_ambiguous_prefix_matches(tmp_path: Path, capsys) -> None:
    atoms_dir = tmp_path / "desk" / "atoms"
    atoms_dir.mkdir(parents=True)
    for atom_id in ["atom-shared-alpha", "atom-shared-beta"]:
        (atoms_dir / f"{atom_id}.md").write_text(
            f"---\nid: {atom_id}\ntitle: {atom_id}\nfive_wh_one_plus: what\ntags: []\n---\n\n"
            f"# {atom_id}\n\n## Answer\n\nAnswer.\n",
            encoding="utf-8",
        )

    shown = main(["show", "atom", "atom-shared", "--root", str(tmp_path)])
    show_out = capsys.readouterr()

    assert shown == 1
    assert "Ambiguous artifact.atom selector 'atom-shared'" in show_out.out


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
    assert "Use 'deskops repo register' for canonical ecosystem registration." in add_out.out

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
