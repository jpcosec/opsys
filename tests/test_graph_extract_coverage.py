from __future__ import annotations

from pathlib import Path

from deskops.graph.extract_coverage import EXTRACTOR_NAME, extract_coverage_graph


def test_extract_coverage_graph_materializes_component_state_and_coverage(tmp_path: Path) -> None:
    write_atom(
        tmp_path / "desk/atoms/atom-runtime.md",
        "runtime",
        "Runtime",
        "what",
        aliases=["Runtime"],
    )
    write_atom(
        tmp_path / "desk/atoms/atom-publishes.md",
        "publishes",
        "Publishes events",
        "how",
        aliases=["publishes"],
    )
    write_atom(
        tmp_path / "desk/atoms/atom-guard.md",
        "guard",
        "Guard",
        "why",
        aliases=["formValid"],
    )
    write_atom(
        tmp_path / "desk/atoms/atom-action.md",
        "action",
        "Action",
        "how",
        tags=["startRequest"],
    )
    write(
        tmp_path / "desk/atoms/atom-diagrams.md",
        """---
id: atom-diagrams
title: Diagram bundle
five_wh_one_plus: what
---

# Runtime View

```mermaid
flowchart TB
  Runtime[Runtime]
  Runtime -- publishes --> Queue[Queue]
```

# Login State

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Submitting : submit / [formValid] / startRequest
```
""",
    )

    result = extract_coverage_graph(tmp_path)
    nodes_by_id = {node.id: node for node in result.nodes}
    edges = [edge.to_dict() for edge in result.edges]

    assert EXTRACTOR_NAME == "desk_kgdb_coverage_v1"
    assert "view:desk-atoms-atom-diagrams-md-runtime-view" in nodes_by_id
    assert "diagram_element:desk-atoms-atom-diagrams-md-runtime-view:node:runtime" in nodes_by_id
    assert "diagram_element:desk-atoms-atom-diagrams-md-login-state:transition:state-idle--submit--state-submitting" in nodes_by_id

    expects = [edge for edge in edges if edge["role"] == "expects_facet"]
    assert ("diagram_element:desk-atoms-atom-diagrams-md-runtime-view:edge:node-runtime--publishes--node-queue", "facet:how") in {
        (edge["source_id"], edge["target_id"]) for edge in expects
    }
    assert ("diagram_element:desk-atoms-atom-diagrams-md-runtime-view:edge:node-runtime--publishes--node-queue", "facet:why") in {
        (edge["source_id"], edge["target_id"]) for edge in expects
    }

    covers = [edge for edge in edges if edge["role"] == "covers_facet"]
    guard_cover = next(edge for edge in covers if edge["atom_id"] == "guard")
    assert guard_cover["facet"] == "why"
    assert guard_cover["match_basis"] == "alias"
    assert "semantics.guard=\"formValid\"" in guard_cover["evidence"]
    assert guard_cover["score"] >= 0.70

    assert not any(edge for edge in covers if edge["atom_id"] == "runtime" and edge["facet"] == "why")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_atom(
    path: Path,
    atom_id: str,
    title: str,
    five_wh_one_plus: str,
    *,
    aliases: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    aliases_block = ""
    if aliases:
        aliases_block = "aliases:\n" + "\n".join(f"  - {alias}" for alias in aliases) + "\n"
    tags_block = "tags:\n" + "\n".join(f"  - {tag}" for tag in (tags or [])) + ("\n" if tags is not None else "tags: []\n")
    write(
        path,
        f"""---
id: {atom_id}
title: {title}
five_wh_one_plus: {five_wh_one_plus}
{aliases_block}{tags_block}---

# {title}

## Answer

Knowledge.
""",
    )
