from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
import html
from pathlib import Path
import re
from typing import Any

import yaml


EXTRACTOR_NAME = "desk_kgdb_coverage_v1"
FACETS = ("what", "why", "when", "who", "where", "how")
MERMAID_FENCE_RE = re.compile(r"```mermaid\s*\n(?P<body>.*?)\n```", re.DOTALL | re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)
HTML_SECTION_RE = re.compile(
    r'<section[^>]*id="(?P<section_id>[^"]+)"[^>]*>(?P<body>.*?)</section>',
    re.DOTALL | re.IGNORECASE,
)
HTML_MERMAID_RE = re.compile(
    r'<pre[^>]*class="[^"]*mermaid[^"]*"[^>]*>(?P<body>.*?)</pre>',
    re.DOTALL | re.IGNORECASE,
)
HTML_TAG_RE = re.compile(r"<[^>]+>")
ATOM_ALIAS_KEYS = ("aliases", "alias")
EXCLUDED_PATH_PARTS = {".git", ".sldb", "node_modules", "__pycache__", "runs", "source_docs", "gian-repo"}
EXCLUDED_PATH_PREFIXES = ("docs/diagram-catalog",)
COMPONENT_EDGE_PATTERNS = (
    re.compile(r"^(?P<left>.+?)\s*-->\|(?P<label>[^|]+)\|\s*(?P<right>.+?)\s*$"),
    re.compile(r"^(?P<left>.+?)\s*--\s*(?P<label>.+?)\s*-->\s*(?P<right>.+?)\s*$"),
    re.compile(r"^(?P<left>.+?)\s*(?P<connector>-->|---)\s*(?P<right>.+?)\s*$"),
)
STATE_TRANSITION_RE = re.compile(r"^(?P<left>.+?)\s*-->\s*(?P<right>.+?)(?:\s*:\s*(?P<label>.+))?\s*$")
STATE_ALIAS_RE = re.compile(r'^state\s+"(?P<label>[^"]+)"\s+as\s+(?P<alias>[A-Za-z0-9_]+)\s*$')
STATE_CONTAINER_RE = re.compile(r"^state\s+(?P<name>[A-Za-z0-9_]+)\s*\{")
FLOWCHART_PREFIX_RE = re.compile(r"^flowchart\b", re.IGNORECASE)
STATE_PREFIX_RE = re.compile(r"^stateDiagram(?:-v2)?\b", re.IGNORECASE)
NODE_DECL_RE = re.compile(
    r"(?P<token>[A-Za-z][A-Za-z0-9_]*)\s*(?P<label>\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\}|\(\([^\)]+\)\)|\[\[[^\]]+\]\]|\>\[[^\]]+\])"
)


@dataclass(frozen=True)
class CoverageGraphNode:
    id: str
    kind: str
    provenance: dict[str, str]
    identity: str | None = None
    path: str | None = None
    label: str | None = None
    atom_id: str | None = None
    title: str | None = None
    five_wh_one_plus: str | list[str] | None = None
    tags: list[str] | dict[str, Any] | None = None
    aliases: list[str] | None = None
    view_id: str | None = None
    diagram_type: str | None = None
    source_ref: str | None = None
    scope: str | None = None
    element_id: str | None = None
    element_kind: str | None = None
    source: str | None = None
    target: str | None = None
    semantics: dict[str, Any] | None = None
    facet: str | None = None
    source_field: str | None = None
    description: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoverageGraphEdge:
    source_id: str
    target_id: str
    role: str
    source_kind: str
    confidence: str
    provenance_path: str
    provenance_locator: str
    extractor: str = EXTRACTOR_NAME
    atom_id: str | None = None
    facet: str | None = None
    score: float | None = None
    match_basis: str | None = None
    evidence: str | None = None
    source_field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoverageExtraction:
    nodes: list[CoverageGraphNode]
    edges: list[CoverageGraphEdge]


@dataclass(frozen=True)
class _ViewInput:
    view_id: str
    diagram_type: str
    title: str
    source_ref: str
    mermaid: str
    provenance_path: str
    provenance_locator: str
    scope: str | None = None


