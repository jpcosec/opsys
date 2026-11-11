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

import pytest

from deskops.atom_tags import sync_tag_declaration
from deskops.cli.main import main
from sldb.api import tag_check
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
    """A desk without a store (``desk install``): sldb checks nothing there."""
    assert main(["desk", "install", str(root)]) == 0
    _domain_axis(root)


def _domain_axis(root: Path) -> None:
    config = root / "desk" / "config.json"
    data = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    data["atom_folder_axis"] = "domain"
    config.write_text(json.dumps(data), encoding="utf-8")


@pytest.fixture
def desk(lifecycle_desk: Path) -> Path:
    """A desk as ``deskops init`` leaves it: a store declaring the namespaces of
    ``tag-namespaces.yaml`` (``domain`` anchored by ``CrossroadDoc.path``, value bare)."""
    _domain_axis(lifecycle_desk)
    assert sync_tag_declaration(lifecycle_desk) is True
    return lifecycle_desk


def _atoms(root: Path, *args: str) -> int:
    return main(["atoms", *args, "--root", str(root)])


def _write_pizzeria_tree(root: Path) -> None:
    assert _atoms(root, "crossroad", "pizzeria", "--title", "Pizzería", "--content", "Everything the pizzeria runs.") == 0
    assert _atoms(root, "crossroad", "pizzeria.carta", "--title", "Carta", "--content", "The dishes on the menu.") == 0


def _tracked(store: Path, model: str) -> set[str]:
    entry = next(item for item in load_store_index(store).models if item.name == model)
    models_index = load_models_index(store.parent / entry.models_index)
    return {doc.name for doc in load_documents_index(store.parent / models_index.documents_index).documents}


def test_parents_must_be_written_before_their_children(desk: Path, capsys) -> None:
    tmp_path = desk
    atoms_dir = tmp_path / "desk" / "atoms"

    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 1
    assert "Write the parent first: no written crossroad for pizzeria, pizzeria.carta" in capsys.readouterr().out
    assert _atoms(tmp_path, "crossroad", "pizzeria.carta", "--title", "Carta", "--content", "Menu.") == 1
    assert "no written crossroad for pizzeria" in capsys.readouterr().out
    assert _atoms(tmp_path, "crossroad", "pizzeria", "--title", "Pizzería", "--content", "   ") == 1
    assert "must describe its children" in capsys.readouterr().out
    assert not list(atoms_dir.rglob("*.md"))

    _write_pizzeria_tree(tmp_path)
    # The crossroad's path `pizzeria.carta` anchors `domain:pizzeria.carta` (value bare).
    assert capsys.readouterr().out.count("Created crossroad") == 2
    assert (atoms_dir / "pizzeria" / "crossroad-pizzeria.md").exists()
    assert (atoms_dir / "pizzeria" / "carta" / "crossroad-pizzeria--carta.md").exists()
    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 0
    assert (atoms_dir / "pizzeria" / "carta" / "proto-masa-madre.md").exists()
    assert _atoms(tmp_path, "crossroad", "pizzeria", "--title", "Again", "--content", "Twice.") == 1


def test_atom_creation_refuses_an_unwritten_domain(desk: Path, capsys) -> None:
    tmp_path = desk
    try:
        code = main([
            "add", "atom", "--root", str(tmp_path), "--title", "Oven temperature",
            "--five-wh-one-plus", "what", "--answer", "450 degrees.", "--tags", "domain:pizzeria",
        ])
    except (SystemExit, ValueError):
        code = 1
    assert code != 0
    assert "Write the parent first: no written crossroad for pizzeria" in capsys.readouterr().out
    assert not list((tmp_path / "desk" / "atoms").rglob("atom-oven-temperature.md"))


def test_validate_all_reports_atoms_hanging_from_unwritten_paths(desk: Path, capsys) -> None:
    tmp_path = desk
    (tmp_path / "desk" / "atoms" / "atom-oven-temperature.md").write_text(HANGING_ATOM, encoding="utf-8")
    # The finding is sldb's tag family: it sees the documents the store tracks.
    assert main(["desk", "update", "--apply", "--root", str(tmp_path)]) == 0
    capsys.readouterr()

    assert _atoms(tmp_path, "validate", "--all") == 1
    assert "no written crossroad for domain path 'pizzeria'" in capsys.readouterr().out

    _write_pizzeria_tree(tmp_path)
    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 0
    capsys.readouterr()
    assert _atoms(tmp_path, "validate", "--all") == 0, capsys.readouterr().out


