from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from desk.materializers import (
    build_architecture_doc_payload,
    build_feature_payload,
    build_pill_payload,
    build_task_payload,
)
from desk.models import AtomDoc
from sldb.runtime.validation import extract_model_data, render_model_markdown


ATOM_SAMPLE = {
    "title": "Self-described store layout",
    "id": "atom-001",
    "status": "stable",
    "category": "store-contract",
    "what": "The .sldb workspace separates durable core state from runtime state and local config.",
    "why": "Contributors need a clear durable-versus-ephemeral boundary so git history and local rebuilds stay clean.",
    "how": "Version durable contracts under core, regenerate runtime indexes, and keep machine-local overrides out of shared history.",
    "when": "Apply whenever store layout, tracking, or git policy changes are under discussion.",
    "where": "The concept applies to .sldb/, store routing code, and contributor workflow guidance.",
    "for_whom": "Maintainers changing SLDB store behavior or operating the repo through desk.",
    "related_atoms": [],
    "materializes_into": [
        "docs/architecture/self-described-store-layout-derivation.md",
        "desk/drawer/features/feature-001-sldb-core-runtime-layout.md",
        "desk/contexts/pill-006-self-described-store-layout.md",
    ],
    "stabilized_in": [
        ".sldb/README.md",
        "docs/workspaces.md",
    ],
    "distinct_from_pills": "A pill is temporary execution context; this atom is durable conceptual policy.",
    "tags": ["system:sldb", "topic:atoms", "topic:store"],
}


def test_atom_doc_roundtrips() -> None:
    rendered = render_model_markdown(AtomDoc, ATOM_SAMPLE)
    extracted = extract_model_data(AtomDoc, rendered)

    assert extracted == ATOM_SAMPLE
    assert "## Materializes Into" in rendered


def test_atom_materializers_embed_source_traceability() -> None:
    doc_payload = build_architecture_doc_payload(ATOM_SAMPLE)
    feature_payload = build_feature_payload(ATOM_SAMPLE, feature_id="feature-x")
    task_payload = build_task_payload(ATOM_SAMPLE, task_id="task-x")
    pill_payload = build_pill_payload(ATOM_SAMPLE, pill_id="pill-x")

    assert "Derived from `atom-001`" in doc_payload["body"]
    assert "source-atom:atom-001" in feature_payload["tags"]
    assert "source-atom:atom-001" in task_payload["tags"]
    assert "source-atom:atom-001" in pill_payload["tags"]
