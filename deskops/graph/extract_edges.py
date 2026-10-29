from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD
from deskops.graph.extract_docs import extract_doc_nodes
from deskops.graph.extract_sources import extract_source_file_nodes


EXTRACTOR_NAME = "desk_declared_edges_v1"

SECTION_HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
# A slug like `atom-pills-carry-transitional-task-knowledge` contains
# `task-knowledge`, which is part of an atom name, not a task reference; a real
# reference starts at a boundary that is not another word character or hyphen.
TASK_OR_ISSUE_RE = re.compile(r"(?<![\w-])(?P<kind>task|issue)-[a-z0-9][a-z0-9-]*\b")
SOURCE_PATH_RE = re.compile(
    r"(?<![\w/.-])(?P<path>(?:deskops|desk|tests|spec|docs)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|md|toml|json|mmd))(?![\w/.-])"
)
# Declared fields that record where a document came from. They link to the
# source while it exists; once it is deleted the provenance stays recorded as
# text and is not a reference that must resolve.
PROVENANCE_FIELDS = {"from_drawer"}
YAML_FENCE_RE = re.compile(r"```ya?ml\s*\n(?P<body>.*?)\n```", re.MULTILINE | re.DOTALL)


@dataclass(frozen=True)
class DeclaredGraphEdge:
    source_id: str
    target_id: str
    role: str
    source_kind: str
    confidence: str
    provenance_path: str
    provenance_locator: str
    extractor: str = EXTRACTOR_NAME
    record: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class MissingGraphTarget:
    source_id: str
    target_id: str
    provenance_path: str
    provenance_locator: str
    reason: str
    extractor: str = EXTRACTOR_NAME
    record: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class DeclaredEdgeExtraction:
    edges: list[DeclaredGraphEdge]
    missing_targets: list[MissingGraphTarget]


def extract_declared_edges(root: Path) -> DeclaredEdgeExtraction:
    project_root = root.resolve()
    doc_nodes = extract_doc_nodes(project_root)
    source_nodes = extract_source_file_nodes(project_root)
    nodes_by_path = {node.path: node for node in [*doc_nodes, *source_nodes]}
    existing_ids = {node.id for node in [*doc_nodes, *source_nodes]}
    ids_by_name = {node.id.split(":", 1)[-1]: node.id for node in [*doc_nodes, *source_nodes]}
    # A portable reference names the document as sldb tracks it: by its file stem. Some documents
    # carry a shorter frontmatter id (``pill-001`` in ``pill-001-task-closure-commit.md``); the stem
    # must resolve to the same node so Board context stays portable (task-board-portable-references).
    for node in [*doc_nodes, *source_nodes]:
        ids_by_name.setdefault(Path(node.path).stem, node.id)
    store = _load_store_context(project_root, doc_nodes)

    edges: list[DeclaredGraphEdge] = []
    missing_targets: list[MissingGraphTarget] = []
    seen_edges: set[tuple[str, str, str, str]] = set()
    seen_missing: set[tuple[str, str, str]] = set()

    if store is not None:
        for edge in _store_declared_edges(project_root, store, nodes_by_path):
            key = (edge.source_id, edge.target_id, edge.role, edge.provenance_locator)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(edge)

    for source_node in doc_nodes:
        path = project_root / source_node.path
        if not path.exists() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        relative_path = source_node.path
        record = True if _is_record_document(text) or _is_closed_issue(source_node.kind, text) else None
        tracked = store.tracked.get(relative_path) if store is not None else None
        # The sldb edge index owns the declared reference and containment fields of
        # tracked documents. The local frontmatter reader keeps only the fields the
        # model does not declare (for example MaterializationContractDoc.source_atoms).
        skip_fields = _declared_fields_for_model(tracked.model) if tracked else frozenset()

        declarations = [
            *_frontmatter_declarations(
                text,
                source_node.kind,
                nodes_by_path,
                ids_by_name,
                skip_fields=skip_fields,
            ),
            *_atom_declarations(text),
            *_section_declarations(text),
        ]
        if source_node.kind == "diagram":
            declarations.extend(_diagram_source_declarations(text))
        if source_node.kind in {"task", "issue"} and not _is_drawer_task_path(relative_path):
            # Drawer tasks are task nodes now, but they keep the extraction they had
            # when their kind was ``drawer_task``: the per-line path scanner never
            # ran for candidates.
            declarations.extend(_explicit_source_file_declarations(text))

        for declaration in declarations:
            target_id = _target_id_for(declaration.target, nodes_by_path)
            if target_id is None:
                target_id = _missing_target_id(declaration.target)
            if target_id not in existing_ids:
                key = (source_node.id, target_id, declaration.locator)
                if key not in seen_missing:
                    seen_missing.add(key)
                    missing_targets.append(
                        MissingGraphTarget(
                            source_id=source_node.id,
                            target_id=target_id,
                            provenance_path=relative_path,
                            provenance_locator=declaration.locator,
                            reason="declared target was not found among extracted graph nodes",
                            record=record,
                        )
                    )
                continue

            key = (source_node.id, target_id, declaration.role, declaration.locator)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(
                DeclaredGraphEdge(
                    source_id=source_node.id,
                    target_id=target_id,
                    role=declaration.role,
                    source_kind="declared",
                    confidence="high",
                    provenance_path=relative_path,
                    provenance_locator=declaration.locator,
                    record=record,
                )
            )

    if store is not None:
        for missing in _store_unresolved_targets(project_root, store, nodes_by_path, existing_ids, ids_by_name):
            if any(
                existing.source_id == missing.source_id and existing.target_id == missing.target_id
                for existing in missing_targets
            ):
                continue
            key = (missing.source_id, missing.target_id, missing.provenance_locator)
            if key in seen_missing:
                continue
            seen_missing.add(key)
            missing_targets.append(missing)

    return DeclaredEdgeExtraction(
        edges=sorted(edges, key=lambda edge: (edge.source_id, edge.target_id, edge.role, edge.provenance_locator)),
        missing_targets=sorted(
            missing_targets,
            key=lambda missing: (missing.source_id, missing.target_id, missing.provenance_locator),
        ),
    )


