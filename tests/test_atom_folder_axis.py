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
from sldb.cli.main import main as sldb_main
from sldb.store.io import load_documents_index
from sldb.store.io import load_models_index
from sldb.store.io import load_store_index


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def _init_store(root: Path) -> None:
    assert sldb_main(["stores", "init", "--path", str(root)]) == 0
    assert sldb_main(
        [
            "models",
            "add",
            "deskops.models:AtomDoc",
            "--store",
            str(root / ".sldb"),
            "--pythonpath",
            str(ROOT),
        ]
    ) == 0


def _register_object_namespace(root: Path) -> None:
    assert main(
        [
            "atoms",
            "add-namespace",
            "object",
            "--root",
            str(root),
            "--meaning",
            "Business object the atom belongs to.",
            "--use-when",
            "The atom is about a business object.",
            "--do-not-use-when",
            "A general topic tag is enough.",
            "--example",
            "object:licitaciones",
        ]
    ) == 0


def _set_axis(root: Path, axis: str | None) -> None:
    config_path = root / "desk" / "config.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))
    data["atom_folder_axis"] = axis
    config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _add_atom(root: Path, title: str, *tags: str) -> int:
    args = [
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        title,
        "--five-wh-one-plus",
        "what",
        "--answer",
        f"Answer for {title}.",
    ]
    if tags:
        args += ["--tags", *tags]
    return main(args)


def _tracked_atom_paths(root: Path) -> dict[str, str]:
    store_index = load_store_index(root / ".sldb")
    model_entry = next(entry for entry in store_index.models if entry.name == "AtomDoc")
    models_index = load_models_index(root / model_entry.models_index)
    documents_index = load_documents_index(root / models_index.documents_index)
    return {entry.name: entry.path for entry in documents_index.documents}


def test_add_atom_with_axis_tag_lands_in_axis_subfolder(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")
    capsys.readouterr()

    assert _add_atom(tmp_path, "Licitaciones rule", "object:licitaciones") == 0

    expected = tmp_path / "desk" / "atoms" / "licitaciones" / "atom-licitaciones-rule.md"
    assert expected.exists()


def test_add_atom_without_axis_tag_stays_flat(tmp_path: Path) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")

    assert _add_atom(tmp_path, "Flat rule", "topic:atoms") == 0

    assert (tmp_path / "desk" / "atoms" / "atom-flat-rule.md").exists()


def test_add_atom_without_configured_axis_is_flat_backcompat(tmp_path: Path) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)

    assert _add_atom(tmp_path, "Old style", "object:licitaciones") == 0

    assert (tmp_path / "desk" / "atoms" / "atom-old-style.md").exists()


def test_add_atom_dot_notation_creates_nested_folders(tmp_path: Path) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")

    assert _add_atom(tmp_path, "Nested rule", "object:compra-agil.docs") == 0

    expected = tmp_path / "desk" / "atoms" / "compra-agil" / "docs" / "atom-nested-rule.md"
    assert expected.exists()


def test_add_atom_with_multiple_axis_values_is_rejected(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")
    capsys.readouterr()

    result = _add_atom(tmp_path, "Two objects", "object:licitaciones", "object:ordenes-compra")
    captured = capsys.readouterr()

    assert result != 0
    assert "multiple 'object' axis values" in captured.out + captured.err
    assert not list((tmp_path / "desk" / "atoms").rglob("atom-two-objects.md"))


def test_add_atom_with_unregistered_axis_namespace_errors(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _set_axis(tmp_path, "object")
    capsys.readouterr()

    result = _add_atom(tmp_path, "Broken axis", "topic:atoms")
    captured = capsys.readouterr()

    assert result != 0
    assert "atom_folder_axis 'object' is not a registered" in captured.out + captured.err


def test_list_atoms_axis_value_filters_and_shows_axis(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")
    assert _add_atom(tmp_path, "Licitaciones rule", "object:licitaciones") == 0
    assert _add_atom(tmp_path, "Ordenes rule", "object:ordenes-compra") == 0
    assert _add_atom(tmp_path, "Flat rule", "topic:atoms") == 0
    capsys.readouterr()

    assert main(["list", "atoms", "--root", str(tmp_path), "--axis-value", "licitaciones"]) == 0
    captured = capsys.readouterr()
    assert "atom-licitaciones-rule" in captured.out
    assert "object:licitaciones" in captured.out
    assert "atom-ordenes-rule" not in captured.out
    assert "atom-flat-rule" not in captured.out

    assert main(["list", "atoms", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "object:-" in captured.out  # flat atom shows no axis value


def test_list_atoms_axis_value_requires_configured_axis(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    capsys.readouterr()

    result = main(["list", "atoms", "--root", str(tmp_path), "--axis-value", "licitaciones"])
    captured = capsys.readouterr()

    assert result != 0
    assert "requires 'atom_folder_axis'" in captured.out


def test_reorganize_moves_flat_atoms_and_updates_store(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _init_store(tmp_path)
    _register_object_namespace(tmp_path)
    # create flat while axis is off, then enable axis
    assert _add_atom(tmp_path, "Legacy ordenes", "object:ordenes-compra") == 0
    _set_axis(tmp_path, "object")
    capsys.readouterr()

    assert main(["atoms", "reorganize", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()

    assert "Moved atom-legacy-ordenes" in captured.out
    assert not (tmp_path / "desk" / "atoms" / "atom-legacy-ordenes.md").exists()
    moved = tmp_path / "desk" / "atoms" / "ordenes-compra" / "atom-legacy-ordenes.md"
    assert moved.exists()
    assert _tracked_atom_paths(tmp_path)["atom-legacy-ordenes"] == "desk/atoms/ordenes-compra/atom-legacy-ordenes.md"

    # store integrity holds after retarget
    assert sldb_main(
        ["stores", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(ROOT)]
    ) == 0


def test_reorganize_is_idempotent(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    assert _add_atom(tmp_path, "Legacy ordenes", "object:ordenes-compra") == 0
    _set_axis(tmp_path, "object")

    assert main(["atoms", "reorganize", "--root", str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["atoms", "reorganize", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()

    assert "No atoms need to move." in captured.out


def test_reorganize_dry_run_moves_nothing(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    assert _add_atom(tmp_path, "Legacy ordenes", "object:ordenes-compra") == 0
    _set_axis(tmp_path, "object")
    capsys.readouterr()

    assert main(["atoms", "reorganize", "--root", str(tmp_path), "--dry-run"]) == 0
    captured = capsys.readouterr()

    assert "Would move atom-legacy-ordenes" in captured.out
    assert (tmp_path / "desk" / "atoms" / "atom-legacy-ordenes.md").exists()


def test_reorganize_without_axis_errors(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    capsys.readouterr()

    result = main(["atoms", "reorganize", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result != 0
    assert "No 'atom_folder_axis' configured" in captured.out


def test_graph_build_and_missing_are_clean_with_axis_subfolders(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)
    _register_object_namespace(tmp_path)
    _set_axis(tmp_path, "object")
    assert _add_atom(tmp_path, "Licitaciones rule", "object:licitaciones") == 0
    assert _add_atom(tmp_path, "Nested rule", "object:compra-agil.docs") == 0
    capsys.readouterr()

    assert main(["graph", "build", "--root", str(tmp_path)]) == 0
    assert main(["graph", "missing", "--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    assert "No missing graph references found." in captured.out
