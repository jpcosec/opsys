from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from desk.models import AtomDoc
from deskops.atom_tags import add_namespace
from deskops.atom_tags import validate_atom_tag_namespaces
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


ATOM_SAMPLE = {
    "title": "Deskops models are sldb documents",
    "id": "atom-deskops-models-are-sldb-documents",
    "five_wh_one_plus": "what",
    "answer": "Deskops persists workflow artifacts as sldb StructuredNLDoc models.",
    "tags": ["system:deskops", "system:sldb", "topic:document-model"],
}


def test_atom_doc_roundtrips_new_single_answer_contract() -> None:
    rendered = render_model_markdown(AtomDoc, ATOM_SAMPLE)
    extracted = extract_model_data(AtomDoc, rendered)

    assert extracted == ATOM_SAMPLE
    assert "5WH1+: what" in rendered
    assert "## Answer" in rendered
    assert "Status:" not in rendered
    assert "Materializes Into" not in rendered


def test_atom_doc_rejects_unknown_5wh1_plus_question() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["five_wh_one_plus"] = "pattern"

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


def test_atom_doc_rejects_tags_without_namespace() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["tags"] = ["deskops"]

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


def test_namespace_registry_validates_known_namespaces(tmp_path: Path) -> None:
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    add_namespace(
        registry,
        "system",
        meaning="System, project, or tool the atom belongs to.",
        use_when="The atom is about a specific system.",
        do_not_use_when="The tag is only a general topic.",
        examples=["system:deskops"],
    )

    validate_atom_tag_namespaces(["system:deskops"], registry)
    with pytest.raises(ValueError, match="Unknown atom tag namespace"):
        validate_atom_tag_namespaces(["topic:atoms"], registry)


def test_add_namespace_rejects_duplicate_namespace(tmp_path: Path) -> None:
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    add_namespace(
        registry,
        "pattern",
        meaning="Reusable solution shape.",
        use_when="The atom describes a repeatable solution.",
        do_not_use_when="The atom only mentions a topic.",
        examples=["pattern:roundtrip-validation"],
    )

    with pytest.raises(ValueError, match="already exists"):
        add_namespace(
            registry,
            "pattern",
            meaning="Duplicate.",
            use_when="Duplicate.",
            do_not_use_when="Duplicate.",
            examples=[],
        )