@dataclass(frozen=True)
class _StoreContext:
    """The store pieces the declared-edge reader needs: the index and its tracked paths."""

    index: Any
    tracked: dict[str, Any]


def _load_store_context(project_root: Path, doc_nodes: list[Any]) -> _StoreContext | None:
    """Read the sldb edge index of the project store, when the project has one.

    A root without ``.sldb`` has no tracked documents, so every document keeps the
    local frontmatter extraction.
    """
    store = project_root / ".sldb"
    if not store.is_dir() or not (store / "core" / "store_index.yaml").is_file():
        return None

    from sldb.api import doc_status
    from sldb.api import load_edge_index

    tracked = {}
    for node in doc_nodes:
        status = doc_status(store, node.path)
        if status.status == "ok":
            tracked[node.path] = status
    return _StoreContext(index=load_edge_index(store, include_linked=False), tracked=tracked)


def _declared_fields_for_model(model_name: str | None) -> frozenset[str]:
    """Fields whose edges the sldb index owns for a tracked model."""
    if not model_name:
        return frozenset()
    from deskops import models

    model = getattr(models, model_name, None)
    if model is None:
        return frozenset()
    return frozenset(
        [
            *getattr(model, "__containment__", {}).keys(),
            *getattr(model, "__references__", []),
        ]
    )


def _store_declared_edges(
    project_root: Path,
    store: _StoreContext,
    nodes_by_path: dict[str, Any],
) -> list[DeclaredGraphEdge]:
    """Schema edges of the sldb index, mapped to deskops graph node ids.

    The role is the declaring field name, so roles such as ``pills`` and
    ``depends_on`` stay what they were when the local regex extractor read them.
    """
    edges: list[DeclaredGraphEdge] = []
    records: dict[str, bool | None] = {}

    for edge in store.index.edges:
        metadata = edge.metadata or {}
        field = metadata.get("field")
        if not field or edge.relation not in {"references", "contains"}:
            continue

        source_record = store.index.nodes.get(edge.source)
        target_record = store.index.nodes.get(edge.target)
        if source_record is None or target_record is None:
            continue
        source_path = source_record.semantics.get("path")
        target_path = target_record.semantics.get("path")
        source_node = nodes_by_path.get(source_path)
        target_node = nodes_by_path.get(target_path)
        if source_node is None or target_node is None:
            # A tracked document or target outside deskops' document surfaces has
            # no deskops node; the edge cannot be projected into this graph.
            continue

        if source_path not in records:
            source_file = project_root / source_path
            records[source_path] = (
                True
                if source_file.is_file() and _is_record_document(source_file.read_text(encoding="utf-8"))
                else None
            )

        edges.append(
            DeclaredGraphEdge(
                source_id=source_node.id,
                target_id=target_node.id,
                role=field,
                source_kind="declared",
                confidence="high",
                provenance_path=source_path,
                provenance_locator="frontmatter",
                record=records[source_path],
            )
        )

    return edges


