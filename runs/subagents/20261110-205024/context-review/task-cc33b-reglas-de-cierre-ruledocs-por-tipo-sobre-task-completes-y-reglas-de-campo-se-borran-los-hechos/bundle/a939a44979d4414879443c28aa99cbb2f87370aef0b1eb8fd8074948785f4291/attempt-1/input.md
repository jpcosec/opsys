FILE:desk/tasks/task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos.md
---
sldb:
  by: agent
  at: '2026-11-10T20:49:33Z'
  authority: generated
  via: save_document_payload
id: task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos
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
- deskops/data/rules/
- deskops/data/lifecycle/
- deskops/models/task_types.py
- deskops/operations.py
- deskops/cli/commands/operations.py
- deskops/services/tasks.py
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/lifecycle.py
- deskops/atom_tags.py
- deskops/domain_tree.py
- deskops/services/atoms.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC33b: Reglas de cierre - RuleDocs por tipo sobre task_completes y reglas de campo; se borran los hechos y gates viejos

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC33b del plan deskops-como-config, dag rev 4: partes (2), borrado de (3) y regla de evidencia (DA5) del agregado CC33. Depende de CC33a (en main, 6d133045). Gates G_GO06 y G_GO08 satisfied.

## Goal

_Describe the concrete result this task must produce._

El cierre de cada tipo de tarea lo decide una RuleDoc semilla on_transition sobre task_completes que exige los recibos evidence de CC33a; las reglas de campo son RuleDocs alert; se borran __closeout_evidence__, closeout_evidence_verified, pill_graduation_verified y _add_closeout_facts; los chequeos de CC38 asignados a CC33 pasan a RuleDoc o quedan con razón.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/data/rules/, deskops/data/lifecycle/, deskops/models/task_types.py, deskops/operations.py, deskops/cli/commands/operations.py, deskops/services/tasks.py, deskops/services/closeout_gates.py, deskops/services/closure.py, deskops/lifecycle.py, deskops/atom_tags.py, deskops/domain_tree.py, deskops/services/atoms.py, tests/, docs/, CHANGELOG.md, desk/rituals vía deskops. Fuera: grafo (CC33c), selectores y escrituras, tags por API de sldb (DO7).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC33b). SCOPE: Partes (2), el borrado de (3) y la regla de evidencia (DA5) del scope de CC33: por tipo, una RuleDoc semilla on_transition sobre la arista task_completes (where current_node = "ritual-testing") que exige los recibos evidence de CC33a (atom|materialization como or de dos); los __closeout_evidence__ de GC01 se borran; las reglas sobre campos pasan a RuleDocs on_check/on_write alert (vocabulario de closeout_evidence, código implícito, python_changes_without_declared_tests, forma de URL, graduación de pills); se borran _add_closeout_facts y su limpieza, closeout_evidence_verified, pill_graduation_verified y has(closeout_evidence_verified); los 9 chequeos entre documentos que el inventario de CC38 asigna a CC33 pasan a RuleDoc y su chequeo viejo se borra en el mismo paso (DK6).

ACCEPTANCE: sin recibo commit accepted, la arista task_completes aparece en edges_blocked con la cláusula fact = "commit"; editar goal tras verificar vuelve a bloquear; grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío; los 9 chequeos de CC38 como RuleDoc con su función vieja borrada; tests de closeout verdes; goldens idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; docs/workflow-policy-reference.md; ritual closeout vía deskops; CHANGELOG.

