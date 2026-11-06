FILE:desk/tasks/task-cc31-ciclo-de-vida-declarado-efectos-en-relationdoc-attributes-y-advance-por-edges-holding.md
---
id: task-cc31-ciclo-de-vida-declarado-efectos-en-relationdoc-attributes-y-advance-por-edges-holding
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
- task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb
pills: []
files:
- deskops/lifecycle.py
- deskops/lifecycle_migration.py
- deskops/spec/workflows/task_lifecycle.yaml
- deskops/data/lifecycle/
- deskops/data/desk_declaration.yaml
- deskops/workspace.py
- deskops/services/tasks.py
- deskops/workflow/next_actions.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/core.py
- tests/
- docs/workflow-policy-reference.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC31: Ciclo de vida declarado - efectos en RelationDoc.attributes y advance por edges_holding

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC31 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3 (autorizado por el dueño 2026-11-05), hijo de PF2, árbol T3.1. Rehace GC04 de gates-por-tipo (DK2) sobre la API general de sldb. Depende de CC30 (93cc1943) y CC36 (d4b49ff6), los dos en main. Gates: G_GO09 y G_GD26, satisfied.

## Goal

_Describe the concrete result this task must produce._

El ciclo de vida es grafo con efectos. Cada RelationDoc de desk/lifecycle/ lleva attributes {sets: {status}, terminal} (GO09) y se escribe como semilla managed del paquete. advance usa edges_holding y apply_effects en vez de los campos sets_status/terminal del YAML. task_lifecycle.yaml queda solo con states. lifecycle.py se reduce a cargar configuración, llamar a sldb y escribir history.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/lifecycle.py, deskops/lifecycle_migration.py (k6), deskops/spec/workflows/task_lifecycle.yaml, deskops/data/lifecycle/ y deskops/data/desk_declaration.yaml (semillas managed e include), deskops/workspace.py (solo si la carga de la declaración lo pide), deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py y core.py (llamadas a ensure_lifecycle_graph), tests, docs/workflow-policy-reference.md y CHANGELOG.md. Fuera: doc_io/transacción (CC35a), gates de activación (CC32), cierre y _add_closeout_facts (CC33), escrituras en sldb, formato del desk salvo desk/lifecycle/ (gestionado por deskops) y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 3, CC31). SCOPE: Rehace GC04 de gates-por-tipo (DK2) sobre la API general. Los RelationDoc y RelationTypeDoc de desk/lifecycle/ se declaran como semillas managed del paquete (deskops/data/lifecycle/, mecanismo de CC36 sobre sldb scaffold_store, GD26): cada RelationDoc lleva attributes: {sets: {status: <valor>}, terminal: <bool>} según la convención de GO09; desk update --apply reescribe un RelationDoc que difiera y lo reporta (reemplaza ensure_lifecycle_graph, lifecycle.py:275-374, que hoy deja los existentes como están, :328, :354); la migración de rituales legados de lifecycle.py:204-272 y lifecycle_migration.py se conserva mientras algún desk de los 6 la necesite (lo dice desk update en dry-run) y si ninguno la necesita se borra. task_lifecycle.yaml queda solo con states (next_actions, advance_when) para el comando next; transitions sale del YAML (su contenido vive en las semillas). lifecycle.py: se borran Transition.sets_status/terminal (:40-49) y LifecycleSpec.effect (:62-66); transitions_from usa edges_holding con effects; advance toma la primera arista de edges_holding en el orden de los RelationDoc (campo order en attributes si hace falta desempatar, como clave extra que GO09 conserva), aplica apply_effects(payload, effects, modelo del tipo de la tarea) y, si terminal, current_node = complete; history la sigue escribiendo deskops. lifecycle.py queda en: cargar la configuración, llamar a sldb y escribir history; objetivo < 150 líneas. _add_closeout_facts sigue hasta CC33. La transición terminal sigue sin persistirse desde advance (la puerta de cierre es closeout commit).

ACCEPTANCE: En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status (active, ready_for_testing, closed) y terminal true en task_completes; cambiar el sets de un RelationDoc del desk temporal (con la API de sldb en el test) hace que advance escriba ese valor sin tocar ningún YAML; un RelationDoc de la versión anterior (sin attributes) queda reescrito por desk update --apply y una segunda corrida no cambia nada; grep de sets_status y de "effect" como atributo de LifecycleSpec en deskops/ vacío; task_lifecycle.yaml sin la clave transitions; tests/test_lifecycle_graph.py y tests/test_lifecycle_end_to_end.py verdes (adaptados a effects, sin cambiar los escenarios); goldens de ayuda y salida de advance y next idénticos; deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno; líneas de lifecycle.py antes y después; CHANGELOG; docs/workflow-policy-reference.md.