def _store_unresolved_targets(
    project_root: Path,
    store: _StoreContext,
    nodes_by_path: dict[str, Any],
    existing_ids: set[str],
    ids_by_name: dict[str, str],
) -> list[MissingGraphTarget]:
    """Declared values the sldb index reports unresolved, as deskops findings.

    sldb resolves against its tracked documents; deskops also has nodes for
    untracked files (tasks, atoms, docs). A value that names one of those nodes is
    not dangling in this graph, so it is left out. Prose in a containment field
    (ritual steps) is not a reference either (``_looks_like_reference``).
    """
    nodes_by_id = {node.id: node for node in nodes_by_path.values()}
    findings: list[MissingGraphTarget] = []

    for reference in store.index.unresolved_references:
        if reference.relation not in {"references", "contains"}:
            continue
        if reference.field in PROVENANCE_FIELDS:
            continue

        value = (reference.target or "").strip()
        if not _looks_like_reference(value, nodes_by_path, ids_by_name):
            continue
        if _unresolved_value_resolves(reference, value, nodes_by_path, existing_ids, ids_by_name):
            continue

        source_node = _unresolved_source_node(reference, nodes_by_path, nodes_by_id, ids_by_name)
        if source_node is None:
            continue

        source_file = project_root / source_node.path
        source_text = source_file.read_text(encoding="utf-8") if source_file.is_file() else ""
        record = (
            True
            if source_text and (_is_record_document(source_text) or _is_closed_issue(source_node.kind, source_text))
            else None
        )
        findings.append(
            MissingGraphTarget(
                source_id=source_node.id,
                target_id=_unresolved_target_id(reference, value, nodes_by_path),
                provenance_path=source_node.path,
                provenance_locator="frontmatter",
                reason=f"declared target was not resolved by the sldb edge index ({reference.reason})",
                record=record,
            )
        )

    return findings


def _unresolved_source_node(
    reference: Any,
    nodes_by_path: dict[str, Any],
    nodes_by_id: dict[str, Any],
    ids_by_name: dict[str, str],
) -> Any | None:
    source_path = (reference.source_path or "").removeprefix("./")
    source_node = nodes_by_path.get(source_path)
    if source_node is not None:
        return source_node
    name = reference.source.split(":", 1)[-1]
    node_id = ids_by_name.get(name)
    return nodes_by_id.get(node_id) if node_id else None


def _unresolved_value_resolves(
    reference: Any,
    value: str,
    nodes_by_path: dict[str, Any],
    existing_ids: set[str],
    ids_by_name: dict[str, str],
) -> bool:
    if reference.target_export_id:
        name = reference.target_export_id.split(":", 1)[-1]
        if name in ids_by_name:
            return True
    candidate = value.strip("`").removeprefix("./")
    if candidate in nodes_by_path:
        return True
    resolved = _declared_reference_id(value, nodes_by_path, ids_by_name)
    return bool(resolved and resolved in existing_ids)


def _unresolved_target_id(reference: Any, value: str, nodes_by_path: dict[str, Any]) -> str:
    if reference.target_export_id:
        model_name, _, name = reference.target_export_id.partition(":")
        kind = _kind_for_model_name(model_name)
        if kind and name:
            return f"{kind}:{name}"
        return reference.target_export_id
    target_id = _target_id_for(value, nodes_by_path)
    if target_id is not None:
        return target_id
    return _missing_target_id(value)


def _kind_for_model_name(model_name: str) -> str | None:
    from deskops import models

    model = getattr(models, model_name, None)
    if model is None:
        return None
    types = (getattr(model, "__semantics__", None) or {}).get("type") or []
    if not types:
        return None
    kind = types[-1]
    return "materialization" if kind == "materialization_contract" else kind


def _is_drawer_task_path(relative_path: str) -> bool:
    return Path(relative_path).parts[:3] == ("desk", "drawer", "tasks")


def _is_closed_issue(kind: str | None, text: str) -> bool:
    """Whether an issue is closed: a closed issue is history, like a ``record: true`` document."""
    if kind != "issue":
        return False
    from deskops.services.issues import issue_status

    return issue_status(text) == "closed"


def _is_record_document(text: str) -> bool:
    """Whether the document carries the archived-record marker in its frontmatter."""
    if not text.startswith("---\n"):
        return False
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return False
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return False
    return isinstance(loaded, dict) and loaded.get("record") is True