@dataclass(frozen=True)
class _ElementRecord:
    element_id: str
    element_kind: str
    diagram_type: str
    order: tuple[int, int, int]
    label: str | None = None
    source: str | None = None
    target: str | None = None
    semantics: dict[str, Any] | None = None


@dataclass(frozen=True)
class _AtomRecord:
    node_id: str
    atom_id: str
    title: str
    facets: list[str]
    tags: list[str] | dict[str, Any]
    aliases: list[str]
    provenance_path: str


@dataclass(frozen=True)
class _MatchSignal:
    facet: str
    element_text: str
    element_source: str


@dataclass(frozen=True)
class _ScoredBasis:
    score: float
    basis: str
    evidence: str


def extract_coverage_graph(root: Path) -> CoverageExtraction:
    project_root = root.resolve()
    atom_records = _extract_atoms(project_root)
    view_inputs = _discover_views(project_root)

    nodes: dict[str, CoverageGraphNode] = {}
    edges: dict[tuple[str, str, str, str, str | None], CoverageGraphEdge] = {}

    for facet in FACETS:
        facet_node = CoverageGraphNode(
            id=f"facet:{facet}",
            kind="facet",
            facet=facet,
            source_field="atom.five_wh_one_plus",
            description=f"W5H1 facet {facet}",
            provenance={"path": ".", "source_kind": "coverage_facet", "extractor": EXTRACTOR_NAME},
        )
        nodes[facet_node.id] = facet_node

    for atom in atom_records:
        atom_node = CoverageGraphNode(
            id=atom.node_id,
            kind="atom",
            identity=atom.atom_id,
            path=atom.provenance_path,
            label=atom.title,
            atom_id=atom.atom_id,
            title=atom.title,
            five_wh_one_plus=atom.facets,
            tags=atom.tags,
            aliases=atom.aliases,
            provenance={"path": atom.provenance_path, "source_kind": "atom_frontmatter", "extractor": EXTRACTOR_NAME},
        )
        nodes[atom.node_id] = atom_node
        for facet in atom.facets:
            _add_edge(
                edges,
                CoverageGraphEdge(
                    source_id=atom.node_id,
                    target_id=f"facet:{facet}",
                    role="answers",
                    source_kind="coverage_materialization",
                    confidence="high",
                    provenance_path=atom.provenance_path,
                    provenance_locator="frontmatter:five_wh_one_plus",
                    facet=facet,
                ),
            )

    for view in view_inputs:
        view_node_id = f"view:{view.view_id}"
        nodes[view_node_id] = CoverageGraphNode(
            id=view_node_id,
            kind="view",
            identity=view.view_id,
            label=view.title,
            view_id=view.view_id,
            diagram_type=view.diagram_type,
            title=view.title,
            source_ref=view.source_ref,
            scope=view.scope,
            provenance={"path": view.provenance_path, "source_kind": "diagram_source", "extractor": EXTRACTOR_NAME},
        )
        elements = _extract_elements(view)
        for element in elements:
            element_node_id = f"diagram_element:{view.view_id}:{element.element_id}"
            nodes[element_node_id] = CoverageGraphNode(
                id=element_node_id,
                kind="diagram_element",
                label=element.label,
                view_id=view.view_id,
                diagram_type=element.diagram_type,
                element_id=element.element_id,
                element_kind=element.element_kind,
                source=element.source,
                target=element.target,
                semantics=element.semantics or {},
                provenance={"path": view.provenance_path, "source_kind": "diagram_source", "extractor": EXTRACTOR_NAME},
            )
            _add_edge(
                edges,
                CoverageGraphEdge(
                    source_id=view_node_id,
                    target_id=element_node_id,
                    role="contains",
                    source_kind="coverage_materialization",
                    confidence="high",
                    provenance_path=view.provenance_path,
                    provenance_locator=view.provenance_locator,
                ),
            )
            _add_edge(
                edges,
                CoverageGraphEdge(
                    source_id=element_node_id,
                    target_id=view_node_id,
                    role="derived_from",
                    source_kind="coverage_materialization",
                    confidence="high",
                    provenance_path=view.provenance_path,
                    provenance_locator=view.provenance_locator,
                ),
            )
            for facet, source_field in _expected_facets_for_element(element):
                _add_edge(
                    edges,
                    CoverageGraphEdge(
                        source_id=element_node_id,
                        target_id=f"facet:{facet}",
                        role="expects_facet",
                        source_kind="coverage_materialization",
                        confidence="high",
                        provenance_path=view.provenance_path,
                        provenance_locator=view.provenance_locator,
                        facet=facet,
                        source_field=source_field,
                    ),
                )
            for match in _match_element_to_atoms(element, atom_records):
                _add_edge(
                    edges,
                    CoverageGraphEdge(
                        source_id=element_node_id,
                        target_id=f"atom:{match['atom_id']}",
                        role="covers_facet",
                        source_kind="coverage_materialization",
                        confidence="high",
                        provenance_path=view.provenance_path,
                        provenance_locator=view.provenance_locator,
                        atom_id=match["atom_id"],
                        facet=match["facet"],
                        score=match["score"],
                        match_basis=match["match_basis"],
                        evidence=match["evidence"],
                    ),
                )

    return CoverageExtraction(
        nodes=sorted(nodes.values(), key=lambda node: node.id),
        edges=sorted(edges.values(), key=lambda edge: (edge.source_id, edge.target_id, edge.role, edge.facet or "", edge.atom_id or "")),
    )


