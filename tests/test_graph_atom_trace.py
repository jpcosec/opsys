from __future__ import annotations

from pathlib import Path

from deskops.graph.atom_trace import atom_use_sites


def test_atom_use_sites_reports_document_without_mutating_atom(tmp_path: Path) -> None:
    atom_path = tmp_path / "desk/atoms/atom-consumer-target.md"
    write_atom(atom_path, "atom-consumer-target", "Consumer Target")
    write(
        tmp_path / "docs/guide.md",
        """---
id: guide-doc
atoms:
  - id: atom-consumer-target
    role: documents
---

# Guide
""",
    )
    before = atom_path.read_bytes()

    sites = atom_use_sites(tmp_path, "atom-consumer-target")

    assert [(site.source_id, site.role, site.path, site.locator) for site in sites] == [
        ("doc:docs/guide.md", "documents", "docs/guide.md", "frontmatter")
    ]
    assert atom_path.read_bytes() == before


def test_atom_use_sites_reports_task_source(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-consumer-target.md", "atom-consumer-target", "Consumer Target")
    write(
        tmp_path / "desk/tasks/task-consumer.md",
        """---
id: task-consumer
atoms:
  - atom-consumer-target
---

# Consumer Task
""",
    )

    sites = atom_use_sites(tmp_path, "atom-consumer-target")

    assert ("task:task-consumer", "references", "desk/tasks/task-consumer.md", "frontmatter") in [
        (site.source_id, site.role, site.path, site.locator) for site in sites
    ]


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