OUTPUT_SCOPE: deskops/data/rules/, deskops/models/task_types.py, deskops/operations.py, deskops/services/tasks.py, deskops/services/closeout_gates.py, deskops/lifecycle.py, tests/, docs/workflow-policy-reference.md, desk/rituals (vía deskops), CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan; base origin/main 6d133045; CC33a en main, CC33c pendiente de integración):
a1 (recibos de CC33a): closeout verify (CLI) escribe ReviewDoc kind evidence con fact en {tests, commit, atom, materialization, document, external}, value, verdict y reason, nombre evidence-<fact>-<n>, subject anclado al contrato de la tarea (deskops/services/closure.py, write_receipts=True solo desde el CLI). La regla de cierre por tipo exige any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada kind de __closeout_evidence__ del tipo (deskops/models/task_types.py:41-105); atom|materialization como or de las dos.
a2 (DO6, decisiones.md): hoy closeout commit (_gate_outcome) y la vista del board llaman a verify sin escribir recibos. Este nodo decide y deja escrito en el TaskDoc si closeout commit escribe los recibos antes de evaluar la regla (si no, la regla bloquea tareas que solo pasaron por closeout commit). DO6 b: cuando el link gate pasa sin documento enlazante (desk exento, solo follow-up o guard-test de skill) no hay recibo atom ni materialization: la regla lo contempla (p. ej. or con el caso exento) o pide otro value; la elección va en el TaskDoc.
a3 (kinds sin productor): __closeout_evidence__ de task.refactor incluye goldens y el de task.aggregate children; CC33a no produce fact goldens ni children. goldens: la regla usa el recibo kind goldens de deskops review record (follow-up de CC32) si existe, si no hipótesis en el TaskDoc. children: no existe campo children (igual que en CC32); hipótesis en el TaskDoc y el tipo no tiene cláusula de hijos hasta que exista.
a4 (arista y semilla): deskops/data/lifecycle/closeout-task_completes.md tiene condition status = "ready_for_testing" and has(closeout_evidence_verified); al borrar el hecho, la condición de la arista queda sin has(...) y la exigencia de recibos pasa a las RuleDocs por tipo (on_transition, where current_node = "ritual-testing"), semillas en deskops/data/rules/ escritas en desk/lifecycle/ por desk update --apply, como las rule-activation-* de CC32.
a5 (borrado, grep de aceptación): closeout_evidence_verified y pill_graduation_verified en services/tasks.py:202-203 y :307, services/closure.py:836-837; __closeout_evidence__ en models/task_types.py, services/closure.py:1094 y cli/commands/operations.py:44 (el tipo pasa a leer sus kinds de la RuleDoc o de una tabla de datos; nada de atributo de clase). grep de los cuatro nombres en deskops/ vacío.
a6 (inventario de CC38, runs/subagents/cc38-worker-report.md filas 3, 5, 13, 14, 15, 18, 24, 25): cada una pasa a RuleDoc o queda con razón escrita. #3 (namespace en tag-namespaces.yaml) y #5 (prefijos de domain path con crossroad) chocan con DO7 (CC35d cortado; sldb H1-H2 en el drawer de sldb 6b34cd5f): si la RuleDoc necesita la API de tags de sldb, quedan como hipótesis con referencia a DO7; si se expresan con el lenguaje de reglas sin esa API, se escriben aquí. Las que lean el filesystem o la ruta (#13, #14, #18, #24) y el lenguaje no las exprese quedan como hipótesis y nota a sldb (regla común 7).
a7 (archivos): files suma deskops/data/lifecycle/, deskops/cli/commands/operations.py, deskops/services/closure.py, deskops/atom_tags.py, deskops/domain_tree.py, deskops/services/atoms.py y docs/ a los del nodo. desk/rituals vía deskops.
a8 (4 pasos): el coordinador corre los 4 pasos del workflow de deskops en clon limpio (los 90 archivos de test de a uno). Cada comando deskops tarda unos 30 s hasta que la lectura indexada de sldb entre.

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-10, coordinador del plan; decisiones revisables):
b1 (cuántos chequeos): el inventario de CC38 (runs/subagents/cc38-worker-report.md) asigna a CC33 8 filas: 3, 5, 13, 14, 15, 18, 24 y 25. El «9» del contrato es la estimación del plan. La fuente es el informe y no hay que buscar un noveno.
b2 (a2, closeout commit): closeout commit NO escribe recibos. Evalúa la regla sobre los recibos que ya escribió `deskops closeout verify`. Si faltan o no están intactos, el bloqueo muestra los findings de edges_blocked y dice que se corra `deskops closeout verify`. El ritual de closeout (vía deskops) queda en este orden: verify, luego commit. La vista del board sigue sin escribir.
b3 (DO6 b, link exento): cuando el link gate pasa sin documento enlazante (desk exento, solo follow-up o guard-test de skill), verify escribe un recibo evidence fact = "atom", verdict accepted, value "exempt: <motivo del gate>". Así la cláusula atom|materialization de la regla no necesita un caso especial. Es un cambio a CC33a dentro de services/closure.py, con test.
b4 (a3): el recibo goldens existe en main: `deskops review record --kind goldens` (seguimiento de CC32, cerrado). La regla de task.refactor exige any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted") en lugar de un fact goldens. children: TaskAggregateDoc no tiene campo children, así que se deja hipótesis en el TaskDoc y la regla de aggregate no tiene cláusula de hijos (igual que CC32).
b5 (criterio de expresividad, a6): una fila pasa a RuleDoc si se expresa en el lenguaje de reglas de sldb, es decir con campos del documento, refs a otros documentos, any/all sobre aristas y has()/exists. Se comprueba con `sldb rules explain` sobre un caso bueno y uno malo. Lo que necesita el filesystem, la ruta o el nombre del archivo, o un archivo que no es documento del store, queda en el código con su razón: #3 tag-namespaces.yaml, #13 nombre de archivo, #14 provenance en disco, #18 desk/config.json y #24 artefacto renderizado. Se agrupa en una sola nota de inbox a sldb. #5 (prefijos con crossroad) depende de H1 de sldb (anchored_by con valor sin namespace, drawer de sldb 6b34cd5f) y queda por DO7. #15 (typed_as existe) y #25 (referencia a documento existente) se intentan como RuleDoc; si no salen, hipótesis.
b6 (aceptación de los chequeos): «los chequeos de CC38 como RuleDoc con su función vieja borrada» vale para los que pasan a RuleDoc. Los que quedan por b5 se listan en el informe con su razón y se eximen del grep, como p10 de CC38.
b7 (reglas de campo): cada RuleDoc alert traduce la condición del chequeo Python actual. Se localiza por nombre, porque los números de línea de a5 pueden haberse movido: el vocabulario de closeout_evidence, la alerta de código implícito, python_changes_without_declared_tests, la forma de URL y la graduación de pills (operations.py). Mismo texto de mensaje que hoy. Si una no se expresa, hipótesis y queda en el código.
b8 (goldens): los de ayuda (tests/fixtures/golden/help/*.txt) y los de salida (tests/fixtures/golden/output/), con test_output_goldens.py sin --update-golden. Si un golden tiene que cambiar (por ejemplo el mensaje de cierre bloqueado), el worker para y avisa con el diff.
b9 (doctor): la línea base es `deskops doctor` en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui) con la base del worktree, antes de cambiar nada. Después, el conjunto de errores y alertas no suma ninguno. Las dos capturas van al informe.

DISPOSICIÓN DE PREFLIGHT-2 Y BUNDLE-2 (2026-11-10, coordinador del plan; decisiones revisables):
c1 (8 contra 9): b1 manda sobre el número del contrato. La aceptación se cumple con las 8 filas del inventario; no se busca un noveno chequeo.
c2 (forma de la RuleDoc): la plantilla son las rule-activation-task-*.md de deskops/data/rules/ (CC32). Un archivo por tipo, rule-closeout-task-<tipo>.md. Frontmatter:
- subject "model <= <Clase del tipo>" (por ejemplo TaskCodeDoc), que liga la regla al tipo por la familia del modelo;
- where current_node = "ritual-testing";
- moment on_transition;
- severity error;
- condition: una cláusula any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada kind; atom|materialization va como or de dos any;
- message en español que nombra el tipo.
Se aplica a la arista task_completes igual que las de activación se aplican a la suya; ver cómo lo resuelve lifecycle/advance para las rule-activation.
c3 (de dónde lee el tipo sus kinds): de una tabla de datos, deskops/data/rules/closeout-evidence.yaml (task_type -> lista de kinds), no de la RuleDoc. La leen closure.py (qué productores corre verify) y cli/commands/operations.py. Un test comprueba que las cláusulas de cada rule-closeout-* coinciden con la tabla.
c4 (gates viejos): son los atributos __closeout_evidence__ de las clases de task_types.py y has(closeout_evidence_verified) en la arista. Los productores de closeout_gates.py se quedan: son los hechos de git y archivos de CC33a.
c5 (DA5, decisiones.md): la evidencia de cierre es solo por tipo. `--evidence` (closeout_evidence de la tarea) solo suma kinds, nunca quita. Un kind extra de la tarea se verifica, se escribe su recibo y, si falla, se reporta como alert sin bloquear.
c6 (goldens): la regla es «idénticos». b8 es el procedimiento si alguno pareciera tener que cambiar: el worker para y avisa, y el coordinador decide. No hay contradicción.
c7 (4 pasos del workflow de deskops, .github/workflows): sldb stores build --store .sldb; pytest, un proceso por archivo de tests/; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio. El worker corre los tests de los archivos que toca.
c8 (condición y mensaje de cada fila): el inventario está en main, en runs/subagents/cc38-worker-report.md, y cada fila apunta al archivo y la línea de su chequeo. La regla traduce esa condición y conserva el mensaje del chequeo.
c9 (ritual): desk/rituals/closeout.md. Se edita vía deskops (edit ritual) para que los pasos digan: verify escribe los recibos y commit evalúa la regla (b2).

## Validation

_List the checks required before this task can close._

- Sin recibo commit accepted, task_completes en edges_blocked con fact = "commit"; editar goal tras verificar vuelve a bloquear
- grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío
- Tests de a uno, test_cli y goldens desde /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

sin recibo commit accepted, la arista task_completes aparece en edges_blocked con la cláusula fact = "commit"; editar goal tras verificar vuelve a bloquear; grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío; los 9 chequeos de CC38 como RuleDoc con su función vieja borrada; tests de closeout verdes; goldens idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; docs/workflow-policy-reference.md; ritual closeout vía deskops; CHANGELOG.

FILE:deskops/models/task_types.py
"""Factory task types: ``TaskDoc`` subclasses that fix ``task_type`` and declare their gates.

A task type is a model, not a string: the family ``model <= TaskCodeDoc`` names the
documents of ``task.code`` and of every subtype that extends it (``task.refactor``), while
``task.debug`` deliberately extends ``TaskDoc`` instead of ``TaskCodeDoc`` because it swaps
``bundle`` for ``reproduction`` — a subtype only ever *adds* gates, it cannot remove one
(brief.md §Tipos, decisions.md DC1/D2).

Each concrete type fixes ``task_type`` to its name with a ``Literal`` default and declares one
class attribute, ``__closeout_evidence__``: the closeout evidence kinds ``deskops closeout
verify`` checks. It uses the vocabulary of
``deskops.services.closeout_gates.CLOSEOUT_EVIDENCE_VOCABULARY`` (tests, commit, atom,
materialization, document, external) plus ``children`` (the aggregate) and ``goldens`` (the
refactor) — both are only *declared* here; their verification lands in GC09 and a later node
(TaskDoc precisión 3).

The activation gate of a type is not Python: it is the ``RuleDoc`` seed
``deskops/data/rules/rule-activation-<type>.md`` (CC32), whose subject ``model <= <TypeDoc>``
names the family, so it needs no attribute here and a subtype inherits it.

``TaskDoc`` itself keeps ``task_type: str`` so old documents still read, and declares
``__contract__`` (the contract fields; sldb GO02 (e)).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .task import TaskDoc


class TaskCodeDoc(TaskDoc):
    """``task.code``: code changes gated by tests, a commit and an atom|materialization link."""

    task_type: Literal["task.code"] = Field(
        default="task.code",
        description="Workflow task type; fixed to 'task.code' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")


class TaskDocsDoc(TaskDoc):
    """``task.docs``: document-only work gated by a commit and a document."""

    task_type: Literal["task.docs"] = Field(
        default="task.docs",
        description="Workflow task type; fixed to 'task.docs' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")


class TaskDebugDoc(TaskDoc):
    """``task.debug``: gated like ``task.code`` but activated by a reproduction, not a bundle.

    It extends ``TaskDoc`` directly: a subtype only adds gates, and this type replaces the
    ``bundle`` receipt of ``task.code`` with ``reproduction``, so it cannot be a ``task.code``.
    """

    task_type: Literal["task.debug"] = Field(
        default="task.debug",
        description="Workflow task type; fixed to 'task.debug' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")


class TaskRefactorDoc(TaskCodeDoc):
    """``task.refactor``: a ``task.code`` that additionally requires goldens before and after."""

    task_type: Literal["task.refactor"] = Field(
        default="task.refactor",
        description="Workflow task type; fixed to 'task.refactor' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization", "goldens")


class TaskDecisionDoc(TaskDoc):
    """``task.decision``: gated by an owner receipt, a commit and a document."""

    task_type: Literal["task.decision"] = Field(
        default="task.decision",
        description="Workflow task type; fixed to 'task.decision' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")


class TaskAggregateDoc(TaskDoc):
    """``task.aggregate``: closes when its children do (``children`` is declared, GC09 verifies it)."""

    task_type: Literal["task.aggregate"] = Field(
        default="task.aggregate",
        description="Workflow task type; fixed to 'task.aggregate' for this model.",
    )
    __closeout_evidence__ = ("children", "commit")


class TaskExternalDoc(TaskDoc):
    """``task.external``: external work evidenced by an http(s) URL."""

    task_type: Literal["task.external"] = Field(
        default="task.external",
        description="Workflow task type; fixed to 'task.external' for this model.",
    )
    __closeout_evidence__ = ("external",)


#: Factory task type name -> model class. Desk-local types extend this set through
#: ``desk/models/*.py`` and are registered into the store by ``deskops desk update --apply``.
TASK_TYPE_MODELS: dict[str, type[TaskDoc]] = {
    "task.code": TaskCodeDoc,
    "task.docs": TaskDocsDoc,
    "task.debug": TaskDebugDoc,
    "task.refactor": TaskRefactorDoc,
    "task.decision": TaskDecisionDoc,
    "task.aggregate": TaskAggregateDoc,
    "task.external": TaskExternalDoc,
}

#: Legacy ``task_type`` strings -> canonical factory type name. Mirrors the migration in
#: ``deskops desk update --apply`` (TaskDoc precisión 4).
LEGACY_TASK_TYPE_MAP: dict[str, str] = {
    "code": "task.code",
    "implementation": "task.code",
    "test": "task.code",
    "docs": "task.docs",
    "spec": "task.docs",
    "design": "task.docs",
    "external": "task.external",
    "": "task.code",
}


def canonical_task_type_name(task_type: str) -> str:
    """Map a stored ``task_type`` to its canonical factory type name.

    A value that is already a factory type name is kept; a known legacy string is mapped;
    anything else (including an unknown value) resolves to ``task.code``, matching the
    ``desk update --apply`` migration.
    """
    name = str(task_type or "").strip().lower()
    if name in TASK_TYPE_MODELS:
        return name
    return LEGACY_TASK_TYPE_MAP.get(name, "task.code")


def factory_task_type_model(task_type: str) -> type[TaskDoc] | None:
    """The factory model class a canonical task type name resolves to, if any."""
    return TASK_TYPE_MODELS.get(canonical_task_type_name(task_type))


def task_type_closeout_evidence(task_type: str) -> tuple[str, ...] | None:
    """The ``__closeout_evidence__`` a factory type declares, or ``None`` when unknown."""
    model = factory_task_type_model(task_type)
    if model is None:
        return None
    return tuple(getattr(model, "__closeout_evidence__", ()))


def declared_evidence_list(value: object) -> list[str]:
    """The stored ``closeout_evidence`` as plain strings; the vocabulary is checked where it is used."""
    if isinstance(value, list):
        items = [str(item) for item in value]
    elif value in (None, ""):
        items = []
    else:
        items = [str(value)]
    return [item.strip() for item in items if item.strip()]

FILE:deskops/operations.py
"""The facade of one desk: every operation the CLI and the UIs call, as one call each.

``DeskopsOperations`` builds the arguments and delegates to the service that owns the
operation (tasks, atoms, closure, drawer, closeout gates), to ``deskops.doc_access`` for
plain document reads and writes, or to ``deskops.lifecycle``. No logic lives here.
"""

from __future__ import annotations

from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.doc_access import ARTIFACT_SUBJECTS
from deskops.doc_access import DocumentRecord
from deskops.doc_access import RepoTaskRoute
from deskops.doc_access import slugify
from deskops.lifecycle import ReadSnapshot
from deskops.lifecycle import TransitionResult
from deskops.paths import data_path
from deskops.runtime import Task
from deskops.services.atoms import AtomCreateResult
from deskops.services.atoms import AtomMergeResult
from deskops.services.atoms import AtomSplitResult
from deskops.services.atoms import AtomValidationRecord
from deskops.services.closure import CloseoutGateReport
from deskops.services.tasks import TaskBundle

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closure import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService

__all__ = [
    "ARTIFACT_MODELS",
    "ARTIFACT_PATHS",
    "ARTIFACT_SUBJECTS",
    "AtomCreateResult",
    "AtomMergeResult",
    "AtomSplitResult",
    "AtomValidationRecord",
    "CloseoutGateReport",
    "DeskopsOperations",
    "DocumentRecord",
    "RepoTaskRoute",
    "TaskBundle",
    "slugify",
]


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = data_path("spec")
        self.snapshot: ReadSnapshot | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @contextmanager
    def read_snapshot(self) -> Iterator[None]:
        """Reuse task-independent graph reads for the duration of one read-only pass.

        Inside the block, the closeout graph context and the lifecycle transitions
        leaving each node are computed once and shared by every task read. The caller
        promises not to write the desk inside the block; nesting reuses the outer one.
        """
        if self.snapshot is not None:
            yield
            return
        self.snapshot = ReadSnapshot()
        try:
            yield
        finally:
            self.snapshot = None

    # ---------------------------------------------------------------- services
    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService

            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService

            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService

            self._tasks = TasksService(self.root, self)
        return self._tasks

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService

            self._atoms = AtomsService(self.root, self)
        return self._atoms

    # ---------------------------------------------------------------- documents
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        return doc_access.create_artifact(self.root, artifact_id, raw_payload)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        return doc_access.edit_artifact_field(self.root, subject, selector, field, raw_value)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        return doc_access.show_artifact(self.root, artifact_id, doc_id)

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        return doc_access.list_repo_task_routes(self.root)

    # ---------------------------------------------------------------- tasks
    def registered_task_types(self) -> dict[str, type[Any]]:
        return self.tasks.registered_task_types()

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        return self.tasks.bind_pill_to_task(task_selector, pill_selector)

    def list_tasks(self) -> list[Task]:
        return self.tasks.list_tasks()

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        return self.tasks.show_task(task_id)

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def render_next_action_diagram(self) -> str:
        return self.tasks.render_next_action_diagram()

    # ---------------------------------------------------------------- closeout
    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        return self.closure.verify_task_closeout(task_selector)

    # ---------------------------------------------------------------- drawer
    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

    # ---------------------------------------------------------------- atoms
    def atom_folder_axis(self) -> str | None:
        return self.atoms.atom_folder_axis()

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    # ---------------------------------------------------------------- private aliases
    # graph_ui (UIs/graph_ui/frontends/mindmap/deskops_routes.py, frontends/desk/serve.py)
    # and deskops/domain_tree.py still call these private names; CC34 replaces that
    # access and removes the aliases.
    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    # CC34: alias for graph_ui, removed by CC34
    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return doc_access.resolve_glob(self.root, directory, doc_id)

    # CC34: alias for graph_ui, removed by CC34
    def _registered_repositories(self) -> list[dict[str, Any]]:
        return doc_access.registered_repositories(self.root)

    def _repository_root(self, repository: dict[str, Any]) -> Path:
        return doc_access.repository_root(self.root, repository)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:deskops/cli/commands/operations.py
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from deskops.cli.parse_input import parse_artifact_input
from deskops.cli.parse_input import parse_task_input
from deskops.cli.render import normalize
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.lifecycle import finding_line
from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS
from deskops.services.closeout_gates import CloseoutEvidenceError
from deskops.services.closeout_gates import CLOSEOUT_EVIDENCE_VOCABULARY
from deskops.services.closeout_gates import normalize_declared_evidence
from deskops.services.closeout_gates import order_evidence_kinds


class OperationsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        operations = DeskopsOperations(root)

        if args.command == "add" and args.subject == "task":
            payload = parse_task_input(args)
            requested_type = str(payload.get("task_type") or "").strip()
            registry = operations.registered_task_types()
            if requested_type:
                if requested_type not in registry:
                    print(
                        f"Error: '{requested_type}' is not a registered task type. "
                        f"Registered types: {', '.join(sorted(registry))}."
                    )
                    return 1
                task_type = requested_type
            else:
                task_type = "task.code"
                print("Note: no --task-type given; defaulting to task.code.")
            payload["task_type"] = task_type

            type_model = registry[task_type]
            type_evidence = list(getattr(type_model, "__closeout_evidence__", ()))
            try:
                declared = normalize_declared_evidence(payload.get("closeout_evidence"))
            except CloseoutEvidenceError as exc:
                print(f"Error: {exc}")
                return 1
            if declared:
                floor = [kind for kind in type_evidence if kind in CLOSEOUT_EVIDENCE_VOCABULARY]
                missing = [kind for kind in floor if kind not in declared]
                if missing:
                    print(
                        f"Error: --evidence removes closeout evidence the task type requires: "
                        f"{', '.join(missing)}. The type's evidence is a floor; add those kinds or drop --evidence."
                    )
                    return 1
                payload["closeout_evidence"] = order_evidence_kinds([*type_evidence, *declared])
            else:
                payload["closeout_evidence"] = []

            drawer_selector = getattr(args, "from_drawer", None)
            if not drawer_selector:
                raw_drawer = payload.get("from_drawer")
                drawer_selector = str(raw_drawer) if raw_drawer else None
            drawer_source = None
            if drawer_selector:
                try:
                    drawer_source = operations.resolve_drawer_source(drawer_selector)
                except (FileNotFoundError, ValueError) as exc:
                    print(f"Error: {exc}")
                    return 1
                payload = operations.attach_drawer_source(payload, drawer_source)
            bundle = operations.create_task_bundle(payload)
            print(f"Created task bundle {bundle.task_id}")
            print(f"Task: {bundle.task_path}")
            if drawer_source is not None:
                print(f"From drawer: {drawer_source} (kept; remove it by hand once the task supersedes it)")
            return 0

        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "add" and args.subject in artifact_subjects:
            artifact_id = artifact_subjects[args.subject]
            payload = parse_artifact_input(artifact_id, args)
            record = operations.create_artifact(artifact_id, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            if args.subject == "repository":
                print("Note: this is a local repository artifact. Use 'deskops repo register' for canonical ecosystem registration.")
            return 0

        if args.command == "edit":
            try:
                record = operations.edit_artifact_field(args.subject, args.selector, args.field, args.value)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Updated {record.kind} {record.doc_id} field {args.field.replace('-', '_')}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "bind" and args.subject == "pill":
            try:
                record, pill_id, changed = operations.bind_pill_to_task(args.task, args.pill)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Bound" if changed else "Already bound"
            print(f"{verb} pill {pill_id} to task {record.doc_id}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "next":
            try:
                if getattr(args, "diagram", False):
                    print(operations.render_next_action_diagram())
                    return 0
                report = operations.next_action_report(getattr(args, "task_id", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            self._print_next_action_report(report, why=getattr(args, "why", False))
            return 0

        if args.command == "list" and args.subject == "tasks":
            tasks = operations.list_tasks()
            repo_routes = operations.list_repo_task_routes() if getattr(args, "include_repos", False) else []
            payload: dict[str, Any] = {"tasks": tasks}
            if getattr(args, "include_repos", False):
                payload["repo_routes"] = repo_routes
            return render(payload, args.format, lambda _data: self._format_task_list(tasks, repo_routes))

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject == "atoms":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads, axis=axis),
            )
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            payloads = operations.list_artifacts(artifact_id)
            return render(
                {args.subject: payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads),
            )

        if args.command == "show" and args.subject == "task":
            task, gates = operations.show_task(args.task_id)
            if task is None:
                return render_error(
                    f"No task found for {args.task_id}",
                    args.format,
                    type_name="DomainError",
                )
            payload = normalize(task)
            payload["lifecycle_gates"] = normalize(gates)
            return render(payload, args.format, lambda _data: self._format_task_detail(task, gates))

        show_artifacts = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "show" and args.subject in show_artifacts:
            artifact_id = show_artifacts[args.subject]
            try:
                payload = operations.show_artifact(artifact_id, args.doc_id)
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                payload,
                args.format,
                lambda _data: self._format_artifact_detail(args.subject, payload),
            )

        if args.command == "advance" and args.subject == "task":
            from deskops.lifecycle import LifecycleGraphMissing

            try:
                task, result = operations.advance_task(args.task_id)
            except LifecycleGraphMissing as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            if task is None:
                print(f"No task found for {args.task_id}", file=sys.stderr)
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Message: {result.message}")
            return 1 if result.blocked else 0

        return 1

    def _print_next_action_report(self, report: dict[str, Any], *, why: bool = False) -> None:
        kind = report.get("kind")
        if kind == "no_board_task":
            print("Next:")
            print(f"No active task is routed by {report['board']}.")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        if kind == "multiple_board_tasks":
            print("Next:")
            print(f"Multiple active tasks are routed by {report['board']}; pass a task selector.")
            print("Routed tasks:")
            for task in report["tasks"]:
                print(f"- {task['id']} | {task['status']} | {task['title']}")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        print(f"Task: {report['task']['id']}")
        print(f"Title: {report['task']['title']}")
        print(f"Status: {report['task']['status']}")
        print(f"Current node: {report['task']['current_node']}")
        if report['task'].get('task_type'):
            print(f"Task type: {report['task']['task_type']}")
        if report['task'].get('inherits_from'):
            print("Inherits from:")
            for item in report['task']['inherits_from']:
                print(f"- {item}")
        print(f"Phase: {report['phase']}")
        if report.get("ritual"):
            print("Required ritual:")
            print(f"- {report['ritual']}")
        if report.get("pills"):
            print("Required pills:")
            for pill in report["pills"]:
                print(f"- {pill}")
        if why:
            print("Why:")
            for item in report.get("why") or []:
                print(f"- {item}")
        print("Next actions:")
        for index, action in enumerate(report["next_actions"], start=1):
            print(f"{index}. {action}")
        if report.get("advance_when"):
            print("Advance when:")
            for item in report["advance_when"]:
                print(f"- {item}")
        if report.get("findings"):
            print("Blocked by:")
            for finding in report["findings"]:
                print(f"- {finding_line(finding)}")
        print("Sources:")
        for label, path in report["sources"].items():
            print(f"- {label}: {path}")

    @staticmethod
    def _format_task_list(tasks: Any, repo_routes: Any) -> str:
        lines = [f"{task.id} | {task.status} | {task.current_node}" for task in tasks]
        lines.extend(
            f"{route.repo_id}:{route.task_id} | {route.status} | {route.title} | {route.task_path}"
            for route in repo_routes
        )
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_list(payloads: list[dict[str, Any]], *, axis: str | None = None) -> str:
        lines: list[str] = []
        for payload in payloads:
            label = payload.get("title") or payload.get("name") or payload["id"]
            if axis:
                values = ",".join(payload.get("axis_values") or []) or "-"
                lines.append(f"{payload['id']} | {label} | {axis}:{values}")
            else:
                lines.append(f"{payload['id']} | {label}")
        return "\n".join(lines)

    @staticmethod
    def _format_task_detail(task: Any, gates: list[dict[str, Any]]) -> str:
        lines = [
            f"Task: {task.id}",
            f"Title: {task.title}",
            f"Status: {task.status}",
            f"Current node: {task.current_node}",
            f"Task type: {task.task_type}",
        ]
        if task.inherits_from:
            lines.append("Inherits from:")
            lines.extend(f"- {item}" for item in task.inherits_from)
        if task.from_drawer:
            lines.append(f"From drawer: {task.from_drawer}")
        if getattr(task, "closeout_evidence", None):
            lines.append(f"Closeout evidence: {', '.join(task.closeout_evidence)}")
        if task.effective_pills:
            lines.append("Effective pills:")
            lines.extend(f"- {item}" for item in task.effective_pills)
        if task.effective_atoms:
            lines.append("Effective atoms:")
            lines.extend(f"- {item}" for item in task.effective_atoms)
        if task.inherit_acceptance_context:
            lines.append("Effective validation:")
            lines.extend(f"- {item}" for item in task.effective_validation)
            lines.append(f"Effective done when: {task.effective_done_when}")
        if gates:
            lines.append("Lifecycle gates:")
            for gate in gates:
                state = "open" if gate["holds"] else "closed"
                condition = gate["condition"] or "(none)"
                lines.append(
                    f"- {gate['relation_type']} -> {gate['target']}: {state} [{condition}]"
                )
                for finding in gate.get("findings") or []:
                    lines.append(f"  blocked by: {finding_line(finding)}")
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_detail(subject: str, payload: dict[str, Any]) -> str:
        lines = [f"{subject.capitalize()}: {payload['id']}"]
        label = payload.get("title") or payload.get("name") or payload["id"]
        lines.append(f"Title: {label}")
        for key, value in payload.items():
            if key in {"id", "title", "current_node", "history", "tags"}:
                continue
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(str(item) for item in value)}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

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
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import PillDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
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
        validated(type_model, compiled.task_payload)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_access.desk_transaction(self.root):
            doc_access.create_doc(self.root, task_path, type_model, compiled.task_payload, task_id)
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
        task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task.id)
        payload = doc_access.read_doc(task_path, TaskDoc)
        self.add_closeout_facts(payload)
        findings = self._transition_findings(task_path, payload)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": lifecycle.condition_holds(t.condition, payload),
                **({"findings": findings} if findings else {}),
            }
            for t in transitions
        ]

    def _transition_findings(self, task_path: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """The findings of the task's ``on_transition`` rules (sldb GO08): what blocks the gate
        leaving its node, as ``show`` and ``next`` print them; empty for an untracked task."""
        document = lifecycle.task_document(self.root, task_path)
        if document is None:
            return []
        try:
            return lifecycle.transition_findings(self.root, document, payload, snapshot=self._ops.snapshot)
        except Exception:
            return []

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
        spec = lifecycle.load_lifecycle_spec()
        return render_workflow_mermaid(spec, lifecycle.lifecycle_transitions(self.root, spec))

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
        findings = self._transition_findings(task_path, dict(payload)) if payload.get("current_node") else []
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
            "findings": findings,
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
        # The edge's effects validate against the task type's model. A task whose task_type is
        # not a registered type (empty or legacy, what `desk update --apply` migrates) validates
        # against TaskDoc, the model it was read with: a typed model's `task_type` literal could
        # not accept it (d4, instead of k5's TaskCodeDoc).
        model = self.registered_task_types().get(str(payload.get("task_type") or "")) or TaskDoc
        result = lifecycle.advance(self.root, payload, model, document=lifecycle.task_document(self.root, task_path))
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

FILE:deskops/services/closeout_gates.py
"""Closeout evidence gates.

Closeout verification accepts only real evidence: a lowercase commit id naming
a commit in HEAD's history, and a Python test file inside the repository's
``tests/`` directory. A front-matter string that merely looks like evidence is
not evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
from typing import Any
from typing import Callable


COMMIT_ID_PATTERN = re.compile(r"[0-9a-f]{7,40}")
URL_PATTERN = re.compile(r"https?://\S+")

# Closed vocabulary for a task's declared closeout evidence. `atom` and
# `materialization` are alternatives of one gate: either link satisfies it.
CLOSEOUT_EVIDENCE_VOCABULARY = ("tests", "commit", "atom", "materialization", "document", "external")

#: Kinds a task type declares but no node verifies yet: the aggregate's ``children`` and the
#: refactor's ``goldens``. `closeout verify` names them as not yet verifiable (TaskDoc precisión 3).
NOT_YET_VERIFIABLE_EVIDENCE = ("children", "goldens")

CODE_EVIDENCE = ("tests", "commit", "atom", "materialization")
DOCUMENT_EVIDENCE = ("commit", "document")
EXTERNAL_EVIDENCE = ("external",)

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})


class CloseoutEvidenceError(ValueError):
    """The declared closeout evidence is invalid or missing."""


def normalize_declared_evidence(value: Any) -> list[str]:
    """Validate a declared evidence list against the closed vocabulary, keeping order."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    declared: list[str] = []
    for item in items:
        kind = str(item).strip().lower()
        if not kind:
            continue
        if kind not in CLOSEOUT_EVIDENCE_VOCABULARY:
            raise CloseoutEvidenceError(
                f"Unknown closeout evidence '{item}'. Allowed: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}."
            )
        if kind not in declared:
            declared.append(kind)
    return declared


def order_evidence_kinds(kinds: list[str]) -> list[str]:
    """Deduplicate a declared evidence list in the vocabulary order, keeping the kinds that
    are declared on a type but not in the CLI vocabulary (``children``, ``goldens``) last.
    """
    seen: list[str] = []
    for kind in [*CLOSEOUT_EVIDENCE_VOCABULARY, *kinds]:
        if kind in kinds and kind not in seen:
            seen.append(kind)
    return seen


def collapse_link_kinds(kinds: list[str]) -> list[str]:
    """Show atom and materialization as the one alternative gate they are."""
    if "atom" in kinds and "materialization" in kinds:
        out: list[str] = []
        for kind in kinds:
            label = "atom|materialization" if kind in {"atom", "materialization"} else kind
            if label not in out:
                out.append(label)
        return out
    return list(kinds)


def gate_summary(declared: list[str], found: list[str]) -> str:
    declared_text = ", ".join(collapse_link_kinds(declared)) or "nada"
    found_text = ", ".join(found) or "nada"
    return f"esta tarea declaró {declared_text}; encontré {found_text}"


class CloseoutGatesService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def closeout_reference_evidence(
        self,
        payload: dict[str, Any],
        *,
        points_to_atom: Callable[[str], bool],
        points_to_routed_follow_up: Callable[[str], bool],
    ) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": [], "document": [], "external": []}
        references = payload.get("references") or []
        if not isinstance(references, list):
            references = [references]
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref, files=files):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
        for candidate in [*references, *files]:
            ref = str(candidate).strip()
            if ref and self.reference_points_to_document(ref) and ref not in evidence["document"]:
                evidence["document"].append(ref)
        return evidence

    @staticmethod
    def reference_points_to_url(reference: str) -> bool:
        """True for an http(s) URL: the record of work done outside this repository."""
        return bool(URL_PATTERN.fullmatch(reference.strip()))

    def reference_points_to_document(self, reference: str) -> bool:
        """True only for an existing document file inside the repository.

        Documents are prose or spec files (``DOCUMENT_SUFFIXES``). Test sources and
        the task bundle itself, which closure removes, are not documents.
        """
        path = Path(reference.split("::", 1)[0].strip())
        if not str(path) or path.is_absolute():
            return False
        resolved = (self.root / path).resolve()
        if resolved.suffix.lower() not in DOCUMENT_SUFFIXES or not resolved.is_file():
            return False
        if not resolved.is_relative_to(self.root):
            return False
        excluded = ((self.root / "tests").resolve(), (self.root / "desk" / "tasks").resolve())
        return not any(resolved.is_relative_to(parent) for parent in excluded)

    def reference_points_to_test(self, reference: str, files: list[Any] | None = None) -> bool:
        """True only for an existing .py file inside the repository that is a test location.

        After dropping an optional ``::node`` suffix (the node is not validated) and the
        ``pytest <path>`` form, the reference must name an existing file, relative to the
        root, whose suffix is exactly ``.py`` and which resolves inside the root. It counts
        when one of its directories (relative to the root) is named ``tests`` (``tests/``,
        ``runtime/foo/tests/``, ``ops/tests/sub/``) or when its path is declared in
        ``files``, the evaluated TaskDoc's ``files``: they widen where tests may live but
        are not evidence by themselves. Absolute paths, paths that leave the root through
        ``..`` or a symlink, and files under a directory starting with ``.`` or named
        ``site-packages`` or ``node_modules`` (third-party code) are not evidence. Each
        reference is checked on its own; the disk is not walked.
        """
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path_text or path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if not resolved.is_relative_to(self.root):
                continue
            directories = resolved.relative_to(self.root).parts[:-1]
            if any(part.startswith(".") or part in {"site-packages", "node_modules"} for part in directories):
                continue
            if "tests" in directories:
                return True
            for entry in files or []:
                declared = str(entry).strip()
                if declared and not Path(declared).is_absolute() and (self.root / declared).resolve() == resolved:
                    return True
        return False

    def full_commit_sha(self, reference: str) -> str:
        """The full id of a commit reference that passes ``reference_points_to_commit``, else ''."""
        if not self.reference_points_to_commit(reference):
            return ""
        resolved = subprocess.run(
            ["git", "rev-parse", "--verify", f"{reference.strip()}^{{commit}}"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        return resolved.stdout.strip() if resolved.returncode == 0 else ""

    def reference_points_to_commit(self, reference: str) -> bool:
        """True only for a lowercase hex id resolving to HEAD or an ancestor.

        The pattern rejects symbolic names such as ``HEAD`` or ``main``; an
        ambiguous abbreviation fails ``rev-parse --verify``; an unrelated or
        descendant commit fails the ancestor check.
        """
        candidate = reference.strip()
        if not COMMIT_ID_PATTERN.fullmatch(candidate):
            return False
        try:
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            if resolved.returncode != 0:
                return False
            full_sha = resolved.stdout.strip()
            if not full_sha:
                return False
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", full_sha, "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return ancestor.returncode == 0

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The declared-edge graph the closeout link gate reads, built lazily.

        Nodes come from one pass over the repository's document surfaces and file tree,
        tracked documents and schema edges from one read of the sldb index; the declared
        edges of a document are read only when the gate asks about it.
        """
        from deskops.graph.desk_graph import desk_graph

        return CloseoutGraph(desk_graph(self.root))

    def _test_path_candidates(self, reference: str) -> list[str]:
        candidates: list[str] = []
        stripped = reference.strip()
        if stripped.startswith("pytest "):
            for token in stripped.split()[1:]:
                token = token.strip("\"'")
                if token.startswith("-"):
                    continue
                if ".py" in token:
                    candidates.append(token)
        elif ".py" in stripped:
            candidates.append(stripped)
        return candidates


class CloseoutGraph:
    """What the closeout link gate asks of the declared-edge graph.

    The gate needs, for a changed file, the edges leaving its node and the edges a
    materialization points at it, plus the edges that link test files to atoms or
    materializations. Only the materialization documents and the documents the gate asks
    about are read; ``edges_around`` and ``test_link_edges`` return supersets of what the
    gate keeps, in the order a full scan of the sorted edge list would visit them, so the
    gate's own conditions produce the same evidence in the same order.
    """

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        lookup = graph.nodes.lookup
        self.node_ids_by_path = {path: node.id for path, node in lookup.by_path.items()}
        materializations = sorted(
            node_id for node_id in lookup.existing_ids | graph.node_ids() if node_id.startswith("materialization:")
        )
        self.invalid_materializations = {node_id for node_id in materializations if graph.missing_from(node_id)}
        self._materialization_edges_to: dict[str, list[Any]] = {}
        for node_id in materializations:
            for edge in graph.edges_from(node_id):
                self._materialization_edges_to.setdefault(edge.target_id, []).append(edge)

    def node_id(self, relative_path: str) -> str | None:
        return self.node_ids_by_path.get(relative_path)

    def edges_around(self, node_id: str) -> list[Any]:
        """Edges leaving ``node_id`` and materialization edges into it, sorted and unique."""
        return _sorted_unique([*self.graph.edges_from(node_id), *self._materialization_edges_to.get(node_id, [])])

    def test_link_edges(self) -> list[Any]:
        """Edges leaving a test file, and materialization edges into a test file."""
        edges = [
            edge
            for node_id in sorted(self.graph.node_ids())
            if node_id.startswith("test_file:")
            for edge in self.graph.edges_from(node_id)
        ]
        edges += [
            edge
            for target_id, into in self._materialization_edges_to.items()
            if target_id.startswith("test_file:")
            for edge in into
        ]
        return _sorted_unique(edges)


def _sorted_unique(edges: list[Any]) -> list[Any]:
    unique = {(edge.source_id, edge.target_id, edge.role, edge.provenance_locator): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

The activation gate of each factory task type is a ``RuleDoc`` (sldb GO06/GO08), also a
managed seed (``deskops/data/rules/``, written to ``desk/lifecycle/rule-activation-<type>.md``):
``on_transition`` over ``ritual-execution``, with subject ``model <= <TypeDoc>`` so a desk's
subtype inherits it without code, requiring the review receipts the type asks for
(``any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")``) and
the task's dependencies closed (``all(depends_on: status = "closed")``). sldb evaluates those
rules when ``edges_holding`` receives the task as ``document``; an ``error`` finding blocks
every edge and ``edges_blocked`` returns them with the findings ``deskops advance``, ``next``
and ``show`` print.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"
RULE_MODEL = "RuleDoc"
RULE_MODEL_REF = "sldb.models.rule_doc:RuleDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False
    #: The findings of the task's ``on_transition`` rules (sldb GO08), as ``finding_dict`` gives
    #: them: every finding on a blocked edge, only alerts on a holding one, none without a document.
    findings: tuple[dict[str, Any], ...] = ()

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it, ``transition_findings`` the store's rule graph (sldb loads the
    whole index for it, ~3 s on a small desk) and the closure service the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None
    rule_graph: Any = None
    has_rules: bool | None = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def finding_dict(finding: Any) -> dict[str, Any]:
    """An sldb ``Finding`` as the plain mapping ``show --format json`` prints."""
    return {"level": finding.level, "code": finding.code, "subject": finding.subject, "what": finding.what}


def finding_line(finding: dict[str, Any]) -> str:
    """One finding as sldb prints it: ``<level>: [<code>] <node>: <message> | <clause> (seen: ...)``."""
    return f"{finding['level']}: [{finding['code']}] {finding['subject']}: {finding['what']}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
        findings=tuple(finding_dict(f) for f in (getattr(edge, "findings", None) or ())),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any]) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them."""
    return [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any], document: str | None = None) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload. With ``document`` (the task's ``Model:name``
    in the store) the task's ``on_transition`` rules run too: an error finding holds every edge back."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transitions_blocked(root: Path, node: str, payload: dict[str, Any], document: str) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` but that an error
    finding of the task's ``on_transition`` rules blocks (``sldb.api.edges_blocked``), each
    carrying every finding."""
    from sldb.api import edges_blocked

    return _lifecycle_edges(node, edges_blocked(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transition_findings(root: Path, document: str, payload: dict[str, Any], *, snapshot: ReadSnapshot | None = None) -> list[dict[str, Any]]:
    """The findings of the task's ``on_transition`` rules read as ``payload`` (``sldb.api.transition_findings``).

    With a ``snapshot``, the store's rule graph is loaded once and shared by every task read of
    the pass (what ``sldb.api.transition_findings`` does on each call); a store without
    ``RuleDoc`` has no findings and loads nothing."""
    if snapshot is None:
        from sldb.api import transition_findings as sldb_transition_findings

        return [finding_dict(f) for f in sldb_transition_findings(_store(root), document, payload)]
    from sldb.api.rules.rule_graph import rule_graph
    from sldb.api.rules.rule_subjects import resolve_subject
    from sldb.api.rules.rules_on_transition import has_rules
    from sldb.api.rules.rules_on_transition import payload_findings

    if snapshot.has_rules is None:
        snapshot.has_rules = has_rules(_store(root))
    if not snapshot.has_rules:
        return []
    if snapshot.rule_graph is None:
        snapshot.rule_graph = rule_graph(_store(root))
    graph = snapshot.rule_graph
    return [finding_dict(f) for f in payload_findings(graph, "on_transition", resolve_subject(graph, document), payload)]


def task_document(root: Path, task_path: Path) -> str | None:
    """The ``Model:name`` the desk's store tracks ``task_path`` under (the subject of its rules);
    None for an untracked task or a desk without a store, where no rule runs."""
    from sldb.api.stores.doc_status import doc_status

    if not (_store(root) / "core").exists():
        return None
    try:
        status = doc_status(_store(root), task_path.resolve().relative_to(root.resolve()).as_posix())
    except Exception:
        return None
    if not status.model or not status.name:
        return None
    return f"{status.model}:{status.name}"


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None, document: str | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).

    With ``document`` (``task_document``) the task's ``on_transition`` rules run: when an error
    finding holds the edges back, the message lists each finding (rule, clause, node and value
    seen) instead of the edges' conditions.
    """
    from sldb.api import apply_effects

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
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload, document)
    if not holding:
        payload["current_node"] = node
        blocked = transitions_blocked(root, node, payload, document) if document else []
        findings = [f for t in blocked for f in t.findings if f["level"] == "error"]
        if findings:
            lines = "; ".join(finding_line(f) for f in findings)
            return TransitionResult(node, status, False, True, f"Gate {node} is blocked by its rules: {lines}")
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    target = COMPLETE if transition.terminal else transition.target
    # The model validates the whole new state (TaskDoc's lifecycle coherence): the edge's
    # ``sets``, the history it appends to and the node it leads to are applied together.
    history = [str(item) for item in payload.get("history") or []]
    sets = {**transition.sets, "history": [*history, transition.relation_type], "current_node": target}
    payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def ensure_rule_model(root: Path) -> bool:
    """Register sldb's ``RuleDoc`` in the desk's store when it lacks it (``sldb.api.add_model``);
    True when it was registered now. Tracking an activation rule needs the model, and each
    ``model <= <TypeDoc>`` of a rule's subject needs the type registered, which the deskops
    models always are."""
    from sldb.api import add_model
    from sldb.api import is_model_registered

    if is_model_registered(_store(root), RULE_MODEL):
        return False
    add_model(_store(root), RULE_MODEL_REF, pythonpath=package_pythonpath())
    return True


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds (the graph and the activation rules) and
    restores one the desk changed (``workspace.seed_desk``), registers sldb's relation models
    and ``RuleDoc`` when the store lacks them and tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import init_relations
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        init_relations(_store(root), pythonpath=package_pythonpath())
    ensure_rule_model(root)
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes

FILE:deskops/atom_tags.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


from deskops.models.atom import ATOM_TAG_PATTERN

NAMESPACE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
# The tag form is the model's (AtomDoc.tags); this is the same pattern with the namespace named.
TAG_PATTERN = re.compile(ATOM_TAG_PATTERN.replace("^[a-z][a-z0-9_]*:", "^(?P<namespace>[a-z][a-z0-9_]*):"))

DEFAULT_ATOM_TAG_NAMESPACES: dict[str, dict[str, Any]] = {
    "system": {
        "meaning": "System, project, or tool the atom belongs to.",
        "use_when": "The atom is about a specific system.",
        "do_not_use_when": "The tag is only a general topic.",
        "examples": ["system:deskops", "system:sldb"],
    },
    "topic": {
        "meaning": "Subject area discussed by the atom.",
        "use_when": "The atom is about a conceptual topic.",
        "do_not_use_when": "The atom describes a reusable implementation shape.",
        "examples": ["topic:atoms", "topic:composition"],
    },
    "layer": {
        "meaning": "Architectural layer where the atom applies.",
        "use_when": "The atom is scoped to a layer of the system.",
        "do_not_use_when": "The tag names only a broad topic or system.",
        "examples": ["layer:document-model", "layer:runtime", "layer:cli"],
    },
    "domain": {
        "meaning": "Problem domain or durable area of concern.",
        "use_when": "The atom belongs to a reusable problem domain.",
        "do_not_use_when": "A more specific system, topic, layer, or pattern tag applies.",
        "examples": ["domain:knowledge-management", "domain:task-execution"],
    },
}


def default_registry_path(root: Path) -> Path:
    return root / "desk" / "atoms" / "tag-namespaces.yaml"


def ensure_default_namespaces(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_registry(path, {"namespaces": DEFAULT_ATOM_TAG_NAMESPACES})


def load_namespaces(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    namespaces = loaded.get("namespaces") or {}
    if not isinstance(namespaces, dict):
        raise ValueError(f"Invalid atom tag namespace registry at {path}")
    return dict(namespaces)


def add_namespace(
    path: Path,
    namespace: str,
    *,
    meaning: str,
    use_when: str,
    do_not_use_when: str,
    examples: list[str],
) -> None:
    namespace = namespace.strip()
    if not NAMESPACE_PATTERN.fullmatch(namespace):
        raise ValueError("Namespace must match ^[a-z][a-z0-9_]*$.")

    path.parent.mkdir(parents=True, exist_ok=True)
    registry = {"namespaces": load_namespaces(path)}
    if namespace in registry["namespaces"]:
        raise ValueError(f"Atom tag namespace '{namespace}' already exists.")

    for example in examples:
        match = TAG_PATTERN.fullmatch(example)
        if match is None or match.group("namespace") != namespace:
            raise ValueError(f"Example '{example}' must use namespace '{namespace}'.")

    registry["namespaces"][namespace] = {
        "meaning": meaning,
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
        "examples": examples,
    }
    _write_registry(path, registry)


def axis_values(tags: list[str], axis: str) -> list[str]:
    """Return the sorted unique values carried by tags of the axis namespace."""
    values: set[str] = set()
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == axis:
            values.add(str(tag).split(":", 1)[1])
    return sorted(values)


def folder_axis_value(tags: list[str], axis: str) -> str | None:
    """Return the single folder-axis value for an atom, or None when absent.

    Raises ValueError when the atom carries more than one value of the axis
    namespace, because the physical folder placement must be deterministic.
    """
    values = axis_values(tags, axis)
    if len(values) > 1:
        raise ValueError(
            f"Atom carries multiple '{axis}' axis values: {', '.join(values)}. "
            f"The folder axis requires exactly one '{axis}:<value>' tag; "
            "remove the extra axis tags or split the atom."
        )
    return values[0] if values else None


def axis_folder_relpath(value: str) -> Path:
    """Map a dot-notated axis value to a nested folder path.

    Example: 'mepu.licitaciones' -> Path('mepu/licitaciones').
    """
    parts = [part for part in str(value).split(".") if part]
    if not parts:
        raise ValueError(f"Axis value '{value}' does not produce a valid folder path.")
    return Path(*parts)


def validate_atom_tag_namespaces(tags: list[str], path: Path) -> None:
    """Every tag's namespace is declared in the registry at ``path`` (a rule between the
    document and ``tag-namespaces.yaml``). The form of a tag is the model's own invariant
    (``AtomDoc.tags``), so a malformed tag is not this function's error.
    """
    namespaces = load_namespaces(path)
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is None:
            continue
        namespace = match.group("namespace")
        if namespace not in namespaces:
            raise ValueError(f"Unknown atom tag namespace '{namespace}' for tag '{tag}'.")


def _write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(registry, sort_keys=True), encoding="utf-8")

FILE:deskops/domain_tree.py
"""Domain tree: crossroads order a knowledge base and protoatoms hang from them.

A ``domain:a.b.c`` tag places a document under the path ``a.b.c``. Every prefix
of that path (``a``, ``a.b``, ``a.b.c``) needs a CrossroadDoc with written
content: the system is forced to write the parent before it can describe the
children. Protoatoms are free atoms; typing one into another sldb model keeps it
as a redirect stub whose ``typed_as`` names the typed document.

What one document must satisfy on its own (the form of its id, its tags and its
domain paths, one ``domain:`` tag per protoatom, a crossroad id naming its path)
is a validator of its model in ``deskops.models``. What is checked here needs
other documents or the file tree: the written parents of a domain path, the file
name of a document, the tag namespace registry and the target of ``typed_as``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.bootstrap import MODEL_REFS
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.models.atom import DOMAIN_NAMESPACE as DOMAIN
from deskops.models.atom import AtomDoc
from deskops.models.atom import domain_paths
from deskops.models.crossroad import CROSSROAD_PREFIX
from deskops.models.crossroad import DOMAIN_PATH_PATTERN
from deskops.models.crossroad import CrossroadDoc
from deskops.models.crossroad import crossroad_id
from deskops.models.protoatom import PROTO_PREFIX
from deskops.models.protoatom import ProtoAtomDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated

__all__ = ["DOMAIN", "PROTO_PREFIX", "CROSSROAD_PREFIX", "domain_paths", "crossroad_id", "DomainTree"]

_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)


def prefixes(path: str) -> list[str]:
    """``a.b.c`` -> ``['a', 'a.b', 'a.b.c']``."""
    parts = path.split(".")
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def read_crossroads(atoms_dir: Path) -> dict[str, dict[str, Any]]:
    """Written crossroads by path. An unreadable or invalid one does not count as written."""
    found: dict[str, dict[str, Any]] = {}
    for file in sorted(atoms_dir.rglob(f"{CROSSROAD_PREFIX}*.md")):
        try:
            payload = extract_model_data(CrossroadDoc, file.read_text(encoding="utf-8"))
            CrossroadDoc(**payload)
        except Exception:
            continue
        found[str(payload["path"])] = {**payload, "file": file}
    return found


def missing_parents(tags: list[str], crossroads: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for value in domain_paths(tags):
        for prefix in prefixes(value):
            if prefix not in crossroads and prefix not in missing:
                missing.append(prefix)
    return missing


def require_domain_parents(atoms_dir: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix.

    The form of each path is the model's invariant (``AtomDoc.tags``); this only asks
    the file tree whether the parents are written.
    """
    missing = missing_parents(tags, read_crossroads(atoms_dir))
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


@dataclass
class Created:
    doc_id: str
    path: Path


@dataclass
class Typed:
    protoatom_id: str
    protoatom_path: Path
    model: str
    doc_id: str
    path: Path


class DomainTree:
    """Crossroads, protoatoms and typing over one repository's desk/atoms."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.desk_root = doc_access.desk_root(self.root)
        self.atoms_dir = self.desk_root / "atoms"

    def create_crossroad(self, path: str, *, title: str, content: str) -> Created:
        doc_access.ensure_workspace(self.root)
        payload = validated(
            CrossroadDoc, {"id": crossroad_id(path), "path": path, "title": title, "content": content}
        ).model_dump(mode="json")
        parent = path.rpartition(".")[0]
        if parent:
            require_domain_parents(self.atoms_dir, [f"{DOMAIN}:{parent}"])
        if path in read_crossroads(self.atoms_dir):
            raise FileExistsError(f"A crossroad for '{path}' already exists.")
        return self._create(CrossroadDoc, payload, [f"{DOMAIN}:{path}"])

    def create_protoatom(self, doc_id: str, *, title: str, content: str = "", tags: list[str]) -> Created:
        doc_access.ensure_workspace(self.root)
        tags = list(tags)
        payload = validated(ProtoAtomDoc, {"id": doc_id, "title": title, "content": content, "tags": tags}).model_dump(
            mode="json"
        )
        validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        require_domain_parents(self.atoms_dir, tags)
        return self._create(ProtoAtomDoc, payload, tags)

    def type_protoatom(
        self,
        selector: str,
        *,
        model_name: str,
        doc_id: str | None = None,
        content_field: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Typed:
        """Create the typed document, then turn the protoatom into its redirect stub."""
        doc_access.ensure_workspace(self.root)
        proto_path = self._find_protoatom(selector)
        proto = doc_access.read_doc(proto_path, ProtoAtomDoc)
        if proto.get("typed_as"):
            raise ValueError(f"{proto['id']} was already typed as {proto['typed_as']}.")
        model = self._resolve_model(model_name)
        slug = str(proto["id"]).removeprefix(PROTO_PREFIX)
        target_id = doc_id or f"{model.__name__.removesuffix('Doc').lower()}-{slug}"
        payload = validated(model, self._typed_payload(model, target_id, proto, content_field, data or {})).model_dump(
            mode="json"
        )
        stub = validated(ProtoAtomDoc, {**proto, "typed_as": f"{model.__name__}:{target_id}",
                                        "content": _redirect_content(model.__name__, target_id)})
        # Rendered before any write, so a stub that cannot be written never leaves a typed orphan.
        stub_text = render_model_markdown(ProtoAtomDoc, stub.model_dump(mode="json")) + "\n"
        target_path = self._typed_path(model, target_id, list(proto.get("tags") or []))
        self._write_and_track(target_path, model, payload, target_id)
        proto_path.write_text(stub_text, encoding="utf-8")
        return Typed(str(proto["id"]), proto_path, model.__name__, target_id, target_path)

    def check(self) -> list[dict[str, Any]]:
        """Domain-tree errors per document under desk/atoms."""
        crossroads = read_crossroads(self.atoms_dir)
        records: list[dict[str, Any]] = []
        for path in sorted(self.atoms_dir.rglob("*.md")):
            if path.name.startswith(CROSSROAD_PREFIX):
                doc_id, errors = self._check_crossroad(path, crossroads)
            elif path.name.startswith(PROTO_PREFIX):
                doc_id, errors = self._check_protoatom(path, crossroads)
            else:
                doc_id, errors = path.stem, self._check_atom(path, crossroads)
            records.append({"id": doc_id, "path": str(path), "errors": errors})
        return records

    def tree(self) -> dict[str, Any]:
        """Crossroads nested by path, with the documents hanging from each one."""
        crossroads = read_crossroads(self.atoms_dir)
        nodes = {
            path: {"path": path, "id": item["id"], "title": item["title"], "children": [], "items": []}
            for path, item in crossroads.items()
        }
        roots: list[dict[str, Any]] = []
        for path in sorted(nodes):
            parent = path.rpartition(".")[0]
            (nodes[parent]["children"] if parent in nodes else roots).append(nodes[path])
        orphans: list[dict[str, Any]] = []
        unplaced: list[dict[str, Any]] = []
        for file in sorted(self.atoms_dir.rglob("*.md")):
            if file.name.startswith(CROSSROAD_PREFIX):
                continue
            model = ProtoAtomDoc if file.name.startswith(PROTO_PREFIX) else AtomDoc
            try:
                payload = doc_access.read_doc(file, model)
            except Exception:
                continue
            item = {"id": payload.get("id") or file.stem, "title": payload.get("title"),
                    "model": model.__name__, "typed_as": payload.get("typed_as")}
            places = domain_paths(list(payload.get("tags") or []))
            if not places:
                unplaced.append(item)
            for place in places:
                (nodes[place]["items"] if place in nodes else orphans).append({**item, "domain": place})
        return {"roots": roots, "orphans": orphans, "unplaced": unplaced}

    def _create(self, model: type[Any], payload: dict[str, Any], tags: list[str]) -> Created:
        doc_id = str(payload["id"])
        if any(self.atoms_dir.rglob(f"{doc_id}.md")):
            raise FileExistsError(f"Refusing to overwrite existing document {doc_id}.")
        path = doc_access.atom_doc_path(self.root, doc_id, tags)
        self._write_and_track(path, model, payload, doc_id)
        return Created(doc_id, path)

    def _write_and_track(self, path: Path, model: type[Any], payload: dict[str, Any], doc_id: str) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)
        try:
            doc_access.track_created_document(self.root, model, path, doc_id)
        except Exception:
            doc_access.remove_created_file(path)
            raise

    def _find_protoatom(self, selector: str) -> Path:
        matches = [path for path in self.atoms_dir.rglob(f"{PROTO_PREFIX}*.md") if selector in {path.stem, path.name}]
        if not matches:
            raise FileNotFoundError(f"No protoatom '{selector}' under {self.atoms_dir}.")
        if len(matches) > 1:
            raise ValueError(f"Protoatom selector '{selector}' is ambiguous: {', '.join(map(str, matches))}")
        return matches[0]

    def _resolve_model(self, name: str) -> type[Any]:
        from sldb.cli.model_utils import resolve_model_ref
        from sldb.store.io import load_store_index
        from sldb.store.layout import store_exists

        store = self.root / ".sldb"
        if store_exists(store):
            entry = next((model for model in load_store_index(store).models if model.name == name), None)
            if entry is None:
                raise ValueError(f"Model '{name}' is not registered in {store}; register it before typing into it.")
            return resolve_model_ref(entry.model_ref, str(self.root))
        if name in MODEL_REFS:
            return resolve_model_ref(MODEL_REFS[name])
        raise ValueError(f"Unknown model '{name}': there is no local store and it is not a deskops model.")

    def _typed_payload(
        self, model: type[Any], target_id: str, proto: dict[str, Any], content_field: str | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        fields = model.model_fields
        carried = {"id": target_id, "title": proto.get("title"),
                   "tags": list(proto.get("tags") or []), "provenance": proto.get("provenance")}
        payload = {name: value for name, value in carried.items() if name in fields and value is not None}
        content = str(proto.get("content") or "")
        target = content_field or ("content" if "content" in fields else None)
        if target is not None:
            if target not in fields:
                raise ValueError(f"{model.__name__} has no field '{target}' to receive the protoatom content.")
            payload[target] = content
        elif content.strip():
            raise ValueError(
                f"{model.__name__} has no 'content' field: pass --content-field to choose where the protoatom "
                "content goes (for AtomDoc, answer)."
            )
        return {**payload, **data}

    def _typed_path(self, model: type[Any], doc_id: str, tags: list[str]) -> Path:
        if model.__name__ == AtomDoc.__name__:
            return doc_access.atom_doc_path(self.root, doc_id, tags)
        artifact = next((key for key, known in ARTIFACT_MODELS.items() if known.__name__ == model.__name__), None)
        folder = Path(ARTIFACT_PATHS[artifact]) if artifact else Path("typed") / model.__name__
        return self.desk_root / folder / f"{doc_id}.md"

    def _check_crossroad(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(CrossroadDoc, path.read_text(encoding="utf-8"), invalid="crossroad is invalid")
        except Exception as exc:
            return path.stem, [f"crossroad is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        if path.stem != doc_id:
            errors.append(f"filename must match crossroad id '{doc_id}'")
        parent = str(payload.get("path") or "").rpartition(".")[0]
        if parent:
            errors.extend(self._domain_errors([f"{DOMAIN}:{parent}"], crossroads))
        return doc_id, errors

    def _check_protoatom(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(ProtoAtomDoc, path.read_text(encoding="utf-8"), invalid="protoatom is invalid")
        except Exception as exc:
            return path.stem, [f"protoatom is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        tags = list(payload.get("tags") or []) if isinstance(payload.get("tags"), list) else []
        if path.stem != doc_id:
            errors.append(f"filename must match protoatom id '{doc_id}'")
        try:
            validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        except ValueError as exc:
            errors.append(str(exc))
        errors.extend(self._domain_errors(tags, crossroads))
        typed_as = str(payload.get("typed_as") or "")
        if typed_as and not any(self.desk_root.rglob(f"{typed_as.split(':', 1)[-1]}.md")):
            errors.append(f"typed_as target not found: {typed_as}")
        return doc_id, errors

    def _check_atom(self, path: Path, crossroads: dict[str, Any]) -> list[str]:
        try:
            tags = check_document(AtomDoc, path.read_text(encoding="utf-8"))[0].get("tags")
        except Exception:
            return []  # atoms validate already reports unreadable atoms
        return self._domain_errors(list(tags) if isinstance(tags, list) else [], crossroads)

    def _domain_errors(self, tags: list[str], crossroads: dict[str, Any]) -> list[str]:
        """The domain paths of ``tags`` without a written crossroad. A malformed path is the
        model's error (reported with the document), so it is left out here."""
        valid = [f"{DOMAIN}:{value}" for value in domain_paths(tags) if _DOMAIN_PATH.fullmatch(value)]
        return [f"no written crossroad for domain path '{path}'" for path in missing_parents(valid, crossroads)]


def _redirect_content(model_name: str, doc_id: str) -> str:
    return (
        f"Typed as {model_name} {doc_id}. This protoatom is kept as a redirect stub so its id keeps "
        "resolving; its content now lives in the typed document."
    )


def _first_line(exc: Exception) -> str:
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return " ".join(lines[:3]) if lines else exc.__class__.__name__

FILE:deskops/services/atoms.py
"""Atom domain service: create, validate, reorganize, split, merge, retarget, delete.

Every atom write goes through ``deskops.doc_access`` and the desk's
``sldb.api.transaction``; split and merge each run inside one ``desk_transaction``
block so a failure restores the original files and store entries.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from sldb.api import Transaction

from deskops import doc_access
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import axis_values
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.doc_access import DocumentRecord
from deskops.models import AtomDoc
from deskops.models import PillDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class AtomValidationRecord:
    doc_id: str
    path: Path
    errors: list[str]


@dataclass(slots=True)
class AtomSplitResult:
    original_id: str
    original_path: Path
    created: list[DocumentRecord]
    redirect_kept: bool
    inbound_references: list[str]


@dataclass(slots=True)
class AtomMergeResult:
    source_id: str
    source_path: Path
    target_id: str
    target_path: Path
    redirect_kept: bool
    rewritten_references: list[str]
    ambiguities: list[str]


@dataclass(slots=True)
class AtomCreateResult:
    doc_id: str
    path: Path
    source_kind: str
    source_selector: str
    provenance: str


def reference_points_to_atom(root: Path, reference: str) -> bool:
    """Whether a task reference names an atom document of this desk (by path or by id)."""
    candidate = reference.strip()
    if not candidate:
        return False
    path_text = candidate.split("::", 1)[0]
    path = Path(path_text)
    if not path.is_absolute():
        path = root / path
    atoms_dir = doc_access.desk_root(root) / "atoms"
    if path.suffix == ".md" and path.exists():
        try:
            path.relative_to(atoms_dir)
            return True
        except ValueError:
            pass
    atom_id = candidate.removeprefix("atom:")
    if not atom_id.startswith("atom-"):
        return False
    return any(atom_path.stem == atom_id for atom_path in atoms_dir.rglob("*.md"))


class AtomsService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Document access is ``deskops.doc_access``; these keep the service's own vocabulary.
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_doc(self.root, path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)

    def _remove_created_file(self, path: Path) -> None:
        doc_access.remove_created_file(path)

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        doc_access.track_created_artifact(self.root, artifact_id, model, path, doc_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return doc_access.resolve_artifact_selector(self.root, artifact_id, directory, selector)

    def _reference_points_to_atom(self, reference: str) -> bool:
        return reference_points_to_atom(self.root, reference)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return doc_access.resolve_artifact_selector_multi(self.root, artifact_id, directories, selector)

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        """List atoms annotated with their folder-axis value.

        Returns (axis, payloads). Each payload carries 'axis_values' with every
        value of the configured axis namespace found on the atom's tags.
        """
        axis = self.atom_folder_axis()
        if axis_value is not None and axis is None:
            raise ValueError(
                "--axis-value requires 'atom_folder_axis' to be configured in desk/config.json."
            )
        payloads = self.list_artifacts("artifact.atom")
        results: list[dict[str, Any]] = []
        for payload in payloads:
            values = axis_values(list(payload.get("tags") or []), axis) if axis else []
            payload["axis_values"] = values
            if axis_value is not None and axis_value not in values:
                continue
            results.append(payload)
        return axis, results

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        """Move atoms carrying a folder-axis tag into their axis subfolder.

        Idempotent: atoms already in the right place are skipped. Atoms without
        an axis tag are left untouched, preserving manual folder organization.
        Atoms with multiple axis values are reported as errors and skipped.
        """
        self.ensure_workspace()
        axis = self.atom_folder_axis()
        if axis is None:
            raise ValueError(
                "No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize."
            )
        moves: list[dict[str, str]] = []
        errors: list[str] = []
        retargets: dict[str, str] = {}
        for path in self._all_atom_paths():
            try:
                payload = self._read_doc(path, AtomDoc)
            except Exception as exc:
                errors.append(f"{path.relative_to(self.root)}: unreadable atom ({exc})")
                continue
            atom_id = str(payload.get("id") or path.stem)
            tags = list(payload.get("tags") or [])
            try:
                value = folder_axis_value(tags, axis)
            except ValueError as exc:
                errors.append(f"{path.relative_to(self.root)}: {exc}")
                continue
            if value is None:
                continue
            target = self.desk_root / "atoms" / axis_folder_relpath(value) / f"{atom_id}.md"
            if target == path:
                continue
            if target.exists():
                errors.append(
                    f"{path.relative_to(self.root)}: target already exists at {target.relative_to(self.root)}"
                )
                continue
            moves.append({
                "id": atom_id,
                "from": str(path.relative_to(self.root)),
                "to": str(target.relative_to(self.root)),
            })
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                path.rename(target)
                retargets[atom_id] = str(target.relative_to(self.root))
        if retargets:
            self._retarget_atom_documents(retargets)
        return {"axis": axis, "moves": moves, "errors": errors, "dry_run": dry_run}

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        self.ensure_workspace()
        paths = [self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)] if selector else self._all_atom_paths()
        results: list[dict[str, Any]] = []
        for path in paths:
            record = self._validate_atom_path(path)
            results.append({
                "id": record.doc_id,
                "path": str(path),
                "errors": list(record.errors),
            })
        return results

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to delete {atom_id}; inbound references found: {refs}. Re-run with --force to delete without rewriting references."
            )
        untracked = doc_access.index_entry(self.root, path) is not None
        doc_access.delete_doc(self.root, path)
        return DocumentRecord(kind="atom-untracked" if untracked else "atom", doc_id=atom_id, path=path)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        self.ensure_workspace()
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(self.desk_root / "atoms", list(tags or []))
        source_flags = [flag for flag in (from_pill, from_graph, from_diagram) if flag]
        if len(source_flags) != 1:
            raise ValueError("Atom create requires exactly one source: --from-pill, --from-graph, or --from-diagram.")

        atom_id = str(atom_id).strip()
        normalized_question = str(five_wh_one_plus).strip()
        if tags:
            validate_atom_tag_namespaces(list(tags), default_registry_path(self.root))

        if from_pill:
            payload, source_selector, provenance = self._build_atom_from_pill(
                atom_id,
                from_pill,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "pill"
        elif from_graph:
            payload, source_selector, provenance = self._build_atom_from_graph_finding(
                atom_id,
                from_graph,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
                graph_path=graph_path,
            )
            source_kind = "graph"
        else:
            payload, source_selector, provenance = self._build_atom_from_diagram(
                atom_id,
                from_diagram or "",
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "diagram"

        validated(AtomDoc, payload)
        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        doc_access.create_doc(self.root, path, AtomDoc, payload, atom_id)
        return AtomCreateResult(
            doc_id=atom_id,
            path=path,
            source_kind=source_kind,
            source_selector=source_selector,
            provenance=provenance,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to split {atom_id}; inbound references found: {refs}. "
                "Re-run with --force to keep the original as a redirect stub without rewriting referrers."
            )

        normalized_ids = [str(item).strip() for item in into_ids if str(item).strip()]
        if len(normalized_ids) < 2:
            raise ValueError("Atom split requires at least two target ids via --into.")
        if len(set(normalized_ids)) != len(normalized_ids):
            raise ValueError("Atom split target ids must be unique.")
        if atom_id in normalized_ids:
            raise ValueError(f"Atom split target ids must not include the source atom id {atom_id}.")

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])
        new_payloads: dict[str, dict[str, Any]] = {}
        for target_id in normalized_ids:
            heading, content = assignments[target_id]
            new_payloads[target_id] = {
                "id": target_id,
                "title": f"{payload['title']} — {heading}",
                "five_wh_one_plus": payload["five_wh_one_plus"],
                "answer": content,
                "tags": list(payload.get("tags") or []),
                "provenance": payload.get("provenance"),
            }
            validated(AtomDoc, new_payloads[target_id])

        created: list[DocumentRecord] = []

        with doc_access.desk_transaction(self.root):
            for target_id in normalized_ids:
                new_payload = new_payloads[target_id]
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                doc_access.create_doc(self.root, new_path, AtomDoc, new_payload, target_id)
                created.append(DocumentRecord(kind="atom", doc_id=target_id, path=new_path))

            payload["answer"] = self._render_atom_split_redirect_answer(atom_id, normalized_ids)
            self._write_doc(path, AtomDoc, payload)

        return AtomSplitResult(
            original_id=atom_id,
            original_path=path,
            created=created,
            redirect_kept=True,
            inbound_references=inbound_references,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        self.ensure_workspace()
        source_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        target_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", into_selector)
        if source_path == target_path:
            raise ValueError("Atom merge source and target must resolve to different atoms.")

        source_payload = self._read_doc(source_path, AtomDoc)
        target_payload = self._read_doc(target_path, AtomDoc)
        source_id = str(source_payload.get("id") or source_path.stem)
        target_id = str(target_payload.get("id") or target_path.stem)

        validated(AtomDoc, source_payload)
        validated(AtomDoc, target_payload)

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        inbound_references = self._find_inbound_atom_references(source_id, excluded_path=source_path)
        rewritten_references: list[str] = []

        with doc_access.desk_transaction(self.root) as transaction:
            rewritten_references = self._rewrite_inbound_atom_references(
                source_id,
                target_id,
                excluded_paths={source_path, target_path},
                transaction=transaction,
            )
            merged_answer = self._merge_atom_answers(target_payload, source_payload)
            target_payload["answer"] = merged_answer
            target_payload["tags"] = self._merge_atom_tags(
                list(target_payload.get("tags") or []),
                list(source_payload.get("tags") or []),
            )
            self._write_doc(target_path, AtomDoc, target_payload)

            source_payload["answer"] = self._render_atom_merge_redirect_answer(source_id, target_id)
            self._write_doc(source_path, AtomDoc, source_payload)

        return AtomMergeResult(
            source_id=source_id,
            source_path=source_path,
            target_id=target_id,
            target_path=target_path,
            redirect_kept=True,
            rewritten_references=rewritten_references,
            ambiguities=ambiguities,
        )

    def _all_atom_paths(self) -> list[Path]:
        atoms_dir = self.desk_root / "atoms"
        if not atoms_dir.exists():
            return []
        return sorted(
            path for path in atoms_dir.rglob("*.md")
            if path.name != "tag-namespaces.yaml"
            # Crossroads and protoatoms have their own models: see deskops.domain_tree.
            and not path.name.startswith(("crossroad-", "proto-"))
        )

    def _build_atom_from_pill(
        self,
        atom_id: str,
        pill_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        field_map = {
            "what": "what",
            "why": "why",
            "how": "how",
            "how_not": "how_not",
            "when": "when",
            "where": "where",
        }
        source_field = field_map.get(five_wh_one_plus)
        if source_field is None:
            raise ValueError(
                "Atom create from pill only supports questions that map directly to pill sections: what, why, how, how_not, when, where."
            )
        directories = [self.desk_root / "contexts", self.desk_root / "drawer" / "pills"]
        pill_path = self._resolve_artifact_selector_multi("artifact.pill", directories, pill_selector)
        pill_payload = self._read_doc(pill_path, PillDoc)
        answer = str(pill_payload.get(source_field) or "").strip()
        if not answer:
            raise ValueError(f"Pill section '{source_field}' is empty; cannot create atom from it.")
        relative_path = pill_path.relative_to(self.root).as_posix()
        source_selector = str(pill_payload.get("id") or pill_path.stem)
        provenance = f"{relative_path}::{source_field}"
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{pill_payload['title']} — {source_field.replace('_', ' ').title()}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, source_selector, provenance

    def _build_atom_from_graph_finding(
        self,
        atom_id: str,
        finding_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
        graph_path: str | None,
    ) -> tuple[dict[str, Any], str, str]:
        from deskops.graph.checks import find_missing_graph_references

        source_id, target_id = self._parse_graph_finding_selector(finding_selector)
        resolved_graph_path = None
        if graph_path:
            resolved_graph_path = Path(graph_path)
            if not resolved_graph_path.is_absolute():
                resolved_graph_path = (self.root / resolved_graph_path).resolve()
        findings = [
            finding for finding in find_missing_graph_references(self.root, resolved_graph_path)
            if finding.source_id == source_id and finding.target_id == target_id
        ]
        if not findings:
            raise FileNotFoundError(
                f"Graph finding not found for selector {finding_selector}. Run 'deskops graph missing --root {self.root}' to inspect available findings."
            )
        if len(findings) > 1:
            kinds = ", ".join(sorted({finding.kind for finding in findings}))
            raise ValueError(
                f"Graph finding selector {finding_selector} matched multiple findings ({kinds}). Narrow the graph input so one finding remains."
            )
        finding = findings[0]
        provenance = self._compose_exact_provenance(finding.provenance_path, finding.provenance_locator)
        if provenance is None:
            raise ValueError(
                f"Graph finding {finding_selector} does not expose a resolvable provenance path; exact-source atom creation is blocked."
            )
        answer_lines = [
            f"Graph finding `{finding.kind}` records a missing reference from `{finding.source_id}` to `{finding.target_id}`.",
            "",
            f"- Reason: {finding.reason}",
        ]
        if finding.role:
            answer_lines.append(f"- Role: `{finding.role}`")
        if finding.extractor:
            answer_lines.append(f"- Extractor: `{finding.extractor}`")
        answer_lines.append(f"- Provenance: `{provenance}`")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"Graph finding — {source_id} → {target_id}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": "\n".join(answer_lines).strip(),
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, f"{source_id}->{target_id}", provenance

    def _build_atom_from_diagram(
        self,
        atom_id: str,
        diagram_path_value: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        diagram_path = Path(diagram_path_value)
        if not diagram_path.is_absolute():
            diagram_path = (self.root / diagram_path).resolve()
        if not diagram_path.exists() or not diagram_path.is_file():
            raise FileNotFoundError(f"Diagram source not found: {diagram_path_value}")
        relative_path = diagram_path.relative_to(self.root).as_posix()
        text = diagram_path.read_text(encoding="utf-8")
        provenance = relative_path
        answer = text.strip()
        if diagram_path.suffix == ".mmd":
            answer = f"```mermaid\n{answer}\n```".strip()
        elif diagram_path.suffix == ".md":
            mermaid_match = re.search(r"```mermaid\s*\n(?P<body>.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
            if mermaid_match is not None:
                answer = f"```mermaid\n{mermaid_match.group('body').strip()}\n```".strip()
                provenance = f"{relative_path}::mermaid:1"
        if not answer:
            raise ValueError(f"Diagram source {diagram_path_value} is empty; cannot create atom from it.")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{diagram_path.stem.replace('-', ' ').replace('_', ' ').title()} — Diagram",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, relative_path, provenance

    def _parse_graph_finding_selector(self, selector: str) -> tuple[str, str]:
        source_id, separator, target_id = str(selector).partition("->")
        source_id = source_id.strip()
        target_id = target_id.strip()
        if not separator or not source_id or not target_id:
            raise ValueError(
                f"Invalid --from-graph value '{selector}'. Expected SOURCE_ID->TARGET_ID."
            )
        return source_id, target_id

    def _compose_exact_provenance(self, provenance_path: str | None, provenance_locator: str | None) -> str | None:
        path_text = str(provenance_path or "").strip()
        if not path_text:
            return None
        locator_text = str(provenance_locator or "").strip()
        return f"{path_text}::{locator_text}" if locator_text else path_text

    def _split_atom_answer_sections(self, answer: str) -> list[tuple[str, str]]:
        trimmed = answer.strip()
        if not trimmed:
            raise ValueError("Source atom answer is empty; nothing to split.")
        matches = list(re.finditer(r"^(#{2,6})\s+(.+?)\s*$", answer, flags=re.MULTILINE))
        if not matches:
            raise ValueError(
                "Source atom answer does not contain markdown subsections. Add heading-based sections under ## Answer or pass a differently structured atom."
            )
        leading = answer[:matches[0].start()].strip()
        if leading:
            raise ValueError(
                "Source atom answer contains content before the first subsection heading; split only supports heading-based sections that start immediately in the answer body."
            )
        sections: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(answer)
            content = answer[match.end():end].strip()
            if not content:
                raise ValueError(f"Source atom subsection '{heading}' is empty.")
            sections.append((heading, content))
        return sections

    def _resolve_atom_split_assignments(
        self,
        into_ids: list[str],
        sections: list[tuple[str, str]],
        section_flags: list[str],
    ) -> dict[str, tuple[str, str]]:
        by_heading = {heading: content for heading, content in sections}
        if len(by_heading) != len(sections):
            raise ValueError("Source atom answer subsection headings must be unique to support atom splitting.")

        if not section_flags:
            if len(sections) != len(into_ids):
                raise ValueError(
                    f"Source atom answer exposes {len(sections)} subsection(s) but --into lists {len(into_ids)} target ids. "
                    "Provide --section NEW_ATOM_ID:SECTION_HEADING for each target or align the counts."
                )
            return {
                target_id: (heading, content)
                for target_id, (heading, content) in zip(into_ids, sections, strict=True)
            }

        assignments: dict[str, tuple[str, str]] = {}
        for raw_flag in section_flags:
            target_id, separator, heading = str(raw_flag).partition(":")
            target_id = target_id.strip()
            heading = heading.strip()
            if not separator or not target_id or not heading:
                raise ValueError(
                    f"Invalid --section value '{raw_flag}'. Expected NEW_ATOM_ID:SECTION_HEADING."
                )
            if target_id not in into_ids:
                raise ValueError(
                    f"Section assignment references unknown target id '{target_id}'. Known ids: {', '.join(into_ids)}"
                )
            if target_id in assignments:
                raise ValueError(f"Section assignment for {target_id} was provided more than once.")
            if heading not in by_heading:
                available = ", ".join(heading_name for heading_name, _ in sections)
                raise ValueError(
                    f"Section heading '{heading}' was not found in the source atom answer. Available headings: {available}"
                )
            content = by_heading[heading]
            if any(existing_heading == heading for existing_heading, _ in assignments.values()):
                raise ValueError(f"Section heading '{heading}' was assigned more than once.")
            assignments[target_id] = (heading, content)

        missing = [target_id for target_id in into_ids if target_id not in assignments]
        if missing:
            raise ValueError(
                f"Missing --section assignment for target ids: {', '.join(missing)}"
            )
        return assignments

    def _render_atom_split_redirect_answer(self, atom_id: str, target_ids: list[str]) -> str:
        bullets = "\n".join(f"- atom:{target_id}" for target_id in target_ids)
        return (
            f"This atom has been split. Use the child atoms below instead of expanding atom:{atom_id} further.\n\n"
            "Redirect targets:\n"
            f"{bullets}\n\n"
            "The original atom is intentionally kept as a redirect stub so existing inbound references continue to resolve until callers are rerouted."
        )

    def _detect_atom_merge_ambiguities(
        self,
        source_payload: dict[str, Any],
        target_payload: dict[str, Any],
    ) -> list[str]:
        ambiguities: list[str] = []
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        target_question = str(target_payload.get("five_wh_one_plus") or "").strip()
        if source_question and target_question and source_question != target_question:
            ambiguities.append(
                f"five_wh_one_plus conflict ({source_question} vs {target_question})"
            )
        return ambiguities

    def _merge_atom_tags(self, target_tags: list[str], source_tags: list[str]) -> list[str]:
        merged: list[str] = []
        for tag in [*target_tags, *source_tags]:
            if tag not in merged:
                merged.append(tag)
        return merged

    def _merge_atom_answers(
        self,
        target_payload: dict[str, Any],
        source_payload: dict[str, Any],
    ) -> str:
        target_answer = str(target_payload.get("answer") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        if not target_answer:
            return source_answer
        if not source_answer:
            return target_answer
        if source_answer == target_answer or source_answer in target_answer:
            return target_answer
        appendix = self._render_atom_merge_appendix(source_payload)
        if appendix in target_answer:
            return target_answer
        return f"{target_answer}\n\n{appendix}".strip()

    def _render_atom_merge_appendix(self, source_payload: dict[str, Any]) -> str:
        source_id = str(source_payload.get("id") or "").strip()
        source_title = str(source_payload.get("title") or source_id).strip()
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        source_provenance = str(source_payload.get("provenance") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        metadata_lines = [
            f"Merged from atom:{source_id} ({source_title}).",
        ]
        if source_question:
            metadata_lines.append(f"Original question: `{source_question}`")
        if source_provenance:
            metadata_lines.append(f"Original provenance: `{source_provenance}`")
        metadata = "\n".join(f"- {line}" for line in metadata_lines)
        return f"### Merged from atom:{source_id}\n\n{metadata}\n\n{source_answer}".strip()

    def _render_atom_merge_redirect_answer(self, source_id: str, target_id: str) -> str:
        return (
            f"This atom has been merged into atom:{target_id}. Use atom:{target_id} instead of expanding atom:{source_id} further.\n\n"
            "The original atom is intentionally kept as a redirect stub so the old id remains traceable after inbound references are reconciled."
        )

    def _validate_atom_path(self, path: Path) -> AtomValidationRecord:
        try:
            payload, errors = check_document(AtomDoc, path.read_text(encoding="utf-8"), invalid="model validation failed")
        except Exception as exc:
            return AtomValidationRecord(doc_id=path.stem, path=path, errors=[f"model validation failed: {exc}"])
        doc_id = str(payload.get("id") or path.stem)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")

        tags = payload.get("tags")
        try:
            validate_atom_tag_namespaces(
                list(tags) if isinstance(tags, list) else [],
                default_registry_path(self.root),
            )
        except ValueError as exc:
            errors.append(str(exc))

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

    def _provenance_is_resolvable(self, provenance: str) -> bool:
        parsed = urlparse(provenance)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return True
        path_text = provenance.split("::", 1)[0].split("#", 1)[0].strip()
        if not path_text:
            return False
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def _find_inbound_atom_references(self, atom_id: str, *, excluded_path: Path | None = None) -> list[str]:
        needle = f"atom:{atom_id}"
        matches: list[str] = []
        if not self.desk_root.exists():
            return matches
        for path in sorted(self.desk_root.rglob("*")):
            if excluded_path is not None and path == excluded_path:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line_number, line in enumerate(lines, start=1):
                for reference in re.findall(r"atom:[a-zA-Z0-9_.-]+", line):
                    if reference == needle and self._reference_points_to_atom(reference):
                        matches.append(f"{path.relative_to(self.root)}:{line_number}")
                        break
        return matches

    def _rewrite_inbound_atom_references(
        self,
        source_id: str,
        target_id: str,
        *,
        excluded_paths: set[Path] | None = None,
        transaction: Transaction | None = None,
    ) -> list[str]:
        needle = f"atom:{source_id}"
        replacement = f"atom:{target_id}"
        rewritten: list[str] = []
        excluded = {path.resolve() for path in (excluded_paths or set())}
        if not self.desk_root.exists():
            return rewritten
        for path in sorted(self.desk_root.rglob("*")):
            if path.resolve() in excluded:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                original_text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if needle not in original_text:
                continue
            pattern = re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])")
            updated_text = pattern.sub(replacement, original_text)
            if updated_text == original_text:
                continue
            changed_lines = [
                line_number
                for line_number, (before, after) in enumerate(
                    zip(original_text.splitlines(), updated_text.splitlines()), start=1
                )
                if before != after
            ]
            if not changed_lines:
                continue
            if transaction is not None:
                transaction.record(path)
            path.write_text(updated_text, encoding="utf-8")
            for line_number in changed_lines:
                rewritten.append(f"{path.relative_to(self.root)}:{line_number}")
        return rewritten

    def _retarget_atom_documents(self, retargets: dict[str, str]) -> bool:
        """Update tracked atom document paths in the .sldb store after moves.

        Retracking through SLDB's own track/untrack API keeps every derived index
        (semantic shards, sections, hashes, journal) consistent; editing the raw
        index files leaves the derived layers stale.
        """
        if not (self.root / ".sldb").is_dir():
            return False

        changed = False
        for atom_id, new_path in retargets.items():
            try:
                with doc_access.desk_transaction(self.root) as transaction:
                    doc_access.untrack_doc(self.root, atom_id)
                    transaction.track(self.root / new_path, "AtomDoc", atom_id)
            except Exception:
                continue
            doc_access.forget_index(self.root)
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        if not (self.root / ".sldb").is_dir():
            return False
        try:
            doc_access.untrack_doc(self.root, atom_id)
        except Exception:
            return False
        return True

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        return doc_access.atom_folder_axis(self.root)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
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

- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
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

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
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
Cold-bundle de la tarea task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Sin recibo commit accepted, task_completes en edges_blocked con fact = "commit"; editar goal tras verificar vuelve a bloquear
- grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío
- Tests de a uno, test_cli y goldens desde /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

