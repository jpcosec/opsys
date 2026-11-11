"""Incoming references of a desk document, read and rewritten by sldb (GD22).

``sldb.api.referrers`` and ``rewrite_references`` find the project graph in the project_graph
key of the store's ``store.yaml``. A desk declares none: its configuration holds a callable
(``closed_document``), so the desk graph is built in process (``desk_graph``, DO8). This module
passes that graph to the sldb functions those two are made of:

- ``resolve_target`` and ``find_hits`` give the referrers. Declared fields come from the
  store's edge index. Prose mentions come from the graph's ``MentionPattern`` rules
  (``SECTION_MENTIONS`` and ``LINE_MENTIONS`` in ``deskops.graph.desk_graph``).
- ``rewrite_references`` rewrites the fields.
- ``rewritten_line`` and ``replace_text`` rewrite the mentions.

Every write joins the caller's ``desk_transaction``, so a failure restores every file.
A desk without a store has no fields and no transaction: its mentions come from the graph,
and the rewritten files are written as plain files.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import TYPE_CHECKING
from typing import Any

from deskops import doc_access
from deskops.graph.desk_graph import PROVENANCE_FIELDS
from deskops.graph.desk_graph import desk_graph
from deskops.paths import package_pythonpath

if TYPE_CHECKING:
    from sldb.api.documents.transaction import Transaction
    from sldb.api.edges.project_graph import ProjectGraph
    from sldb.api.edges.referrer import Referrer
    from sldb.api.edges.referrers import Target

# The GD22 pieces are imported where they are used, as `deskops.services.replace` does with
# `replace_text`, so importing deskops does not depend on them.


@dataclass(frozen=True)
class Inbound:
    """One incoming reference: the file that holds it and where it sits in that file."""

    path: str
    location: str
    referrer: Referrer


class _Lookup:
    """The desk's store (when it has one), its graph, and a document resolved over both."""

    def __init__(self, root: Path) -> None:
        from sldb.api.stores.open_store import open_store

        self.root = root.resolve()
        self.location: Any = (
            open_store(doc_access.store_path(self.root), mode="readonly") if doc_access.has_store(self.root) else None
        )
        self.graph: ProjectGraph = desk_graph(self.root)

    def target(self, path: Path | str) -> Target | None:
        """The document at ``path``, as a tracked document or as a graph node. None when it is neither."""
        from sldb.api.edges.referrers import Target
        from sldb.api.edges.referrers import resolve_target
        from sldb.core.exceptions import SLDBDocumentTargetError

        relative = doc_access.relative_path(self.root, path)
        if self.location is not None:
            try:
                return resolve_target(self.location, self.graph, relative)
            except SLDBDocumentTargetError:
                pass
        node = self.graph.nodes.lookup.by_path.get(relative)
        return Target(relative, None, None, None, node.id) if node is not None else None

    def hits(self, target: Target) -> list[Referrer]:
        from sldb.api.edges.referrers import find_hits
        from sldb.api.edges.rewrite_mentions import mention_hits

        if self.location is not None:
            return [referrer for referrer, _ in find_hits(self.location, target, self.graph)]
        return [referrer for referrer, _ in mention_hits(self.graph, target.node_id)] if target.node_id else []

    def paths_by_export_id(self) -> dict[str, str]:
        return {f"{entry.model}:{entry.name}": path for path, entry in doc_access.index_entries(self.root).items()}


def referrers_of(root: Path, path: Path | str, *, excluded: Iterable[Path | str] = ()) -> list[Inbound]:
    """Every reference to the document at ``path``. Files in ``excluded`` are left out, and so is the document itself.

    A field reference is located at ``<path> (<field>)``, a mention at ``<path>:<line>``.
    """
    lookup = _Lookup(root)
    target = lookup.target(path)
    if target is None:
        return []
    return _inbound(lookup, target, _skipped(lookup.root, path, excluded))