def _extract_atoms(root: Path) -> list[_AtomRecord]:
    atoms: list[_AtomRecord] = []
    for path in sorted(root.glob("**/desk/atoms/**/*.md")):
        if _is_excluded(root, path):
            continue
        metadata = _read_frontmatter(path)
        atom_id = str(metadata.get("id") or path.stem).strip()
        title = str(metadata.get("title") or path.stem).strip()
        facets = _normalize_facets(metadata.get("five_wh_one_plus"))
        tags = metadata.get("tags") or []
        aliases = _normalize_aliases(metadata, title)
        atoms.append(
            _AtomRecord(
                node_id=f"atom:{atom_id}",
                atom_id=atom_id,
                title=title,
                facets=facets,
                tags=tags,
                aliases=aliases,
                provenance_path=path.relative_to(root).as_posix(),
            )
        )
    return atoms


def _discover_views(root: Path) -> list[_ViewInput]:
    views: list[_ViewInput] = []
    for path in sorted(root.rglob("*.md")):
        if _is_excluded(root, path) or "desk/atoms" not in path.as_posix():
            continue
        views.extend(_discover_markdown_views(root, path))
    for path in sorted(root.rglob("*.html")):
        if _is_excluded(root, path) or "/docs/" not in path.as_posix():
            continue
        views.extend(_discover_html_views(root, path))
    return sorted(views, key=lambda view: (view.source_ref, view.view_id))


def _discover_markdown_views(root: Path, path: Path) -> list[_ViewInput]:
    text = path.read_text(encoding="utf-8")
    relative_path = path.relative_to(root).as_posix()
    scope = _scope_from_relative_path(relative_path)
    headings = list(HEADING_RE.finditer(text))
    metadata = _read_frontmatter(path)
    default_title = str(metadata.get("title") or path.stem).strip()
    views: list[_ViewInput] = []
    for index, match in enumerate(MERMAID_FENCE_RE.finditer(text), start=1):
        mermaid = match.group("body").strip()
        diagram_type = _diagram_type_for_mermaid(mermaid)
        if diagram_type is None:
            continue
        title = _nearest_heading_title(headings, match.start()) or default_title
        heading_slug = _slugify(title)
        source_ref = f"{relative_path}#{heading_slug or f'mermaid-{index}'}"
        views.append(
            _ViewInput(
                view_id=_slugify(source_ref),
                diagram_type=diagram_type,
                title=title,
                source_ref=source_ref,
                mermaid=mermaid,
                provenance_path=relative_path,
                provenance_locator=f"mermaid:{index}",
                scope=scope,
            )
        )
    return views


