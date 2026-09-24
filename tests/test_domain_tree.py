from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from sldb.cli import main as sldb_main
from sldb.store.io import load_documents_index, load_models_index, load_store_index


HANGING_ATOM = """---
id: atom-oven-temperature
title: Oven temperature
five_wh_one_plus: what
tags:
- domain:pizzeria
---

# Oven temperature

## Answer

The oven runs at 450 degrees.
"""


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0
    config = root / "desk" / "config.json"
    data = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    data["atom_folder_axis"] = "domain"
    config.write_text(json.dumps(data), encoding="utf-8")


def _atoms(root: Path, *args: str) -> int:
    return main(["atoms", *args, "--root", str(root)])


def _write_pizzeria_tree(root: Path) -> None:
    assert _atoms(root, "crossroad", "pizzeria", "--title", "Pizzería", "--content", "Everything the pizzeria runs.") == 0
    assert _atoms(root, "crossroad", "pizzeria.carta", "--title", "Carta", "--content", "The dishes on the menu.") == 0


def _tracked(store: Path, model: str) -> set[str]:
    entry = next(item for item in load_store_index(store).models if item.name == model)
    models_index = load_models_index(store.parent / entry.models_index)
    return {doc.name for doc in load_documents_index(store.parent / models_index.documents_index).documents}


def test_parents_must_be_written_before_their_children(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    atoms_dir = tmp_path / "desk" / "atoms"

    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 1
    assert "Write the parent first: no written crossroad for pizzeria, pizzeria.carta" in capsys.readouterr().out
    assert _atoms(tmp_path, "crossroad", "pizzeria.carta", "--title", "Carta", "--content", "Menu.") == 1
    assert "no written crossroad for pizzeria" in capsys.readouterr().out
    assert _atoms(tmp_path, "crossroad", "pizzeria", "--title", "Pizzería", "--content", "   ") == 1
    assert "must describe its children" in capsys.readouterr().out
    assert not list(atoms_dir.rglob("*.md"))

    _write_pizzeria_tree(tmp_path)
    assert (atoms_dir / "pizzeria" / "crossroad-pizzeria.md").exists()
    assert (atoms_dir / "pizzeria" / "carta" / "crossroad-pizzeria--carta.md").exists()
    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 0
    assert (atoms_dir / "pizzeria" / "carta" / "proto-masa-madre.md").exists()
    assert _atoms(tmp_path, "crossroad", "pizzeria", "--title", "Again", "--content", "Twice.") == 1


def test_atom_creation_refuses_an_unwritten_domain(tmp_path: Path) -> None:
    _install_sandbox(tmp_path)
    try:
        code = main([
            "add", "atom", "--root", str(tmp_path), "--title", "Oven temperature",
            "--five-wh-one-plus", "what", "--answer", "450 degrees.", "--tags", "domain:pizzeria",
        ])
    except (SystemExit, ValueError):
        code = 1
    assert code != 0
    assert not list((tmp_path / "desk" / "atoms").rglob("atom-oven-temperature.md"))


def test_validate_all_reports_atoms_hanging_from_unwritten_paths(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    (tmp_path / "desk" / "atoms" / "atom-oven-temperature.md").write_text(HANGING_ATOM, encoding="utf-8")

    assert _atoms(tmp_path, "validate", "--all") == 1
    assert "no written crossroad for domain path 'pizzeria'" in capsys.readouterr().out

    _write_pizzeria_tree(tmp_path)
    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 0
    capsys.readouterr()
    assert _atoms(tmp_path, "validate", "--all") == 0, capsys.readouterr().out


def test_typing_a_protoatom_creates_the_typed_doc_and_keeps_a_redirect_stub(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _write_pizzeria_tree(tmp_path)
    assert _atoms(
        tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre",
        "--content", "Fermented for 48 hours.", "--tag", "domain:pizzeria.carta",
    ) == 0
    carta = tmp_path / "desk" / "atoms" / "pizzeria" / "carta"

    assert _atoms(tmp_path, "type", "proto-masa-madre", "--model", "AtomDoc") == 1
    assert "pass --content-field" in capsys.readouterr().out
    assert not (carta / "atom-masa-madre.md").exists()

    assert _atoms(
        tmp_path, "type", "proto-masa-madre", "--model", "AtomDoc",
        "--content-field", "answer", "--data", '{"five_wh_one_plus": "what"}',
    ) == 0
    atom_text = (carta / "atom-masa-madre.md").read_text(encoding="utf-8")
    assert "Fermented for 48 hours." in atom_text and "domain:pizzeria.carta" in atom_text
    stub_text = (carta / "proto-masa-madre.md").read_text(encoding="utf-8")
    assert "typed_as: AtomDoc:atom-masa-madre" in stub_text

    assert _atoms(tmp_path, "type", "proto-masa-madre", "--model", "AtomDoc", "--content-field", "answer") == 1
    assert "already typed" in capsys.readouterr().out
    assert _atoms(tmp_path, "validate", "--all") == 0, capsys.readouterr().out

    capsys.readouterr()
    assert _atoms(tmp_path, "tree") == 0
    tree = capsys.readouterr().out
    assert "pizzeria — Pizzería" in tree and "  pizzeria.carta — Carta" in tree
    assert "atom-masa-madre  Masa madre" in tree
    assert "proto-masa-madre  Masa madre -> AtomDoc:atom-masa-madre" in tree


def test_domain_tree_documents_are_tracked_in_the_store(tmp_path: Path) -> None:
    _install_sandbox(tmp_path)
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    store = tmp_path / ".sldb"
    for model in ("AtomDoc", "ProtoAtomDoc", "CrossroadDoc"):
        assert sldb_main(["models", "add", f"deskops.models:{model}", "--store", str(store), "--pythonpath", str(ROOT)]) == 0

    _write_pizzeria_tree(tmp_path)
    assert _atoms(
        tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre",
        "--content", "Fermented for 48 hours.", "--tag", "domain:pizzeria.carta",
    ) == 0
    assert _atoms(
        tmp_path, "type", "proto-masa-madre", "--model", "AtomDoc",
        "--content-field", "answer", "--data", '{"five_wh_one_plus": "what"}',
    ) == 0

    assert _tracked(store, "CrossroadDoc") == {"crossroad-pizzeria", "crossroad-pizzeria--carta"}
    assert _tracked(store, "ProtoAtomDoc") == {"proto-masa-madre"}
    assert _tracked(store, "AtomDoc") == {"atom-masa-madre"}
