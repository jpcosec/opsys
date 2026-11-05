"""The desk's graph as configuration over sldb's project graph.

sldb (``sldb.api.edges.project_graph``) reads the nodes, the store's edge index and the
declarations; this module only says what a desk is made of: where its documents live, which
files are nodes, which fields and sections declare references, and which documents are history.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from sldb.api.edges.project_graph import DeclaredFileTargets
from sldb.api.edges.project_graph import DocumentNode
from sldb.api.edges.project_graph import DocumentSurface
from sldb.api.edges.project_graph import FileExclusions
from sldb.api.edges.project_graph import FileNode
from sldb.api.edges.project_graph import FileRule
from sldb.api.edges.project_graph import LineMentions
from sldb.api.edges.project_graph import MentionPattern
from sldb.api.edges.project_graph import MissingTargetKind
from sldb.api.edges.project_graph import ProjectGraph
from sldb.api.edges.project_graph import ProjectGraphConfig
from sldb.api.edges.project_graph import ProjectGraphExtraction
from sldb.api.edges.project_graph import ReferenceField
from sldb.api.edges.project_graph import SectionMentions
from sldb.api.edges.project_graph import extract_document_nodes
from sldb.api.edges.project_graph import extract_file_nodes

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD


DOC_NODE_EXTRACTOR = "desk_doc_nodes_v1"
SOURCE_FILE_NODE_EXTRACTOR = "desk_source_file_nodes_v1"
DECLARED_EDGE_EXTRACTOR = "desk_declared_edges_v1"

# Declared fields that record where a document came from. They link to the source while it
# exists; once it is deleted the provenance stays recorded as text and is not a reference.
PROVENANCE_FIELDS = ("from_drawer",)

_MD = (".md",)
SURFACES = (
    DocumentSurface(kind="atom", directory="desk/atoms", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="materialization", directory="desk/materializations", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="role", directory="desk/roles", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="runtime_profile", directory="desk/runtimes", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="run", directory="desk/runs", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="pill", directory="desk/contexts", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="task", directory="desk/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="issue", directory="desk/drawer/issues", pattern="*.md", identity="document_id_or_slug"),
    DocumentSurface(kind="question", directory="desk/drawer/questions", pattern="*.md"),
    DocumentSurface(kind="task", directory="desk/drawer/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="feature", directory="desk/drawer/features", pattern="*.md"),
    DocumentSurface(kind="use_case", directory="desk/drawer/use-cases", pattern="*.md"),
    DocumentSurface(kind="stress_test", directory="desk/drawer/stress-tests", pattern="**/*.md"),
    DocumentSurface(kind="diagram", directory="docs/diagrams", pattern="**/*", suffixes=(".md", ".mmd")),
    DocumentSurface(kind="doc", directory="docs", pattern="**/*.md", excluded_parts=("diagrams",)),
    DocumentSurface(kind="doc", directory="", pattern="README.md"),
    DocumentSurface(kind="doc", directory="deskops/data", pattern="**/*.md"),
    DocumentSurface(kind="spec", directory="spec", pattern="**/*", suffixes=(".md", ".yaml", ".yml")),
    DocumentSurface(kind="board", directory="desk/tasks", pattern="Board.md", identity="document_id"),
    DocumentSurface(kind="drawer_board", directory="desk/drawer/tasks", pattern="Board.md"),
    DocumentSurface(kind="ritual", directory="desk/rituals", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="step", directory="desk/steps", pattern="*.md", identity="document_id"),
)

_SPEC = (".md", ".yaml", ".yml")
_DATA = (".json", ".yaml", ".yml")
FILE_RULES = (
    FileRule(kind="spec", file_kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"), suffixes=_SPEC),
    FileRule(kind="test_file", file_kind="test", path_prefixes=("tests",), suffixes=(".py",)),
    FileRule(kind="config_file", file_kind="config", suffixes=(".cfg", ".ini", ".toml")),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, hidden_name=True),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, stem_keywords=("config", "namespace", "registry")),
    FileRule(kind="source_file", file_kind="source", path_prefixes=("desk", "deskops"), suffixes=(".py",)),
)

EXCLUSIONS = FileExclusions(
    directories=(".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tmp", ".venv", "__pycache__", "build", "dist", "node_modules", "tools", "venv"),
    path_prefixes=(".sldb/runtime", "tests/fixtures"),
    suffixes=(".pyc", ".pyo"),
    path_endings=(".graph.json", ".kgdb.json", ".snapshot.json"),
)

MATERIALIZATION_TARGETS = DeclaredFileTargets(
    directory="desk/materializations", field="target_identity", kind="source_file", file_kind="source",
    source_kind="declared_materialization_target",
)


def _atom_field(*path: str, index_owned: bool = False) -> ReferenceField:
    return ReferenceField(path=path, target_prefix="atom:", default_role=DEFAULT_ROLE, allowed_roles=ALLOWED_ROLES, index_owned=index_owned)


def _target_field(*path: str) -> ReferenceField:
    return ReferenceField(path=path, default_role=DEFAULT_ROLE, scalar_only=True)


REFERENCE_FIELDS = (
    *(_atom_field(field, index_owned=True) for field in (CANONICAL_FIELD, MATERIALIZATION_FIELD, *LEGACY_FIELDS)),
    _atom_field("materialization", "source_atoms"),
    _target_field("materialization", "target_identity"),
    _target_field("target_identity"),
)

# A slug like `atom-pills-carry-transitional-task-knowledge` contains `task-knowledge`, which is
# part of an atom name, not a task reference; a real reference starts at a non-word, non-hyphen.
TASK_OR_ISSUE = MentionPattern(regex=r"(?<![\w-])(?P<kind>task|issue)-[a-z0-9][a-z0-9-]*\b", target="{kind}:{0}")
ATOM = MentionPattern(regex=r"\batom-[a-z0-9][a-z0-9-]*\b", target="atom:{0}")
SOURCE_PATH = MentionPattern(
    regex=r"(?<![\w/.-])(?P<path>(?:deskops|desk|tests|spec|docs)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|md|toml|json|mmd))(?![\w/.-])",
    target="{path}",
)
SECTION_MENTIONS = (
    SectionMentions(
        headings=("related atoms", "source atoms", "related tasks", "related issues", "related task", "related issue"),
        patterns=(ATOM, TASK_OR_ISSUE), role=DEFAULT_ROLE,
    ),
    SectionMentions(headings=("source", "sources", "diagram source", "diagram sources"), patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, kinds=("diagram",)),
)
# Drawer tasks keep the extraction they had as `drawer_task` nodes: their lines are not scanned.
LINE_MENTIONS = (
    LineMentions(
        kinds=("task", "issue"), excluded_path_prefixes=("desk/drawer/tasks",), skipped_frontmatter_fields=PROVENANCE_FIELDS,
        patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, locator="source-file-reference",
    ),
)
MISSING_TARGET_KINDS = (
    MissingTargetKind(parts=("docs", "diagrams"), kind="diagram"),
    MissingTargetKind(parts=("docs",), kind="doc"),
    MissingTargetKind(parts=("tests",), kind="test_file"),
    MissingTargetKind(parts=("spec",), kind="spec"),
    MissingTargetKind(parts=(), one_of_first=("desk", "deskops"), ending=".py", kind="source_file"),
)


def _closed_issue(kind: str, text: str) -> bool:
    """A closed issue is history, like a ``record: true`` document."""
    if kind != "issue":
        return False
    from deskops.services.issues import issue_status

    return issue_status(text) == "closed"


def _model_classes() -> dict[str, Any]:
    from deskops import models

    return {name: value for name, value in vars(models).items() if isinstance(value, type)}


def _declared_fields(model: Any) -> tuple[str, ...]:
    return (*getattr(model, "__containment__", {}).keys(), *getattr(model, "__references__", []))


def _model_kind(model: Any) -> str | None:
    types = (getattr(model, "__semantics__", None) or {}).get("type") or []
    return types[-1] if types else None


def _fields_by_kind() -> dict[str, tuple[str, ...]]:
    """Model-declared reference fields per surface kind: the first model (in ``models.__all__``) of that type."""
    from deskops import models

    fields: dict[str, tuple[str, ...]] = {}
    for kind in {surface.kind for surface in SURFACES}:
        normalized = kind.removeprefix("drawer_")
        model = next((getattr(models, name) for name in models.__all__ if _model_kind(getattr(models, name)) == normalized), None)
        if model is not None:
            fields[kind] = _declared_fields(model)
    return fields


@lru_cache(maxsize=1)
def desk_graph_config() -> ProjectGraphConfig:
    """What a desk's graph is made of."""
    classes = _model_classes()
    kinds = {name: _model_kind(model) for name, model in classes.items()}
    return ProjectGraphConfig(
        document_extractor=DOC_NODE_EXTRACTOR, file_extractor=SOURCE_FILE_NODE_EXTRACTOR, edge_extractor=DECLARED_EDGE_EXTRACTOR,
        surfaces=SURFACES, file_rules=FILE_RULES, exclusions=EXCLUSIONS, declared_file_targets=(MATERIALIZATION_TARGETS,),
        reference_fields=REFERENCE_FIELDS, fields_by_kind=_fields_by_kind(),
        fields_by_model={name: _declared_fields(model) for name, model in classes.items()},
        kind_by_model={name: "materialization" if kind == "materialization_contract" else kind for name, kind in kinds.items() if kind},
        provenance_fields=PROVENANCE_FIELDS, section_mentions=SECTION_MENTIONS, line_mentions=LINE_MENTIONS,
        missing_target_kinds=MISSING_TARGET_KINDS, closed_document=_closed_issue,
    )


def desk_graph(root: Path) -> ProjectGraph:
    """The desk's declared-edge graph, read source by source."""
    return ProjectGraph(root, desk_graph_config())


def extract_doc_nodes(root: Path) -> list[DocumentNode]:
    """Every desk document as a node."""
    return extract_document_nodes(root, desk_graph_config())


def extract_source_file_nodes(root: Path) -> list[FileNode]:
    """Every source, test, config and spec file (and declared materialization target) as a node."""
    return extract_file_nodes(root, desk_graph_config())


def extract_declared_edges(root: Path) -> ProjectGraphExtraction:
    """Every declared edge of the desk and every declared target that does not resolve."""
    return desk_graph(root).extraction()