def _discover_html_views(root: Path, path: Path) -> list[_ViewInput]:
    text = path.read_text(encoding="utf-8")
    relative_path = path.relative_to(root).as_posix()
    scope = _scope_from_relative_path(relative_path)
    views: list[_ViewInput] = []
    for section in HTML_SECTION_RE.finditer(text):
        section_id = section.group("section_id")
        body = section.group("body")
        mermaid_match = HTML_MERMAID_RE.search(body)
        if mermaid_match is None:
            continue
        mermaid = html.unescape(mermaid_match.group("body")).strip()
        diagram_type = _diagram_type_for_mermaid(mermaid)
        if diagram_type is None:
            continue
        title_match = re.search(r"<h2[^>]*>(?P<title>.*?)</h2>", body, re.DOTALL | re.IGNORECASE)
        lbl_match = re.search(r'<div[^>]*class="[^"]*lbl[^"]*"[^>]*>(?P<label>.*?)</div>', body, re.DOTALL | re.IGNORECASE)
        title = _strip_html((title_match.group("title") if title_match else lbl_match.group("label") if lbl_match else section_id)).strip()
        source_ref = f"{relative_path}#{section_id}"
        views.append(
            _ViewInput(
                view_id=_slugify(f"{relative_path}-{section_id}"),
                diagram_type=diagram_type,
                title=title,
                source_ref=source_ref,
                mermaid=mermaid,
                provenance_path=relative_path,
                provenance_locator=f"section:{section_id}",
                scope=scope,
            )
        )
    return views


def _extract_elements(view: _ViewInput) -> list[_ElementRecord]:
    lines = view.mermaid.splitlines()
    if view.diagram_type == "component":
        return _extract_component_elements(lines)
    return _extract_state_elements(lines)


def _extract_component_elements(lines: list[str]) -> list[_ElementRecord]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    for line_index, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or FLOWCHART_PREFIX_RE.match(line) or line.lower() in {"end"} or line.lower().startswith("subgraph"):
            continue
        edge_match = _match_component_edge(line)
        if edge_match is not None:
            left_token, left_label = _parse_component_endpoint(edge_match["left"])
            right_token, right_label = _parse_component_endpoint(edge_match["right"])
            if left_token and left_token not in nodes:
                nodes[left_token] = {"token": left_token, "label": left_label or left_token, "order": (line_index, 0, len(nodes))}
            elif left_token and left_label:
                nodes[left_token]["label"] = left_label
            if right_token and right_token not in nodes:
                nodes[right_token] = {"token": right_token, "label": right_label or right_token, "order": (line_index, 1, len(nodes))}
            elif right_token and right_label:
                nodes[right_token]["label"] = right_label
            if left_token and right_token:
                relation = edge_match["label"] or "connects_to"
                edges.append(
                    {
                        "source_token": left_token,
                        "target_token": right_token,
                        "label": edge_match["label"],
                        "relation": relation,
                        "order": (line_index, 2, len(edges)),
                    }
                )
            continue
        for decl_index, match in enumerate(NODE_DECL_RE.finditer(line)):
            token = match.group("token")
            label = _clean_component_label(match.group("label")) or token
            nodes.setdefault(token, {"token": token, "label": label, "order": (line_index, decl_index, len(nodes))})
            if label:
                nodes[token]["label"] = label

    node_elements: list[_ElementRecord] = []
    for token, payload in sorted(nodes.items(), key=lambda item: item[1]["order"]):
        element_id = f"node:{_slugify(token)}"
        node_elements.append(
            _ElementRecord(
                element_id=element_id,
                element_kind="node",
                diagram_type="component",
                label=payload["label"],
                semantics={"label": payload["label"]},
                order=payload["order"],
            )
        )
        payload["element_id"] = element_id

    edge_elements: list[_ElementRecord] = []
    for edge in sorted(edges, key=lambda item: item["order"]):
        source_id = nodes[edge["source_token"]]["element_id"]
        target_id = nodes[edge["target_token"]]["element_id"]
        relation_slug = _slugify(edge["relation"] or "connects-to")
        element_id = f"edge:{_embedded_element_slug(source_id)}--{relation_slug}--{_embedded_element_slug(target_id)}"
        semantics: dict[str, Any] = {"relation": edge["relation"]}
        if edge["label"]:
            semantics["label"] = edge["label"]
        edge_elements.append(
            _ElementRecord(
                element_id=element_id,
                element_kind="edge",
                diagram_type="component",
                label=edge["label"],
                source=source_id,
                target=target_id,
                semantics=semantics,
                order=edge["order"],
            )
        )

    return _apply_collision_suffixes([*node_elements, *edge_elements])


