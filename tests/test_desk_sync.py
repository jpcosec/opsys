import json
import pytest
from pathlib import Path
from sldb.api.stores.init_store import init_store
from sldb.cli.commands.model import ModelCLI
from deskops.cli.main import CLI
from deskops.workspace import scaffold_desk
from sldb.api.documents.track_document_file import track_document_file
import yaml
from types import SimpleNamespace
from deskops.bootstrap import SLDBBootstrap

def test_desk_update_command(tmp_path: Path):
    # Setup desk
    cli = CLI()
    assert cli.run(["init", str(tmp_path)]) == 0

    desk_dir = tmp_path / "desk"
    store_dir = tmp_path / ".sldb"

    # Create untracked file
    untracked_path = desk_dir / "tasks" / "task-untracked.md"
    untracked_path.write_text("---\nid: task-untracked\nstatus: active\ntags: []\n---\n# Untracked\n\n## Rationale\n\n## Goal\n")

    # Create tracked file then modify it to make hash stale
    tracked_path = desk_dir / "tasks" / "task-stale.md"
    tracked_path.write_text("---\nid: task-stale\nstatus: active\ntags: []\n---\n# Stale\n\n## Rationale\n\n## Goal\n")
    track_document_file(
        store_dir, "TaskDoc", tracked_path, name="task-stale",
        pythonpath=str(Path(__file__).resolve().parents[1]), force=True
    )
    tracked_path.write_text("---\nid: task-stale\nstatus: active\ntags: []\n---\n# Stale modified\n\n## Rationale\n\n## Goal\n")

    # Unregister a model
    store_idx = store_dir / "core" / "store_index.yaml"
    if not store_idx.exists():
        # Maybe it's json? No, sldb uses yaml for store_index now. 
        # But if not, we can just use bootstrap logic.
        store_idx = store_dir / "index.json"
    if store_idx.exists():
        if store_idx.suffix == ".yaml":
            with open(store_idx) as f: data = yaml.safe_load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: yaml.safe_dump(data, f)
        else:
            with open(store_idx) as f: data = json.load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: json.dump(data, f)

    # Test update (dry run)
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 1

    # Test update apply
    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    # Ensure it's clean now
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0



def test_desk_update_untracks_a_document_whose_file_is_gone(tmp_path: Path) -> None:
    """A deleted file must be untracked, not re-indexed.

    `git rm` on a tracked document leaves the store describing something that is
    not there, and neither 'stores update' nor an index rebuild clears it.
    """
    from deskops.cli.main import main
    from sldb.store.diagnostics import diagnose_store
    from sldb.api.model_registry.model_reference import resolve_model_ref

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        ["add", "atom", "--root", str(tmp_path), "--title", "Gone soon",
         "--five-wh-one-plus", "what", "--answer", "Answered."]
    ) == 0

    atom = tmp_path / "desk" / "atoms" / "atom-gone-soon.md"
    assert atom.exists()
    atom.unlink()

    assert main(["desk", "update", "--root", str(tmp_path)]) != 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    diagnosis = diagnose_store(
        tmp_path / ".sldb", resolve_model_ref, project_root=tmp_path, pythonpath=str(tmp_path)
    )
    notes = [doc.note.value for model in diagnosis.models for doc in model.documents]
    assert "missing" not in notes


def test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph(tmp_path: Path, capsys) -> None:
    """One --apply on a fresh repo must leave a desk that the next update calls up to date."""
    cli = CLI()

    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out


def _make_faq_model_legacy(root: Path) -> None:
    """Rewrite the store as it looked when the deskops FAQ model was still `FAQDoc`."""
    store = root / ".sldb"
    index_path = store / "core" / "store_index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    entry = next(model for model in index["models"] if model["name"] == "DeskFAQDoc")
    entry["name"] = "FAQDoc"
    entry["model_ref"] = "deskops.models:FAQDoc"
    entry["models_index"] = ".sldb/core/models/FAQDoc.yaml"
    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

    models_dir = store / "core" / "models"
    (models_dir / "DeskFAQDoc.yaml").rename(models_dir / "FAQDoc.yaml")
    model_index_path = models_dir / "FAQDoc.yaml"
    model_index = yaml.safe_load(model_index_path.read_text(encoding="utf-8"))
    model_index["name"] = "FAQDoc"
    model_index["model_ref"] = "deskops.models:FAQDoc"
    model_index["documents_index"] = ".sldb/core/documents/FAQDoc.yaml"
    model_index["sections_index"] = ".sldb/runtime/sections/FAQDoc.yaml"
    model_index_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")

    documents_dir = store / "core" / "documents"
    (documents_dir / "DeskFAQDoc").rename(documents_dir / "FAQDoc")


def test_desk_update_apply_migrates_the_legacy_faq_model(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.api import describe_model

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        [
            "add",
            "faq-doc",
            "--root",
            str(tmp_path),
            "--title",
            "Legacy FAQ",
            "--body",
            "Question?\n\nAnswer.",
        ]
    ) == 0
    faq_path = tmp_path / "desk" / "faq" / "faq-legacy-faq.md"
    original = faq_path.read_bytes()
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()
    _make_faq_model_legacy(tmp_path)

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Legacy FAQ model" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    names = {
        model["name"]
        for model in yaml.safe_load(
            (tmp_path / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8")
        )["models"]
    }
    assert "DeskFAQDoc" in names
    assert "FAQDoc" not in names

    documents = describe_model(
        tmp_path / ".sldb",
        "DeskFAQDoc",
        pythonpath=str(Path(__file__).resolve().parents[1]),
    ).documents
    assert [document.name for document in documents] == ["faq-legacy-faq"]
    assert faq_path.read_bytes() == original

    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_desk_update_does_not_call_the_owner_store_models_copies(tmp_path: Path, monkeypatch, capsys) -> None:
    from deskops.bootstrap import SLDBBootstrap
    from deskops.cli.main import main

    # Without an owner store, init registers the models directly, which is the
    # shape of the deskops owner store itself.
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    assert main(["init", str(tmp_path)]) == 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    other = tmp_path.parent / f"{tmp_path.name}-owner" / ".sldb"
    other.mkdir(parents=True)
    capsys.readouterr()

    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: other)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" in capsys.readouterr().out, "another store's direct models are copies"

    owner = tmp_path / ".sldb"
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: owner)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" not in capsys.readouterr().out
def test_desk_update_apply_resigns_a_moved_model_contract(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.store.hashing import hash_model_contract
    from deskops.models import RitualDoc

    assert main(["init", str(tmp_path)]) == 0
    model_path = tmp_path / ".sldb" / "core" / "models" / "RitualDoc.yaml"
    model_index = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    model_index["contract_hash"] = "0" * 64
    model_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Moved model contracts: RitualDoc" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    resigned = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    assert resigned["contract_hash"] == hash_model_contract(RitualDoc)
    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_guess_model_treats_extra_boards_in_tasks_as_boards(tmp_path: Path) -> None:
    """`deskops add board` writes `board-<slug>.md` next to Board.md (ARTIFACT_PATHS puts boards in
    tasks/); tracking it as a TaskDoc fails validation (no `status`) and breaks `desk update --apply`."""
    from deskops import models
    from deskops.cli.commands.desk import guess_model_for_path

    desk = tmp_path / "desk"
    assert guess_model_for_path(desk, desk / "tasks" / "Board.md") is models.BoardDoc
    assert guess_model_for_path(desk, desk / "tasks" / "board-compromisos-26-10.md") is models.BoardDoc
    assert guess_model_for_path(desk, desk / "tasks" / "task-doc-7.md") is models.TaskDoc
