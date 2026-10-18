"""Derived reverse traceability for atoms.

Atoms do not store outgoing use-site lists. This module projects the declared
edges extracted from documents, tasks, tests, and diagrams into the reverse
question: which artifacts reference a given atom, and in what role?
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops.graph.extract_edges import extract_declared_edges


@dataclass(frozen=True)
class AtomUseSite:
    """One artifact that declares a reference to an atom."""

    source_id: str
    role: str
    path: str
    locator: str


def atom_use_sites(root: Path, atom_id: str) -> list[AtomUseSite]:
    """Return the declared use sites of ``atom_id`` under ``root``.

    The result is a read-only projection over ``extract_declared_edges``; atom
    documents are neither read nor written here. Sites are sorted by provenance
    path and locator.
    """
    target_id = f"atom:{atom_id.removeprefix('atom:')}"
    result = extract_declared_edges(root)
    sites = [
        AtomUseSite(
            source_id=edge.source_id,
            role=edge.role,
            path=edge.provenance_path,
            locator=edge.provenance_locator,
        )
        for edge in result.edges
        if edge.target_id == target_id
    ]
    return sorted(sites, key=lambda site: (site.path, site.locator))
