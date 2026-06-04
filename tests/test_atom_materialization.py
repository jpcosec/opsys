from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from desk.materializers import build_architecture_doc_payload
from desk.models import AtomDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


ATOM_SAMPLE = {
    "title": "Deskops reads through sldb",
    "id": "atom-deskops-reads-through-sldb",
    "five_wh_one_plus": "how",
    "answer": "Deskops extracts model payloads from structured markdown with sldb runtime validation.",
    "tags": ["system:deskops", "system:sldb", "topic:composition"],
}


def test_atom_doc_roundtrips() -> None:
    rendered = render_model_markdown(AtomDoc, ATOM_SAMPLE)
    extracted = extract_model_data(AtomDoc, rendered)

    assert extracted == ATOM_SAMPLE
    assert "## Answer" in rendered
    assert "## Materializes Into" not in rendered


def test_atom_materializer_builds_composed_document_payload() -> None:
    doc_payload = build_architecture_doc_payload(ATOM_SAMPLE)

    assert "Materialized from `atom-deskops-reads-through-sldb`" in doc_payload["body"]
    assert "5WH1+: `how`" in doc_payload["body"]
    assert ATOM_SAMPLE["answer"] in doc_payload["body"]
