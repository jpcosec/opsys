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
            data["models"] = [m for m in data["models"] if m["name"] != "FAQDoc"]
            with open(store_idx, "w") as f: yaml.safe_dump(data, f)
        else:
            with open(store_idx) as f: data = json.load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "FAQDoc"]
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