def _extract_state_elements(lines: list[str]) -> list[_ElementRecord]:
    aliases: dict[str, str] = {}
    states: dict[str, dict[str, Any]] = {}
    transitions: list[dict[str, Any]] = []

    def ensure_state(token: str, label: str, order: tuple[int, int, int]) -> None:
        states.setdefault(token, {"token": token, "label": label, "order": order})
        if label:
            states[token]["label"] = label

    for line_index, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or STATE_PREFIX_RE.match(line) or line.lower() in {"end"}:
            continue
        alias_match = STATE_ALIAS_RE.match(line)
        if alias_match:
            alias = alias_match.group("alias")
            label = alias_match.group("label").strip()
            aliases[alias] = label
            ensure_state(alias, label, (line_index, 0, len(states)))
            continue
        container_match = STATE_CONTAINER_RE.match(line)
        if container_match:
            token = container_match.group("name")
            ensure_state(token, aliases.get(token, token), (line_index, 0, len(states)))
            continue
        transition_match = STATE_TRANSITION_RE.match(line)
        if transition_match:
            left_token, left_label = _parse_state_endpoint(transition_match.group("left"), aliases, is_source=True)
            right_token, right_label = _parse_state_endpoint(transition_match.group("right"), aliases, is_source=False)
            ensure_state(left_token, left_label, (line_index, 0, len(states)))
            ensure_state(right_token, right_label, (line_index, 1, len(states)))
            label = transition_match.group("label").strip() if transition_match.group("label") else None
            semantics = {"relation": "transitions_to"}
            if label:
                semantics["label"] = label
                parts = [part.strip() for part in label.split("/", 2)]
                if parts and parts[0]:
                    semantics["on"] = parts[0]
                if len(parts) >= 2 and parts[1]:
                    guard = parts[1]
                    if guard.startswith("[") and guard.endswith("]"):
                        guard = guard[1:-1].strip()
                    semantics["guard"] = guard
                if len(parts) >= 3 and parts[2]:
                    semantics["action"] = parts[2]
            transitions.append(
                {
                    "source_token": left_token,
                    "target_token": right_token,
                    "label": label,
                    "semantics": semantics,
                    "order": (line_index, 2, len(transitions)),
                }
            )
            continue
        if re.match(r"^[A-Za-z0-9_]+$", line):
            ensure_state(line, aliases.get(line, line), (line_index, 0, len(states)))

    state_elements: list[_ElementRecord] = []
    for token, payload in sorted(states.items(), key=lambda item: item[1]["order"]):
        basis = token
        element_id = f"state:{_slugify(basis)}"
        label = payload["label"]
        state_elements.append(
            _ElementRecord(
                element_id=element_id,
                element_kind="state",
                diagram_type="state",
                label=label,
                semantics={"label": label},
                order=payload["order"],
            )
        )
        payload["element_id"] = element_id

    transition_elements: list[_ElementRecord] = []
    for transition in sorted(transitions, key=lambda item: item["order"]):
        source_id = states[transition["source_token"]]["element_id"]
        target_id = states[transition["target_token"]]["element_id"]
        on_slug = _slugify(transition["semantics"].get("on") or "transition")
        element_id = f"transition:{_embedded_element_slug(source_id)}--{on_slug}--{_embedded_element_slug(target_id)}"
        transition_elements.append(
            _ElementRecord(
                element_id=element_id,
                element_kind="transition",
                diagram_type="state",
                label=transition["label"],
                source=source_id,
                target=target_id,
                semantics=transition["semantics"],
                order=transition["order"],
            )
        )

    return _apply_collision_suffixes([*state_elements, *transition_elements])


