from __future__ import annotations

from pathlib import Path

import yaml

from deskops.graph.extract_edges import extract_declared_edges


ROOT = Path(__file__).resolve().parents[1]

COMPOSED_DOCS = (
    "README.md",
    "docs/atoms.md",
    "docs/faq.md",
    "docs/how-to-report.md",
    "docs/how-to-test-ux-cli.md",
    "docs/knowledge-materialization-model.md",
    "docs/quickstart.md",
    "docs/sldb-templates.md",
    "docs/workflow-policy-reference.md",
)

ALLOWED_ROLES = {"references", "documents", "specifies", "constrains", "validates"}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} has no YAML frontmatter"
    _, rest = text.split("---\n", 1)
    block, _body = rest.split("\n---", 1)
    loaded = yaml.safe_load(block)
    assert isinstance(loaded, dict), f"{path} frontmatter is not a mapping"
    return loaded


def test_composed_docs_declare_atom_frontmatter() -> None:
    for relative_path in COMPOSED_DOCS:
        atoms = _frontmatter(ROOT / relative_path).get("atoms")
        assert isinstance(atoms, list) and atoms, f"{relative_path} declares no atoms"
        for atom in atoms:
            assert isinstance(atom, dict) and isinstance(atom.get("id"), str)
            assert atom["id"].startswith("atom-")
            assert atom.get("role") in ALLOWED_ROLES


def test_packaged_faq_is_a_projection_of_the_docs_faq() -> None:
    assert (ROOT / "deskops" / "data" / "faq.md").read_bytes() == (
        ROOT / "docs" / "faq.md"
    ).read_bytes()


def test_composed_doc_frontmatter_emits_declared_atom_edges() -> None:
    result = extract_declared_edges(ROOT)
    edges = {(edge.source_id, edge.target_id, edge.role) for edge in result.edges}

    assert (
        "doc:README.md",
        "atom:atom-docs-are-human-facing-atom-materializations",
        "documents",
    ) in edges
