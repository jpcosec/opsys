from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from sldb.api import add_model, doc_status, init_store, track_document_file
from sldb.api import store_links
from sldb.store.io import load_store_index

from deskops.bootstrap import MODEL_REFS
from deskops.cli.main import main
from deskops.workspace import scaffold_desk

ROOT = Path(__file__).resolve().parents[1]


def _deskops_model_entries(store_path: Path) -> list:
    return [
        entry
        for entry in load_store_index(store_path).models
        if (entry.model_ref or "").startswith("deskops.models:")
    ]


def _stores_check(store_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_deskops_init_inherits_deskops_models_instead_of_copying(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_machine_ready", lambda self: 0)
    root = tmp_path / "repo"
    root.mkdir()

    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    store = root / ".sldb"
    entries = {entry.name: entry for entry in _deskops_model_entries(store)}

    assert set(entries) == set(MODEL_REFS)
    for name, model_ref in MODEL_REFS.items():
        entry = entries[name]
        assert entry.origin == "deskops"
        assert entry.path == ""
        assert entry.model_ref == model_ref

    links = store_links(store)
    assert [link["name"] for link in links] == ["deskops"]
    assert links[0]["status"] == "ok"

    check = _stores_check(store)
    assert check.returncode == 0, check.stdout + check.stderr


def test_desk_update_apply_converts_copied_deskops_models(tmp_path: Path, capsys) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    location = init_store(root)
    store = location.store_path
    for model_ref in MODEL_REFS.values():
        add_model(store, model_ref, pythonpath=str(ROOT))
    scaffold_desk(root)
    track_document_file(
        store,
        "BoardDoc",
        root / "desk" / "tasks" / "Board.md",
        name="Board",
        pythonpath=str(ROOT),
    )
    assert doc_status(store, "BoardDoc/Board").status == "ok"

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    capsys.readouterr()

    for name in MODEL_REFS:
        entry = next(entry for entry in load_store_index(store).models if entry.name == name)
        assert entry.origin == "deskops"
        assert entry.path == ""
    assert doc_status(store, "BoardDoc/Board").status == "ok", "conversion keeps tracked documents"

    check = _stores_check(store)
    assert check.returncode == 0, check.stdout + check.stderr

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 0
    assert "Desk is up to date." in capsys.readouterr().out