def test_typing_a_protoatom_creates_the_typed_doc_and_keeps_a_redirect_stub(desk: Path, capsys) -> None:
    tmp_path = desk
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


def test_a_desk_without_a_store_checks_no_domain_or_namespace(tmp_path: Path, capsys) -> None:
    """Without a store sldb has nothing to check: deskops does not check either (CC35d resto)."""
    _install_sandbox(tmp_path)
    assert _atoms(tmp_path, "proto", "proto-masa-madre", "--title", "Masa madre", "--tag", "domain:pizzeria.carta") == 0
    assert _atoms(tmp_path, "proto", "proto-libre", "--title", "Libre", "--tag", "undeclared:x") == 0
    assert _atoms(tmp_path, "crossroad", "pizzeria.carta", "--title", "Carta", "--content", "Menu.") == 0
    capsys.readouterr()
    assert _atoms(tmp_path, "validate", "--all") == 0, capsys.readouterr().out


def test_an_atom_with_an_undeclared_namespace_is_an_sldb_finding(desk: Path, capsys) -> None:
    atom = HANGING_ATOM.replace("- domain:pizzeria", "- undeclared:value")
    (desk / "desk" / "atoms" / "atom-oven-temperature.md").write_text(atom, encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(desk)]) == 0

    codes = {(finding.code, finding.subject.rsplit(":", 1)[-1]) for finding in tag_check(desk / ".sldb")}
    assert ("rules/builtin:tag_namespace:undeclared", "atom-oven-temperature") in codes
    capsys.readouterr()
    assert _atoms(desk, "validate", "--all") == 1
    assert "Unknown atom tag namespace 'undeclared' for tag 'undeclared:value'." in capsys.readouterr().out
    assert _atoms(desk, "proto", "proto-libre", "--title", "Libre", "--tag", "undeclared:x") == 1
    assert "Unknown atom tag namespace 'undeclared' for tag 'undeclared:x'." in capsys.readouterr().out


def test_tasks_and_pills_with_undeclared_namespaces_are_not_findings(desk: Path) -> None:
    """``tag_models`` limits the family to atoms and protoatoms: a task or a pill keeps its
    ``workspace:``, ``artifact:`` or ``pill-type:`` tags (none declared) without a finding."""
    assert main([
        "add", "pill", "--root", str(desk), "--title", "Una pill", "--summary", "s", "--what", "w",
        "--why", "y", "--when", "n", "--where", "e", "--how", "h", "--how-not", "x",
        "--tags", "workspace:desk", "pill-type:rule",
    ]) == 0
    assert main([
        "add", "task", "--root", str(desk), "--title", "Una tarea", "--goal", "g", "--scope", "s",
        "--implementation-path", "i", "--done-when", "d", "--validation", "pytest", "--task-type", "task.code",
    ]) == 0
    texts = [path.read_text(encoding="utf-8") for path in (desk / "desk").rglob("*.md")]
    assert any("pill-type:rule" in text for text in texts)
    assert any("artifact:task" in text for text in texts)

    assert tag_check(desk / ".sldb") == []


def test_desk_update_apply_writes_the_tag_declaration_once(lifecycle_desk: Path, capsys) -> None:
    from sldb.api import tag_namespaces
    from sldb.api.stores.store_declaration import load_declaration

    root = lifecycle_desk
    assert main(["desk", "update", "--root", str(root)]) == 1
    assert "- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml" in capsys.readouterr().out

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert "Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml." in capsys.readouterr().out
    declared = {item["name"]: item for item in tag_namespaces(root / ".sldb")}
    assert declared["domain"]["anchored_by"] == {"model": "CrossroadDoc", "field": "path", "value": "bare"}
    assert load_declaration(root / ".sldb").tag_models == ["AtomDoc", "ProtoAtomDoc"]
    text = (root / ".sldb" / "store.yaml").read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out
    assert (root / ".sldb" / "store.yaml").read_text(encoding="utf-8") == text

    # The file wins: a namespace added through deskops reaches the declaration.
    assert main([
        "atoms", "add-namespace", "pattern", "--root", str(root), "--meaning", "m", "--use-when", "u",
        "--do-not-use-when", "d", "--example", "pattern:x",
    ]) == 0
    assert "pattern" in {item["name"] for item in tag_namespaces(root / ".sldb")}
    capsys.readouterr()
    assert main(["desk", "update", "--root", str(root)]) == 0