@dataclass(frozen=True)
class _Declaration:
    target: str
    role: str
    locator: str


def _frontmatter_declarations(
    text: str,
    kind: str | None = None,
    nodes_by_path: dict[str, Any] | None = None,
    ids_by_name: dict[str, str] | None = None,
    *,
    skip_fields: frozenset[str] = frozenset(),
) -> list[_Declaration]:
    if not text.startswith("---\n"):
        return []
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return []
    
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return []

    if not isinstance(loaded, dict):
        return []

    declarations = _declarations_from_mapping(loaded, "frontmatter", skip_fields)

    if kind:
        model = _model_for_kind(kind)
        if model:
            declared_fields = [
                *getattr(model, "__containment__", {}).keys(),
                *getattr(model, "__references__", []),
            ]
            for field_name in declared_fields:
                if field_name in skip_fields or field_name not in loaded:
                    continue
                value = loaded[field_name]
                items = value if isinstance(value, list) else [value]
                for item in items:
                    if not isinstance(item, str) or not item.strip():
                        continue
                    if field_name in PROVENANCE_FIELDS:
                        node = (nodes_by_path or {}).get(item.strip().removeprefix("./"))
                        if node is not None:
                            declarations.append(_Declaration(node.id, field_name, "frontmatter"))
                        continue
                    reference = _declared_reference_id(
                        item, nodes_by_path or {}, ids_by_name or {}
                    )
                    if reference is not None:
                        declarations.append(_Declaration(reference, field_name, "frontmatter"))
                    elif _looks_like_reference(item, nodes_by_path or {}, ids_by_name or {}):
                        declarations.append(_Declaration(item.strip(), field_name, "frontmatter"))

    return declarations


def _looks_like_reference(value: str, nodes_by_path: dict[str, Any], ids_by_name: dict[str, str]) -> bool:
    """Whether a declared value is meant to name a document.

    Declared containment and reference fields also hold prose (`steps` on a
    ritual) or workflow node names (`complete` on an edge). Those are not
    document references and must not be reported as unresolved targets.
    """
    candidate = value.strip()
    if any(ch.isspace() for ch in candidate):
        # Document ids and repo paths never hold whitespace; a value that does is prose,
        # even when it quotes a path or a `key: value` (ritual steps often do).
        return False
    if "/" in candidate or ":" in candidate:
        return True
    return Path(candidate).stem in ids_by_name or candidate in nodes_by_path


def _declared_reference_id(
    value: str, nodes_by_path: dict[str, Any], ids_by_name: dict[str, str]
) -> str | None:
    """Resolve one declared value to a node id, using the existing schemes only."""
    candidate = value.strip()
    if any(ch.isspace() for ch in candidate):
        return None  # prose, not a reference (see _looks_like_reference)
    if candidate in ids_by_name:
        return ids_by_name[candidate]
    node = nodes_by_path.get(candidate.removeprefix("./"))
    if node is not None:
        return node.id
    stem = Path(candidate).stem
    if stem in ids_by_name:
        return ids_by_name[stem]
    if ":" in candidate:
        return candidate
    return None
def _model_for_kind(kind: str) -> Any | None:
    from deskops import models
    normalized = kind.removeprefix("drawer_")
    for name in models.__all__:
        cls = getattr(models, name)
        semantics = getattr(cls, "__semantics__", None)
        if semantics and "type" in semantics:
            if semantics["type"][-1] == normalized:
                return cls
    return None



