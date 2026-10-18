from __future__ import annotations

import json
from pathlib import Path
import subprocess
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
from deskops.constants import CURRENT_DESK_FORMAT
from deskops.models import InboxNoteDoc
from deskops.models import RepositoryDoc
from deskops.workspace import classify_desk
from sldb.runtime.validation import render_model_markdown


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
    assert "{about,doctor,status,faq,bootstrap,init,inbox,message,promote,drawer,add,edit,bind,next,list,show,advance,repo,desk,atoms,graph,materialize,drift,closeout,runtime}" in captured.out
    assert "Typical flow:" in captured.out
    assert "deskops add task --root ." in captured.out
    assert "Use docs/quickstart.md" in captured.out


def test_core_help_documents_examples_and_selectors(capsys) -> None:
    inbox_help = main(["inbox", "--help"])
    inbox_output = " ".join(capsys.readouterr().out.split())
    assert inbox_help == 0
    assert "deskops inbox" in inbox_output
    assert "--show/--ack selector" in inbox_output

    promote_help = main(["promote", "--help"])
    promote_output = " ".join(capsys.readouterr().out.split())
    assert promote_help == 0
    assert "inbox-to-drawer-task" in promote_output
    assert "drawer-task-to-active-task" not in promote_output

    show_help = main(["show", "task", "--help"])
    show_output = " ".join(capsys.readouterr().out.split())
    assert show_help == 0
    assert "deskops show task task-fix-thing" in show_output
    assert "exact id, filename, stem, or unique slug fragment" in show_output

    advance_help = main(["advance", "task", "--help"])
    advance_output = " ".join(capsys.readouterr().out.split())
    assert advance_help == 0
    assert "deskops advance task task-fix-thing" in advance_output
    assert "lifecycle transition" in advance_output


def test_generated_artifact_help_uses_model_descriptions(capsys) -> None:
    # Help text now comes from Pydantic field descriptions (model as single source of truth),
    # not from YAML spec FIELD_HELP_OVERRIDES.
    result = main(["add", "pill", "--help"])
    output = capsys.readouterr().out
    assert result == 0
    assert "Title Field" not in output
    # Help text from PillDoc field descriptions
    assert "Pill title" in output
    assert "What the pill defines" in output  # --what help text
    # tags is now exposed (was missing before model-as-source-of-truth fix)
    assert "--tags" in output


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
        tmp_path / "desk" / "rituals" / "phase.md",
        tmp_path / "desk" / "rituals" / "execution.md",
        tmp_path / "desk" / "rituals" / "testing.md",
        tmp_path / "desk" / "rituals" / "closeout.md",
        tmp_path / "desk" / "inbox",
        tmp_path / "desk" / "drawer" / "README.md",
        tmp_path / "desk" / "atoms",
        tmp_path / "desk" / "atoms" / "tag-namespaces.yaml",
        tmp_path / "desk" / "roles",
    ]
    for path in expected_paths:
        assert path.exists()

    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/rituals/execution.md" in board_text
    assert "desk/contexts/pills.md" in board_text
    # The board is rendered by its model, so the model can read it back and an
    # update cannot blank the fields it declares.
    from deskops.doc_readability import is_unreadable_by_model
    from deskops.models import BoardDoc

    assert is_unreadable_by_model(BoardDoc, board_text) == []


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


def _write_legacy_desk_fixture(root: Path) -> tuple[Path, Path, bytes, bytes]:
    board = root / "desk" / "tasks" / "Board.md"
    task = root / "desk" / "tasks" / "task-legacy-demo.md"
    board.parent.mkdir(parents=True, exist_ok=True)
    board.write_text(
        "# Legacy Board\n\nThis is an authored board without modeled frontmatter.\n",
        encoding="utf-8",
    )
    task.write_text(
        "# Legacy Task\n\nThis is an authored task without modeled frontmatter.\n",
        encoding="utf-8",
    )
    return board, task, board.read_bytes(), task.read_bytes()


@pytest.mark.parametrize(
    ("setup", "expected"),
    [
        (lambda root: None, "absent"),
        (lambda root: (root / "desk").mkdir(parents=True, exist_ok=True), "empty"),
        (_write_legacy_desk_fixture, "legacy"),
        (lambda root: main(["desk", "install", str(root)]), "current"),
    ],
)
def test_classify_desk_distinguishes_workspace_states(tmp_path: Path, setup, expected: str) -> None:
    root = tmp_path / expected
    root.mkdir()
    setup(root)
    assert classify_desk(root) == expected