def _apply_collision_suffixes(elements: list[_ElementRecord]) -> list[_ElementRecord]:
    grouped: dict[tuple[str, str], list[_ElementRecord]] = {}
    for element in elements:
        grouped.setdefault((element.element_kind, element.element_id), []).append(element)
    result: list[_ElementRecord] = []
    for (_kind, _element_id), group in grouped.items():
        for index, element in enumerate(sorted(group, key=lambda item: item.order), start=1):
            if index == 1:
                result.append(element)
            else:
                result.append(
                    _ElementRecord(
                        element_id=f"{element.element_id}--{index}",
                        element_kind=element.element_kind,
                        diagram_type=element.diagram_type,
                        label=element.label,
                        source=element.source,
                        target=element.target,
                        semantics=element.semantics,
                        order=element.order,
                    )
                )
    return sorted(result, key=lambda element: element.order)


def _expected_facets_for_element(element: _ElementRecord) -> list[tuple[str, str]]:
    semantics = element.semantics or {}
    if element.diagram_type == "component" and element.element_kind == "node":
        return [("what", "label")]
    if element.diagram_type == "component" and element.element_kind == "edge":
        return [("how", "semantics.relation"), ("why", "semantics.relation")]
    if element.diagram_type == "state" and element.element_kind == "state":
        return [("what", "label")]
    if element.diagram_type == "state" and element.element_kind == "transition":
        result: list[tuple[str, str]] = []
        if semantics.get("action"):
            result.append(("how", "semantics.action"))
        if semantics.get("on"):
            result.append(("when", "semantics.on"))
        if semantics.get("guard"):
            result.append(("why", "semantics.guard"))
        return result
    return []