def _atom_declarations(text: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    for match in YAML_FENCE_RE.finditer(text):
        try:
            loaded_documents = list(yaml.safe_load_all(match.group("body")))
        except yaml.YAMLError:
            # A block that is not a single YAML document is not evidence of
            # atom declarations.
            continue
        if len(loaded_documents) != 1:
            continue
        loaded = loaded_documents[0]
        if not isinstance(loaded, dict):
            continue
        line_number = text[: match.start()].count("\n") + 1
        declarations.extend(_declarations_from_mapping(loaded, f"line:{line_number}:yaml"))
    return declarations


def _declarations_from_mapping(
    mapping: dict[Any, Any],
    locator: str,
    skip_fields: frozenset[str] = frozenset(),
) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    for key in (CANONICAL_FIELD, MATERIALIZATION_FIELD, *LEGACY_FIELDS):
        if key in skip_fields:
            continue
        declarations.extend(_atom_declarations_from_value(mapping.get(key), locator, DEFAULT_ROLE))
    materialization = mapping.get("materialization")
    if isinstance(materialization, dict):
        declarations.extend(
            _atom_declarations_from_value(materialization.get("source_atoms"), locator, DEFAULT_ROLE)
        )
        declarations.extend(_target_identity_declaration(materialization.get("target_identity"), locator))
    declarations.extend(_target_identity_declaration(mapping.get("target_identity"), locator))
    return declarations


def _target_identity_declaration(value: Any, locator: str) -> list[_Declaration]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [_Declaration(value.strip(), DEFAULT_ROLE, locator)]


def _atom_declarations_from_value(value: Any, locator: str, default_role: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    if isinstance(value, str):
        declarations.append(_Declaration(_atom_id(value), default_role, locator))
        return declarations
    if not isinstance(value, list):
        return declarations
    for item in value:
        if isinstance(item, str):
            declarations.append(_Declaration(_atom_id(item), default_role, locator))
        elif isinstance(item, dict) and isinstance(item.get("id"), str):
            role = item.get("role") if isinstance(item.get("role"), str) else default_role
            if role not in ALLOWED_ROLES:
                role = default_role
            declarations.append(_Declaration(_atom_id(item["id"]), role, locator))
    return declarations


def _section_declarations(text: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    lines = text.splitlines()
    active_section: str | None = None
    active_level = 0

    for index, line in enumerate(lines, start=1):
        heading = SECTION_HEADING_RE.match(line)
        if heading:
            active_level = len(heading.group(1))
            active_section = _normalize_heading(heading.group(2))
            continue
        if active_section is None:
            continue
        nested_heading = SECTION_HEADING_RE.match(line)
        if nested_heading and len(nested_heading.group(1)) <= active_level:
            active_section = None
            continue
        if not _is_reference_section(active_section):
            continue

        for atom_id in re.findall(r"\batom-[a-z0-9][a-z0-9-]*\b", line):
            declarations.append(_Declaration(_atom_id(atom_id), DEFAULT_ROLE, f"line:{index}:{active_section}"))
        for match in TASK_OR_ISSUE_RE.finditer(line):
            target = f"{match.group('kind')}:{match.group(0)}"
            declarations.append(_Declaration(target, DEFAULT_ROLE, f"line:{index}:{active_section}"))
    return declarations


def _diagram_source_declarations(text: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    lines = text.splitlines()
    active_section: str | None = None
    for index, line in enumerate(lines, start=1):
        heading = SECTION_HEADING_RE.match(line)
        if heading:
            active_section = _normalize_heading(heading.group(2))
            continue
        if active_section not in {"source", "sources", "diagram source", "diagram sources"}:
            continue
        for path in _paths_in_line(line):
            declarations.append(_Declaration(path, DEFAULT_ROLE, f"line:{index}:{active_section}"))
    return declarations


def _explicit_source_file_declarations(text: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    in_frontmatter = False
    for index, line in enumerate(text.splitlines(), start=1):
        if line == "---" and (index == 1 or in_frontmatter):
            in_frontmatter = index == 1
            continue
        if in_frontmatter and line.split(":", 1)[0] in PROVENANCE_FIELDS:
            continue
        for path in _paths_in_line(line):
            declarations.append(_Declaration(path, DEFAULT_ROLE, f"line:{index}:source-file-reference"))
    return declarations


def _paths_in_line(line: str) -> list[str]:
    return [match.group("path") for match in SOURCE_PATH_RE.finditer(line)]


def _target_id_for(target: str, nodes_by_path: dict[str, Any]) -> str | None:
    if ":" in target:
        return target
    node = nodes_by_path.get(target.removeprefix("./"))
    if node is None:
        return None
    return node.id


def _missing_target_id(target: str) -> str:
    if ":" in target:
        return target
    path = target.removeprefix("./")
    parts = Path(path).parts
    if parts[:2] == ("docs", "diagrams"):
        return f"diagram:{path}"
    if parts and parts[0] == "docs":
        return f"doc:{path}"
    if parts and parts[0] == "tests":
        return f"test_file:{path}"
    if parts and parts[0] == "spec":
        return f"spec:{path}"
    if parts and parts[0] in {"desk", "deskops"} and path.endswith(".py"):
        return f"source_file:{path}"
    return path


def _atom_id(value: str) -> str:
    value = value.strip()
    return value if value.startswith("atom:") else f"atom:{value}"


def _normalize_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _is_reference_section(heading: str) -> bool:
    return heading in {
        "related atoms",
        "source atoms",
        "related tasks",
        "related issues",
        "related task",
        "related issue",
    }