def test_doctor_reports_legacy_desk_with_missing_config(tmp_path: Path, capsys) -> None:
    root = tmp_path / "legacy-project"
    root.mkdir()
    _write_legacy_desk_fixture(root)

    result = main(["doctor", "--root", str(root)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Doctor Findings:" in captured.out
    assert "Legacy desk detected: desk/config.json" in captured.out
    assert "Run with --repair to attempt automatic fixes." in captured.out


def test_desk_migrate_preserves_authored_legacy_files_and_scaffolds_missing_surfaces(tmp_path: Path, capsys) -> None:
    root = tmp_path / "legacy-project"
    root.mkdir()
    board, task, board_before, task_before = _write_legacy_desk_fixture(root)

    result = main(["desk", "migrate", "--root", str(root)])

    captured = capsys.readouterr()
    assert result == 0
    assert board.read_bytes() == board_before
    assert task.read_bytes() == task_before
    assert (root / "desk" / "contexts" / "pills.md").exists()
    config = json.loads((root / "desk" / "config.json").read_text(encoding="utf-8"))
    assert config["versions"]["desk_format"] == CURRENT_DESK_FORMAT
    assert classify_desk(root) == "current"
    assert "Adopted:" in captured.out
    assert "- desk/config.json" in captured.out
    assert "- desk/contexts/pills.md" in captured.out
    assert "Preserved:" in captured.out
    assert f"- {board.relative_to(root)}" in captured.out
    assert f"- {task.relative_to(root)}" in captured.out
    assert "Still manual:" in captured.out
    assert "manual model conversion or sldb docs track required" in captured.out


def test_desk_migrate_patches_unrecognized_desk_format_without_overwriting_board(tmp_path: Path, capsys) -> None:
    root = tmp_path / "format-project"
    root.mkdir()
    assert main(["desk", "install", str(root)]) == 0
    capsys.readouterr()
    board = root / "desk" / "tasks" / "Board.md"
    board_before = board.read_bytes()
    (root / "desk" / "config.json").write_text(
        json.dumps({"project_identity": "format-project", "versions": {"desk_format": "0.1.0"}}, indent=2) + "\n",
        encoding="utf-8",
    )

    assert classify_desk(root) == "legacy"
    result = main(["desk", "migrate", "--root", str(root)])
    captured = capsys.readouterr()

    config = json.loads((root / "desk" / "config.json").read_text(encoding="utf-8"))
    assert result == 0
    assert config["versions"]["desk_format"] == CURRENT_DESK_FORMAT
    assert board.read_bytes() == board_before
    assert "desk/config.json (patched desk_format)" in captured.out


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
    monkeypatch.setattr("deskops.lifecycle.ensure_lifecycle_graph", lambda root: [])

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


def test_message_uses_local_pythonpath_without_global_bootstrap(monkeypatch) -> None:
    called = {"sldb": 0, "machine": 0}

    class FakeMessageCLI:
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

    monkeypatch.setattr("deskops.cli.commands.message.MessageCLI", FakeMessageCLI)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", fake_sldb_available)
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", fake_machine_ready)

    assert CLI().run(["message", "list"]) == 0
    assert called["machine"] == 0
    assert called["sldb"] == 2


def _write_repo_doc(registry_dir: Path, *, repo_id: str, repo_path: str, name: str | None = None) -> None:
    payload = {
        "id": repo_id,
        "name": name or repo_id,
        "path": repo_path,
        "status": "active",
        "description": f"Repository for {repo_id}.",
        "tags": [],
    }
    (registry_dir / f"repo-{repo_id}.md").write_text(
        render_model_markdown(RepositoryDoc, payload) + "\n",
        encoding="utf-8",
    )



def _write_desk_config(repo_root: Path, project_identity: str) -> None:
    (repo_root / "desk").mkdir(parents=True, exist_ok=True)
    (repo_root / "desk" / "config.json").write_text(
        json.dumps({"project_identity": project_identity}, indent=2) + "\n",
        encoding="utf-8",
    )



def _setup_inbox_identity_env(tmp_path: Path, monkeypatch) -> tuple[Path, Path, Path]:
    registry_dir = tmp_path / "desk" / "registry"
    registry_dir.mkdir(parents=True)
    sender_repo = tmp_path / "sender-repo"
    target_repo = tmp_path / "target-repo"
    _write_desk_config(sender_repo, "sender-repo")
    _write_desk_config(target_repo, "target-repo")
    _write_repo_doc(registry_dir, repo_id="sender-repo", repo_path="sender-repo", name="Sender Repo")
    _write_repo_doc(registry_dir, repo_id="target-repo", repo_path="target-repo", name="Target Repo")

    store_path = tmp_path / ".sldb"
    tracked: list[str] = []

    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)
    monkeypatch.setattr("deskops.identity.get_store_context", lambda _arg: (store_path, tmp_path))
    monkeypatch.setattr("deskops.cli.commands.message.get_store_context", lambda _arg: (store_path, tmp_path))
    monkeypatch.setattr(
        "deskops.cli.commands.message.registered_model",
        lambda store, name, pythonpath: (InboxNoteDoc, object(), "idx"),
    )

    def fake_track_document(store_path_arg, root, idx, model_type, entry, path, note_name, resolver, pythonpath):
        tracked.append(note_name)

    monkeypatch.setattr("deskops.cli.commands.message.track_document", fake_track_document)
    return sender_repo, target_repo, store_path



def test_inbox_delivery_returns_verification_result_json(tmp_path: Path, monkeypatch, capsys) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)

    result = main(
        [
            "inbox",
            "A message to this project.",
            "--title",
            "Cross desk message",
            "--kind",
            "suggestion",
            "--repo",
            "target-repo",
            "--store",
            str(store_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    notes = list((target_repo / "desk" / "inbox").glob("*.md"))
    assert result == 0
    assert payload["sender_project"] == "sender-repo"
    assert payload["target_project"] == "target-repo"
    assert payload["verified"] is True
    assert len(notes) == 1
    note_text = notes[0].read_text(encoding="utf-8")
    assert "sender_project: sender-repo" in note_text
    assert "target_project: target-repo" in note_text



def test_inbox_resolves_sender_project_from_repo_store(tmp_path: Path, monkeypatch) -> None:
    from deskops.cli.commands.message import MessageCLI

    sender_repo, _target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    sender_subdir = sender_repo / "subdir"
    sender_subdir.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(sender_subdir)

    args = SimpleNamespace(store=str(store_path), pythonpath=None, sender=None)

    assert MessageCLI()._sender_project(args) == "sender-repo"



def test_inbox_fails_when_sender_identity_is_unresolvable(tmp_path: Path, monkeypatch, capsys) -> None:
    _sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    unknown_repo = tmp_path / "unknown-repo"
    unknown_repo.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(unknown_repo)

    result = main(
        [
            "inbox",
            "A message without a resolvable sender.",
            "--title",
            "Unknown sender",
            "--desk-root",
            str(target_repo / "desk"),
            "--store",
            str(store_path),
        ]
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "Unable to resolve sender identity" in captured.out



def test_inbox_ack_flips_status_and_records_metadata(tmp_path: Path, monkeypatch, capsys) -> None:
    sender_repo, target_repo, store_path = _setup_inbox_identity_env(tmp_path, monkeypatch)
    monkeypatch.chdir(sender_repo)
    assert main(
        [
            "inbox",
            "Please acknowledge this note.",
            "--title",
            "Ack me",
            "--repo",
            "target-repo",
            "--store",
            str(store_path),
        ]
    ) == 0
    capsys.readouterr()

    note = next((target_repo / "desk" / "inbox").glob("*.md"))
    monkeypatch.chdir(target_repo)
    result = main(
        [
            "inbox",
            "--ack",
            note.stem,
            "--desk-root",
            str(target_repo / "desk"),
            "--store",
            str(store_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    note_text = note.read_text(encoding="utf-8")
    assert result == 0
    assert payload["status"] == "closed"
    assert payload["acknowledged_by"] == "target-repo"
    assert payload["target_project"] == "target-repo"
    assert "status: closed" in note_text
    assert "acknowledged_by: target-repo" in note_text
    assert "acknowledged_at:" in note_text


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
    assert not (tmp_path / "desk" / "routines").exists(), "the lifecycle is the desk's graph, not per-task routines"
    assert not (tmp_path / "desk" / "primitives").exists()
    task_text = (tmp_path / "desk" / "tasks" / "task-ship-semantic-cli.md").read_text(
        encoding="utf-8"
    )
    assert "## Rationale" in task_text
    assert "Operators need explicit task intent." in task_text

    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-ship-semantic-cli.md" in board_text


def test_add_task_tracks_generated_bundle_in_local_sldb_store(tmp_path: Path, capsys) -> None:
    from sldb.cli.main import main as sldb_main

    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Track bundle",
            "--goal",
            "Persist generated bundle docs in the store.",
            "--scope",
            "Task bundle creation only.",
            "--implementation-path",
            "Track task bundle docs right after creation.",
            "--validation",
            "pytest tests/test_cli.py -q",
        ]
    )
    create_out = capsys.readouterr()
    assert created == 0
    assert "Created task bundle task-track-bundle" in create_out.out

    for doc_id, model_name in [
        ("task-track-bundle", "TaskDoc"),
        ("ritual-execution", "RitualDoc"),
        ("execution-task_activates", "RelationDoc"),
        ("type-task_activates", "RelationTypeDoc"),
    ]:
        shown = sldb_main(
            [
                "docs",
                "show",
                doc_id,
                "--store",
                str(tmp_path / ".sldb"),
                "--pythonpath",
                str(ROOT),
            ]
        )
        sldb_out = capsys.readouterr()
        assert shown == 0
        assert f'"name": "{doc_id}"' in sldb_out.out
        assert f'"model": "{model_name}"' in sldb_out.out


def test_add_task_uses_test_root_override_for_sandboxed_generation(tmp_path: Path, monkeypatch, capsys) -> None:
    sandbox_root = tmp_path / ".tmp" / "deskops-cli-test"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DESKOPS_TEST_ROOT", str(sandbox_root))

    result = main(
        [
            "add",
            "task",
            "--title",
            "Sandboxed test task",
            "--goal",
            "Keep exploratory CLI output out of the repo desk.",
            "--scope",
            "Only the sandbox root.",
            "--implementation-path",
            "Route default writes through a test desk.",
            "--done-when",
            "Generated task docs land under .tmp.",
            "--validation",
            "pytest",
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert str(sandbox_root / "desk" / "tasks" / "task-sandboxed-test-task.md") in captured.out
    assert (sandbox_root / "desk" / "tasks" / "task-sandboxed-test-task.md").exists()
    assert not (tmp_path / "desk" / "tasks" / "task-sandboxed-test-task.md").exists()


def test_next_task_reports_current_workflow_action_without_mutating(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Plan next action",
            "--goal",
            "Explain what to do next.",
            "--scope",
            "Read-only workflow state.",
            "--implementation-path",
            "deskops/workflow/next_actions.py",
            "--done-when",
            "Next action is visible.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert created == 0
    task_path = tmp_path / "desk" / "tasks" / "task-plan-next-action.md"
    before = task_path.read_text(encoding="utf-8")

    result = main(["next", "task-plan-next-action", "--root", str(tmp_path)])
    output = capsys.readouterr()

    assert result == 0
    assert "Task: task-plan-next-action" in output.out
    assert "Phase: execution" in output.out
    assert "Required ritual:" in output.out
    assert "desk/rituals/execution.md" in output.out
    assert "Next actions:" in output.out
    assert "Run a fresh-context subagent review." in output.out
    assert "Sources:" in output.out
    assert "deskops/spec/workflows/task_lifecycle.yaml" in output.out
    assert task_path.read_text(encoding="utf-8") == before


def test_next_diagram_renders_workflow_graph_from_spec(capsys) -> None:
    result = main(["next", "--diagram"])
    output = capsys.readouterr()

    assert result == 0
    assert "flowchart TD" in output.out
    assert 'execution_gate -->|"task_activates"| testing_gate' in output.out
    assert 'testing_gate -->|"task_hands_to_closeout: nonempty(validation)"| closeout_gate' in output.out
    assert "closeout_gate -->|" in output.out and "| complete" in output.out


def test_list_tasks_warns_on_malformed_artifact(tmp_path: Path, capsys) -> None:
    main(["init", str(tmp_path)])
    task_dir = tmp_path / "desk" / "tasks"
    malformed_task = task_dir / "task-malformed.md"
    malformed_task.write_text("---\ninvalid yaml\n---", encoding="utf-8")

    main(["list", "tasks", "--root", str(tmp_path)])
    captured = capsys.readouterr()
    assert "Warning: Failed to load task" in captured.err
    assert "task-malformed.md" in captured.err


def test_list_tasks_include_repos_routes_registered_repo_board(tmp_path: Path, capsys) -> None:
    registered = main(
        [
            "add",
            "repository",
            "--root",
            str(tmp_path),
            "--name",
            "Sibling Repo",
            "--path",
            "sibling",
            "--description",
            "Sibling project.",
        ]
    )
    capsys.readouterr()
    assert registered == 0

    sibling_tasks = tmp_path / "sibling" / "desk" / "tasks"
    sibling_tasks.mkdir(parents=True)
    (sibling_tasks / "Board.md").write_text(
        """---
id: board-sibling
scope: desk
tasks:
- desk/tasks/task-sibling-demo.md
pills: []
rituals: []
tags: []
---

# Sibling Board

## Purpose

Route sibling work.

## Notes

None.
""",
        encoding="utf-8",
    )
    (sibling_tasks / "task-sibling-demo.md").write_text(
        """---
id: task-sibling-demo
status: active
---

# Sibling demo

## Goal

Prove routed sibling task discovery.
""",
        encoding="utf-8",
    )

    listed = main(["list", "tasks", "--root", str(tmp_path), "--include-repos"])
    list_out = capsys.readouterr()

    assert listed == 0
    assert "repo-sibling-repo:task-sibling-demo | active | Sibling demo" in list_out.out
    assert str(sibling_tasks / "task-sibling-demo.md") in list_out.out


def test_list_tasks_include_repos_skips_board_refs_outside_repo_tasks(tmp_path: Path, capsys) -> None:
    registered = main(
        [
            "add",
            "repository",
            "--root",
            str(tmp_path),
            "--name",
            "Sibling Repo",
            "--path",
            "sibling",
            "--description",
            "Sibling project.",
        ]
    )
    capsys.readouterr()
    assert registered == 0

    sibling_root = tmp_path / "sibling"
    sibling_tasks = sibling_root / "desk" / "tasks"
    sibling_tasks.mkdir(parents=True)
    secret = sibling_root / "secret.md"
    secret.write_text("# Secret\n", encoding="utf-8")
    bad_dir = sibling_tasks / "task-directory.md"
    bad_dir.mkdir()
    (sibling_tasks / "Board.md").write_text(
        f"""---
id: board-sibling
scope: desk
tasks:
- {secret}
- desk/tasks/Board.md
- desk/secret.md
- desk/tasks/task-directory.md
pills: []
rituals: []
tags: []
---

# Sibling Board
""",
        encoding="utf-8",
    )

    listed = main(["list", "tasks", "--root", str(tmp_path), "--include-repos"])
    list_out = capsys.readouterr()

    assert listed == 0
    assert "Secret" not in list_out.out
    assert "Sibling Board" not in list_out.out
    assert "task-directory" not in list_out.out


def test_list_tasks_include_repos_supports_json_output(tmp_path: Path, capsys) -> None:
    registered = main(
        [
            "add",
            "repository",
            "--root",
            str(tmp_path),
            "--name",
            "Sibling Repo",
            "--path",
            "sibling",
            "--description",
            "Sibling project.",
        ]
    )
    capsys.readouterr()
    assert registered == 0

    sibling_tasks = tmp_path / "sibling" / "desk" / "tasks"
    sibling_tasks.mkdir(parents=True)
    (sibling_tasks / "Board.md").write_text(
        """---
id: board-sibling
scope: desk
tasks:
- desk/tasks/task-sibling-demo.md
pills: []
rituals: []
tags: []
---

# Sibling Board
""",
        encoding="utf-8",
    )
    task_path = sibling_tasks / "task-sibling-demo.md"
    task_path.write_text(
        """---
id: task-sibling-demo
status: active
---

# Sibling demo
""",
        encoding="utf-8",
    )

    listed = main(["list", "tasks", "--root", str(tmp_path), "--include-repos", "--format", "json"])
    list_out = capsys.readouterr()

    assert listed == 0
    payload = json.loads(list_out.out)
    assert payload["tasks"] == []
    assert payload["repo_routes"] == [
        {
            "repo_id": "repo-sibling-repo",
            "repo_root": str((tmp_path / "sibling").resolve()),
            "task_id": "task-sibling-demo",
            "task_path": str(task_path),
            "board_path": str(sibling_tasks / "Board.md"),
            "title": "Sibling demo",
            "status": "active",
        }
    ]


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


def test_edit_task_resolves_tracked_task_with_legacy_file_name(tmp_path: Path, capsys) -> None:
    assert main(["init", str(tmp_path)]) == 0
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Legacy task",
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
    assert created == 0
    # Simulate a task written before the `task-*` naming: same tracked document, older file name.
    tasks = tmp_path / "desk" / "tasks"
    (tasks / "task-legacy-task.md").rename(tasks / "001-legacy-task.md")
    record = tmp_path / ".sldb" / "core" / "documents" / "TaskDoc" / "task-legacy-task.yaml"
    record.write_text(
        record.read_text(encoding="utf-8").replace(
            "path: desk/tasks/task-legacy-task.md", "path: desk/tasks/001-legacy-task.md"
        ),
        encoding="utf-8",
    )
    (tasks / "notes.md").write_text("# Not a task\n", encoding="utf-8")
    capsys.readouterr()

    edited = main(["edit", "task", "001-legacy-task", "goal", "Edited goal.", "--root", str(tmp_path)])
    capsys.readouterr()
    untracked = main(["edit", "task", "notes", "goal", "Nope.", "--root", str(tmp_path)])
    capsys.readouterr()

    assert edited == 0
    assert "Edited goal." in (tasks / "001-legacy-task.md").read_text(encoding="utf-8")
    assert untracked != 0


def test_edit_task_refuses_to_erase_undeclared_content(tmp_path: Path, capsys) -> None:
    assert main(["init", str(tmp_path)]) == 0
    created = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Hand written task",
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
    assert created == 0
    task_path = tmp_path / "desk" / "tasks" / "task-hand-written-task.md"
    hand_written = task_path.read_text(encoding="utf-8").replace(
        "## Goal", "## Out of scope\n\nNever touch prod.\n\n## Goal", 1
    )
    task_path.write_text(hand_written, encoding="utf-8")
    capsys.readouterr()

    edited = main(["edit", "task", "task-hand-written-task", "goal", "New goal.", "--root", str(tmp_path)])
    output = capsys.readouterr()

    assert edited != 0
    assert "## Out of scope" in output.out + output.err
    assert task_path.read_text(encoding="utf-8") == hand_written

    with_key = task_path.read_text(encoding="utf-8").replace(
        "## Out of scope\n\nNever touch prod.\n\n", "", 1
    ).replace("---\nid:", "---\npriority: p0\nid:", 1)
    task_path.write_text(with_key, encoding="utf-8")
    capsys.readouterr()

    edited = main(["edit", "task", "task-hand-written-task", "goal", "New goal.", "--root", str(tmp_path)])
    output = capsys.readouterr()

    assert edited != 0
    assert "priority" in output.out + output.err
    assert task_path.read_text(encoding="utf-8") == with_key


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


def test_bind_pill_appends_task_pills_list_from_cli(tmp_path: Path, capsys) -> None:
    created_task = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Bindable task",
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
    assert created_task == 0

    created_pill = main(
        [
            "add",
            "pill",
            "--root",
            str(tmp_path),
            "--title",
            "Guardrail: Bound pill",
            "--what",
            "What.",
            "--why",
            "Why.",
            "--when",
            "When.",
            "--where",
            "Where.",
            "--how",
            "How.",
            "--how-not",
            "How not.",
        ]
    )
    capsys.readouterr()
    assert created_pill == 0

    bound = main([
        "bind",
        "pill",
        "task-bindable-task",
        "pill-guardrail-bound-pill",
        "--root",
        str(tmp_path),
    ])
    bound_out = capsys.readouterr()

    assert bound == 0
    assert "Bound pill desk/contexts/pill-guardrail-bound-pill.md to task task-bindable-task" in bound_out.out
    task_text = (tmp_path / "desk" / "tasks" / "task-bindable-task.md").read_text(encoding="utf-8")
    assert "pills:\n- desk/contexts/pill-guardrail-bound-pill.md" in task_text

    rebound = main([
        "bind",
        "pill",
        "task-bindable-task",
        "pill-guardrail-bound-pill",
        "--root",
        str(tmp_path),
    ])
    rebound_out = capsys.readouterr()

    assert rebound == 0
    assert "Already bound pill desk/contexts/pill-guardrail-bound-pill.md to task task-bindable-task" in rebound_out.out
    assert task_text == (tmp_path / "desk" / "tasks" / "task-bindable-task.md").read_text(encoding="utf-8")



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


def test_show_task_json_resolves_inherited_workflow_context(tmp_path: Path, capsys) -> None:
    from deskops.models import TaskDoc
    from sldb.runtime.validation import render_model_markdown

    tasks_dir = tmp_path / "desk" / "tasks"
    tasks_dir.mkdir(parents=True)
    parent = tasks_dir / "task-parent.md"
    child = tasks_dir / "task-child.md"
    parent.write_text(
        render_model_markdown(
            TaskDoc,
            {
                "id": "task-parent",
                "title": "Parent",
                "status": "active",
                "why": "Why.",
                "goal": "Parent goal.",
                "scope": "Parent scope.",
                "references": ["docs/parent.md"],
                "depends_on": [],
                "pills": ["desk/contexts/pill-parent.md"],
                "files": [],
                "routine": "",
                "checklists": [],
                "current_node": "",
                "history": [],
                "implementation_path": "Parent path.",
                "validation": ["pytest parent"],
                "done_when": "Parent done.",
                "tags": ["tag:parent"],
                "task_type": "design",
                "inherits_from": [],
                "inherit_acceptance_context": False,
                "atoms": ["desk/atoms/atom-parent.md"],
            },
        ),
        encoding="utf-8",
    )
    child.write_text(
        render_model_markdown(
            TaskDoc,
            {
                "id": "task-child",
                "title": "Child",
                "status": "active",
                "why": "Why.",
                "goal": "Child goal.",
                "scope": "Child scope.",
                "references": ["docs/child.md"],
                "depends_on": [],
                "pills": ["desk/contexts/pill-child.md"],
                "files": [],
                "routine": "",
                "checklists": [],
                "current_node": "",
                "history": [],
                "implementation_path": "Child path.",
                "validation": ["pytest child"],
                "done_when": "Child done.",
                "tags": ["tag:child"],
                "task_type": "implementation",
                "inherits_from": ["task-parent"],
                "inherit_acceptance_context": True,
                "atoms": ["desk/atoms/atom-child.md"],
            },
        ),
        encoding="utf-8",
    )

    result = main(["show", "task", "task-child", "--root", str(tmp_path), "--format", "json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert result == 0
    assert payload["task_type"] == "implementation"
    assert payload["inherits_from"] == ["task-parent"]
    assert payload["effective_pills"] == ["desk/contexts/pill-parent.md", "desk/contexts/pill-child.md"]
    assert payload["effective_atoms"] == ["desk/atoms/atom-parent.md", "desk/atoms/atom-child.md"]
    assert payload["effective_validation"] == ["pytest parent", "pytest child"]
    assert payload["effective_done_when"] == "Child done."


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


@pytest.mark.parametrize(
    ("args", "created_glob"),
    [
        (
            [
                "add", "pill",
                "--what", "W", "--why", "Y", "--when", "T",
                "--where", "L", "--how", "H", "--how-not", "N",
            ],
            "desk/contexts/*.md",
        ),
    ],
)
def test_add_surfaces_reject_non_mapping_yaml(
    tmp_path: Path, capsys, args: list[str], created_glob: str
) -> None:
    # Note: pill args must provide all required fields (--what, --why, etc.).
    # --from-yaml comes at the end so str(payload) is its value.
    yaml_flag = "--from-yaml"
    cmd_args = [a for a in args if a != yaml_flag]
    payload = tmp_path / "payload.yaml"
    payload.write_text("scalar payload\n", encoding="utf-8")

    cmd = [*cmd_args, yaml_flag, str(payload), "--root", str(tmp_path)]
    result = main(cmd)

    captured = capsys.readouterr()
    assert result == 1
    assert "must be a mapping/object, got str" in captured.err
    assert not list(tmp_path.glob(created_glob))


def test_show_list_and_advance_task_uses_operational_runtime(lifecycle_desk: Path, capsys) -> None:
    tmp_path = lifecycle_desk
    import subprocess
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=tmp_path)
    subprocess.run(['git', 'commit', '--allow-empty', '-q', '-m', 'seed'], cwd=tmp_path)
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
    # The task is committed before work starts, as the desk workflow requires.
    subprocess.run(['git', 'add', '-A'], cwd=tmp_path, check=True)
    subprocess.run(['git', 'commit', '-q', '-m', 'add task'], cwd=tmp_path, check=True)

    list_result = main(["list", "tasks", "--root", str(tmp_path)])
    listed = capsys.readouterr()
    assert list_result == 0
    assert "task-advance-task-runtime | draft | ritual-execution" in listed.out

    show_result = main(["show", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    shown = capsys.readouterr()
    assert show_result == 0
    assert "Status: draft" in shown.out
    assert "Current node: ritual-execution" in shown.out

    first_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    first = capsys.readouterr()
    assert first_advance == 0
    assert "Status: active" in first.out
    assert "Current node: ritual-testing" in first.out

    second_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    second = capsys.readouterr()
    assert second_advance == 0
    assert "Status: ready_for_testing" in second.out
    assert "Current node: ritual-closeout" in second.out

    blocked_advance = main(["advance", "task", "task-advance-task-runtime", "--root", str(tmp_path)])
    blocked = capsys.readouterr()
    assert blocked_advance == 1
    assert "Status: ready_for_testing" in blocked.out
    assert "Current node: ritual-closeout" in blocked.out
    assert "Message: Gate ritual-closeout is not complete" in blocked.out

    runtime_test = tmp_path / "tests" / "test_runtime.py"
    runtime_test.parent.mkdir(parents=True, exist_ok=True)
    runtime_test.write_text("def test_runtime():\n    assert True\n", encoding="utf-8")
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS]) == 0
    capsys.readouterr()
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()

    evidence_edit = main([
        "edit",
        "task",
        "task-advance-task-runtime",
        "references",
        f'["desk/atoms/atom-trackable-atom.md", "pytest tests/test_runtime.py::test_runtime", "{commit}"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert evidence_edit == 0
    files_edit = main([
        "edit",
        "task",
        "task-advance-task-runtime",
        "files",
        '["desk/atoms/atom-trackable-atom.md"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert files_edit == 0

    closed = main([
        "closeout", "commit", "--root", str(tmp_path),
        "--task", "task-advance-task-runtime",
        "--no-run", "--reason", "Runtime smoke test",
        "--paths", "desk/atoms/atom-trackable-atom.md", "tests/test_runtime.py",
    ])
    close_out = capsys.readouterr()
    assert closed == 0
    assert "Closing commit " in close_out.out
    assert not (tmp_path / "desk" / "tasks" / "task-advance-task-runtime.md").exists()
    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-advance-task-runtime.md" not in board_text



def test_list_and_show_task_support_json_output(lifecycle_desk: Path, capsys) -> None:
    tmp_path = lifecycle_desk
    add_result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "JSON task output",
            "--goal",
            "Expose task data through the CLI.",
            "--scope",
            "Task list/show surfaces only.",
            "--implementation-path",
            "Serialize the modeled task payload.",
            "--done-when",
            "The CLI returns parseable task JSON.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert add_result == 0

    listed = main(["list", "tasks", "--root", str(tmp_path), "--format", "json"])
    list_out = capsys.readouterr()
    assert listed == 0
    list_payload = json.loads(list_out.out)
    assert list_payload["tasks"][0]["id"] == "task-json-task-output"
    assert list_payload["tasks"][0]["status"] == "draft"
    assert list_payload["tasks"][0]["validation"] == ["pytest"]

    shown = main(["show", "task", "task-json-task-output", "--root", str(tmp_path), "--format", "json"])
    show_out = capsys.readouterr()
    assert shown == 0
    show_payload = json.loads(show_out.out)
    assert show_payload["id"] == "task-json-task-output"
    assert "routine" not in show_payload
    assert show_payload["current_node"] == "ritual-execution"
    assert [gate["relation_type"] for gate in show_payload["lifecycle_gates"]] == ["task_activates"]



def test_list_and_show_artifact_support_json_output(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "pill",
            "--root",
            str(tmp_path),
            "--title",
            "JSON pill output",
            "--what",
            "Expose artifact data through the CLI.",
            "--why",
            "Scripts need a stable contract.",
            "--when",
            "When operators read modeled pill data.",
            "--where",
            "List/show surfaces.",
            "--how",
            "Serialize the stored payload.",
            "--how-not",
            "Do not rely on text scraping.",
        ]
    )
    capsys.readouterr()
    assert created == 0

    listed = main(["list", "pills", "--root", str(tmp_path), "--format", "json"])
    list_out = capsys.readouterr()
    assert listed == 0
    list_payload = json.loads(list_out.out)
    assert list_payload["pills"][0]["id"] == "pill-json-pill-output"
    assert list_payload["pills"][0]["title"] == "JSON pill output"

    shown = main(["show", "pill", "pill-json-pill-output", "--root", str(tmp_path), "--format", "json"])
    show_out = capsys.readouterr()
    assert shown == 0
    show_payload = json.loads(show_out.out)
    assert show_payload["id"] == "pill-json-pill-output"
    assert show_payload["how_not"] == "Do not rely on text scraping."



def test_advance_task_blocks_testing_and_closeout_without_required_evidence(lifecycle_desk: Path, capsys) -> None:
    tmp_path = lifecycle_desk
    import subprocess
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=tmp_path)
    subprocess.run(['git', 'commit', '--allow-empty', '-q', '-m', 'seed'], cwd=tmp_path)
    add_result = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Advance blocked task",
            "--goal",
            "Enforce phase gates.",
            "--scope",
            "Task state machine only.",
            "--implementation-path",
            "Advance only when each gate has proof.",
            "--done-when",
            "Advancement halts when gate evidence is missing.",
        ]
    )
    capsys.readouterr()
    assert add_result == 0

    first_advance = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    first = capsys.readouterr()
    assert first_advance == 0
    assert "Status: active" in first.out
    assert "Current node: ritual-testing" in first.out

    blocked_testing = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    blocked_testing_out = capsys.readouterr()
    assert blocked_testing == 1
    assert "Status: active" in blocked_testing_out.out
    assert "Current node: ritual-testing" in blocked_testing_out.out
    assert "Message: Gate ritual-testing is not complete" in blocked_testing_out.out

    blocked_test = tmp_path / "tests" / "test_blocked.py"
    blocked_test.parent.mkdir(parents=True, exist_ok=True)
    blocked_test.write_text("def test_blocked():\n    assert True\n", encoding="utf-8")

    add_validation = main([
        "edit",
        "task",
        "task-advance-blocked-task",
        "validation",
        '["pytest tests/test_blocked.py::test_blocked"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert add_validation == 0

    move_to_closeout = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    move_to_closeout_out = capsys.readouterr()
    assert move_to_closeout == 0
    assert "Status: ready_for_testing" in move_to_closeout_out.out
    assert "Current node: ritual-closeout" in move_to_closeout_out.out

    blocked_closeout = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    blocked_closeout_out = capsys.readouterr()
    assert blocked_closeout == 1
    assert "Status: ready_for_testing" in blocked_closeout_out.out
    assert "Current node: ritual-closeout" in blocked_closeout_out.out
    assert "Message: Gate ritual-closeout is not complete" in blocked_closeout_out.out

    add_invalid_evidence = main([
        "edit",
        "task",
        "task-advance-blocked-task",
        "references",
        '["not-real-evidence"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert add_invalid_evidence == 0

    still_blocked = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    still_blocked_out = capsys.readouterr()
    assert still_blocked == 1
    assert "Message: Gate ritual-closeout is not complete" in still_blocked_out.out

    add_evidence = main([
        "edit",
        "task",
        "task-advance-blocked-task",
        "references",
        '["pytest tests/test_blocked.py::test_blocked"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert add_evidence == 0

    # Evidence now clears the lifecycle gate, but `advance` still refuses to
    # close: the only closing entry point is `closeout commit`.
    close_attempt = main(["advance", "task", "task-advance-blocked-task", "--root", str(tmp_path)])
    close_attempt_out = capsys.readouterr()
    assert close_attempt == 1
    assert "deskops closeout commit" in close_attempt_out.out
    assert (tmp_path / "desk" / "tasks" / "task-advance-blocked-task.md").exists()

    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS]) == 0
    capsys.readouterr()
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()
    full_evidence = main([
        "edit",
        "task",
        "task-advance-blocked-task",
        "references",
        f'["desk/atoms/atom-trackable-atom.md", "pytest tests/test_blocked.py::test_blocked", "{commit}"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert full_evidence == 0
    files_edit = main([
        "edit",
        "task",
        "task-advance-blocked-task",
        "files",
        '["desk/atoms/atom-trackable-atom.md"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert files_edit == 0

    closed = main([
        "closeout", "commit", "--root", str(tmp_path),
        "--task", "task-advance-blocked-task",
        "--no-run", "--reason", "Blocked gate smoke test",
        "--paths", "desk/atoms/atom-trackable-atom.md", "tests/test_blocked.py",
    ])
    close_out = capsys.readouterr()
    assert closed == 0
    assert "Closing commit " in close_out.out
    assert not (tmp_path / "desk" / "tasks" / "task-advance-blocked-task.md").exists()


def test_advance_task_accepts_atom_reference_as_closeout_evidence(lifecycle_desk: Path, capsys) -> None:
    tmp_path = lifecycle_desk
    import subprocess
    subprocess.run(['git', 'init', '-q'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=tmp_path)
    subprocess.run(['git', 'commit', '--allow-empty', '-q', '-m', 'seed'], cwd=tmp_path)
    add_atom = main([
        "add",
        "atom",
        "--root",
        str(tmp_path),
        *ATOM_PAYLOAD_ARGS,
    ])
    capsys.readouterr()
    assert add_atom == 0

    add_task = main(
        [
            "add",
            "task",
            "--root",
            str(tmp_path),
            "--title",
            "Advance with atom evidence",
            "--goal",
            "Allow atom-backed closeout.",
            "--scope",
            "Task closeout evidence only.",
            "--implementation-path",
            "Carry atom evidence through closeout.",
            "--done-when",
            "An atom reference can satisfy closeout evidence.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert add_task == 0

    assert main(["advance", "task", "task-advance-with-atom-evidence", "--root", str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["advance", "task", "task-advance-with-atom-evidence", "--root", str(tmp_path)]) == 0
    capsys.readouterr()

    set_atom_reference = main([
        "edit",
        "task",
        "task-advance-with-atom-evidence",
        "references",
        '["desk/atoms/atom-trackable-atom.md"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert set_atom_reference == 0

    # The atom reference clears the lifecycle gate (not "Gate ... not
    # complete"), but closing itself belongs to `closeout commit`.
    close_attempt = main(["advance", "task", "task-advance-with-atom-evidence", "--root", str(tmp_path)])
    close_attempt_out = capsys.readouterr()
    assert close_attempt == 1
    assert "deskops closeout commit" in close_attempt_out.out
    assert "Gate ritual-closeout is not complete" not in close_attempt_out.out

    atom_test = tmp_path / "tests" / "test_atom_evidence.py"
    atom_test.parent.mkdir(parents=True, exist_ok=True)
    atom_test.write_text("def test_atom_evidence():\n    assert True\n", encoding="utf-8")
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()
    full_evidence = main([
        "edit",
        "task",
        "task-advance-with-atom-evidence",
        "references",
        f'["desk/atoms/atom-trackable-atom.md", "pytest tests/test_atom_evidence.py::test_atom_evidence", "{commit}"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert full_evidence == 0
    files_edit = main([
        "edit",
        "task",
        "task-advance-with-atom-evidence",
        "files",
        '["desk/atoms/atom-trackable-atom.md"]',
        "--root",
        str(tmp_path),
    ])
    capsys.readouterr()
    assert files_edit == 0

    close_result = main([
        "closeout", "commit", "--root", str(tmp_path),
        "--task", "task-advance-with-atom-evidence",
        "--no-run", "--reason", "Atom evidence smoke test",
        "--paths", "desk/atoms/atom-trackable-atom.md", "tests/test_atom_evidence.py",
    ])
    close_out = capsys.readouterr()
    assert close_result == 0
    assert "Closing commit " in close_out.out



def test_advance_task_allows_empty_implementation_path(lifecycle_desk: Path, capsys) -> None:
    tmp_path = lifecycle_desk
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
    assert "Current node: ritual-testing" in first.out


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

def test_fresh_init_scaffolds_every_ritual_the_doctor_requires(tmp_path: Path, capsys) -> None:
    """A freshly initialised desk must not report missing structure.

    The doctor requires desk/rituals/phase.md, so the scaffold has to write it;
    otherwise every new repository starts one finding away from healthy.
    """
    from deskops.cli.main import main

    root = tmp_path / "project"
    root.mkdir()

    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    assert (root / "desk" / "rituals" / "phase.md").exists()

    assert main(["doctor", "--root", str(root)]) == 0
    out, _err = capsys.readouterr()
    assert "Missing desk structure" not in out


def test_doctor_reports_untracked_documents_and_missing_structure(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    import subprocess
    import sys

    root = tmp_path / "project"
    root.mkdir()
    
    # Run init to get a valid store and desk scaffolding
    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    # Now we break the desk structure
    import shutil
    shutil.rmtree(root / "desk" / "drawer")

    # Add an untracked document
    (root / "desk" / "tasks" / "untracked-task.md").write_text("# Untracked\n", encoding="utf-8")

    # Run doctor without repair
    assert main(["doctor", "--root", str(root)]) == 1
    out, err = capsys.readouterr()
    assert "Doctor Findings:" in out
    assert "Missing desk structure: desk/drawer/" in out
    assert "Untracked desk documents: desk/tasks/untracked-task.md" in out
    assert "Run with --repair to attempt automatic fixes." in out

    # Run doctor with repair
    assert main(["doctor", "--root", str(root), "--repair"]) == 1
    out, err = capsys.readouterr()
    assert "Scaffolded missing desk/ structure." in out
    assert "Manual repair required to track documents (use sldb docs track)." in out

    # Check if things were repaired
    assert (root / "desk" / "drawer").exists()

def test_doctor_reports_invalid_documents(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    import subprocess
    import sys

    root = tmp_path / "project"
    root.mkdir()
    
    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    # Create a tracked document cleanly
    task_doc = root / "desk" / "tasks" / "task-foo.md"
    main(["add", "task", "--title", "Foo", "--root", str(root)])
    capsys.readouterr()

    # Corrupt it
    task_doc.write_text("corrupted content", encoding="utf-8")
    
    # Let's run stores update so hash_c changes, but hash_d might be broken because it fails to parse
    # Or just let doctor detect hash_c/hash_d mismatch from store check
    
    # Run doctor
    assert main(["doctor", "--root", str(root)]) == 1
    out, err = capsys.readouterr()
    assert "SLDB store check crashed (likely malformed documents)" in out

def test_edit_pill_lifecycle_slots_including_drawer(tmp_path: Path, capsys) -> None:
    from sldb.runtime.validation import render_model_markdown
    from deskops.models.pill import PillDoc
    
    # 1. Create a pill in desk/contexts
    ctx_path = tmp_path / "desk" / "contexts" / "pill-ctx-test.md"
    ctx_path.parent.mkdir(parents=True, exist_ok=True)
    doc_ctx = PillDoc(id="pill-ctx-test", title="Context Pill", what="A", why="A", when="A", where="A", how="A", how_not="A", tags=[])
    ctx_path.write_text(render_model_markdown(PillDoc, doc_ctx.render_payload()))
    
    # 2. Create a pill in desk/drawer/pills
    drw_path = tmp_path / "desk" / "drawer" / "pills" / "pill-drawer-test.md"
    drw_path.parent.mkdir(parents=True, exist_ok=True)
    doc_drw = PillDoc(id="pill-drawer-test", title="Drawer Pill", what="B", why="B", when="B", where="B", how="B", how_not="B", tags=[])
    drw_path.write_text(render_model_markdown(PillDoc, doc_drw.render_payload()))
    
    from deskops.cli.main import main
    
    # Edit the context pill's status
    assert main(["edit", "pill", "pill-ctx-test", "status", "active", "--root", str(tmp_path)]) == 0
    
    # Edit the drawer pill's summary
    assert main(["edit", "pill", "pill-drawer-test", "summary", "A short summary", "--root", str(tmp_path)]) == 0
    
    # Verify persistence
    from sldb.runtime.validation import Validator
    parsed_ctx = Validator(PillDoc).extract(ctx_path.read_text())
    assert parsed_ctx["status"] == "active"
    
    parsed_drw = Validator(PillDoc).extract(drw_path.read_text())
    assert parsed_drw["summary"] == "A short summary"


def test_empty_selector_is_rejected_before_any_lookup(tmp_path: Path, capsys) -> None:
    """An unset shell variable must not resolve to an unrelated document.

    Before this, `show task ""` fell through to the lookup and reported a
    Pydantic error about the board's missing status field: a document the user
    never named.
    """
    from deskops.cli.main import main

    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    for argv in (
        ["show", "task", "", "--root", str(tmp_path)],
        ["show", "task", "   ", "--root", str(tmp_path)],
        ["edit", "task", "", "status", "closed", "--root", str(tmp_path)],
    ):
        assert main(argv) != 0, argv
        out, err = capsys.readouterr()
        assert "cannot be empty" in (out + err), argv
        assert "validation error" not in (out + err).lower(), argv


def test_empty_selector_guard_holds_at_the_resolution_layer(tmp_path: Path, capsys) -> None:
    """The CLI guard is the first line; the resolver refuses too."""
    from deskops.operations import DeskopsOperations

    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    operations = DeskopsOperations(tmp_path)
    with pytest.raises(ValueError, match="Empty or whitespace-only"):
        operations._resolve_artifact_selector_multi("artifact.task", [tmp_path / "desk" / "tasks"], "")


def test_drift_check_reports_knowledge_surface_findings(tmp_path: Path, capsys) -> None:
    """Drift includes knowledge surfaces, and reports without repairing."""
    from deskops.cli.main import main

    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    # A document that declares a target nothing resolves.
    (tmp_path / "desk" / "drawer" / "issues").mkdir(parents=True, exist_ok=True)
    (tmp_path / "desk" / "drawer" / "issues" / "issue-dangling.md").write_text(
        "# Dangling\n\n## Related Atoms\n\n- atom-that-does-not-exist\n", encoding="utf-8"
    )
    before = (tmp_path / "desk" / "drawer" / "issues" / "issue-dangling.md").read_text(encoding="utf-8")

    assert main(["drift", "check", "--root", str(tmp_path)]) == 1
    out, _err = capsys.readouterr()

    assert "Drift findings:" in out
    assert "atom-that-does-not-exist" in out
    # Review surface: the desk is untouched.
    assert (tmp_path / "desk" / "drawer" / "issues" / "issue-dangling.md").read_text(encoding="utf-8") == before


def test_drift_check_is_quiet_on_a_fresh_desk(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main

    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    assert main(["drift", "check", "--root", str(tmp_path)]) == 0
    out, _err = capsys.readouterr()
    assert "No drift found." in out


def test_runtime_workers_text_and_json_formats(capsys, monkeypatch) -> None:
    import deskops.cli.commands.runtime as runtime_module
    from deskops.cli.commands.runtime import RuntimeCLI

    agents = [
        {
            "pane_id": "w-1:p-1",
            "agent": "pi",
            "name": "executor",
            "agent_status": "idle",
            "cwd": "/tmp/work",
            "workspace_id": "w-1",
            "tab_id": "t-1",
            "terminal_title_stripped": "deskops executor",
            "state_change_seq": 7,
            "focused": True,
        },
        {
            "pane_id": "w-2:p-3",
            "agent": "codex",
            "agent_status": "blocked",
            "cwd": "/tmp/other",
            "workspace_id": "w-2",
            "tab_id": "t-2",
            "terminal_title_stripped": None,
            "state_change_seq": 3,
            "focused": False,
        },
        {
            "pane_id": "w-99:p-9",
            "agent": "claude",
            "name": "stray",
            "agent_status": "working",
            "cwd": "/tmp/stray",
            "workspace_id": "w-99",
            "tab_id": "t-99",
            "terminal_title_stripped": None,
            "state_change_seq": 1,
            "focused": False,
        },
    ]
    workspaces = [
        {
            "workspace_id": "w-1",
            "label": "sldb",
            "number": 2,
            "agent_status": "active",
            "pane_count": 1,
            "focused": True,
        },
        {
            "workspace_id": "w-2",
            "label": "setup",
            "number": 1,
            "agent_status": "active",
            "pane_count": 1,
            "focused": False,
        },
    ]

    class FakeHerdrClient:
        def __init__(self, executable: str) -> None:
            self.executable = executable

        def call(self, *args: str):
            if args[0:2] == ("workspace", "list"):
                return {"result": {"workspaces": workspaces}}
            if args[0:2] == ("agent", "list"):
                return {"result": {"agents": agents}}
            raise AssertionError(f"unexpected herdr call: {args}")

    monkeypatch.setattr(runtime_module, "HerdrClient", FakeHerdrClient)
    cli = RuntimeCLI()

    assert cli.run(SimpleNamespace(runtime_command="workers", root=".", herdr="herdr", format="text")) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == [
        "w-2  setup  (1 workers)",
        "  w-2:p-3 | codex | - | blocked | /tmp/other",
        "w-1  sldb  (1 workers)",
        "  w-1:p-1 | pi | executor | idle | /tmp/work",
        "-  -  (1 workers)",
        "  w-99:p-9 | claude | stray | working | /tmp/stray",
    ]

    assert cli.run(SimpleNamespace(runtime_command="workers", root=".", herdr="herdr", format="json")) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["workers"][0] == {
        "pane": "w-1:p-1",
        "kind": "pi",
        "name": "executor",
        "status": "idle",
        "cwd": "/tmp/work",
        "title": "deskops executor",
        "workspace": "w-1",
        "seq": 7,
        "focused": True,
    }
    assert payload["workers"][1]["name"] is None
    assert "name" in payload["workers"][1]
    assert payload["workers"][1]["title"] is None
    assert [space["workspace"] for space in payload["spaces"]] == ["w-2", "w-1", None]
    assert [space["label"] for space in payload["spaces"]] == ["setup", "sldb", None]
    assert [space["number"] for space in payload["spaces"]] == [1, 2, None]
    assert payload["spaces"][0]["workers"] == [payload["workers"][1]]
    assert payload["spaces"][1]["workers"] == [payload["workers"][0]]
    assert payload["spaces"][2]["status"] is None
    assert payload["spaces"][2]["workers"] == [payload["workers"][2]]


def test_runtime_workers_empty_fleet_prints_notice(capsys, monkeypatch) -> None:
    import deskops.cli.commands.runtime as runtime_module
    from deskops.cli.commands.runtime import RuntimeCLI

    class FakeHerdrClient:
        def __init__(self, executable: str) -> None:
            self.executable = executable

        def call(self, *args: str):
            if args[0:2] == ("workspace", "list"):
                return {"result": {"workspaces": []}}
            if args[0:2] == ("agent", "list"):
                return {"result": {"agents": []}}
            raise AssertionError(f"unexpected herdr call: {args}")

    monkeypatch.setattr(runtime_module, "HerdrClient", FakeHerdrClient)
    cli = RuntimeCLI()

    assert cli.run(SimpleNamespace(runtime_command="workers", root=".", herdr="herdr", format="text")) == 0
    assert capsys.readouterr().out.strip() == "No live Herdr agents."

    assert cli.run(SimpleNamespace(runtime_command="workers", root=".", herdr="herdr", format="json")) == 0
    assert json.loads(capsys.readouterr().out) == {"workers": [], "spaces": []}


def test_runtime_workers_herdr_failure_prints_error_and_returns_one(capsys, monkeypatch) -> None:
    import deskops.cli.commands.runtime as runtime_module
    from deskops.cli.commands.runtime import RuntimeCLI
    from deskops.runtime.herdr import HerdrError

    class FailingHerdrClient:
        def __init__(self, executable: str) -> None:
            self.executable = executable

        def call(self, *args: str):
            raise HerdrError("herdr agent list: boom")

    monkeypatch.setattr(runtime_module, "HerdrClient", FailingHerdrClient)
    cli = RuntimeCLI()

    assert cli.run(SimpleNamespace(runtime_command="workers", root=".", herdr="herdr", format="text")) == 1
    assert capsys.readouterr().out.strip() == "Error: herdr agent list: boom"


def test_unexpected_error_exits_three_with_type_and_hint(capsys, monkeypatch) -> None:
    def boom() -> int:
        raise RuntimeError("kaboom")

    monkeypatch.setattr("deskops.cli.main.print_about", boom)

    assert main(["about"]) == 3

    captured = capsys.readouterr()
    assert captured.out == ""
    assert (
        "Unexpected error: RuntimeError: kaboom "
        "(rerun with --debug for the traceback)"
    ) in captured.err
    assert "Traceback" not in captured.err


def test_unexpected_error_with_debug_prints_traceback_then_the_line(capsys, monkeypatch) -> None:
    def boom() -> int:
        raise RuntimeError("kaboom")

    monkeypatch.setattr("deskops.cli.main.print_about", boom)

    assert main(["--debug", "about"]) == 3

    captured = capsys.readouterr()
    assert "Traceback (most recent call last):" in captured.err
    assert "Unexpected error: RuntimeError: kaboom" in captured.err
    assert captured.err.index("Traceback (most recent call last):") < captured.err.index(
        "Unexpected error:"
    )


@pytest.mark.parametrize(
    ("stdout", "returncode"),
    [
        ("", 127),  # sldb missing
        ("this is not json", 1),  # unparseable output
    ],
)
def test_desk_update_exits_three_when_stores_check_has_no_json(
    tmp_path: Path, capsys, monkeypatch, stdout: str, returncode: int
) -> None:
    import deskops.cli.commands.desk as desk_module

    (tmp_path / ".sldb").mkdir()

    def fake_run(*args, **kwargs):
        return SimpleNamespace(stdout=stdout, stderr="", returncode=returncode)

    monkeypatch.setattr(desk_module.subprocess, "run", fake_run)

    assert main(["desk", "update", "--root", str(tmp_path)]) == 3
    assert "sldb stores check" in capsys.readouterr().err


def test_desk_update_without_store_reports_divergence_and_apply_repairs(
    tmp_path: Path, capsys
) -> None:
    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert "Desk divergence report:" in captured.out
    assert "Missing store: .sldb" in captured.out
    assert "failed" not in captured.out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    check = subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(tmp_path / ".sldb")],
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stdout + check.stderr


def test_explicit_root_dot_bypasses_the_sandbox_override(tmp_path: Path, monkeypatch, capsys) -> None:
    """An explicit `--root .` is not the default, so the sandbox redirect must not fire."""
    repo = tmp_path / "explicit-root-repo"
    (repo / "desk").mkdir(parents=True)
    sandbox_root = tmp_path / "sandbox-must-stay-empty"
    monkeypatch.chdir(repo)
    monkeypatch.setenv("DESKOPS_TEST_ROOT", str(sandbox_root))

    result = main(
        [
            "add",
            "task",
            "--root",
            ".",
            "--title",
            "Explicit root task",
            "--goal",
            "Prove explicit roots win over the sandbox redirect.",
            "--scope",
            "Only the explicit root.",
            "--implementation-path",
            "Guard the override on explicit flags.",
            "--done-when",
            "The task lands in the explicit root.",
            "--validation",
            "pytest",
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    task_path = repo / "desk" / "tasks" / "task-explicit-root-task.md"
    assert str(task_path) in captured.out
    assert task_path.exists()
    assert not (sandbox_root / "desk" / "tasks" / "task-explicit-root-task.md").exists()


def _capture_main(argv: list[str], capsys) -> tuple[int, str, str]:
    result = main(argv)
    captured = capsys.readouterr()
    return result, captured.out, captured.err


def test_status_alias_warns_and_matches_doctor(tmp_path: Path, capsys) -> None:
    alias_result, alias_out, alias_err = _capture_main(
        ["status", "--root", str(tmp_path)], capsys
    )
    canonical_result, canonical_out, canonical_err = _capture_main(
        ["doctor", "--root", str(tmp_path)], capsys
    )

    assert alias_result == canonical_result
    assert alias_out == canonical_out
    assert alias_err == "Deprecated: use `deskops doctor`\n"
    assert canonical_err == ""


def test_atoms_list_alias_warns_and_matches_canonical(tmp_path: Path, capsys) -> None:
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS]) == 0
    capsys.readouterr()

    alias_result, alias_out, alias_err = _capture_main(
        ["atoms", "list", "--root", str(tmp_path)], capsys
    )
    canonical_result, canonical_out, canonical_err = _capture_main(
        ["list", "atoms", "--root", str(tmp_path)], capsys
    )

    assert alias_result == canonical_result == 0
    assert alias_out == canonical_out
    assert alias_err == "Deprecated: use `deskops list atoms`\n"
    assert canonical_err == ""


def test_atoms_show_alias_warns_and_matches_canonical(tmp_path: Path, capsys) -> None:
    assert main(["add", "atom", "--root", str(tmp_path), *ATOM_PAYLOAD_ARGS]) == 0
    capsys.readouterr()

    alias_result, alias_out, alias_err = _capture_main(
        ["atoms", "show", "atom-trackable-atom", "--root", str(tmp_path)], capsys
    )
    canonical_result, canonical_out, canonical_err = _capture_main(
        ["show", "atom", "atom-trackable-atom", "--root", str(tmp_path)], capsys
    )

    assert alias_result == canonical_result == 0
    assert alias_out == canonical_out
    assert alias_err == "Deprecated: use `deskops show atom`\n"
    assert canonical_err == ""