def _match_element_to_atoms(element: _ElementRecord, atoms: list[_AtomRecord]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    expected = _expected_facets_for_element(element)
    for facet, _source_field in expected:
        signal = _primary_signal_for_element(element, facet)
        if signal is None:
            continue
        for atom in atoms:
            if facet not in atom.facets:
                continue
            best = _best_basis_for_match(signal, atom)
            if best is None or best.score < 0.70:
                continue
            matches.append(
                {
                    "atom_id": atom.atom_id,
                    "facet": facet,
                    "score": round(best.score, 2),
                    "match_basis": best.basis,
                    "evidence": best.evidence,
                }
            )
    return sorted(matches, key=lambda item: (item["facet"], -item["score"], item["atom_id"]))


def _primary_signal_for_element(element: _ElementRecord, facet: str) -> _MatchSignal | None:
    semantics = element.semantics or {}
    if element.diagram_type == "component" and element.element_kind == "node" and facet == "what":
        text = semantics.get("label") or element.label or element.element_id
        return _MatchSignal(facet=facet, element_text=text, element_source="label")
    if element.diagram_type == "component" and element.element_kind == "edge" and facet in {"how", "why"}:
        text = semantics.get("relation")
        if text:
            return _MatchSignal(facet=facet, element_text=text, element_source="semantics.relation")
    if element.diagram_type == "state" and element.element_kind == "state" and facet == "what":
        text = semantics.get("label") or element.label or element.element_id
        return _MatchSignal(facet=facet, element_text=text, element_source="label")
    if element.diagram_type == "state" and element.element_kind == "transition":
        if facet == "when" and semantics.get("on"):
            return _MatchSignal(facet=facet, element_text=semantics["on"], element_source="semantics.on")
        if facet == "why" and semantics.get("guard"):
            return _MatchSignal(facet=facet, element_text=semantics["guard"], element_source="semantics.guard")
        if facet == "how" and semantics.get("action"):
            return _MatchSignal(facet=facet, element_text=semantics["action"], element_source="semantics.action")
    return None


def _best_basis_for_match(signal: _MatchSignal, atom: _AtomRecord) -> _ScoredBasis | None:
    element_tokens = _normalize_tokens(signal.element_text)
    if not element_tokens:
        return None
    element_phrase = " ".join(element_tokens)

    candidates: list[tuple[_ScoredBasis, int, str]] = []

    title_tokens = _normalize_tokens(atom.title)
    title_score = _score_title_or_alias(element_tokens, title_tokens, exact=1.00, contained=0.90, overlap=0.75)
    if title_score is not None:
        candidates.append((_ScoredBasis(title_score, "title", f'{signal.element_source}="{signal.element_text}" matched atom.title="{atom.title}"'), 0, atom.atom_id))

    for index, alias in enumerate(atom.aliases):
        alias_tokens = _normalize_tokens(alias)
        alias_score = _score_title_or_alias(element_tokens, alias_tokens, exact=0.95, contained=0.85, overlap=0.70)
        if alias_score is not None:
            candidates.append((_ScoredBasis(alias_score, "alias", f'{signal.element_source}="{signal.element_text}" matched atom.aliases[{index}]="{alias}"'), 1, atom.atom_id))

    for label, tag_text in _iter_tag_texts(atom.tags):
        tag_tokens = _normalize_tokens(tag_text)
        tag_score = _score_title_or_alias(element_tokens, tag_tokens, exact=0.88, contained=0.78, overlap=0.65)
        if tag_score is not None:
            candidates.append((_ScoredBasis(tag_score, "tag", f'{signal.element_source}="{signal.element_text}" matched {label}="{tag_text}"'), 2, atom.atom_id))

    atom_union_tokens = sorted({*title_tokens, *[token for alias in atom.aliases for token in _normalize_tokens(alias)], *[token for _label, text in _iter_tag_texts(atom.tags) for token in _normalize_tokens(text)]})
    semantics_score = _score_semantics_token(element_tokens, atom_union_tokens)
    if semantics_score is not None:
        candidates.append((_ScoredBasis(semantics_score, "semantics-token", f'{signal.element_source}="{signal.element_text}" matched atom.token-union="{' '.join(atom_union_tokens)}"'), 3, atom.atom_id))

    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item[0].score, item[1], item[2]))
    return candidates[0][0]


def _score_title_or_alias(element_tokens: list[str], atom_tokens: list[str], exact: float, contained: float, overlap: float) -> float | None:
    if not atom_tokens:
        return None
    if " ".join(element_tokens) == " ".join(atom_tokens):
        return exact
    if set(element_tokens).issubset(set(atom_tokens)):
        return contained
    ratio = _token_overlap_ratio(element_tokens, atom_tokens)
    if ratio >= 0.50:
        return overlap
    return None


def _score_semantics_token(element_tokens: list[str], atom_tokens: list[str]) -> float | None:
    if not atom_tokens:
        return None
    if set(element_tokens).issubset(set(atom_tokens)):
        return 0.72
    if _token_overlap_ratio(element_tokens, atom_tokens) >= 0.50:
        return 0.60
    return None


def _token_overlap_ratio(element_tokens: list[str], atom_tokens: list[str]) -> float:
    element_unique = set(element_tokens)
    if not element_unique:
        return 0.0
    return len(element_unique & set(atom_tokens)) / len(element_unique)


