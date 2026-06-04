from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from deskops.graph.extract_docs import extract_doc_nodes
from deskops.graph.extract_sources import extract_source_file_nodes


EXTRACTOR_NAME = "desk_declared_edges_v1"

ALLOWED_ATOM_ROLES = {"references", "documents", "specifies", "constrains", "validates"}
DEFAULT_ROLE = "references"

SECTION_HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
TASK_OR_ISSUE_RE = re.compile(r"\b(?P<kind>task|issue)-[a-z0-9][a-z0-9-]*\b")
SOURCE_PATH_RE = re.compile(
    r"(?<![\w/.-])(?P<path>(?:deskops|desk|tests|spec|docs)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|md|toml|json|mmd))(?![\w/.-])"
)
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MissingGraphTarget:
    source_id: str
    target_id: str
    provenance_path: str
    provenance_locator: str
    reason: str
    extractor: str = EXTRACTOR_NAME

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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

    edges: list[DeclaredGraphEdge] = []
    missing_targets: list[MissingGraphTarget] = []
    seen_edges: set[tuple[str, str, str, str]] = set()
    seen_missing: set[tuple[str, str, str]] = set()

    for source_node in doc_nodes:
        path = project_root / source_node.path
        if not path.exists() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        relative_path = source_node.path

        declarations = [*_atom_declarations(text), *_section_declarations(text)]
        if source_node.kind == "diagram":
            declarations.extend(_diagram_source_declarations(text))
        if source_node.kind in {"task", "issue"}:
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
                )
            )

    return DeclaredEdgeExtraction(
        edges=sorted(edges, key=lambda edge: (edge.source_id, edge.target_id, edge.role, edge.provenance_locator)),
        missing_targets=sorted(
            missing_targets,
            key=lambda missing: (missing.source_id, missing.target_id, missing.provenance_locator),
        ),
    )


@dataclass(frozen=True)
class _Declaration:
    target: str
    role: str
    locator: str


def _atom_declarations(text: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    for match in YAML_FENCE_RE.finditer(text):
        loaded = yaml.safe_load(match.group("body"))
        if not isinstance(loaded, dict):
            continue
        line_number = text[: match.start()].count("\n") + 1
        declarations.extend(_atom_declarations_from_mapping(loaded, f"line:{line_number}:yaml"))
    return declarations


def _atom_declarations_from_mapping(mapping: dict[Any, Any], locator: str) -> list[_Declaration]:
    declarations: list[_Declaration] = []
    for key in ("atoms", "source_atoms", "related_atoms"):
        declarations.extend(_atom_declarations_from_value(mapping.get(key), locator, DEFAULT_ROLE))
    materialization = mapping.get("materialization")
    if isinstance(materialization, dict):
        declarations.extend(
            _atom_declarations_from_value(materialization.get("source_atoms"), locator, DEFAULT_ROLE)
        )
    return declarations


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
            if role not in ALLOWED_ATOM_ROLES:
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
    for index, line in enumerate(text.splitlines(), start=1):
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
