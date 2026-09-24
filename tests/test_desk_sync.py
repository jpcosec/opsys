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