def _iter_tag_texts(tags: list[str] | dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    if isinstance(tags, dict):
        for key, value in sorted(tags.items()):
            values.append((f"atom.tags[{key}]", str(key)))
            if isinstance(value, list):
                for item in value:
                    values.append((f"atom.tags[{key}]", str(item)))
            else:
                values.append((f"atom.tags[{key}]", str(value)))
    elif isinstance(tags, list):
        for index, tag in enumerate(tags):
            values.append((f"atom.tags[{index}]", str(tag)))
    return values


def _normalize_tokens(value: str) -> list[str]:
    text = (value or "").lower().strip()
    text = re.sub(r"[_\-/:.,()\[\]{}|><]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return [token for token in text.split(" ") if token]


def _match_component_edge(line: str) -> dict[str, str | None] | None:
    for pattern in COMPONENT_EDGE_PATTERNS:
        match = pattern.match(line)
        if match:
            return {
                "left": match.group("left").strip(),
                "right": match.group("right").strip(),
                "label": match.groupdict().get("label") and match.group("label").strip(),
            }
    return None


def _parse_component_endpoint(value: str) -> tuple[str | None, str | None]:
    value = value.strip()
    token_match = re.match(r"(?P<token>[A-Za-z][A-Za-z0-9_]*)", value)
    if token_match is None:
        return None, None
    token = token_match.group("token")
    label_match = re.search(r"([\[(\{]{1,2})(?P<label>.*?)([\])\}]{1,2})", value)
    label = _clean_component_label(label_match.group("label")) if label_match else token
    return token, label


def _clean_component_label(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().strip('"').replace("<br/>", " ").replace("<br>", " ")
    cleaned = HTML_TAG_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or None


def _parse_state_endpoint(value: str, aliases: dict[str, str], *, is_source: bool) -> tuple[str, str]:
    token = value.strip()
    if token == "[*]":
        return ("start", "Start") if is_source else ("end", "End")
    token = token.strip('"')
    return token, aliases.get(token, token)


def _embedded_element_slug(element_id: str) -> str:
    return element_id.replace(":", "-")


def _read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return {}
    loaded = yaml.safe_load(block) or {}
    return loaded if isinstance(loaded, dict) else {}


def _normalize_facets(value: Any) -> list[str]:
    items = value if isinstance(value, list) else [value]
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        facet = str(item or "").strip().lower()
        if facet in FACETS and facet not in seen:
            seen.add(facet)
            result.append(facet)
    return result


def _normalize_aliases(metadata: dict[str, Any], title: str) -> list[str]:
    aliases: list[str] = []
    for key in ATOM_ALIAS_KEYS:
        value = metadata.get(key)
        if isinstance(value, str):
            aliases.append(value)
        elif isinstance(value, list):
            aliases.extend(str(item) for item in value)
    aliases.append(title)
    tags = metadata.get("tags") or []
    if isinstance(tags, list):
        for tag in tags:
            aliases.append(str(tag))
            if ":" in str(tag):
                aliases.append(str(tag).split(":", 1)[1])
    normalized: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        alias = str(alias).strip()
        if alias and alias not in seen:
            seen.add(alias)
            normalized.append(alias)
    return normalized


def _diagram_type_for_mermaid(mermaid: str) -> str | None:
    first_line = next((line.strip() for line in mermaid.splitlines() if line.strip()), "")
    if FLOWCHART_PREFIX_RE.match(first_line):
        return "component"
    if STATE_PREFIX_RE.match(first_line):
        return "state"
    return None


def _nearest_heading_title(headings: list[re.Match[str]], position: int) -> str | None:
    title = None
    for heading in headings:
        if heading.start() >= position:
            break
        title = heading.group("title").strip()
    return title


def _scope_from_relative_path(relative_path: str) -> str | None:
    parts = Path(relative_path).parts
    if not parts:
        return None
    if parts[0] in {"projects", "software"} and len(parts) >= 3:
        return "/".join(parts[:3])
    return parts[0]


def _strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", HTML_TAG_RE.sub("", value)).strip()


def _slugify(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[/:><|()\[\]{}\"'.]", "-", text)
    text = re.sub(r"[^a-z0-9_-]", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "unnamed"


def _is_excluded(root: Path, path: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    if any(relative == prefix or relative.startswith(f"{prefix}/") for prefix in EXCLUDED_PATH_PREFIXES):
        return True
    return any(part in EXCLUDED_PATH_PARTS for part in Path(relative).parts)


def _add_edge(
    edges: dict[tuple[str, str, str, str, str | None], CoverageGraphEdge],
    edge: CoverageGraphEdge,
) -> None:
    key = (edge.source_id, edge.target_id, edge.role, edge.facet or "", edge.atom_id)
    edges.setdefault(key, edge)
