"""Document invariants are validators of the model (DK6): the model rejects the bad payload,
and sldb, which applies the model on every write, rejects it through ``fields update`` and
``docs update`` too."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.models import AtomDoc, CrossroadDoc, ProtoAtomDoc
from deskops.models.validation import InvalidDocument, model_errors, validated, validation_messages
from sldb.cli import main as sldb_main

ATOM = {"id": "atom-oven", "title": "Oven", "five_wh_one_plus": "what", "answer": "450 degrees."}
PROTO = {"id": "proto-masa", "title": "Masa"}
CROSSROAD = {"id": "crossroad-pizzeria--carta", "path": "pizzeria.carta", "title": "Carta", "content": "Dishes."}


def _rejects(model, payload: dict, text: str) -> None:
    with pytest.raises(ValidationError) as excinfo:
        model(**payload)
    assert text in str(excinfo.value)
    assert validation_messages(excinfo.value) == [text]


# ------------------------------------------------------------------ AtomDoc
def test_atom_id_follows_the_slug_convention() -> None:
    _rejects(AtomDoc, {**ATOM, "id": "bad-atom"}, "atom id must follow slug convention atom-<slug>: bad-atom")
    _rejects(AtomDoc, {**ATOM, "id": "atom-"}, "atom id must follow slug convention atom-<slug>: atom-")
    _rejects(AtomDoc, {**ATOM, "id": "atom-Oven"}, "atom id must follow slug convention atom-<slug>: atom-Oven")
    assert AtomDoc(**{**ATOM, "id": "atom-oven-450"}).id == "atom-oven-450"


def test_atom_tags_are_namespaced() -> None:
    _rejects(AtomDoc, {**ATOM, "tags": ["deskops"]}, "Invalid atom tag 'deskops'. Expected namespace:value.")
    _rejects(AtomDoc, {**ATOM, "tags": ["system:deskops", "bad tag"]}, "Invalid atom tag 'bad tag'. Expected namespace:value.")
    assert AtomDoc(**{**ATOM, "tags": ["system:deskops", "topic:atoms"]}).tags == ["system:deskops", "topic:atoms"]


def test_atom_domain_tag_is_a_domain_path() -> None:
    _rejects(AtomDoc, {**ATOM, "tags": ["domain:a..b"]}, "Invalid domain path 'a..b': use lowercase segments separated by dots.")
    _rejects(AtomDoc, {**ATOM, "tags": ["domain:a."]}, "Invalid domain path 'a.': use lowercase segments separated by dots.")
    assert AtomDoc(**{**ATOM, "tags": ["domain:pizzeria.carta"]}).tags == ["domain:pizzeria.carta"]


# ------------------------------------------------------------------ ProtoAtomDoc
def test_protoatom_id_follows_the_slug_convention() -> None:
    _rejects(ProtoAtomDoc, {**PROTO, "id": "badproto"}, "Protoatom id must follow slug convention proto-<slug>: badproto")
    _rejects(ProtoAtomDoc, {**PROTO, "id": "proto-"}, "Protoatom id must follow slug convention proto-<slug>: proto-")
    assert ProtoAtomDoc(**PROTO).id == "proto-masa"


def test_protoatom_tags_are_namespaced_domain_paths() -> None:
    _rejects(ProtoAtomDoc, {**PROTO, "tags": ["bad tag"]}, "Invalid atom tag 'bad tag'. Expected namespace:value.")
    _rejects(ProtoAtomDoc, {**PROTO, "tags": ["domain:a..b"]}, "Invalid domain path 'a..b': use lowercase segments separated by dots.")


def test_protoatom_hangs_from_one_place() -> None:
    _rejects(
        ProtoAtomDoc,
        {**PROTO, "tags": ["domain:a", "domain:b"]},
        "A protoatom hangs from one place in the domain tree: use a single domain:<path> tag.",
    )
    assert ProtoAtomDoc(**{**PROTO, "tags": ["domain:a", "system:x"]}).tags == ["domain:a", "system:x"]


# ------------------------------------------------------------------ CrossroadDoc
def test_crossroad_path_is_a_domain_path() -> None:
    _rejects(
        CrossroadDoc,
        {**CROSSROAD, "id": "crossroad-Bad--Path", "path": "Bad.Path"},
        "Invalid domain path 'Bad.Path': use lowercase segments separated by dots.",
    )


def test_crossroad_id_names_its_path() -> None:
    _rejects(CrossroadDoc, {**CROSSROAD, "id": "crossroad-wrong"}, "crossroad id must be crossroad-pizzeria--carta")
    assert CrossroadDoc(**CROSSROAD).id == "crossroad-pizzeria--carta"


def test_crossroad_content_is_written() -> None:
    _rejects(CrossroadDoc, {**CROSSROAD, "content": "   "}, "a crossroad must describe its children: content cannot be empty")


# ------------------------------------------------------------------ reporting
def test_services_report_the_validators_own_line() -> None:
    with pytest.raises(InvalidDocument) as excinfo:
        validated(AtomDoc, {**ATOM, "id": "bad-atom", "tags": ["bad tag"]})
    assert isinstance(excinfo.value, ValueError)
    assert str(excinfo.value) == (
        "atom id must follow slug convention atom-<slug>: bad-atom\nInvalid atom tag 'bad tag'. Expected namespace:value."
    )
    assert model_errors(AtomDoc, ATOM) == []
    assert model_errors(AtomDoc, {**ATOM, "tags": 5}, invalid="model validation failed") == [
        "model validation failed: tags: Input should be a valid list"
    ]


# ------------------------------------------------------------------ sldb applies the model on every write
def _sldb(argv: list[str]) -> int:
    code, _ = _sldb_run(argv)
    return code


def _sldb_run(argv: list[str]) -> tuple[int, str]:
    """Exit code and the message sldb refuses with (its CLI exits with the text as the code)."""
    try:
        return int(sldb_main(argv) or 0), ""
    except SystemExit as exc:
        if isinstance(exc.code, int) or exc.code is None:
            return int(exc.code or 0), ""
        return 1, str(exc.code)


@pytest.fixture
def tracked_desk(tmp_path: Path) -> Path:
    assert main(["desk", "install", str(tmp_path)]) == 0
    config = tmp_path / "desk" / "config.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    data["atom_folder_axis"] = "domain"
    config.write_text(json.dumps(data), encoding="utf-8")
    assert _sldb(["stores", "init", "--path", str(tmp_path)]) == 0
    store = tmp_path / ".sldb"
    for model in ("AtomDoc", "ProtoAtomDoc", "CrossroadDoc"):
        assert _sldb(["models", "add", f"deskops.models:{model}", "--store", str(store), "--pythonpath", str(ROOT)]) == 0
    assert main(["atoms", "crossroad", "pizzeria", "--title", "Pizzería", "--content", "All.", "--root", str(tmp_path)]) == 0
    assert main([
        "add", "atom", "--root", str(tmp_path), "--title", "Oven", "--five-wh-one-plus", "what",
        "--answer", "450 degrees.", "--tags", "domain:pizzeria",
    ]) == 0
    return tmp_path


def _store_args(root: Path) -> list[str]:
    return ["--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]


def test_sldb_fields_update_rejects_an_atom_id_off_the_slug_convention(tracked_desk: Path, capsys) -> None:
    atom = tracked_desk / "desk" / "atoms" / "pizzeria" / "atom-oven.md"
    before = atom.read_text(encoding="utf-8")
    code, message = _sldb_run(["fields", "update", "docs/AtomDoc/atom-oven/id", '"bad-atom"', *_store_args(tracked_desk)])
    out = capsys.readouterr()
    assert code != 0
    assert "atom id must follow slug convention atom-<slug>: bad-atom" in message + out.out + out.err
    assert atom.read_text(encoding="utf-8") == before


def test_sldb_fields_update_rejects_a_crossroad_path_that_is_not_a_domain_path(tracked_desk: Path, capsys) -> None:
    crossroad = tracked_desk / "desk" / "atoms" / "pizzeria" / "crossroad-pizzeria.md"
    before = crossroad.read_text(encoding="utf-8")
    code, message = _sldb_run(["fields", "update", "docs/CrossroadDoc/crossroad-pizzeria/path", '"Bad.Path"', *_store_args(tracked_desk)])
    out = capsys.readouterr()
    assert code != 0
    assert "Invalid domain path 'Bad.Path': use lowercase segments separated by dots." in message + out.out + out.err
    assert crossroad.read_text(encoding="utf-8") == before


def test_sldb_docs_update_rejects_an_atom_with_a_malformed_tag(tracked_desk: Path, capsys) -> None:
    atom = tracked_desk / "desk" / "atoms" / "pizzeria" / "atom-oven.md"
    before = atom.read_text(encoding="utf-8")
    payload = json.dumps({**ATOM, "tags": ["bad tag"]})
    code, message = _sldb_run(["docs", "update", "atom-oven", payload, *_store_args(tracked_desk)])
    out = capsys.readouterr()
    assert code != 0
    assert "Invalid atom tag 'bad tag'. Expected namespace:value." in message + out.out + out.err
    assert atom.read_text(encoding="utf-8") == before


def test_sldb_docs_update_rejects_a_crossroad_whose_id_does_not_name_its_path(tracked_desk: Path, capsys) -> None:
    crossroad = tracked_desk / "desk" / "atoms" / "pizzeria" / "crossroad-pizzeria.md"
    before = crossroad.read_text(encoding="utf-8")
    payload = json.dumps({"id": "crossroad-wrong", "path": "pizzeria", "title": "Pizzería", "content": "All."})
    code, message = _sldb_run(["docs", "update", "crossroad-pizzeria", payload, *_store_args(tracked_desk)])
    out = capsys.readouterr()
    assert code != 0
    assert "crossroad id must be crossroad-pizzeria" in message + out.out + out.err
    assert crossroad.read_text(encoding="utf-8") == before