OUTPUT_SCOPE: deskops/lifecycle.py, deskops/lifecycle_migration.py, deskops/spec/workflows/task_lifecycle.yaml, deskops/data/lifecycle/, deskops/services/tasks.py, deskops/workflow/next_actions.py, deskops/cli/commands/desk.py, tests/, docs/workflow-policy-reference.md, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-06, coordinador del plan):
k1 (gates y base): G_GO09 y G_GD26 están satisfied (sldb 33b3c7a0 y d39bf915 para GO09; 96d7b823 para GD26). El pin efectivo es el main de sldb editable, y pyproject.toml no se toca. CC30 (93cc1943) y CC36 (d4b49ff6) están en main. Las dos quedan abiertas solo por la verificación de goldens de task.refactor, lo que no bloquea a este nodo.
k2 (líneas vigentes en main, en lugar de las del SCOPE): deskops/lifecycle.py tiene 406 líneas: Transition :41-50 (sets_status :48, terminal :49), LifecycleSpec.effect :62, load_lifecycle_spec :90, transitions_from :135, advance :178-216, migración de rituales legados :228-298 (_ensure_ritual_readable, _archive_legacy_ritual), ensure_lifecycle_graph :299-400 y lifecycle_graph_present :401. deskops/lifecycle_migration.py tiene 172 líneas y lo usan cli/commands/desk.py:196-211. ensure_lifecycle_graph lo llaman cli/commands/core.py:48-50 (init), cli/commands/desk.py:146-148 y :436-440, y lifecycle_migration.py:168. desk/lifecycle/ del desk de deskops tiene 3 RelationDoc (execution-task_activates, testing-task_hands_to_closeout, closeout-task_completes) y 3 RelationTypeDoc (type-*.md).
k3 (semillas con el mecanismo de CC36): los 6 documentos de desk/lifecycle/ se declaran como semillas mode: managed en deskops/data/desk_declaration.yaml (o en un archivo hermano de deskops/data/lifecycle/ que la declaración incluye) y se rinden en proceso como en CC36 (H1: todo a texto, comparando bytes). Un RelationDoc del desk que difiera se reescribe y se reporta (rewritten). El tracking que hoy hace ensure_lifecycle_graph (registrar los modelos de relación de sldb, trackear los RelationDoc y RelationTypeDoc y trackear los rituales por su id) pasa a include declarados ({model, glob} para desk/lifecycle/*.md por modelo y {model, paths: [{path, name}]} para los rituales con nombre ritual-<x>), aplicados con apply_includes. Si algo no se expresa así, queda como código del caso y se anota como hipótesis.
k4 (orden de aristas): hoy cada nodo de ritual tiene una sola arista saliente, así que no hace falta desempate. advance toma la primera arista de edges_holding en el orden que devuelve sldb. No se agrega attributes.order. Si al implementar aparece más de una arista que se cumple a la vez desde un mismo nodo, el worker para y avisa.
k5 (modelo para apply_effects): es el modelo registrado del tipo de la tarea (el registro de tipos de tareas de deskops, services/tasks.registered_task_types; TaskCodeDoc si el tipo no está). history la sigue escribiendo deskops como hoy. La transición terminal sigue sin persistirse desde advance, porque la puerta de cierre es closeout commit.
k6 (migración legada, decisión por evidencia): antes de borrar nada se corre desk update en dry-run sobre una copia de cada uno de los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), bajo /dev/shm y borrada al terminar, con el código de main. Si alguno reporta que necesita la migración de rituales legados o lifecycle_migration, ambas se conservan y el informe dice cuál la necesita. Si ninguno la necesita, se borran (lifecycle.py :228-298 y lifecycle_migration.py, con sus llamadas en desk.py) en el mismo commit.
k7 (fuera): doc_io sigue en ensure_lifecycle_graph o en lo que lo reemplace hasta CC35a. Este nodo no migra escrituras a sldb.api.transaction. _add_closeout_facts sigue hasta CC33. Las gates de activación por tipo son de CC32.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-06; prevalecen sobre el SCOPE):
m1 (orden): manda k4. No se agrega attributes.order; advance toma la primera arista de edges_holding en el orden que devuelve sldb. Si dos aristas se cumplen a la vez desde un mismo nodo, el worker para y avisa. La frase del SCOPE sobre «campo order si hace falta desempatar» no se aplica en este nodo.
m2 (task_lifecycle.yaml): las claves de nivel superior que quedan son id, version, source_files, entry_node y states. Sale solo transitions. Cada elemento de states conserva sus campos actuales (id, current_node, phase, ritual, purpose, next_actions, advance_when). «Solo con states» quiere decir sin transitions, no que cambie la forma de states.
m3 (objetivo de líneas): «< 150 líneas» es un objetivo, no aceptación. Si k6 conserva la migración de rituales legados, ese código (lifecycle.py :228-298) pasa a deskops/lifecycle_migration.py y lifecycle.py se mide sin él. Las líneas de ambos archivos, antes y después, van en el informe.
m4 (referencias de línea): mandan las de k2 (ensure_lifecycle_graph :299-400 en main). Las del SCOPE (:275-374) son de antes de CC30.

## Validation

_List the checks required before this task can close._

- En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status y terminal; segunda corrida sin cambios; un RelationDoc sin attributes queda reescrito (test)
- Cambiar el sets de un RelationDoc con la API de sldb hace que advance escriba ese valor sin tocar YAML (test)
- grep -rn 'sets_status' deskops/ vacío; grep de effect como atributo de LifecycleSpec vacío; task_lifecycle.yaml sin la clave transitions
- Evidencia de k6: desk update en dry-run sobre copias de los 6 desks y decisión sobre la migración legada
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_lifecycle_graph, test_lifecycle_end_to_end, test_scaffold_golden, test_desk_sync, test_output_goldens y test_cli_help_examples (sin --update-golden), y los que importen módulos tocados
- deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno
- wc -l deskops/lifecycle.py antes (406) y después (objetivo < 150)
- CHANGELOG y docs/workflow-policy-reference.md

## Done When

_Name the observable condition that makes the task complete._

En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status (active, ready_for_testing, closed) y terminal true en task_completes; cambiar el sets de un RelationDoc del desk temporal (con la API de sldb en el test) hace que advance escriba ese valor sin tocar ningún YAML; un RelationDoc de la versión anterior (sin attributes) queda reescrito por desk update --apply y una segunda corrida no cambia nada; grep de sets_status y de "effect" como atributo de LifecycleSpec en deskops/ vacío; task_lifecycle.yaml sin la clave transitions; tests/test_lifecycle_graph.py y tests/test_lifecycle_end_to_end.py verdes (adaptados a effects, sin cambiar los escenarios); goldens de ayuda y salida de advance y next idénticos; deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno; líneas de lifecycle.py antes y después; CHANGELOG; docs/workflow-policy-reference.md.

FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task. deskops writes those documents
once per desk from ``deskops/spec/workflows/task_lifecycle.yaml`` and reads the transitions back
from the graph with ``sldb.api.edges.edges_from``; there are no per-task primitives.

What the graph does not carry is the effect of a transition: the status it sets and
whether it closes the task. Those come from the spec, keyed by relation type. Conditions
are evaluated by sldb itself (``sldb.api.where_matches``, sldb >= 0.1.6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import render_model_markdown

from deskops import doc_io
from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


@dataclass(frozen=True, slots=True)
class Transition:
    relation_type: str
    title: str
    description: str
    source: str
    target: str
    condition: str
    sets_status: str
    terminal: bool = False


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    entry_node: str
    transitions: tuple[Transition, ...]
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return list(dict.fromkeys(node for t in self.transitions for node in (t.source, t.target)))

    def effect(self, relation_type: str) -> Transition:
        for transition in self.transitions:
            if transition.relation_type == relation_type:
                return transition
        raise KeyError(f"Relation type '{relation_type}' is not part of the task lifecycle in {SPEC_PATH}")


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it and the closure service keeps the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    transitions = tuple(
        Transition(
            relation_type=str(item["relation_type"]),
            title=str(item.get("title") or item["relation_type"]),
            description=str(item.get("description") or ""),
            source=str(item["source"]),
            target=str(item["target"]),
            condition=str(item.get("condition") or ""),
            sets_status=str(item.get("sets_status") or ""),
            terminal=bool(item.get("terminal") or False),
        )
        for item in payload.get("transitions") or []
    )
    if not transitions:
        raise ValueError(f"Lifecycle spec declares no transitions: {path}")
    return LifecycleSpec(
        entry_node=str(payload.get("entry_node") or transitions[0].source),
        transitions=transitions,
        states=tuple(state for state in payload.get("states") or [] if isinstance(state, dict)),
    )


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def _pythonpath() -> str:
    return package_pythonpath()


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def transitions_from(
    root: Path, node: str, spec: LifecycleSpec | None = None, *, snapshot: ReadSnapshot | None = None
) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology and conditions come from the graph; the effect of each transition comes from
    the spec. A relation type the spec does not know is not a lifecycle transition.

    The lifecycle graph lives in the desk's own store (``ensure_lifecycle_graph`` writes it
    there), so only that store's edge index is read (sldb keeps it composed while its shards
    do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node, spec)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    spec = spec or load_lifecycle_spec()
    known = {t.relation_type for t in spec.transitions}
    found: list[Transition] = []
    for edge in edges_from(_store(root), ritual_export_id(node), include_linked=False):
        if edge.relation not in known or edge.metadata.get("origin") != "relation_doc":
            continue
        effect = spec.effect(edge.relation)
        target = edge.target.rsplit(":", 1)[-1]
        found.append(
            Transition(
                relation_type=edge.relation,
                title=effect.title,
                description=effect.description,
                source=node,
                target=target,
                condition=str(edge.metadata.get("condition") or ""),
                sets_status=effect.sets_status,
                terminal=effect.terminal,
            )
        )
    return sorted(found, key=lambda t: [x.relation_type for x in spec.transitions].index(t.relation_type))


def advance(root: Path, payload: dict[str, Any], spec: LifecycleSpec | None = None) -> TransitionResult:
    """Fire the first transition out of the task's current node whose condition holds.

    Mutates ``payload`` (``current_node``, ``status``, ``history``) and reports what
    happened; one call fires at most one transition.
    """
    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    transitions = transitions_from(root, node, spec)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    for transition in transitions:
        if not condition_holds(transition.condition, payload):
            continue
        if transition.sets_status:
            payload["status"] = transition.sets_status
        history = payload.setdefault("history", [])
        if isinstance(history, list):
            history.append(transition.relation_type)
        payload["current_node"] = COMPLETE if transition.terminal else transition.target
        verb = "Completed" if transition.terminal else "Advanced to"
        target = COMPLETE if transition.terminal else transition.target
        return TransitionResult(payload["current_node"], str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")
    payload["current_node"] = node
    gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
    return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")


# ---------------------------------------------------------------- writing the graph
def _doc_tracked(root: Path, model: str, name: str) -> bool:
    from sldb.api import doc_exists

    return doc_exists(_store(root), f"{model}/{name}")


def _track(root: Path, model: str, path: Path, name: str) -> None:
    doc_io.track(root, path, model, name=name, pythonpath=_pythonpath(), force=False)


def _ensure_ritual_readable(path: Path, ritual_id: str, relative: str) -> bool:
    """Re-render a ritual RitualDoc cannot read; raise if it still cannot round-trip.

    Returns whether the file was rewritten. A hand-authored or older-template ritual can
    extract as empty while its sections still hold text, so the extracted payload alone
    is not enough: the source must also be readable by the model.
    """
    from deskops.doc_readability import is_unreadable_by_model
    from deskops.models import RitualDoc
    from sldb.runtime.validation import extract_model_data

    text = path.read_text(encoding="utf-8")
    try:
        payload = extract_model_data(RitualDoc, text)
        rendered = render_model_markdown(RitualDoc, payload)
        round_trips = extract_model_data(RitualDoc, rendered) == payload
    except Exception as exc:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} cannot be read as {RITUAL_MODEL}: {exc}"
        ) from exc
    from sldb.api.documents.structural_noise import find_structural_noise

    undeclared = find_structural_noise(RitualDoc, text, relative).undeclared
    if undeclared:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} has sections {RITUAL_MODEL} does not declare: "
            + "; ".join(undeclared)
        )
    missing = is_unreadable_by_model(RitualDoc, text)
    if not missing and round_trips:
        return False

    path.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
    repaired = path.read_text(encoding="utf-8")
    try:
        still_missing = is_unreadable_by_model(RitualDoc, repaired)
        lost = [key for key in payload if extract_model_data(RitualDoc, repaired).get(key) != payload.get(key)]
    except Exception as exc:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} cannot be read as {RITUAL_MODEL} after re-rendering: {exc}"
        ) from exc
    if still_missing or lost:
        fields = ", ".join(still_missing or lost)
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} still cannot round-trip through {RITUAL_MODEL} "
            f"after re-rendering; missing sections: {fields}"
        )
    return True


def _archive_legacy_ritual(root: Path, path: Path, ritual_id: str) -> Path:
    """Move a ritual RitualDoc cannot carry to desk/drawer/rituals/ and write the default one.

    A hand-written ritual (no frontmatter id, its own sections, other field shapes) would
    lose text if it were re-rendered, so it is kept byte for byte where the desk does not
    model documents, and the lifecycle state gets the ritual `deskops init` writes.
    """
    from deskops.workspace import default_ritual_text

    archive_dir = root / "desk" / "drawer" / "rituals"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = archive_dir / f"legacy-{path.name}"
    counter = 2
    while archived.exists():
        archived = archive_dir / f"legacy-{path.stem}-{counter}.md"
        counter += 1
    path.rename(archived)
    path.write_text(default_ritual_text(ritual_id, root.name), encoding="utf-8")
    return archived


def ensure_lifecycle_graph(root: Path, spec: LifecycleSpec | None = None) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: registers sldb's relation models, tracks the lifecycle rituals by their
    ids, and writes plus tracks one RelationTypeDoc and one RelationDoc per transition
    under desk/lifecycle/. Existing documents are left as they are.
    """
    from sldb.models.relation_doc import RelationDoc
    from sldb.models.relation_type_doc import RelationTypeDoc

    root = root.resolve()
    spec = spec or load_lifecycle_spec()
    changes: list[str] = []
    doc_io.init_relations_in(root, pythonpath=_pythonpath())

    from sldb.api import doc_status

    pending_rituals: list[tuple[str, Path, str]] = []
    for ritual_id in spec.rituals:
        if _doc_tracked(root, RITUAL_MODEL, ritual_id):
            continue
        path = root / "desk" / "rituals" / f"{ritual_id.removeprefix('ritual-')}.md"
        if not path.exists():
            raise LifecycleGraphMissing(f"Lifecycle ritual '{ritual_id}' has no document at {path.relative_to(root)}")
        relative = path.relative_to(root).as_posix()
        try:
            rerendered = _ensure_ritual_readable(path, ritual_id, relative)
        except LifecycleGraphMissing as exc:
            archived = _archive_legacy_ritual(root, path, ritual_id)
            changes.append(
                f"archived {relative} to {archived.relative_to(root).as_posix()} "
                f"and wrote the default ritual in its place ({exc})"
            )
            rerendered = _ensure_ritual_readable(path, ritual_id, relative)
        if rerendered:
            changes.append(f"re-rendered {relative} to the current {RITUAL_MODEL} template")
        pending_rituals.append((ritual_id, path, relative))

    for ritual_id, path, relative in pending_rituals:
        current = doc_status(_store(root), relative)
        if current.exists and current.name != ritual_id:
            # `desk update` tracks surface documents by file stem; the graph names a
            # ritual by its id, so the ritual is re-tracked under that id.
            doc_io.untrack(root, root / relative, pythonpath=_pythonpath())
            changes.append(f"untracked {relative} (was {current.model}:{current.name})")
        _track(root, RITUAL_MODEL, path, ritual_id)
        changes.append(f"tracked {relative} as {ritual_export_id(ritual_id)}")

    lifecycle_dir = root / LIFECYCLE_DIR
    lifecycle_dir.mkdir(parents=True, exist_ok=True)
    for transition in spec.transitions:
        type_name = transition.relation_type
        type_path = lifecycle_dir / f"type-{type_name}.md"
        if not type_path.exists():
            type_path.write_text(
                render_model_markdown(
                    RelationTypeDoc,
                    {
                        "title": transition.title,
                        "name": type_name,
                        "direction": "directed",
                        "cardinality": "many_to_many",
                        "axis": "HOW",
                        "source_types": [RITUAL_MODEL],
                        "target_types": [RITUAL_MODEL],
                        "condition": "",
                        "description": transition.description,
                    },
                )
                + "\n",
                encoding="utf-8",
            )
            changes.append(f"wrote {type_path.relative_to(root)}")
        if not _doc_tracked(root, RELATION_TYPE_MODEL, f"type-{type_name}"):
            _track(root, RELATION_TYPE_MODEL, type_path, f"type-{type_name}")
            changes.append(f"tracked {type_path.relative_to(root)}")

        edge_name = f"{transition.source.removeprefix('ritual-')}-{type_name}"
        edge_path = lifecycle_dir / f"{edge_name}.md"
        if not edge_path.exists():
            edge_path.write_text(
                render_model_markdown(
                    RelationDoc,
                    {
                        "title": transition.title,
                        "source_id": ritual_export_id(transition.source),
                        "target_id": ritual_export_id(transition.target),
                        "relation_type": type_name,
                        "condition": transition.condition,
                        "notes": transition.description,
                    },
                )
                + "\n",
                encoding="utf-8",
            )
            changes.append(f"wrote {edge_path.relative_to(root)}")
        if not _doc_tracked(root, RELATION_MODEL, edge_name):
            _track(root, RELATION_MODEL, edge_path, edge_name)
            changes.append(f"tracked {edge_path.relative_to(root)}")
    return changes


def lifecycle_graph_present(root: Path, spec: LifecycleSpec | None = None) -> bool:
    spec = spec or load_lifecycle_spec()
    try:
        return all(transitions_from(root, node, spec) for node in {t.source for t in spec.transitions})
    except Exception:
        return False

FILE:deskops/lifecycle_migration.py
"""Move a desk from per-task primitives to the lifecycle graph (deskops/lifecycle.py).

Desks written before the lifecycle graph carry, for every task, a routine under
desk/routines/ and 17 primitives under desk/primitives/, all tracked in the store, and
TaskDocs whose frontmatter holds `routine`, `checklists` and a `current_node` naming one of
those primitives. `deskops desk update --apply` calls `migrate_legacy_lifecycle` to:

- unregister the six retired models together with their tracked documents
  (`sldb.api.remove_model(..., untrack_documents=True)`, structuredLanguageDB >= 0.1.8), then
  delete every routine and primitive file;
- rewrite each task: drop `routine`, `checklists` and the gate facts older versions leaked
  into the frontmatter, and map `current_node` onto the ritual it stood for;
- write the lifecycle graph and refresh the store's indexes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re

import yaml

from deskops import doc_io
from deskops import lifecycle
from deskops.paths import package_pythonpath

LEGACY_MODELS = ("RoutineDoc", "ConditionDoc", "ChecklistDoc", "OperatorDoc", "EdgeDoc", "HookDoc")
LEGACY_DIRS = (Path("desk") / "routines", Path("desk") / "primitives")
LEGACY_TASK_KEYS = ("routine", "checklists", "closeout_evidence_verified", "pill_graduation_verified")
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# checklist-<task id>-<gate>-ready -> the ritual that gate belonged to
_LEGACY_NODE = re.compile(r"^checklist-.+-(execution|testing|closeout)-ready$")


class LegacyMigrationBlocked(RuntimeError):
    """The store refused a step; nothing irreversible was done for that step."""


@dataclass
class LegacyLifecycleReport:
    primitive_docs: list[Path] = field(default_factory=list)
    tasks_to_rewrite: list[Path] = field(default_factory=list)
    graph_missing: bool = False
    registered_legacy_models: list[str] = field(default_factory=list)

    @property
    def needs_migration(self) -> bool:
        return bool(self.primitive_docs or self.tasks_to_rewrite or self.graph_missing)


def legacy_node_to_ritual(node: str) -> str:
    """The lifecycle node a legacy `current_node` stood for (unchanged if not legacy)."""
    match = _LEGACY_NODE.match(node or "")
    if match:
        return f"ritual-{match.group(1)}"
    return node


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _task_needs_rewrite(path: Path) -> bool:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return False
    data, _ = parsed
    if any(key in data for key in LEGACY_TASK_KEYS):
        return True
    return legacy_node_to_ritual(str(data.get("current_node") or "")) != str(data.get("current_node") or "")


def legacy_registered_models(root: Path) -> list[str]:
    store = root / ".sldb"
    if not store.exists():
        return []
    try:
        from sldb.store.io import load_store_index

        names = {entry.name for entry in load_store_index(store).models}
    except Exception:
        return []
    return [name for name in LEGACY_MODELS if name in names]


def inspect_legacy_lifecycle(root: Path) -> LegacyLifecycleReport:
    root = root.resolve()
    report = LegacyLifecycleReport()
    for directory in LEGACY_DIRS:
        base = root / directory
        if base.exists():
            report.primitive_docs.extend(sorted(base.rglob("*.md")))
    tasks_dir = root / "desk" / "tasks"
    if tasks_dir.exists():
        report.tasks_to_rewrite = [p for p in sorted(tasks_dir.glob("task-*.md")) if _task_needs_rewrite(p)]
    report.graph_missing = (root / ".sldb").exists() and not lifecycle.lifecycle_graph_present(root)
    report.registered_legacy_models = legacy_registered_models(root)
    return report


def _rewrite_task(path: Path) -> bool:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return False
    data, text = parsed
    changed = False
    for key in LEGACY_TASK_KEYS:
        if key in data:
            data.pop(key)
            changed = True
    node = str(data.get("current_node") or "")
    mapped = legacy_node_to_ritual(node)
    if mapped != node:
        data["current_node"] = mapped
        changed = True
    if not changed:
        return False
    body = text[_FRONTMATTER.match(text).end():]
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body, encoding="utf-8")
    return True


def migrate_legacy_lifecycle(root: Path) -> list[str]:
    """Apply the migration; return one line per change. Safe to run twice."""
    root = root.resolve()
    store = root / ".sldb"
    report = inspect_legacy_lifecycle(root)
    changes: list[str] = []

    # The store lets go first: each retired model is unregistered together with its tracked
    # documents (sldb never imports the deleted class). Files are deleted only after that
    # succeeded, so a refusal leaves every file in place and a rerun picks up from there.
    pythonpath = package_pythonpath()
    if store.exists():
        for name in legacy_registered_models(root):
            try:
                doc_io.remove_model_from(root, name, pythonpath=pythonpath, untrack_documents=True)
            except Exception as exc:
                raise LegacyMigrationBlocked(
                    f"sldb could not unregister {name} with its documents: {exc}. No file was deleted. "
                    "This needs structuredLanguageDB >= 0.1.8."
                ) from exc
            changes.append(f"unregistered model {name} and untracked its documents")
    for path in report.primitive_docs:
        path.unlink()
        changes.append(f"deleted {path.relative_to(root).as_posix()}")
    for directory in LEGACY_DIRS:
        base = root / directory
        if base.exists():
            for sub in sorted((p for p in base.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
                if not any(sub.iterdir()):
                    sub.rmdir()
            if not any(base.iterdir()):
                base.rmdir()
                changes.append(f"removed {directory.as_posix()}/")

    for path in report.tasks_to_rewrite:
        if _rewrite_task(path):
            changes.append(f"rewrote {path.relative_to(root).as_posix()} (lifecycle fields)")

    if store.exists():
        for change in lifecycle.ensure_lifecycle_graph(root):
            changes.append(f"lifecycle graph: {change}")
        doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
        changes.append("updated store indexes")
    return changes

FILE:deskops/spec/workflows/task_lifecycle.yaml
id: workflow.task_lifecycle
version: "0.2"
source_files:
  implements:
    - deskops/lifecycle.py
    - deskops/workflow/next_actions.py
  exposes:
    - deskops/cli/parser.py
    - deskops/cli/main.py
  validates:
    - tests/test_cli.py
    - tests/test_lifecycle_graph.py
# The lifecycle lives in the sldb graph of each desk: every state is a tracked RitualDoc,
# every transition is a RelationDoc between two rituals whose `condition` is an sldb
# `--where` predicate on the task. `deskops init` and `deskops desk update --apply` write
# those documents into desk/lifecycle/ from the `transitions` below; `deskops advance`
# reads them back from the graph. `sets_status` is the status a task takes when the
# transition fires; a `terminal` transition closes the task (current_node: complete).
entry_node: ritual-execution
transitions:
  - relation_type: task_activates
    title: Task activates
    description: The task passes its execution gate and enters active work, under the testing ritual.
    source: ritual-execution
    target: ritual-testing
    condition: ""
    sets_status: active
  - relation_type: task_hands_to_closeout
    title: Task hands to closeout
    description: The task has validation to prove and moves to the closeout ritual.
    source: ritual-testing
    target: ritual-closeout
    condition: nonempty(validation)
    sets_status: ready_for_testing
  - relation_type: task_completes
    title: Task completes
    description: The task is ready for closeout and its references verify durable evidence; it closes.
    source: ritual-closeout
    target: ritual-closeout
    condition: status = "ready_for_testing" and has(closeout_evidence_verified)
    sets_status: closed
    terminal: true
states:
  - id: execution_gate
    current_node: ritual-execution
    phase: execution
    ritual: desk/rituals/execution.md
    purpose: Confirm initialization gate before implementation.
    next_actions:
      - Make the active task, scope, touched files, and validation targets explicit.
      - Run a fresh-context subagent review.
      - Bind matching board and task pills.
      - Start implementation only after the initialization gate is satisfied.
    advance_when:
      - Execution gate obligations are recorded or satisfied.
  - id: testing_gate
    current_node: ritual-testing
    phase: testing
    ritual: desk/rituals/testing.md
    purpose: Prove the implementation contract and bound pill guardrails.
    next_actions:
      - Confirm the handoff names the contract, touched files, and pill guardrails.
      - Add or update relevant tests.
      - Run the smallest relevant test scope, then broader validation if shared behavior changed.
    advance_when:
      - Relevant tests pass and the testing-to-closeout handoff is explicit.
  - id: closeout_gate
    current_node: ritual-closeout
    phase: closeout
    ritual: desk/rituals/closeout.md
    purpose: Close only after evidence, cleanup, and atomic commit.
    next_actions:
      - Confirm passing validation evidence and pill coverage.
      - Remove the task from the active board and delete the resolved task file when ready.
      - Untrack the store entry if tracked.
      - Create one atomic closing commit.
    advance_when:
      - Closeout ritual obligations are satisfied.
  - id: complete
    current_node: complete
    phase: complete
    purpose: No further workflow action is required for this task.
    next_actions:
      - No active next action for this task.
    advance_when: []

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/templates/`;
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# Every seed is `if_missing`: a desk that already has the file keeps its own. The `include`
# rules say which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`); the four lifecycle rituals, the Board,
# the tasks and `desk/lifecycle/` are tracked by their own paths, so no rule names them.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
include:
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:deskops/workspace.py
from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from typing import Literal

import yaml

from deskops.constants import CURRENT_DESK_FORMAT
from deskops.paths import data_path

DeskClassification = Literal["absent", "empty", "legacy", "current"]

_MODELED_DESK_TOP_LEVEL_DIRS = {
    "tasks",
    "contexts",
    "rituals",
    "atoms",
    "roles",
    "registry",
    "steps",
    "faq",
}


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths)


@dataclass
class DeskInspection:
    classification: DeskClassification
    surface_docs: list[Path]
    missing_surfaces: list[str]
    malformed_surfaces: list[str]
    tracked_surface_docs: set[Path]
    invalid_surface_docs: list[str]
    store_check_message: str | None = None


@dataclass
class DeskMigrationResult:
    adopted: list[str]
    preserved: list[str]
    still_manual: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.adopted)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def classify_desk(root: Path) -> DeskClassification:
    return inspect_desk(root).classification


def inspect_desk(root: Path) -> DeskInspection:
    desk_dir = root / "desk"
    if not desk_dir.exists():
        return DeskInspection(
            classification="absent",
            surface_docs=[],
            missing_surfaces=["desk/"],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    surface_docs = _surface_docs(desk_dir)
    if not surface_docs:
        return DeskInspection(
            classification="empty",
            surface_docs=[],
            missing_surfaces=[],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    missing_surfaces: list[str] = []
    malformed_surfaces: list[str] = []

    config_path = desk_dir / "config.json"
    if not config_path.exists():
        missing_surfaces.append("desk/config.json")
        return DeskInspection(
            classification="legacy",
            surface_docs=surface_docs,
            missing_surfaces=missing_surfaces,
            malformed_surfaces=malformed_surfaces,
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    desk_format = _read_declared_desk_format(config_path)
    if desk_format != CURRENT_DESK_FORMAT:
        malformed_surfaces.append(
            f"desk/config.json (versions.desk_format={desk_format!r}; expected {CURRENT_DESK_FORMAT!r})"
        )

    tracked_surface_docs, invalid_surface_docs, store_check_message = _inspect_surface_store_health(root, surface_docs)
    malformed_surfaces.extend(invalid_surface_docs)
    if store_check_message:
        malformed_surfaces.append(store_check_message)

    classification: DeskClassification = "legacy" if malformed_surfaces else "current"
    return DeskInspection(
        classification=classification,
        surface_docs=surface_docs,
        missing_surfaces=missing_surfaces,
        malformed_surfaces=malformed_surfaces,
        tracked_surface_docs=tracked_surface_docs,
        invalid_surface_docs=invalid_surface_docs,
        store_check_message=store_check_message,
    )


def migrate_desk(root: Path) -> DeskMigrationResult:
    before = inspect_desk(root)
    adopted: list[str] = []
    preserved = [str(path.relative_to(root)) for path in before.surface_docs]
    still_manual: list[str] = []

    result = seed_desk(root)
    adopted.extend(str(path.relative_to(root)) for path in result.created_paths)

    if _write_or_patch_config(root) == "updated":
        adopted.append("desk/config.json (patched desk_format)")

    after = inspect_desk(root)
    tracked_after = after.tracked_surface_docs if after.classification in {"legacy", "current"} else set()
    for path in after.surface_docs:
        rel = str(path.relative_to(root))
        if path not in tracked_after:
            still_manual.append(f"{rel} (preserved; manual model conversion or sldb docs track required)")

    for invalid in after.invalid_surface_docs:
        still_manual.append(f"{invalid} (manual SLDB/model repair required)")

    if after.store_check_message:
        still_manual.append(f"{after.store_check_message} (manual SLDB health follow-up)")

    return DeskMigrationResult(
        adopted=_dedupe(adopted),
        preserved=_dedupe(preserved),
        still_manual=_dedupe(still_manual),
    )


#: The one placeholder the desk templates use (CC36, e3): replaced with the project directory's
#: name by ``str.replace``; the JSON and YAML templates have braces of their own.
DESK_NAME_PLACEHOLDER = "{desk_name}"

#: The declaration of the desk a repository gets, and the templates its ``file:`` seeds name.
DESK_DECLARATION_PATH = data_path("data", "desk_declaration.yaml")
DESK_TEMPLATES_PATH = data_path("data", "templates")

#: The document seed whose ``system_prompt`` is code (``deskops.services.review.SYSTEM``), not
#: declaration data (CC36, f3).
_REVIEW_RUNTIME_SEED = "runtime-pi-deepseek-flash"


def desk_declaration(name: str) -> Any:
    """The desk declaration (``deskops/data/desk_declaration.yaml``) for a desk called ``name``.

    The ``folders`` and ``include`` rules are the file's; every seed comes back rendered as
    ``text``: ``file:`` templates read from ``deskops/data/templates/`` and ``document:`` payloads
    rendered through their deskops model, both with ``{desk_name}`` replaced. The bytes are the
    ones ``deskops init`` always wrote, and sldb only has to write them: its own ``document``
    seed resolves the model from the store, which ``desk install`` and the first desk operation
    do not have yet.
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration

    declared = StoreDeclaration.model_validate(yaml.safe_load(DESK_DECLARATION_PATH.read_text(encoding="utf-8")))
    seeds = [Seed(path=seed.path, mode=seed.mode, text=_seed_text(seed, name)) for seed in declared.seeds]
    return StoreDeclaration(folders=declared.folders, seeds=seeds, include=declared.include)


def _seed_text(seed: Any, name: str) -> str:
    if seed.text is not None:
        return seed.text.replace(DESK_NAME_PLACEHOLDER, name)
    if seed.file is not None:
        template = (DESK_TEMPLATES_PATH / seed.file).read_text(encoding="utf-8")
        return template.replace(DESK_NAME_PLACEHOLDER, name)
    document = seed.document
    payload = _replace_desk_name(document["payload"], name)
    if document["name"] == _REVIEW_RUNTIME_SEED:
        from deskops.services.review import SYSTEM

        payload["system_prompt"] = SYSTEM
    return _render_document(document["model"], payload)


def _render_document(model_name: str, payload: dict[str, Any]) -> str:
    """A document seed rendered by its model, as ``deskops init`` rendered the Board."""
    from sldb.runtime.validation import render_model_markdown

    import deskops.models as models

    return render_model_markdown(getattr(models, model_name), payload) + "\n"


def _replace_desk_name(value: Any, name: str) -> Any:
    if isinstance(value, str):
        return value.replace(DESK_NAME_PLACEHOLDER, name)
    if isinstance(value, list):
        return [_replace_desk_name(item, name) for item in value]
    if isinstance(value, dict):
        return {key: _replace_desk_name(item, name) for key, item in value.items()}
    return value


def seed_desk(target_path: Path, *, apply: bool = True) -> DeskScaffoldResult:
    """Create the declared desk folders and seed files that are missing (``sldb.api.scaffold_store``).

    Every seed is ``if_missing``, so a desk that exists keeps its files. ``created_paths`` are the
    absolute paths of what was created, folders first and then seeds in declaration order; with
    ``apply=False`` nothing is written and they are what a run would create.
    """
    from sldb.api import scaffold_store

    report = scaffold_store(target_path, declaration=desk_declaration(target_path.name), apply=apply)
    return DeskScaffoldResult(created_paths=[target_path / relative for relative in report.created])


def desk_seed_text(name: str, path: str) -> str:
    """The text the desk seed at ``path`` (project-relative) carries for a desk called ``name``."""
    for seed in desk_declaration(name).seeds:
        if seed.path == path:
            return seed.text
    raise KeyError(path)


def default_ritual_text(ritual_id: str, name: str) -> str:
    """The ritual `deskops init` writes for one lifecycle state."""
    return desk_seed_text(name, f"desk/rituals/{ritual_id.removeprefix('ritual-')}.md")


def pending_desk_includes(root: Path) -> list[tuple[str, str]]:
    """``(model, path)`` of each desk document the declared includes name and the store does not
    track yet: what ``apply_desk_includes`` would track (every declared file when there is no store)."""
    from sldb.api.stores.declared_files import declared_files
    from sldb.api.stores.declared_includes import tracked_rows

    root = root.resolve()
    store_dir = root / ".sldb"
    tracked = set(tracked_rows(store_dir, root)) if store_dir.exists() else set()
    return [
        (model, path)
        for model, path, name in declared_files(root, desk_declaration(root.name))
        if (model, path, name) not in tracked and (root / path).is_file()
    ]


def apply_desk_includes(root: Path) -> list[str]:
    """Track every pending declared desk document under its declared model; the paths tracked."""
    from sldb.api.stores.apply_declaration import apply_includes

    root = root.resolve()
    return apply_includes(root / ".sldb", root, desk_declaration(root.name))


def _write_or_patch_config(root: Path) -> str | None:
    """Patch an existing ``desk/config.json`` to the current desk format and identity.

    The file itself is a seed, written by ``seed_desk`` before this runs; a missing one is left
    alone (this is migration, not scaffold).
    """
    config_path = root / "desk" / "config.json"
    if not config_path.exists():
        return None

    data: dict[str, object]
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    data = dict(payload)
    versions = data.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    versions = dict(versions)
    changed = versions.get("desk_format") != CURRENT_DESK_FORMAT
    versions["desk_format"] = CURRENT_DESK_FORMAT
    data["versions"] = versions
    data.setdefault("project_identity", root.name)

    rendered = json.dumps(data, indent=2) + "\n"
    if config_path.read_text(encoding="utf-8") != rendered:
        config_path.write_text(rendered, encoding="utf-8")
        return "updated"
    return None


def desk_markdown_docs(desk_dir: Path) -> list[Path]:
    return sorted(path for path in desk_dir.rglob("*.md") if path.is_file())


def desk_doc_is_modeled_by_sldb(root: Path, doc_path: Path) -> bool:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return False

    parts = relative.parts
    if not parts:
        return False

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return False

    return top_level in _MODELED_DESK_TOP_LEVEL_DIRS


def desk_doc_unmodeled_reason(root: Path, doc_path: Path) -> str | None:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return None

    parts = relative.parts
    if not parts:
        return None

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return f"desk/{relative.name} is a top-level desk note intentionally not SLDB-modeled"
    if top_level not in _MODELED_DESK_TOP_LEVEL_DIRS:
        return f"desk/{top_level}/** is intentionally not SLDB-modeled"
    return None


def modeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if desk_doc_is_modeled_by_sldb(root, path)]


def unmodeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if not desk_doc_is_modeled_by_sldb(root, path)]


def _surface_docs(desk_dir: Path) -> list[Path]:
    docs: list[Path] = []
    board = desk_dir / "tasks" / "Board.md"
    if board.exists():
        docs.append(board)

    tasks_dir = desk_dir / "tasks"
    if tasks_dir.exists():
        docs.extend(sorted(path for path in tasks_dir.glob("*.md") if path.name != "Board.md"))

    contexts_dir = desk_dir / "contexts"
    if contexts_dir.exists():
        docs.extend(sorted(path for path in contexts_dir.glob("*.md")))
    return docs


def _read_declared_desk_format(config_path: Path) -> str | None:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    versions = payload.get("versions")
    if not isinstance(versions, dict):
        return None
    desk_format = versions.get("desk_format")
    return desk_format if isinstance(desk_format, str) else None


def _inspect_surface_store_health(root: Path, surface_docs: list[Path]) -> tuple[set[Path], list[str], str | None]:
    store_path = root / ".sldb"
    if not store_path.exists():
        return set(), [], None

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(store_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    tracked: set[Path] = set()
    invalid: list[str] = []
    tracked_surface_set = {path.resolve() for path in surface_docs}

    payload: dict[str, object] | None = None
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout)
        except json.JSONDecodeError:
            return tracked, invalid, "sldb stores check returned unreadable JSON"
        if isinstance(loaded, dict):
            payload = loaded

    if payload is not None:
        for model in payload.get("models", []):
            if not isinstance(model, dict):
                continue
            for doc in model.get("documents", []):
                if not isinstance(doc, dict):
                    continue
                doc_path = doc.get("path")
                if not isinstance(doc_path, str):
                    continue
                absolute = (root / doc_path).resolve()
                if absolute not in tracked_surface_set:
                    continue
                tracked.add(absolute)
                # An edited, re-contracted or moved document is an alert, not a malformed
                # surface: it does not make the desk legacy (see deskops.doctor_findings).
                note = doc.get("note")
                if note not in _NOT_MALFORMED_NOTES:
                    invalid.append(f"{doc_path} ({note})")

    # `stores check` exits 1 on a store that only moved; its JSON is the verdict, the exit
    # code only matters when there is no JSON to read.
    if result.returncode != 0 and payload is None:
        stderr = result.stderr.strip().splitlines()
        if stderr:
            return tracked, invalid, f"sldb stores check failed: {stderr[0]}"
        return tracked, invalid, "sldb stores check failed"

    return tracked, invalid, None


_NOT_MALFORMED_NOTES = frozenset({"ok", "benign_mutation", "data_mutation", "contract_mutation", "missing"})


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


# ---------------------------------------------------------------------------
# Desk-local task type registration and legacy task_type migration (GC01).
#
# A desk adds its own task types as `desk/models/*.py` subclasses (DC7); `desk update
# --apply` registers them with `sldb add_model` and `pythonpath` = the desk root. Legacy
# `task_type` strings are then re-tracked under the model their canonical type names
# (TaskDoc precisión 4).

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

#: The legacy ``task_type`` values that map onto a known type (the same map the migration
#: uses). Anything else is an unknown legacy value and migrates to ``task.code``.
LEGACY_TASK_TYPE_KEYS = frozenset({"code", "implementation", "test", "docs", "spec", "design", "external", ""})


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _frontmatter_task_type(path: Path) -> str:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return ""
    return str(parsed[0].get("task_type") or "").strip()


def discover_local_task_type_models(desk_dir: Path) -> list[tuple[str, str]]:
    """``(model_ref, class_name)`` for every ``TaskDoc`` subclass defined in ``desk/models/*.py``."""
    from deskops.models import TaskDoc

    models_dir = desk_dir / "models"
    if not models_dir.is_dir():
        return []
    desk_root = str(desk_dir.resolve())
    added = desk_root not in sys.path
    if added:
        sys.path.insert(0, desk_root)
    found: list[tuple[str, str]] = []
    try:
        for path in sorted(models_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            module_name = f"models.{path.stem}"
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            for name in dir(module):
                obj = getattr(module, name, None)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, TaskDoc)
                    and obj is not TaskDoc
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    found.append((f"{module_name}:{name}", name))
    finally:
        if added:
            sys.path.remove(desk_root)
    return found


def pending_local_task_type_models(root: Path) -> list[str]:
    """Desk-local task type models that are not registered yet, as readable labels."""
    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    try:
        from deskops.bootstrap import SLDBBootstrap

        registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    except Exception:
        registered = set()
    return [
        f"{module_ref} ({class_name})"
        for module_ref, class_name in discover_local_task_type_models(root / "desk")
        if class_name not in registered
    ]


def register_local_task_type_models(root: Path) -> list[str]:
    """Register unregistered desk-local task types; one change line per registration."""
    from deskops import doc_io
    from deskops.bootstrap import SLDBBootstrap

    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for module_ref, class_name in discover_local_task_type_models(root / "desk"):
        if class_name in registered:
            continue
        try:
            doc_io.register_model(root, module_ref, pythonpath=pythonpath)
        except Exception as exc:
            raise RuntimeError(f"could not register desk-local task type {class_name}: {exc}") from exc
        changes.append(f"registered {class_name} from {module_ref}")
    return changes


def _task_type_migration_plan(root: Path) -> list[dict]:
    """Per-task migration plan for ``desk/tasks``, including the canonical type and target model."""
    from deskops.models.task_types import LEGACY_TASK_TYPE_MAP
    from deskops.models.task_types import canonical_task_type_name
    from deskops.operations import DeskopsOperations

    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    operations = DeskopsOperations(root)
    registry = operations.registered_task_types()
    fallback = registry.get("task.code")
    plan: list[dict] = []
    for path in sorted(tasks_dir.glob("*.md")):
        if path.name == "Board.md" or path.name.startswith("board-"):
            continue
        raw = _frontmatter_task_type(path)
        canonical = raw if raw in registry else canonical_task_type_name(raw)
        target = registry.get(canonical) or fallback
        plan.append(
            {
                "path": path,
                "raw": raw,
                "canonical": canonical,
                "target_cls": target,
                "target_name": target.__name__ if target is not None else "TaskDoc",
                "unknown": bool(raw) and raw not in registry and raw not in LEGACY_TASK_TYPE_MAP,
            }
        )
    return plan


def pending_task_type_migration(root: Path) -> list[str]:
    """The change lines ``migrate_task_types`` would apply, so the dry run can list them."""
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    lines: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        lines.append(_task_type_migration_line(item, rel))
    return lines


def _task_type_migration_line(item: dict, rel: str) -> str:
    if item["unknown"]:
        return (
            f"unknown legacy task_type {item['raw']!r} in {rel}: migrated to {item['canonical']} "
            f"(tracked as {item['target_name']})"
        )
    return (
        f"migrated {rel}: task_type {item['raw']!r} -> {item['canonical']!r} "
        f"(tracked as {item['target_name']})"
    )


def _rewrite_task_type(path: Path, canonical: str) -> None:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return
    data, text = parsed
    data["task_type"] = canonical
    body = text[_FRONTMATTER_RE.match(text).end():]
    path.write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body,
        encoding="utf-8",
    )


def migrate_task_types(root: Path) -> list[str]:
    """Rewrite legacy ``task_type`` values and re-track each task under its type's model.

    Idempotent: a second run changes nothing. ``closeout_evidence`` is preserved because the
    frontmatter rewrite only touches ``task_type``.
    """
    from deskops import doc_io
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        if needs_rewrite:
            _rewrite_task_type(path, item["canonical"])
        if store_dir.exists() and item["target_cls"] is not None:
            if tracked_model is not None:
                try:
                    doc_io.untrack(root, path)
                except Exception:
                    pass
            doc_io.track(root, path, item["target_cls"], name=path.stem, pythonpath=pythonpath, force=True)
        changes.append(_task_type_migration_line(item, rel))
    return changes

FILE:deskops/services/tasks.py
"""Task lifecycle service: create, list, show, advance, next, and the task type registry.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Document storage (read/write/track,
selector resolution, the task payload with its inherited context) is
``deskops.doc_access``; the lifecycle graph is ``deskops.lifecycle``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops import doc_io
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import PillDoc
from deskops.models import TaskDoc
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.models.task_types import canonical_task_type_name
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path


def registered_task_types(root: Path) -> dict[str, type[Any]]:
    """task_type name -> model class: the factory types plus desk-local types in the store.

    A desk adds its own types as ``desk/models/*.py`` subclasses; ``desk update --apply``
    registers them with ``pythonpath`` = the desk root. Factory types are importable directly
    and are merged in first, so local modules never shadow them.
    """
    registry: dict[str, type[Any]] = dict(TASK_TYPE_MODELS)
    store_dir = root / ".sldb"
    if store_dir.exists():
        try:
            from sldb.api.model_registry.model_reference import resolve_model_ref

            from deskops.bootstrap import SLDBBootstrap

            entries = SLDBBootstrap()._registered_model_entries(store_dir)
            pythonpath = str(doc_access.desk_root(root))
            for name, entry in entries.items():
                if name in registry:
                    continue
                model_ref = getattr(entry, "model_ref", "") or ""
                if not model_ref:
                    continue
                try:
                    cls = resolve_model_ref(model_ref, pythonpath=pythonpath)
                except Exception:
                    continue
                if not isinstance(cls, type) or not issubclass(cls, TaskDoc):
                    continue
                field = cls.model_fields.get("task_type")
                default = getattr(field, "default", None)
                if default not in (None, ""):
                    registry[str(default)] = cls
        except Exception:
            pass
    return registry


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger
        self._task_type_registry: dict[str, type[Any]] | None = None

    def registered_task_types(self) -> dict[str, type[Any]]:
        """The task type registry of this desk, read once per service instance."""
        if self._task_type_registry is None:
            self._task_type_registry = registered_task_types(self.root)
        return self._task_type_registry

    # ---------------------------------------------------------------- create
    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        doc_access.ensure_workspace(self.root)
        # A task's closeout evidence is declared by its type, not written into the task. The
        # task is stored under its type's model so `model <= TaskCodeDoc` finds it.
        raw_task_type = str(raw_payload.get("task_type") or "").strip()
        registry = self.registered_task_types()
        task_type = raw_task_type if raw_task_type in registry else canonical_task_type_name(raw_task_type)
        type_model = registry.get(task_type) or registry.get("task.code") or TaskDoc
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec({**raw_payload, "task_type": task_type}, entry_node=spec.entry_node)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_io.DocTransaction(self.root):
            doc_access.write_new_doc(self.root, task_path, type_model, compiled.task_payload)
            doc_access.track_created_document(self.root, type_model, task_path, task_id)
            self._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[doc_access.DocumentRecord, str, bool]:
        doc_access.ensure_workspace(self.root)
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        pill_path = doc_access.resolve_artifact_selector(self.root, "artifact.pill", self.desk_root / "contexts", pill_selector)
        task_payload = doc_access.read_doc(task_path, TaskDoc)
        doc_access.read_doc(pill_path, PillDoc)
        pill_ref = str(pill_path.relative_to(self.root))
        pills = list(task_payload.get("pills") or [])
        record = doc_access.DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path)
        if pill_ref in pills:
            return record, pill_ref, False
        task_payload["pills"] = [*pills, pill_ref]
        doc_access.write_doc(self.root, task_path, TaskDoc, task_payload)
        return record, pill_ref, True

    # ---------------------------------------------------------------- read
    def list_tasks(self) -> list[Task]:
        task_dir = self.desk_root / "tasks"
        if not task_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            try:
                tasks.append(doc_access.load_task(self.root, path.stem))
            except Exception as e:
                print(f"Warning: Failed to load task {path}: {e}", file=sys.stderr)
        return tasks

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        """The task and the lifecycle transitions leaving its current node, each with
        whether its condition holds now (empty when the graph is missing or the task is
        complete)."""
        try:
            task = doc_access.load_task(self.root, task_id)
        except FileNotFoundError:
            return None, []
        return task, self._lifecycle_gates(task)

    def _lifecycle_gates(self, task: Task) -> list[dict[str, Any]]:
        if not task.current_node or task.current_node == lifecycle.COMPLETE:
            return []
        try:
            transitions = lifecycle.transitions_from(self.root, task.current_node, snapshot=self._ops.snapshot)
        except Exception:
            return []
        payload = doc_access.read_doc(doc_access.resolve_glob(self.root, self.desk_root / "tasks", task.id), TaskDoc)
        self.add_closeout_facts(payload)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": lifecycle.condition_holds(t.condition, payload),
            }
            for t in transitions
        ]

    def add_closeout_facts(self, payload: dict[str, Any]) -> None:
        """Facts the lifecycle conditions test with has(): present only when they hold."""
        closure = self._ops.closure
        for key, holds in (
            ("closeout_evidence_verified", closure.has_verified_task_closeout_evidence(payload)),
            ("pill_graduation_verified", closure.has_verified_task_pill_graduation(payload)),
        ):
            if holds:
                payload[key] = "verified"
            else:
                payload.pop(key, None)

    def render_next_action_diagram(self) -> str:
        return render_workflow_mermaid(lifecycle.load_lifecycle_spec())

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_ref = str(board_path.relative_to(self.root))
        if not task_selector:
            task_refs = list(doc_access.read_doc(board_path, BoardDoc).get("tasks") or [])
            if not task_refs:
                return {
                    "kind": "no_board_task",
                    "board": board_ref,
                    "suggested_commands": [
                        "deskops list tasks --root .",
                        "deskops promote inbox-to-drawer-task <selector> --root .",
                        'deskops add task --root . --title "..." ...',
                    ],
                }
            if len(task_refs) > 1:
                tasks = []
                for task_ref in task_refs:
                    path = self.root / str(task_ref)
                    payload = doc_access.read_doc(path, TaskDoc)
                    tasks.append(
                        {
                            "id": str(payload.get("id") or path.stem),
                            "status": str(payload.get("status") or ""),
                            "title": str(payload.get("title") or ""),
                        }
                    )
                return {
                    "kind": "multiple_board_tasks",
                    "board": board_ref,
                    "tasks": tasks,
                    "suggested_commands": [
                        "deskops next <task-id> --root .",
                        "deskops list tasks --root .",
                    ],
                }
        task_path = self._next_task_path(task_selector, board_path)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        spec = lifecycle.load_lifecycle_spec()
        state = match_workflow_state(spec, str(payload.get("current_node") or ""))
        pills = list(dict.fromkeys([*self._board_pills(board_path), *list(payload.get("effective_pills") or payload.get("pills") or [])]))
        sources = {
            "task": str(task_path.relative_to(self.root)),
            "board": str(board_path.relative_to(self.root)),
            "workflow": "deskops/spec/workflows/task_lifecycle.yaml",
        }
        why = [
            "task selected by explicit selector"
            if task_selector
            else "task selected from the single board route",
            f"current_node {payload.get('current_node', '')} matched workflow state {state['id']} in {sources['workflow']}",
            "pills merged from desk/tasks/Board.md and the task",
            f"source task: {sources['task']}",
            f"source board: {sources['board']}",
            f"source workflow: {sources['workflow']}",
        ]
        return {
            "task": {
                "id": payload["id"],
                "title": payload["title"],
                "status": payload["status"],
                "current_node": payload.get("current_node", ""),
                "task_type": payload.get("task_type", ""),
                "inherits_from": list(payload.get("inherits_from") or []),
            },
            "phase": state["phase"],
            "ritual": state.get("ritual", ""),
            "pills": pills,
            "next_actions": list(state.get("next_actions") or []),
            "advance_when": list(state.get("advance_when") or []),
            "why": why,
            "sources": sources,
        }

    # ---------------------------------------------------------------- advance
    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = doc_access.read_doc(task_path, TaskDoc)

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        self.add_closeout_facts(payload)
        result = lifecycle.advance(self.root, payload)
        for key in ("closeout_evidence_verified", "pill_graduation_verified"):
            payload.pop(key, None)
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return doc_access.hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = doc_access.hydrate_task(payload)
        if result.progressed:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    @staticmethod
    def _closure_required(task_id: str, payload: dict[str, Any]) -> TransitionResult:
        node = str(payload.get("current_node") or "")
        status = str(payload.get("status") or "")
        message = (
            f"Task {task_id} closes with 'deskops closeout commit --task {task_id} "
            f"--run-dir <runs/subagents/dir>' or 'deskops closeout commit --task {task_id} "
            f"--no-run --reason <why>'."
        )
        return TransitionResult(node, status, False, True, message)

    # ---------------------------------------------------------------- paths
    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]

FILE:deskops/workflow/next_actions.py
from __future__ import annotations

from typing import Any

from deskops.lifecycle import COMPLETE
from deskops.lifecycle import LifecycleSpec
from deskops.lifecycle import SPEC_PATH


def match_workflow_state(spec: LifecycleSpec, current_node: str) -> dict[str, Any]:
    """The state of ``deskops/spec/workflows/task_lifecycle.yaml`` whose ``current_node``
    is the task's; an empty node matches the first state."""
    node = current_node or ""
    for state in spec.states:
        if state.get("current_node") == node:
            return state
    if not node:
        return _first_state(spec)
    raise ValueError(f"No workflow state in {SPEC_PATH} matches current node '{current_node}'")


def render_workflow_mermaid(spec: LifecycleSpec) -> str:
    """Mermaid of the lifecycle graph: one node per state, one arrow per transition,
    labelled with its relation type and condition."""
    states = list(spec.states)
    by_node = {str(state.get("current_node")): str(state["id"]) for state in states}
    lines = ["flowchart TD"]
    for state in states:
        state_id = str(state["id"])
        label = str(state.get("phase") or state_id).replace('"', "'")
        lines.append(f'    {state_id}["{label}"]')
    for transition in spec.transitions:
        source = by_node.get(transition.source, transition.source)
        target_node = COMPLETE if transition.terminal else transition.target
        target = by_node.get(target_node, target_node)
        label = transition.relation_type
        if transition.condition:
            label += f": {transition.condition}"
        lines.append(f'    {source} -->|"{label.replace(chr(34), chr(39))}"| {target}')
    return "\n".join(lines)


def _first_state(spec: LifecycleSpec) -> dict[str, Any]:
    if not spec.states:
        raise ValueError(f"Workflow spec has no states: {SPEC_PATH}")
    return spec.states[0]

FILE:deskops/cli/commands/desk.py
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from deskops import doc_io
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import migrate_desk
from deskops.workspace import migrate_task_types
from deskops.workspace import apply_desk_includes
from deskops.workspace import pending_local_task_type_models
from deskops.workspace import pending_task_type_migration
from deskops.workspace import pending_desk_includes
from deskops.workspace import register_local_task_type_models
from deskops.workspace import seed_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def moved_model_contracts(root: Path, entries: dict[str, Any]) -> list[str]:
    """Registered deskops models whose store contract no longer matches this checkout."""
    from sldb.store.hashing import hash_model_contract
    from sldb.store.io import load_models_index

    moved: list[str] = []
    for name, entry in sorted(entries.items()):
        model_ref = getattr(entry, "model_ref", "") or ""
        model_type = getattr(models, name, None)
        models_index = getattr(entry, "models_index", None)
        if not model_ref.startswith("deskops.models:") or model_type is None or not models_index:
            continue
        try:
            stored = load_models_index(root / models_index).contract_hash
        except Exception:
            continue
        if stored != hash_model_contract(model_type):
            moved.append(name)
    return moved


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        doc_io.register_model(root, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        doc_io.track(root, document.path, FAQ_MODEL, name=document.name, pythonpath=pythonpath)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    doc_io.remove_model_from(
        root, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True
    )
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "replace":
            return self.replace(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def replace(self, args: Any) -> int:
        from deskops.services.replace import replace_text

        result = replace_text(
            Path(args.root),
            args.path,
            args.old,
            args.new,
            count=args.count,
        )
        print(f"Replaced {result.replacements} occurrence(s) in {result.path}")
        return 0

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = seed_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import ensure_lifecycle_graph

            for change in ensure_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"

        from deskops.lifecycle_migration import inspect_legacy_lifecycle
        from deskops.lifecycle_migration import migrate_legacy_lifecycle

        legacy = inspect_legacy_lifecycle(root) if desk_dir.exists() else None
        legacy_pending = bool(legacy and (legacy.needs_migration or legacy.registered_legacy_models))
        if legacy_pending and apply:
            from deskops.lifecycle_migration import LegacyMigrationBlocked

            print("Migrating the task lifecycle to the desk's sldb graph...")
            if store_dir.exists() and "RitualDoc" not in SLDBBootstrap()._registered_model_entries(store_dir):
                # The lifecycle states are RitualDocs; a store that never registered the
                # model (an early desk) gets the deskops models before the graph is written.
                SLDBBootstrap().init_local_store(root)
                print("- registered the deskops models the lifecycle graph needs")
            try:
                for change in migrate_legacy_lifecycle(root):
                    print(f"- {change}")
            except LegacyMigrationBlocked as exc:
                print(f"Error: {exc}")
                return 1
            legacy_pending = False

        inspection = inspect_desk(root)

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "reviews").exists():
                missing_desk_files.append("desk/reviews/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")
            if not (desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md").exists():
                missing_desk_files.append("desk/runtimes/runtime-pi-deepseek-flash.md")

        bootstrap = SLDBBootstrap()
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        moved_contracts = (
            moved_model_contracts(root, registered_entries) if store_dir.exists() else []
        )
        if moved_contracts and apply:
            pythonpath = package_pythonpath()
            for model_name in moved_contracts:
                print(f"Updating the {model_name} contract...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "sldb",
                        "models",
                        "update",
                        model_name,
                        "--store",
                        str(store_dir),
                        "--pythonpath",
                        pythonpath,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip()
                    print(f"Error: could not update the {model_name} contract: {detail}")
                    return 1
                print(f"Updated {model_name} contract.")
            registered_entries = bootstrap._registered_model_entries(store_dir)
            moved_contracts = moved_model_contracts(root, registered_entries)

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None:
                if result.returncode != 0:
                    raise DeskopsEnvironmentError(
                        f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}"
                    )
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
            for model in payload.get("models", []):
                for doc in model.get("documents", []):
                    doc_path = doc.get("path")
                    if not doc_path:
                        continue
                    if doc.get("note") not in ("ok",):
                        invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                        if doc.get("note") == "missing":
                            missing_docs.append(doc.get("name") or Path(doc_path).stem)

        # The desk documents the package's declared includes name and the store does not
        # track yet, each with its declared model (deskops/data/desk_declaration.yaml).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() else []

        pending_local_types = pending_local_task_type_models(root)
        pending_migration = pending_task_type_migration(root)

        if not legacy_pending and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not moved_contracts and not pending_local_types and not pending_migration:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if moved_contracts:
            print(f"- Moved model contracts: {', '.join(moved_contracts)}")
        if legacy_pending and legacy is not None:
            print(
                "- Legacy task lifecycle: "
                f"{len(legacy.primitive_docs)} routine/primitive documents to delete, "
                f"{len(legacy.tasks_to_rewrite)} tasks to rewrite, "
                f"lifecycle graph {'missing' if legacy.graph_missing else 'present'}, "
                f"retired models still registered: {', '.join(legacy.registered_legacy_models) or 'none'}"
            )
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
        if untracked_docs:
            print(f"- Untracked desk documents: {', '.join(path for _model, path in untracked_docs)}")
        if pending_local_types:
            print(f"- Unregistered desk-local task types: {', '.join(pending_local_types)}")
        if pending_migration:
            print(f"- Pending task type migration: {len(pending_migration)} task(s)")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")

        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")
        
        if missing_desk_files:
            seed_desk(root)
            print("Scaffolded missing desk structure.")

        if unregistered_models or copied_models:
            bootstrap.init_local_store(root)
            print("Registered missing models and converted copied deskops models.")

        try:
            for change in register_local_task_type_models(root):
                print(f"- {change}")
        except Exception as exc:
            print(f"Error: {exc}")
            return 1
        for change in migrate_task_types(root):
            print(f"- {change}")

        if untracked_docs:
            declared_models = {path: model_name for model_name, path in untracked_docs}
            try:
                tracked_paths = apply_desk_includes(root)
            except Exception as exc:
                print(f"Error: could not track the declared desk documents: {exc}")
                return 1
            for path in tracked_paths:
                print(f"Tracked {path} as {declared_models.get(path, 'its declared model')}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    doc_io.untrack(root, name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs:
            pythonpath = package_pythonpath()
            doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
            print("Updated store derived indexes.")

        if store_dir.exists():
            from deskops.lifecycle import ensure_lifecycle_graph
            from deskops.lifecycle import lifecycle_graph_present

            if not lifecycle_graph_present(root):
                for change in ensure_lifecycle_graph(root):
                    print(f"Lifecycle graph: {change}")

        return 0

FILE:deskops/cli/commands/core.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import seed_desk


class AboutCLI:
    def run(self, args: Any) -> int:
        # Resolved through the CLI module so a patched entrypoint stays visible.
        from deskops.cli import main as main_module

        return main_module.print_about()


class BootstrapCLI:
    def run(self, args: Any) -> int:
        return SLDBBootstrap().ensure_machine_ready()


class InitCLI:
    def run(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        bootstrap = SLDBBootstrap()
        ready = bootstrap.ensure_machine_ready()
        if ready != 0:
            return ready

        local_store = bootstrap.init_local_store(target_path)
        if local_store != 0:
            return local_store

        result = seed_desk(target_path)
        if result.wrote_anything:
            print(f"Scaffolded desk at {target_path / 'desk'}.")
            for path in result.created_paths:
                print(f"Wrote {path}")
        else:
            print(f"Desk already exists at {target_path / 'desk'}.")
        from deskops.lifecycle import ensure_lifecycle_graph

        for change in ensure_lifecycle_graph(target_path):
            print(f"Lifecycle graph: {change}")
        print("Initialization complete.")
        return 0

FILE:docs/workflow-policy-reference.md
---
atoms:
- id: atom-cheap-zero-context-reviews-test-the-brief-recursively
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-pills-carry-transitional-task-knowledge
  role: documents
- id: atom-pills-are-reusable-across-tasks
  role: documents
- id: atom-pills-end-as-atoms-docs-or-deletion
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-phase-closeout-reconciles-pills-and-next-work
  role: documents
- id: atom-tasks-enable-zero-context-subagents
  role: documents
- id: atom-task-board-phases
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# Workflow Policy Reference

Source atoms are declared in the YAML frontmatter.

This reference summarizes the current workflow policy used by `deskops`.

> **No task is complete without the closeout evidence it declared at creation and its own closing commit. No phase is complete without integration validation and pill reconciliation.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items
- [Context Review Ritual](../desk/rituals/context-review.md) - Cheap recursive brief comprehension
- [Phase Ritual](../desk/rituals/phase.md) - Dependency-layer execution and closeout

---

## Core Model

### Tasks

A task is the atomic workflow unit.

- One coherent deliverable.
- May depend on other tasks.
- Executes in a fresh subagent context.
- Declares how it closes by choosing a task type (`deskops add task --task-type`); the type declares its closeout evidence and its activation receipts, and closes only after exactly that evidence verifies, with its own atomic closing commit. `--evidence` only adds kinds to the type's floor, never removes one the type requires.

#### Task types

A task type is a model: a `TaskDoc` subclass registered in the store. `model <= <Tipo>` names the type's family (including its subtypes); a subtype inherits the gates of its ancestors and can only add, never remove.

| Type | Extends | Activation receipts | Closeout evidence |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle` | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight` | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` | `tests` + `commit` + `atom\|materialization` |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` | `task.code` + `goldens` |
| `task.decision` | `TaskDoc` | `owner` | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | (never executes; activates when children close) | `children` + `commit` |
| `task.external` | `TaskDoc` | `preflight` | `external` (URL) |

`atom|materialization` is one gate with two alternatives. `commit` means a commit reachable from `HEAD`. A desk adds its own subtypes in `desk/models/*.py`; `deskops desk update --apply` registers them and migrates legacy `task_type` strings (`code`/`implementation`/`test` → `task.code`; `docs`/`spec`/`design` → `task.docs`; `external` → `task.external`; empty → `task.code`).

### Phases

Tasks form an execution dependency graph.

A **phase** is one horizontal dependency layer in that graph:

- task prerequisites are already satisfied
- tasks are ready at the same time
- planned operational changes do not overlap
- tasks may run in parallel when the environment supports it

A phase has execution meaning, not business meaning. It is the workflow unit above individual tasks and below the whole board.

### Boards

The board is the routing surface for active work.

- It names the active tasks.
- It routes board-wide pills and rituals.
- Its current ready dependency layer is the current phase.

---

## Cheap Context Review and Fresh Subagents

Before promoting or executing a draft, plan, package or leaf, run the [context-review ritual](../desk/rituals/context-review.md). It tests the quality of the written question with a cheap reviewer: faithful reformulation, explicit ambiguities and a detailed dry-run of proposed readings, changes, validation and dependencies. The reviewer names intended commands without executing them or editing sources.

Supply the exact versioned brief and only necessary explicit references. Use a new ephemeral process for every attempt, without chat history, earlier reviews, oral fixes, persistent memory, automatic context/skills or tools. Record the chosen cheap provider/model/profile and reason; an expert cannot rescue a failed cheap comprehension gate. The ritual specifies the verified Pi isolation profile and per-node evidence layout.

The coordinator compares understanding with intent, corrects the written brief and recursively decomposes large nodes into children and explicit edges. Review root, packages, every leaf and dependency interfaces before selecting ready leaves. A root-only review does not cover descendants. Unresolved ambiguity blocks execution. Changed input or a changed dependency contract invalidates affected reviews; retries use a new process. Technical transport/quota failures are recorded separately from ambiguity.

Before Executor dispatch, preserve two distinct cheap roles: TaskDoc-only preflight (also saved in `runs/subagents/<run-dir>/preflight.md`) and cold-bundle coverage. The explicit execution bundle contains task, board-routed instructions/rituals, bound pills, linked atoms/files and validation targets. Neither review executes implementation. Expert council review, Executor work, independent Tester validation and human product approval remain separate gates; a word such as APTO or structural PASS grants none of them.

Evidence lives at `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`: exact input bytes/hash, model/profile/selection, command/isolation, reformulation/ambiguities/dry-run, coordinator comparison and required edits. These are process records, not runtime enforcement or a new lifecycle state. Each active task then executes in its own fresh context, and an independent Tester validates implementation. The coordinator integrates outputs and enforces task/phase closeout. Do not carry unrelated tasks through one long-lived context.

---

## Pill Lifecycle

Pills are temporary execution aids, but they are not task-specific instances. Correction: pills are not 1:1 with tasks.

```text
Draft or refresh reusable pills -> bind pills to tasks opportunistically -> execute tasks ->
close tasks -> reconcile pills at phase closeout ->
keep / delete / merge / graduate to atoms -> prepare next phase pills
```

At phase closeout, classify touched pills explicitly:

- **still active** - keep for the next phase
- **stale** - delete or retire
- **redundant** - merge or remove duplicates
- **durable** - promote the stabilized residue into atoms first
- **materialization-worthy** - land resulting changes in code, specs, or docs as needed

Do not let durable knowledge remain pill-only once it stabilizes. Do not create a new pill just because a new task exists; create or update a pill only when there is a reusable atomic truth worth rebinding.

---

## Ritual Stack

### 1. Phase Ritual

Before starting a ready dependency layer:

```text
0. REVIEW   -> Review root/packages/leaves and edges cheaply; correct briefs and decompose.
1. IDENTIFY -> Select reviewed ready non-overlapping leaves.
2. BUNDLE   -> Confirm each task has its fresh context bundle.
3. EXECUTE  -> Run the execution ritual per task.
4. CLOSE    -> Require each task to close with its declared evidence and a task commit.
5. VALIDATE -> Run phase-level integration or end-to-end checks.
6. REGRESS  -> Fix interaction regressions.
7. RECONCILE-> Audit pills; delete, merge, or graduate them.
8. SURFACE  -> Capture newly discovered tasks and next-phase pills.
9. COMMIT   -> Make the phase-closing commit.
```

### 2. Task Execution Ritual

For each task in the phase:

```text
1. INIT   -> Confirm task scope, files, pills, validation, and declared closeout evidence.
2. REVIEW -> Accept cheap TaskDoc-only preflight, then separate cheap cold-bundle coverage.
3. BIND   -> Bind every relevant pill.
4. IMPLEMENT -> Make only task-scoped changes.
5. HANDOFF   -> Open an explicit testing handoff.
```

### 3. Task Testing Ritual

```text
1. CHECK  -> Confirm the intended contract and pill guardrails.
2. UPDATE -> Fix stale tests or add missing ones.
3. RUN    -> Execute the smallest relevant scope first.
4. EXPAND -> Run broader checks when shared behavior changed.
5. HANDOFF-> Open an explicit closeout handoff.
```

### 4. Task Closeout Ritual

```text
1. VERIFY -> Run `deskops closeout verify`: it checks exactly the declared evidence
             (declared X; found Y) and the pill guardrails.
2. CLEAN  -> Remove stale task-local context when appropriate.
3. DELETE -> Remove the resolved task from active routing.
4. COMMIT -> Close with `deskops closeout commit`; `closeout supersede` when the
             subject no longer exists, `closeout retire` for a pre-lifecycle resolution.
5. WAIT   -> If this was the last task in the phase, do not start the next phase until phase closeout passes.
```

---

## Commit Rules

### Task commit

Every closed task gets its own atomic commit, made by `deskops closeout commit`, `closeout supersede`, or `closeout retire`. The evidence it must show is the set declared when the task was created, not a fixed list.

### Phase commit

When all tasks in a phase are closed, make one separate descriptive phase commit for:

- integration fixes
- pill reconciliation
- captured next work
- board/phase bookkeeping

Do not hide unfinished task work inside a phase commit.

---

## Anti-Patterns

- Starting implementation before identifying the ready phase.
- Treating semantic milestones as phases when tasks still depend on each other.
- Running multiple unrelated tasks through one stale context.
- Closing tasks without the evidence they declared or without a dedicated task commit.
- Starting the next phase after isolated green task tests without integration validation.
- Carrying stale or overlapping pills forward because each task passed independently.
- Leaving durable rules only in pills instead of promoting them into atoms.
- Skipping newly discovered task capture at phase closeout.

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.

### Changed

- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.

### Fixed

- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

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
Cold-bundle de la tarea task-cc31-ciclo-de-vida-declarado-efectos-en-relationdoc-attributes-y-advance-por-edges-holding: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- En un desk temporal, desk update --apply escribe los RelationDoc con attributes.sets.status y terminal; segunda corrida sin cambios; un RelationDoc sin attributes queda reescrito (test)
- Cambiar el sets de un RelationDoc con la API de sldb hace que advance escriba ese valor sin tocar YAML (test)
- grep -rn 'sets_status' deskops/ vacío; grep de effect como atributo de LifecycleSpec vacío; task_lifecycle.yaml sin la clave transitions
- Evidencia de k6: desk update en dry-run sobre copias de los 6 desks y decisión sobre la migración legada
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_lifecycle_graph, test_lifecycle_end_to_end, test_scaffold_golden, test_desk_sync, test_output_goldens y test_cli_help_examples (sin --update-golden), y los que importen módulos tocados
- deskops doctor sin hallazgos nuevos en los 6 desks tras desk update --apply en una copia de cada uno
- wc -l deskops/lifecycle.py antes (406) y después (objetivo < 150)
- CHANGELOG y docs/workflow-policy-reference.md

