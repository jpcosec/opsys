FILE:desk/tasks/task-cc35c-referencias-entrantes-referrers-y-rewrite-references-dentro-de-la-transacción-menciones-en-pro.md
---
sldb:
  by: agent
  at: '2026-11-11T03:26:57Z'
  authority: generated
  via: save_document_payload
id: task-cc35c-referencias-entrantes-referrers-y-rewrite-references-dentro-de-la-transacción-menciones-en-pro
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/
- deskops/atom_references.py
- deskops/graph/desk_graph.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35c: Referencias entrantes - referrers y rewrite_references dentro de la transacción; menciones en prosa como MentionPattern

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35c del plan deskops-como-config: parte (3) del agregado CC35. Depende de CC35a (transacción, en main) y CC33c (grafo de proyecto con la configuración de deskops, en main). Gate G_GD22 satisfied.

## Goal

_Describe the concrete result this task must produce._

atoms delete/split/merge, retire, drawer remove y closeout buscan y reescriben las referencias entrantes con referrers y rewrite_references de sldb dentro de la misma transacción; las menciones en prosa se ven por los MentionPattern de la configuración de grafo; se borran las búsquedas propias.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py, tests/, docs/, CHANGELOG.md. Fuera: la API de tags (CC35d resto, DO7) y las vistas (CC34).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml, CC35c). SCOPE: Parte (3) del scope de CC35. atoms delete/split/merge, retire, drawer remove y closeout usan referrers/rewrite_references (GD22) dentro de la misma transacción. Las menciones atom:<id> en prosa y los bullets del drawer se declaran como MentionPattern en la configuración de grafo de deskops que deja CC33. Por eso depende de CC33: esa parte queda en este nodo y no se movió a CC33.

ACCEPTANCE: grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío; retire de una pill la quita del Board y de las tareas en una sola transacción; atoms merge reescribe menciones atom:<id> en prosa; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py (MentionPattern), tests/, CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-11, coordinador del plan; base origin/main b990c49e, con CC33a, CC33b y CC33c cerrados):
a1 (lo que hay hoy): deskops/services/atoms.py _find_inbound_atom_references (:767) y _rewrite_inbound_atom_references (:788), que usan atoms delete, split y merge (:222, :309, :389-393). deskops/services/retire.py _inbound_references (:212), que usa retire (:96). Los números de línea son orientativos; se localiza por nombre.
a2 (API de sldb, GD22): sldb.api.edges.referrers(store, target) y sldb.api.edges.rewrite_references(store, target, replacement, transaction=..., dry_run=...). Se llaman dentro de la misma desk_transaction (CC35a) que hace la escritura principal, así que un fallo revierte todo.
a3 (menciones en prosa): la configuración de grafo de deskops/graph/desk_graph.py ya declara MentionPattern ATOM (atom-<slug>), TASK_OR_ISSUE y SOURCE_PATH (CC33c). Este nodo comprueba que referrers de sldb ve las menciones atom:<id> en prosa y los bullets del drawer a través de esa configuración. Si no las ve, el MentionPattern que falte se suma ahí; si sldb no admite el caso, hipótesis y nota a sldb.
a4 (drawer remove y closeout): se localizan las vías que hoy quitan referencias entrantes a un documento borrado. Si no tienen, se deja escrito en el informe; no se inventan.
a5 (aceptación de retire de una pill): un test sobre tmp_path con una pill ligada en el Board y en dos tareas. `deskops retire` (o el comando que retire pills hoy) la quita de los tres en una sola transacción y deja un solo commit o una sola escritura atómica. Si se fuerza un fallo a mitad, nada cambia en disco.
a6 (DO8): el grafo se arma con ProjectGraph(root, desk_graph_config()) en proceso, no con sldb.api.project_graph(store).
a7 (files): deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py, tests/, docs/, CHANGELOG.md.
a8 (4 pasos): sldb stores build --store .sldb; pytest, un proceso por archivo de tests/; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio.

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-11, coordinador del plan; decisiones revisables):
b1 (formas de mención): en el desk hay dos formas, `atom:atom-<slug>` (con prefijo de kind) y el id pelado `atom-<slug>`, a veces entre backticks. MentionPattern ATOM ya captura la segunda; la primera la cubre el target "atom:{0}". El test de atoms merge usa las dos y comprueba que las dos se reescriben. Si una no la ve referrers, se suma el patrón que falte en desk_graph.py.
b2 (criterio para la nota a sldb): si con el MentionPattern declarado `sldb.api.edges.referrers` no devuelve la mención de una de las dos formas sobre un desk de tmp_path, es caso de sldb: hipótesis en el informe con el desk mínimo que lo reproduce. El coordinador abre la nota.
b3 (drawer remove y closeout): las vías son `deskops drawer remove` (services/drawer.py remove_entry) y los cierres de closeout que borran la tarea (commit, supersede, retire, resolved-by). Si alguna hoy no toca referencias entrantes, sigue sin tocarlas (no se suma comportamiento). Cuando borra un documento que tiene referrers, reporta los que quedan colgando con un alert que nombra cada referrer, sin reescribir. Se prueba en un caso.
b4 (retire de una pill): el comando es `deskops retire <path> --reason --ref` (acepta pills). Lo que se exige y prueba es una sola desk_transaction: Board y tareas se reescriben en la misma transacción, y un fallo forzado a mitad deja el disco sin cambios. El commit no es parte de retire.
b5 (líneas antes y después): tabla en el informe runs/subagents/cc35c-worker-report.md con `wc -l` de cada archivo tocado de deskops/services/, deskops/atom_references.py y deskops/graph/desk_graph.py, antes (base) y después.
b6 (docs/): sí entra. docs/operator-manual.md, en las secciones de atoms delete/split/merge, retire y drawer remove, si cambia lo que el operador ve.

