from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main


def _install_sandbox(root: Path) -> None:
    assert main(["desk", "install", str(root)]) == 0


def test_atoms_create_from_pill_uses_matching_section_and_exact_provenance(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)

    result = main(
        [
            "add",
            "pill",
            "--root",
            str(tmp_path),
            "--title",
            "Guardrail: Keep layers clean",
            "--what",
            "Keep modeled fields authoritative.",
            "--why",
            "The model is the durable source of truth.",
            "--when",
            "Whenever changing tracked docs.",
            "--where",
            "desk/ and docs/ surfaces.",
            "--how",
            "Render through modeled templates.",
            "--how-not",
            "Do not patch rendered docs by hand.",
        ]
    )
    assert result == 0

    created = main(
        [
            "atoms",
            "create",
            "atom-pill-what-guidance",
            "--five-wh-one-plus",
            "what",
            "--from-pill",
            "pill-guardrail-keep-layers-clean",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert created == 0
    assert "Created atom atom-pill-what-guidance" in captured.out
    assert "Source kind: pill" in captured.out
    assert "Source selector: pill-guardrail-keep-layers-clean" in captured.out
    assert "Source provenance: desk/contexts/pill-guardrail-keep-layers-clean.md::what" in captured.out

    atom_text = (tmp_path / "desk" / "atoms" / "atom-pill-what-guidance.md").read_text(encoding="utf-8")
    assert "Guardrail: Keep layers clean — What" in atom_text
    assert "five_wh_one_plus: what" in atom_text
    assert "Keep modeled fields authoritative." in atom_text
    assert "provenance: desk/contexts/pill-guardrail-keep-layers-clean.md::what" in atom_text


def test_atoms_create_from_graph_finding_preserves_finding_provenance(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)

    issue_path = tmp_path / "desk" / "drawer" / "issues" / "issue-missing-references.md"
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    issue_path.write_text(
        """# Missing References

ID: issue-missing-references

## Related Atoms

- atom-missing
""",
        encoding="utf-8",
    )

    created = main(
        [
            "atoms",
            "create",
            "atom-graph-finding-missing-atom",
            "--five-wh-one-plus",
            "why",
            "--from-graph",
            "issue:issue-missing-references->atom:atom-missing",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert created == 0
    assert "Source kind: graph" in captured.out
    assert "Source selector: issue:issue-missing-references->atom:atom-missing" in captured.out
    assert "Source provenance: desk/drawer/issues/issue-missing-references.md::line:7:related atoms" in captured.out

    atom_text = (tmp_path / "desk" / "atoms" / "atom-graph-finding-missing-atom.md").read_text(encoding="utf-8")
    assert "five_wh_one_plus: why" in atom_text
    assert "Graph finding `dangling_source_atom_reference` records a missing reference" in atom_text
    assert "- Reason: declared target was not found among extracted graph nodes" in atom_text
    assert "provenance: desk/drawer/issues/issue-missing-references.md::line:7:related atoms" in atom_text


def test_atoms_create_from_diagram_wraps_mermaid_source_and_preserves_path(tmp_path: Path, capsys) -> None:
    _install_sandbox(tmp_path)

    diagram_path = tmp_path / "docs" / "diagrams" / "runtime" / "source.mmd"
    diagram_path.parent.mkdir(parents=True, exist_ok=True)
    diagram_path.write_text(
        "flowchart TB\n  Runtime[Runtime]\n  Runtime --> Queue[Queue]\n",
        encoding="utf-8",
    )

    created = main(
        [
            "atoms",
            "create",
            "atom-runtime-diagram",
            "--five-wh-one-plus",
            "what",
            "--from-diagram",
            "docs/diagrams/runtime/source.mmd",
            "--root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert created == 0
    assert "Source kind: diagram" in captured.out
    assert "Source selector: docs/diagrams/runtime/source.mmd" in captured.out
    assert "Source provenance: docs/diagrams/runtime/source.mmd" in captured.out

    atom_text = (tmp_path / "desk" / "atoms" / "atom-runtime-diagram.md").read_text(encoding="utf-8")
    assert "Source — Diagram" in atom_text
    assert "provenance: docs/diagrams/runtime/source.mmd" in atom_text
    assert "```mermaid" in atom_text
    assert "Runtime --> Queue[Queue]" in atom_text
