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
from deskops.graph.checks import find_missing_graph_references
from deskops.models import MaterializationContractDoc
from deskops.operations import DeskopsOperations
from deskops.specs.loader import SpecRegistry
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MATERIALIZATION_SAMPLE = {
    "id": "materialization-knowledge-materialization-model",
    "title": "Knowledge materialization model",
    "source_atoms": ["atom-source-a", "atom-source-b"],
    "target_kind": "doc",
    "target_identity": "docs/knowledge-materialization-model.md",
    "intent": "Compose the selected atoms into the durable explanation doc.",
    "validation": ["pytest"],
    "tags": ["system:deskops", "topic:materialization"],
    "provenance": "docs/knowledge-materialization-model.md",
}


def test_materialization_contract_doc_roundtrips() -> None:
    rendered = render_model_markdown(MaterializationContractDoc, MATERIALIZATION_SAMPLE)
    extracted = extract_model_data(MaterializationContractDoc, rendered)

    assert extracted == MATERIALIZATION_SAMPLE
    assert "## Intent" in rendered
    assert "source_atoms:" in rendered
    assert "target_identity: docs/knowledge-materialization-model.md" in rendered



def test_materialization_contract_spec_and_workspace_scaffold(tmp_path: Path) -> None:
    registry = SpecRegistry.load(ROOT / "spec")

    assert "artifact.materialization" in registry.artifacts
    assert "field.source_atoms" in registry.fields
    assert "field.target_kind" in registry.fields
    assert "field.target_identity" in registry.fields
    assert "field.intent" in registry.fields
    assert "field.provenance" in registry.fields

    operations = DeskopsOperations(tmp_path)
    operations.ensure_workspace()

    assert (tmp_path / "desk" / "materializations").exists()



def test_cli_add_list_and_show_materialization(tmp_path: Path, capsys) -> None:
    created = main(
        [
            "add",
            "materialization",
            "--root",
            str(tmp_path),
            "--title",
            "Knowledge materialization model",
            "--source-atoms",
            "atom-knowledge-a",
            "atom-knowledge-b",
            "--target-kind",
            "doc",
            "--target-identity",
            "docs/knowledge-materialization-model.md",
            "--intent",
            "Compose the selected atoms into a guide.",
            "--validation",
            "pytest",
        ]
    )
    created_out = capsys.readouterr()

    assert created == 0
    assert "Created materialization materialization-knowledge-materialization-model" in created_out.out
    assert (tmp_path / "desk" / "materializations" / "materialization-knowledge-materialization-model.md").exists()

    listed = main(["list", "materializations", "--root", str(tmp_path)])
    listed_out = capsys.readouterr()
    assert listed == 0
    assert "materialization-knowledge-materialization-model | Knowledge materialization model" in listed_out.out

    shown = main(["show", "materialization", "materialization-knowledge-materialization-model", "--root", str(tmp_path)])
    shown_out = capsys.readouterr()
    assert shown == 0
    assert "Materialization: materialization-knowledge-materialization-model" in shown_out.out
    assert "source_atoms: atom-knowledge-a, atom-knowledge-b" in shown_out.out
    assert "target_kind: doc" in shown_out.out
    assert "target_identity: docs/knowledge-materialization-model.md" in shown_out.out



def test_materialization_graph_checks_accept_resolved_source_atoms_and_target_identity(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")
    write(tmp_path / "docs/guide.md", "# Guide\n")
    write(
        tmp_path / "desk/materializations/materialization-guide.md",
        """---
id: materialization-guide
title: Guide Materialization
source_atoms:
- atom-existing
target_kind: doc
target_identity: docs/guide.md
validation:
- pytest
tags: []
---

# Guide Materialization

## Intent

Project the atom into the guide.
""",
    )

    assert find_missing_graph_references(tmp_path) == []



def test_graph_missing_reports_materialization_reference_failures(tmp_path: Path, capsys) -> None:
    write(
        tmp_path / "desk/materializations/materialization-guide.md",
        """---
id: materialization-guide
title: Guide Materialization
source_atoms:
- atom-missing
target_kind: doc
target_identity: docs/missing-guide.md
validation:
- pytest
tags: []
---

# Guide Materialization

## Intent

Project the atom into the guide.
""",
    )

    result = main(["graph", "missing", "--root", str(tmp_path)])
    captured = capsys.readouterr()

    assert result == 1
    assert "dangling_source_atom_reference: materialization:materialization-guide -> atom:atom-missing" in captured.out
    assert "missing_declared_target: materialization:materialization-guide -> doc:docs/missing-guide.md" in captured.out
    assert "provenance: desk/materializations/materialization-guide.md:frontmatter" in captured.out



def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")



def write_atom(path: Path, atom_id: str, title: str) -> None:
    write(
        path,
        f"""---
id: {atom_id}
title: {title}
five_wh_one_plus: what
tags: []
---

# {title}

## Answer

Existing knowledge.
""",
    )