## Validation

_List the checks required before this task can close._

- grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío
- retire de una pill la quita del Board y de las tareas en una sola transacción (a5)
- atoms merge reescribe menciones atom:<id> en prosa
- Goldens de ayuda y salida idénticos; tests de los archivos tocados verdes
- deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío; retire de una pill la quita del Board y de las tareas en una sola transacción; atoms merge reescribe menciones atom:<id> en prosa; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

FILE:deskops/atom_references.py
"""Canonical atom reference metadata.

One artifact field carries structured atom references: ``atoms``. A reference is
either a bare atom id or a mapping with an ``id`` and an optional ``role``. The
role vocabulary is deliberately small; ``related_atoms`` is a legacy alias that
``deskops drift check`` reports, and ``source_atoms`` remains the
``MaterializationContractDoc`` field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CANONICAL_FIELD = "atoms"
LEGACY_FIELDS = ("related_atoms",)
MATERIALIZATION_FIELD = "source_atoms"
ALLOWED_ROLES = ("references", "documents", "specifies", "constrains", "validates")
DEFAULT_ROLE = "references"

INVALID_ROLE_VIOLATION = "invalid_atom_reference_role"
LEGACY_FIELD_VIOLATION = "legacy_atom_reference_field"


@dataclass(frozen=True)
class ParsedAtomReference:
    """One declared atom reference.

    ``role`` keeps the declared value even when it is invalid; ``violation``
    names the problem so extractors can fall back to ``DEFAULT_ROLE`` while the
    drift validator reports the declaration instead of hiding it.
    """

    atom_id: str
    role: str
    field_name: str
    violation: str | None = None

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.atom_id, self.role, self.field_name)


def parse_atom_reference(
    value: Any,
    field_name: str = CANONICAL_FIELD,
) -> ParsedAtomReference | None:
    """Parse a string or ``{id, role}`` mapping into an atom reference.

    Returns ``None`` when the value is not a reference shape. An unknown role is
    returned as an explicit ``invalid_atom_reference_role`` violation; it is
    never silently rewritten here.
    """
    if isinstance(value, str):
        atom_id = value.strip()
        if not atom_id:
            return None
        return ParsedAtomReference(atom_id=atom_id, role=DEFAULT_ROLE, field_name=field_name)

    if not isinstance(value, dict):
        return None

    atom_id = value.get("id")
    if not isinstance(atom_id, str) or not atom_id.strip():
        return None

    role = value.get("role")
    if not isinstance(role, str) or not role.strip():
        return ParsedAtomReference(
            atom_id=atom_id.strip(),
            role=DEFAULT_ROLE,
            field_name=field_name,
        )

    role = role.strip()
    violation = None if role in ALLOWED_ROLES else INVALID_ROLE_VIOLATION
    return ParsedAtomReference(
        atom_id=atom_id.strip(),
        role=role,
        field_name=field_name,
        violation=violation,
    )


def iter_atom_reference_values(value: Any) -> list[Any]:
    """Normalize a declared field value to the reference shapes to parse."""
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]

FILE:deskops/graph/desk_graph.py
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
    path_prefixes=(".sldb/runtime", ".sldb/core/documents", ".sldb_cache", "tests/fixtures"),
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

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Closeout rules (CC33b): the closeout gate of each factory task type is a `RuleDoc` seed, `deskops/data/rules/rule-closeout-task-<type>.md`, written as a managed seed to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`, glob `rule-closeout-*.md`; a second `--apply` changes nothing). Each is `on_transition`, `severity: error`, `where current_node = "ritual-closeout"` (the source of `task_completes`), subject `model <= <TypeDoc>`, and asks for the evidence receipts of CC33a, accepted and intact: `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")` per kind, `atom|materialization` as an `or` of two. `task.refactor` adds the `goldens` review receipt (`deskops review record --kind goldens`) to the `task.code` rule its family gets; `task.aggregate` asks only for `commit` (no `children` field yet). The kinds per type are data, `deskops/data/rules/closeout-evidence.yaml`, which `deskops closeout verify` and `deskops add task` read (a desk subtype reads its nearest factory ancestor's entry); `tests/test_closeout_rules.py` checks the rules against it. Two `on_write` alert rules cover task fields: `rule-closeout-alert-implicit-code` and `rule-closeout-alert-pill-graduation`.
- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
- Scion autonomy contract (task-scion-autonomy-coordinator-contract): runtime templates add independent `--mode tester`, strict `--context-file` and separate task-data `--task-root`. Coordinators reconcile their own children and Scion activity before selecting work, prepare missing reviews, require independent passing tests, and verify scoped closeout before continuing through phases. Child identities use the full canonical SLDB contract; native label descriptors fit Scion ASCII/63-character limits. RunDocs record immutable launch intent, and the supervisor may mutate modeled workflow through CLIs while implementation stays with executors.
- `deskops review record --kind preflight|bundle --operator <name>` (main en verde, decisión B del coordinador de proyecto con las condiciones del overlord): a desk without a model (CI scenarios, the quickstart) records those receipts by hand. `--operator` is required for both kinds (without it nothing is written); the receipt keeps `engine: human`, names the operator as `actor` and says `no model available` in its title and summary. Real desk tasks still get them from `deskops review preflight|bundle`.
- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).
- `deskops closeout resolved-by --task <id> --reason "..." --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] [--paths ...] [--message ...]` closes a task whose work already entered the history (for example through a PR) before its closeout (`ClosureService.close_resolved_by`). It does not ask for an atom per changed file: at least one `--ref` must be a commit that is HEAD or an ancestor of the `--root` repository, the other refs may be ancestor commits or http(s) URLs, and at least one `--test` is required, each one accepted by the tests gate for the task's `files`. Any ref or test that does not resolve, or a blank reason, is refused with exit 1 and writes nothing. It makes one closing commit with `Task-Id`, `Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and one `Closeout-Test` per test, marks the task `resolved` with `resolved-by` in its history, takes it off the Board and records the index entry with `mode: resolved-by` (`tests/test_closeout_resolved_by.py`).

### Changed

- `deskops desk replace` writes through `sldb.api.replace_text` (CC35d a4, GD27) inside the desk transaction (`doc_access.desk_transaction`), instead of writing the bytes and untracking and re-tracking the document itself. deskops keeps which files the verb reaches (modeled subjects are still pointed at `deskops edit`) and the count guard with its message (`Refusing to replace in <path>: found N occurrence(s) of --old, expected M. The file is unchanged.`), checked before sldb is called. A plain file (a drawer note, an issue body, `tag-namespaces.yaml`) is rewritten as before. A store-tracked file (a role prompt) is now validated under its model and the store's `on_write` rules before it is rewritten and tracked again, and a replacement that breaks it is refused with `Refusing to replace in <path>: <sldb error> The file is unchanged.` (exit 1), the transaction rolled back. A desk without a store still writes the file directly. The rest of CC35d (tag namespaces, the domain tree, `tag_folder`) waits on sldb (H1-H3) (`tests/test_desk_replace.py`).
- `deskops closeout commit` writes no receipt and no longer gates on verify's result: it evaluates the task type's closeout rule on the receipts `deskops closeout verify` wrote (task read at `ritual-closeout`). A blocked commit prints `Closeout gate blocked <task>; the closing commit was not made.`, the declared/found line and alerts of a read-only verify, one `- error: [rules/rule-closeout-<type>] ...` line per finding and `Run 'deskops closeout verify --task <task>' ...`; a task the store does not track cannot be evaluated and is blocked with that reason. The `task_completes` edge condition is `status = "ready_for_testing"` (the `has(closeout_evidence_verified)` fact is gone), so `deskops show task`, `next` and `advance` show the rule's findings on that gate. Editing a contract field after verify leaves the receipts `changed` and blocks again.
- `deskops closeout verify`: the task's `closeout_evidence` only adds kinds to its type's (DA5): an added kind is verified and gets its receipt, and a failure is the alert `added_closeout_evidence_not_verified` instead of a blocking finding; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`. `goldens` is read by the rule from the review receipt, not produced by verify, and `children` is no longer declared, so `closeout_evidence_not_verifiable` is gone. When the atom|materialization gate passes without a linking document (exempt desk, follow-up only, skill guard test) verify writes an accepted `atom` receipt with `value: exempt: <why>` (b3). The `closeout_evidence_not_declared` alert moved to the `rule-closeout-alert-implicit-code` rule.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
- `deskops graph neighbors|missing|reflect` and `deskops drift check` read sldb's project graph of the desk (CC33c, GD21: `sldb.api.edges.project_graph.ProjectGraph` with the configuration of `deskops/graph/desk_graph.py`) instead of a snapshot deskops built and read back. Without `--graph`, `graph neighbors` and `graph reflect` no longer need a prior `graph build` and no longer read `.sldb/runtime/graphs/deskops.kg.json` or the legacy `.sldb/runtime/knowledge_graph.kg.json`; `drift check` reads the graph's edges and its dangling edge targets whether or not a snapshot was built. `--graph <path>` still reads that graph file (`deskops/graph/view.py`, `read_graph_file`). `deskops graph build` still writes the KGDB GraphSnapshot and its NetworkX sibling, unchanged, from the same graph (`deskops/graph/export.py`). `deskops/graph/snapshot.py` is gone (its runtime-path fallback and `read_graph_neighbors` with it), and the atom-reference check of `drift check` reads the frontmatter of the project graph's documents under `desk/` and `docs/` instead of an `rglob` (`grep rglob deskops/graph/` is empty). `graph neighbors` and `graph missing` were compared with the frozen v1 extractors over a copy of the real desk (619 nodes, 296 edges, the same `(source, target, role)` sets and the same missing findings), and `tests/graph_oracle_v1/` was then removed; `tests/closeout_graph_oracle.py` keeps only the lifecycle-transitions oracle.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. CC33c lo decidió (a4): el grafo de proyecto de sldb sigue sin nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json`, así que la excepción queda. Tests en `tests/test_graph_missing_existing_files.py`.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or `deferred`, what a drawer task holds, when `current_node` is empty); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or, when `current_node` is empty (a task outside the lifecycle), `deferred` (a drawer task) or `resolved`/`closed`/`done`/`complete` (a task resolved before the lifecycle, what `closeout retire` removes)); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- Selectors of tracked desk documents resolve through `sldb.api.select_documents` (CC35b, GD23). `doc_access.resolve_document` asks the store twice, in order: by name (`prefix`, where an exact name wins over the one prefix match) under the directory's pattern, then, only if that found nothing, by file name (`path_glob` of `<selector>*.md`), so a ritual tracked as `ritual-execution` in `desk/rituals/execution.md` resolves as `ritual-execution` and as `execution`; an ambiguous query stops there. `resolve_glob`, `resolve_artifact_selector[_multi]`, `resolve_ritual_selector`, `registered_repositories` and the task and pill lookups of `deskops review` use it; the messages are the same (`No <what> file found for selector '<s>'`, `Ambiguous <what> selector '<s>': <paths relative to desk/>`), the ambiguity candidates being the rows sldb names. Gone: `_tracked_task_paths` (which read `.sldb/core/documents/` directly) and the frontmatter-id fallbacks of reviews and rituals (`frontmatter_id`): a legacy task resolves by the `TaskDoc` model family, a review and a ritual by the name the store tracks them by. A file on a tracked surface that the store does not track no longer resolves. The drawer and `desk/issues`, which the store does not track, and a desk without a store keep the disk rule of `desk_paths.resolve_selector` (marked `CC35b-a3`); the `operations.py` aliases graph_ui calls are marked `CC34`. `resolve_artifact_selector_multi` tries its directories in order (an active pill before a drawer pill of the same selector) instead of one candidate set across them. The desk declaration's `include` now names the seeded Board (`desk/tasks/Board.md` as `BoardDoc:Board`) and phase ritual (`desk/rituals/phase.md` as `RitualDoc:ritual-phase`), so `deskops init` and `deskops desk update --apply` track them and a new desk's `deskops edit board Board` resolves (CC35b d1); the Board seed keeps `track: false`.
- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- `__activation_receipts__` and `task_type_activation_receipts` are gone from `deskops/models/task_types.py`: the receipts a type requires live only in its activation `RuleDoc` (CC32). `ReviewDoc`'s docstring says what sldb does with `subject` now that GO07 is in (pins it on save, computes `anchor_state` on read); the model is unchanged. The tests that activate a task write its receipts first with `tests/activation_receipts.py` (accepted and pinned through `sldb.api.transaction`).
- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.
- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).

### Fixed

- `deskops review status` preserves current accepted/rejected dispositions, selects matching exact-input receipts before applying verdict priority, and groups pinned task subjects by task id. Older receipts no longer mask a current acceptance or turn a changed input into a technical failure.

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

### Removed

- `__closeout_evidence__` on the task type classes, the `closeout_evidence_verified` and `pill_graduation_verified` facts, `TasksService.add_closeout_facts`, `ClosureService.has_verified_task_closeout_evidence` and `has_verified_task_pill_graduation`, `task_type_closeout_evidence` and `NOT_YET_VERIFIABLE_EVIDENCE` (CC33b).

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-cc35c-referencias-entrantes-referrers-y-rewrite-references-dentro-de-la-transacción-menciones-en-pro: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío
- retire de una pill la quita del Board y de las tareas en una sola transacción (a5)
- atoms merge reescribe menciones atom:<id> en prosa
- Goldens de ayuda y salida idénticos; tests de los archivos tocados verdes
- deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después
- 4 pasos del workflow en clon limpio