def rewrite_referrers(
    root: Path,
    path: Path | str,
    replacement: Path | str | None,
    *,
    transaction: Transaction | None,
    excluded: Iterable[Path | str] = (),
) -> list[str]:
    """Point every reference to ``path`` at ``replacement``. With None, remove the field references.

    Mentions in prose are never deleted, so with None they are left in place. Every write
    joins ``transaction``. Returns where each change was made: ``<path> (<field>)`` or
    ``<path>:<line>``.
    """
    from sldb.api.edges.rewrite_references import rewrite_references

    lookup = _Lookup(root)
    target = lookup.target(path)
    if target is None:
        return []
    new = lookup.target(replacement) if replacement is not None else None
    if replacement is not None and new is None:
        raise ValueError(f"{doc_access.relative_path(lookup.root, replacement)} is neither a tracked document nor a desk graph node")
    inbound = _inbound(lookup, target, _skipped(lookup.root, path, excluded))
    changed: list[str] = []
    fields = [item for item in inbound if item.referrer.origin == "schema"]
    if fields and lookup.location is not None and target.export_id:
        report = rewrite_references(
            lookup.location.store_path,
            target.export_id,
            new.export_id or new.given if new is not None else None,
            transaction=transaction,
            pythonpath=package_pythonpath(),
        )
        changed.extend(
            f"{lookup.paths_by_export_id().get(change['source'], change['source'])} ({change['field']})"
            for change in report.changed
            if change.get("field")
        )
    if new is not None:
        changed.extend(_rewrite_mentions(lookup, target, new, [item for item in inbound if item.referrer.origin == "mention"], transaction))
    doc_access.forget_index(lookup.root)
    return list(dict.fromkeys(changed))


def dangling_referrers(root: Path, path: Path | str, *, excluded: Iterable[Path | str] = ()) -> list[Inbound]:
    """The references a deletion of ``path`` would leave behind.

    Provenance fields (``from_drawer``) are left out: once the source is deleted they are
    records, not references.
    """
    return [item for item in referrers_of(root, path, excluded=excluded) if item.referrer.field not in PROVENANCE_FIELDS]


def alert_dangling(removed: str, inbound: Iterable[Inbound]) -> None:
    """Print one ``alert:`` line to stderr for each file that still references the removed document. The exit code does not change."""
    for path in dict.fromkeys(item.path for item in inbound):
        print(f"alert: {removed} still referenced by {path}", file=sys.stderr)


def _skipped(root: Path, path: Path | str, excluded: Iterable[Path | str]) -> set[str]:
    return {doc_access.relative_path(root, item) for item in (path, *excluded)}


def _inbound(lookup: _Lookup, target: Target, skipped: set[str]) -> list[Inbound]:
    by_export_id = lookup.paths_by_export_id()
    tracked = set(by_export_id.values())
    found: list[Inbound] = []
    for referrer in lookup.hits(target):
        if referrer.origin == "schema":
            source = by_export_id.get(referrer.source, referrer.source)
            location = f"{source} ({referrer.field})"
        else:
            source, location = referrer.source, referrer.location or referrer.source
            # A line mention (SOURCE_PATH) also reads the frontmatter. In a tracked document, the store's
            # field index already gives those lines as fields, so they are not counted again as prose.
            if source in tracked and _in_frontmatter(lookup.root / source, location):
                continue
        if source not in skipped:
            found.append(Inbound(path=source, location=location, referrer=referrer))
    return found


def _in_frontmatter(path: Path, location: str) -> bool:
    try:
        lines = path.read_text(encoding="utf-8").split("\n")
        number = int(location.rsplit(":", 1)[1])
    except (OSError, UnicodeDecodeError, ValueError):
        return False
    if not lines or lines[0] != "---":
        return False
    end = next((index for index, line in enumerate(lines[1:], start=2) if line == "---"), None)
    return end is not None and number < end


def _rewrite_mentions(lookup: _Lookup, target: Target, new: Target, mentions: list[Inbound], transaction: Transaction | None) -> list[str]:
    """Rewrite each mentioning file once. A file whose lines are unchanged is not written."""
    from sldb.api.documents.replace_text import replace_text
    from sldb.api.edges.rewrite_mentions import rewritten_line

    changed: list[str] = []
    by_path: dict[str, list[Inbound]] = {}
    for item in mentions:
        by_path.setdefault(item.path, []).append(item)
    for relative, items in by_path.items():
        file = lookup.root / relative
        text = file.read_text(encoding="utf-8")
        lines = text.split("\n")
        for item in items:
            number = int(item.location.rsplit(":", 1)[1])
            if not 0 < number <= len(lines):
                continue
            lines[number - 1], made, _ = rewritten_line(lines[number - 1], lookup.graph, target, new, item.referrer)
            if made:
                changed.append(item.location)
        new_text = "\n".join(lines)
        if new_text == text:
            continue
        if lookup.location is not None:
            replace_text(lookup.location.store_path, relative, text, new_text, count=1, transaction=transaction, pythonpath=package_pythonpath())
        else:
            file.write_text(new_text, encoding="utf-8")
    return changed
