FILE:desk/tasks/task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra.md
---
id: task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra
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
- task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests
pills: []
files:
- deskops/doc_io.py
- deskops/doc_access.py
- deskops/services/
- deskops/cli/commands/message.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/repo.py
- deskops/runtime/scion.py
- deskops/lifecycle.py
- deskops/workspace.py
- deskops/bootstrap.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35a: Transacción - toda escritura por sldb.api.transaction; doc_io.py se borra

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35a del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3: parte (1), transacción, del agregado CC35 (L, partido en la rev 3), en PF3, árbol T3.5. Depende de CC30, CC36 y CC38, los tres en main. Gate: G_GD24 (sldb.api.transaction y apply_batch), satisfied.

## Goal

_Describe the concrete result this task must produce._

Toda escritura de deskops pasa por sldb.api.transaction (GD24), con expected_source_hash en los updates, y deskops/doc_io.py desaparece: su transacción propia y sus envoltorios de llamadas a sldb se reemplazan por sldb.api. message send/ack escriben dentro de la transacción, sin rollback manual. Un fallo a mitad de una operación compuesta revierte todo.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/doc_io.py (borrado), deskops/doc_access.py, deskops/services/, deskops/cli/commands/message.py, desk.py y repo.py, deskops/runtime/scion.py, deskops/lifecycle.py, deskops/workspace.py, deskops/bootstrap.py (P4: solo el import y la llamada, a3), tests y CHANGELOG.md. Fuera: selectores (CC35b), referencias entrantes (CC35c), tags/reemplazo (CC35d), escrituras en sldb, formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 3, CC35a, hijo del agregado CC35). SCOPE: Parte (1) del scope de CC35. Todo caller de doc_io.DocTransaction usa sldb.api.transaction (GD24) con expected_source_hash en los updates; message send/ack escribe por la transacción, sin rollback manual; doc_io.py se borra. Las líneas se fijan al promover, sobre main con CC30, CC36 y CC38 integrados.

ACCEPTANCE: grep -rn "doc_io\|DocTransaction" deskops/ vacío; un fallo inyectado a mitad de atoms merge revierte el atom, los referrers y el índice (hash de archivos y sldb stores check iguales antes y después); una escritura con expected_source_hash viejo falla con el mensaje de conflicto de deskops; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/doc_io.py (borrado), deskops/doc_access.py, deskops/services/, deskops/cli/commands/message.py, deskops/runtime/scion.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-07, coordinador del plan):
a1 (inventario en main 4e79fbac): deskops/doc_io.py tiene 319 líneas. Lo usan, con número de líneas: deskops/bootstrap.py (8), deskops/cli/commands/desk.py (6), deskops/cli/commands/message.py (4), deskops/cli/commands/repo.py (4), deskops/doc_access.py (4), deskops/lifecycle.py (2), deskops/runtime/scion.py (2), deskops/services/atoms.py (10), deskops/services/closure.py (2), deskops/services/drawer.py (4), deskops/services/issues.py (4), deskops/services/replace.py (2), deskops/services/retire.py (2), deskops/services/review.py (3), deskops/services/tasks.py (2), deskops/workspace.py (7). Además de DocTransaction (:250) y _RootTransaction (:174), doc_io envuelve llamadas a sldb: track/untrack (:121-130), is_tracked (:86), register_model (:131), link_store_alias (:136), inherit_model_from (:140), init_store_at (:144), init_relations_in (:148), update_store_indexes_in (:152) y remove_model_from (:156).
a2 (alcance del grep de aceptación): «grep -rn "doc_io\|DocTransaction" deskops/ vacío» cubre todo doc_io, no solo la transacción. Cada envoltorio pasa a una llamada directa a sldb.api: transaction para escribir y create/update/delete/track/untrack/register_model/etc. con su nombre en sldb. No se crea un módulo nuevo que repita doc_io con otro nombre. Si una llamada necesita lógica propia de deskops (por ejemplo, el pythonpath por defecto del desk), puede vivir en deskops/doc_access.py como función con esa lógica y el informe la lista.
a3 (files fuera del output_scope del dag): para vaciar el grep entran también deskops/lifecycle.py, deskops/workspace.py, deskops/bootstrap.py, deskops/cli/commands/desk.py, deskops/cli/commands/repo.py, deskops/services/review.py, deskops/services/__init__.py y deskops/services/replace.py. bootstrap.py es P4 (brief, «No toca P4»): en P4 solo se cambia el import y la llamada de doc_io por su equivalente de sldb.api, sin cambiar la lógica.
a4 (expected_source_hash): cada lectura-modificación-escritura de un documento trackeado en los servicios lee el source hash al leer el documento (sldb lo da en el estado o la referencia del documento) y lo pasa como expected_source_hash al update dentro de la transacción. Las creaciones no llevan guarda. Si sldb lanza ConflictError, deskops lo traduce al mensaje de a5.
a5 (mensaje de conflicto de deskops; hoy no existe): «Error: <ruta relativa> changed since deskops read it; nothing was written. Re-run the command.» en stderr, exit 1, sin traza. Ningún golden lo fija; un test lo fija.
a6 (fallo inyectado en atoms merge): el test hace monkeypatch de una llamada que ocurre a mitad del merge, después de escribir el átomo destino y antes de reescribir los referrers, y la hace lanzar. Antes y después compara el sha256 de todos los archivos de desk/ y .sldb/core/ del desk temporal y la salida de sldb stores check, que deben ser iguales.
a7 (message send/ack): cli/commands/message.py escribe la nota (create) y el ack (update con guarda) dentro de sldb.api.transaction. Se borra el rollback manual que hoy hace a mano.
a8 (verificación en 6 desks; lección de CC31): deskops doctor sobre copias de los 6 desks con main y con la rama, comparando hallazgos. deskops se ejecuta con un cwd neutro (fuera de las copias), para que PYTHONPATH decida qué código se importa: python -m deskops con el cwd dentro de una copia del repo de deskops importa el paquete copiado. Hay plantilla del coordinador en ~/proyectos/SLDB_1/coord2-ccconfig/cc31/coord/n7c.sh.
a9 (fuera): selectores (CC35b), referencias entrantes (CC35c) y tags/reemplazo (CC35d). Este nodo no cambia la forma de resolver documentos ni de reescribir referencias: solo con qué se escribe.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-07):
b1 (ruta del mensaje de a5): relativa a la raíz del proyecto, el directorio que contiene desk/ y .sldb/, con separadores «/» (como desk/tasks/<id>.md). El test fija el texto exacto.
b2 (punto del fallo inyectado de a6): en services/atoms.py:merge_atom, el orden actual es: reescribir los referrers (_rewrite_inbound_atom_references), escribir el átomo destino (_write_doc(target_path, ...)) y escribir el origen (_write_doc(source_path, ...)). El test intercepta la escritura del ORIGEN (la segunda _write_doc del merge, o lo que la reemplace) para que lance después de que los referrers y el destino ya se escribieron. Si al migrar cambia el nombre de esa llamada, el informe nombra el punto exacto que intercepta el test.
b3 (de dónde sale el source hash y qué no puede romperse): la guarda de sldb (Transaction.update(expected_source_hash=...); batch_prevalidate.check_guards) compara contra el source_hash DEL ÍNDICE, y sldb.api no tiene un accesor público para leerlo; doc_status no lo trae. Restricción: un documento trackeado editado a mano en disco y no reindexado, seguido de un deskops edit, tiene que seguir funcionando como hoy, sin conflicto; un test lo fija. El worker elige el mecanismo, por ejemplo pasar el hash del índice leído por una vía de sldb o reindexar ese documento antes de la guarda, y si lo único posible usa un módulo interno de sldb (sldb.store.*), lo anota como hipótesis para sldb (pedir un accesor público del source hash) y lo usa en un solo lugar de doc_access. El test de aceptación (update con un expected_source_hash viejo falla con el mensaje de a5) se hace pasando un hash que no coincide con el del índice.
b4 (qué updates llevan guarda): manda el Goal. Todo update de un documento trackeado que deskops hace después de leerlo lleva guarda, esté en services/, en cli/commands/message.py (ack), en lifecycle.py (advance) o en otro módulo. Las creaciones y los archivos no modelados (write_file) no la llevan, salvo que ya la tengan.

## Validation

_List the checks required before this task can close._

- grep -rn 'doc_io\|DocTransaction' deskops/ vacío (a2)
- Fallo inyectado a mitad de atoms merge: sha256 de desk/ y .sldb/core/ y sldb stores check iguales antes y después (test, a6)
- Update con expected_source_hash viejo falla con el mensaje de conflicto de a5 (test)
- message send/ack dentro de la transacción, sin rollback manual (test)
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests de los archivos tocados (test_doc_io se reescribe o se borra con su módulo), test_atoms_*, test_message_cli, test_retire_cli, test_issue_cli, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- deskops doctor sin hallazgos nuevos en los 6 desks, con cwd neutro (a8)
- wc -l antes y después por archivo tocado
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

grep -rn "doc_io\|DocTransaction" deskops/ vacío; un fallo inyectado a mitad de atoms merge revierte el atom, los referrers y el índice (hash de archivos y sldb stores check iguales antes y después); una escritura con expected_source_hash viejo falla con el mensaje de conflicto de deskops; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

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

FILE:deskops/doc_io.py
"""The one place deskops writes to an sldb store.

Everything here goes through the public ``sldb.api`` surface. Store writes that have no
public equivalent are named wrappers around the remaining private calls, and every such
import is listed in :data:`PRIVATE_SLDB_IMPORTS` so an import scan can keep the boundary
honest.

``DocTransaction`` is a re-entrant, file-and-store transaction: it records a path's
original bytes and tracked state before touching it, and on failure restores the store
entries and the file bytes before re-raising the original error. An inner
``with DocTransaction(root)`` joins the outer transaction keyed by root, so
``create_task_bundle`` and the ``_write_doc`` calls it makes roll back as one unit.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Any

from deskops.paths import package_pythonpath
from sldb.api import (
    add_model,
    doc_status,
    inherit_model,
    init_relations,
    init_store,
    link_store,
    remove_model,
    track_document_file,
    untrack_document,
    update_store_indexes,
)

logger = logging.getLogger("deskops.doc_io")

#: Private sldb modules this module is allowed to import. Every write-side operation
#: used here is public ``sldb.api``; only the renderer lacks a public re-export. Keep
#: this in sync if a needed operation has no public equivalent (and record the gap in
#: ``runs/planning/sldb-requests.md``).
PRIVATE_SLDB_IMPORTS: tuple[str, ...] = (
    "sldb.runtime.validation",  # render_model_markdown has no sldb.api re-export
)

def _store(root: Path) -> Path:
    return root / ".sldb"


def _has_store(root: Path) -> bool:
    return _store(root).is_dir()


def _pythonpath(pythonpath: str | None) -> str:
    return pythonpath or package_pythonpath()


def _model_name(model: Any) -> str:
    if isinstance(model, str):
        return model
    return str(getattr(model, "__name__", model))


def _absolute(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def _relative(root: Path, path: Path | str) -> str:
    absolute = _absolute(root, path).resolve()
    try:
        return absolute.relative_to(root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _status(root: Path, path: Path | str) -> Any | None:
    if not _has_store(root):
        return None
    try:
        return doc_status(_store(root), _relative(root, path))
    except Exception:
        return None


def is_tracked(root: Path, path: Path | str) -> bool:
    """Whether ``path`` is the tracked location of exactly one document."""
    status = _status(root, path)
    return bool(status is not None and status.exists)


def _track(root: Path, path: Path, model: Any, *, name: str | None = None, pythonpath: str | None = None, force: bool = True) -> Any | None:
    if not _has_store(root):
        return None
    return track_document_file(
        _store(root),
        _model_name(model),
        path,
        name=name or path.stem,
        pythonpath=_pythonpath(pythonpath),
        force=force,
    )


def _untrack(root: Path, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
    """Untrack by document name or path. A document that is not tracked is left alone."""
    if not _has_store(root):
        return False
    reference = str(path_or_name)
    path_like = isinstance(path_or_name, Path) or Path(reference).exists()
    status = _status(root, path_or_name) if path_like else _status(root, reference)
    if status is None or not status.exists:
        # Already untracked is not a failure; real store errors still raise below.
        return False
    untrack_document(_store(root), status.name, pythonpath=_pythonpath(pythonpath))
    return True


# ---------------------------------------------------------------------------
# One-off helpers for writes outside a transaction.
def track(root: Path, path: Path | str, model: Any, *, name: str | None = None, pythonpath: str | None = None, force: bool = True) -> Any | None:
    """Track one document, if the root has a store."""
    return _track(root, _absolute(root, path), model, name=name, pythonpath=pythonpath, force=force)


def untrack(root: Path, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
    """Untrack one document by name or path, if the root has a store."""
    return _untrack(root, path_or_name, pythonpath=pythonpath)


def register_model(root: Path, model_ref: str, *, pythonpath: str | None = None, canonical: bool = False) -> Any:
    """Register a model in ``root``'s store."""
    return add_model(_store(root), model_ref, pythonpath=_pythonpath(pythonpath), canonical=canonical)


def link_store_alias(root: Path, other_store: Path | str, name: str, *, replace: bool = False) -> Any:
    return link_store(_store(root), other_store, name, replace=replace)


def inherit_model_from(root: Path, ref: str, *, pythonpath: str | None = None) -> Any:
    return inherit_model(_store(root), ref, pythonpath=_pythonpath(pythonpath))


def init_store_at(path: Path | str) -> Any:
    return init_store(path=path)


def init_relations_in(root: Path, *, pythonpath: str | None = None) -> Any:
    return init_relations(_store(root), pythonpath=_pythonpath(pythonpath))


def update_store_indexes_in(root: Path, *, pythonpath: str | None = None, wait: bool = False) -> Any:
    return update_store_indexes(_store(root), _pythonpath(pythonpath), wait=wait)


def remove_model_from(root: Path, name: str, *, pythonpath: str | None = None, untrack_documents: bool = False) -> Any:
    return remove_model(_store(root), name, pythonpath=_pythonpath(pythonpath), untrack_documents=untrack_documents)


# ---------------------------------------------------------------------------
@dataclass
class _PathState:
    path: Path
    relative: str
    original_bytes: bytes | None
    tracked_model: str | None
    tracked_name: str | None

    @property
    def was_tracked(self) -> bool:
        return self.tracked_name is not None


class _RootTransaction:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.states: dict[str, _PathState] = {}
        self.depth = 0

    def record(self, path: Path | str) -> _PathState:
        absolute = _absolute(self.root, path).resolve()
        relative = _relative(self.root, absolute)
        state = self.states.get(relative)
        if state is not None:
            return state
        status = _status(self.root, absolute)
        tracked_model = status.model if status is not None and status.exists else None
        tracked_name = status.name if status is not None and status.exists else None
        state = _PathState(
            path=absolute,
            relative=relative,
            original_bytes=absolute.read_bytes() if absolute.exists() else None,
            tracked_model=tracked_model,
            tracked_name=tracked_name,
        )
        self.states[relative] = state
        return state

    def rollback(self) -> None:
        # 1. Drop store entries the transaction created, and reset entries whose file
        #    bytes moved so they can be re-tracked against the restored bytes.
        for state in reversed(list(self.states.values())):
            if not _has_store(self.root):
                break
            current = _status(self.root, state.path)
            if current is None or not current.exists:
                continue
            file_moved = state.original_bytes != (state.path.read_bytes() if state.path.exists() else None)
            if not state.was_tracked or file_moved:
                try:
                    untrack_document(_store(self.root), current.name, pythonpath=_pythonpath(None))
                except Exception as exc:  # noqa: BLE001 - rollback must not mask the original error
                    logger.warning("doc_io rollback: could not untrack %s: %s", state.relative, exc)
        # 2. Restore the file bytes.
        for state in reversed(list(self.states.values())):
            try:
                if state.original_bytes is None:
                    if state.path.exists():
                        state.path.unlink()
                else:
                    state.path.parent.mkdir(parents=True, exist_ok=True)
                    state.path.write_bytes(state.original_bytes)
            except Exception as exc:  # noqa: BLE001
                logger.warning("doc_io rollback: could not restore %s: %s", state.relative, exc)
        # 3. Re-track the documents that were tracked before the transaction.
        for state in reversed(list(self.states.values())):
            if state.tracked_name is None or state.tracked_model is None:
                continue
            if not state.path.exists():
                continue
            current = _status(self.root, state.path)
            if current is not None and current.exists:
                continue
            try:
                track_document_file(
                    _store(self.root),
                    state.tracked_model,
                    state.path,
                    name=state.tracked_name,
                    pythonpath=_pythonpath(None),
                    force=True,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("doc_io rollback: could not re-track %s: %s", state.relative, exc)


_STACKS: dict[Path, _RootTransaction] = {}


class DocTransaction:
    """Re-entrant file + store transaction scoped to one repository root."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def __enter__(self) -> "DocTransaction":
        transaction = _STACKS.get(self.root)
        if transaction is None:
            transaction = _RootTransaction(self.root)
            _STACKS[self.root] = transaction
        transaction.depth += 1
        self._transaction = transaction
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        transaction = self._transaction
        transaction.depth -= 1
        if transaction.depth > 0:
            return False
        _STACKS.pop(self.root, None)
        if exc_type is not None:
            transaction.rollback()
        return False

    def record(self, path: Path | str) -> _PathState:
        """Record a path's original bytes and tracked state before a plain file write."""
        return self._transaction.record(path)

    def write(self, path: Path | str, model: Any, payload: dict[str, Any]) -> None:
        absolute = _absolute(self.root, path)
        state = self._transaction.record(absolute)
        from sldb.runtime.validation import render_model_markdown

        rendered = render_model_markdown(model, payload) + "\n"
        if state.tracked_name is not None and _has_store(self.root):
            untrack_document(_store(self.root), state.tracked_name, pythonpath=_pythonpath(None))
        absolute.parent.mkdir(parents=True, exist_ok=True)
        absolute.write_text(rendered, encoding="utf-8")
        if state.was_tracked:
            track_document_file(
                _store(self.root),
                state.tracked_model,
                absolute,
                name=state.tracked_name,
                pythonpath=_pythonpath(None),
                force=True,
            )

    def track(self, path: Path | str, model: Any, *, name: str | None = None, pythonpath: str | None = None) -> Any | None:
        absolute = _absolute(self.root, path)
        self._transaction.record(absolute)
        return _track(self.root, absolute, model, name=name, pythonpath=pythonpath)

    def untrack(self, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
        if isinstance(path_or_name, Path) or Path(str(path_or_name)).exists():
            self._transaction.record(path_or_name)
        else:
            status = _status(self.root, path_or_name)
            if status is not None and status.exists and status.path:
                self._transaction.record(status.path)
        return _untrack(self.root, path_or_name, pythonpath=pythonpath)

    def delete(self, path: Path | str) -> None:
        absolute = _absolute(self.root, path)
        state = self._transaction.record(absolute)
        if state.tracked_name is not None and _has_store(self.root):
            untrack_document(_store(self.root), state.tracked_name, pythonpath=_pythonpath(None))
        if absolute.exists():
            absolute.unlink()

FILE:deskops/doc_access.py
"""Reading, writing and resolving the documents of one desk.

Every function takes the repository ``root`` (the directory that holds ``desk/``) and
works on the desk documents under it: parse a document into its model payload, write
one through a ``doc_io`` transaction, resolve a selector to a file, read a task with
its inherited context, or list the artifacts of one kind. ``DeskopsOperations`` is a
facade over these functions and the services; the services call them directly.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any

import yaml
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_io
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.desk_paths import resolve_selector
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import DeskFAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import ReviewDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.runtime import Task
from deskops.specs import compile_artifact_spec
from deskops.specs import compile_task_spec
from deskops.workspace import seed_desk


ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.materialization": MaterializationContractDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.review": ReviewDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": DeskFAQDoc,
    "artifact.step": StepDoc,
}

ARTIFACT_PATHS = {
    "artifact.task": "tasks",
    "artifact.pill": "contexts",
    "artifact.ritual": "rituals",
    "artifact.board": "tasks",
    "artifact.atom": "atoms",
    "artifact.materialization": "materializations",
    "artifact.repository": "registry",
    "artifact.review": "reviews",
    "artifact.inbox_note": "inbox",
    "artifact.faq": "faq",
    "artifact.step": "steps",
}

ARTIFACT_SUBJECTS = {
    "artifact.pill": {"subject": "pill", "list_subject": "pills"},
    "artifact.ritual": {"subject": "ritual", "list_subject": "rituals"},
    "artifact.board": {"subject": "board", "list_subject": "boards"},
    "artifact.atom": {"subject": "atom", "list_subject": "atoms"},
    "artifact.materialization": {"subject": "materialization", "list_subject": "materializations"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.review": {"subject": "review", "list_subject": "reviews", "create": False},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}

# Fields whose value is an effect of a workflow command, not a free edit. The
# value names who writes the field, so the refusal teaches the correct entry
# point instead of only saying no.
_TASK_OWNED_FIELDS = {
    "status": "deskops advance (transition effects) and deskops closeout commit",
    "current_node": "deskops advance",
    "history": "deskops advance and deskops closeout (append-only)",
    "task_type": "deskops add task --task-type (create a new task to change the type)",
    "closeout_evidence": "the task type, and deskops add task --evidence at creation",
}

# Artifacts whose documents are named by hand: their files are not `<id_pattern>.md`.
_FREE_NAMED_ARTIFACTS = {"artifact.inbox_note", "artifact.board", "artifact.ritual", "artifact.review"}

# Artifacts `create_artifact` tracks in the desk's store on creation.
_TRACKED_ON_CREATE = {"artifact.atom", "artifact.pill", "artifact.materialization"}

# (absolute path, model) -> (text, payload): ``read_doc`` parses a document once per text.
_DOC_PAYLOADS: dict[tuple[str, Any], tuple[str, dict[str, Any]]] = {}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


@dataclass(slots=True)
class DocumentRecord:
    kind: str
    doc_id: str
    path: Path


@dataclass(slots=True)
class RepoTaskRoute:
    repo_id: str
    repo_root: Path
    task_id: str
    task_path: Path
    board_path: Path
    title: str
    status: str


def desk_root(root: Path) -> Path:
    return root / "desk"


# ---------------------------------------------------------------- workspace
def ensure_workspace(root: Path) -> None:
    """The desk scaffold: its declared folders (the artifact directories among them), seed files
    and default tag namespaces, whichever are missing (``seed_desk``)."""
    seed_desk(root)


# ---------------------------------------------------------------- read / write
def read_doc(path: Path, model: type[Any]) -> dict[str, Any]:
    """The model payload of a document, parsed once per text of the file.

    The parse is kept for the whole process under (path, model) with the text it came
    from, and handed out as a copy: a reader that builds a new ``DeskopsOperations`` per
    request (the UI's server) does not re-parse unchanged documents, and a caller that
    edits the payload it got does not edit the kept one.
    """
    raw_text = path.read_text(encoding="utf-8")
    key = (os.path.abspath(path), model)
    hit = _DOC_PAYLOADS.get(key)
    if hit is not None and hit[0] == raw_text:
        return copy.deepcopy(hit[1])
    payload = extract_model_data(model, raw_text)
    if "id" not in payload:
        payload["id"] = path.stem
    _DOC_PAYLOADS[key] = (raw_text, copy.deepcopy(payload))
    return payload


def write_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    rendered = render_model_markdown(model, payload) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        # A short new value is not proof the model cannot read the file: only
        # refuse when the current text really extracts empty for that field.
        unreadable = set(is_unreadable_by_model(model, existing))
        lost = [field for field in unread_section_fields(model, existing, rendered) if field in unreadable]
        if lost:
            raise ValueError(
                f"Refusing to rewrite {path.name}: its model cannot read "
                f"{', '.join(lost)} from the current file, so writing this payload "
                "would erase that content. The document was not produced by the "
                "model's own renderer; rewrite it through sldb (or fix the model's "
                "template) before editing it here."
            )
        # Headings and frontmatter keys the template never declares are dropped by
        # extraction; refuse when the rewrite would erase one. A heading counts only
        # if re-rendering the file's own payload loses it, so replacing a field that
        # carries a heading (atoms split/merge) is not refused.
        kept = set((render_model_markdown(model, extract_model_data(model, existing)) + "\n").splitlines())
        erased = [line for line in find_structural_noise(model, existing, path.name).undeclared if line not in kept]
        erased += [f"frontmatter key '{key}'" for key in undeclared_frontmatter_keys(model, existing)]
        if erased:
            raise ValueError(
                f"Refusing to rewrite {path.name}: it has content its model "
                f"({model.__name__}) does not declare, and rewriting would erase it: "
                f"{'; '.join(erased)}. Move that content into a declared field "
                "(or remove it) before editing the document here."
            )
    with doc_io.DocTransaction(root) as transaction:
        transaction.write(path, model, payload)


def write_new_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    try:
        write_doc(root, path, model, payload)
    except Exception:
        remove_created_file(path)
        raise


def remove_created_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def track_created_document(root: Path, model: type[Any], path: Path, doc_id: str) -> None:
    doc_io.track(root, path, model, name=doc_id)


def track_created_artifact(root: Path, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
    if artifact_id not in _TRACKED_ON_CREATE:
        return
    track_created_document(root, model, path, doc_id)


# ---------------------------------------------------------------- values
def coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def merge_unique(*values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value_list in values:
        for value in value_list:
            item = str(value)
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return merged


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    YAML folds the line breaks of multi-line text and reads `**bold` as an alias,
    so a text field (`str` or `str | None`) takes the raw value as written. A JSON
    string literal (`"..."`) is still decoded, for callers that quote their text.
    """
    annotation = model.model_fields[field_name].annotation
    if annotation in (str, str | None):
        if raw_value.startswith('"'):
            try:
                decoded = json.loads(raw_value)
            except ValueError:
                return raw_value
            if isinstance(decoded, str):
                return decoded
        return raw_value
    return parse_data_value(raw_value)


# ---------------------------------------------------------------- paths and selectors
def artifact_path(root: Path, artifact_id: str, doc_id: str) -> Path:
    return desk_root(root) / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"


def artifact_glob_pattern(artifact_id: str) -> str:
    if artifact_id in _FREE_NAMED_ARTIFACTS:
        return "*.md"
    id_pattern = str(getattr(ARTIFACT_MODELS[artifact_id], "__artifact__", {})["id_pattern"])
    return id_pattern.replace("{slug}", "*") + ".md"


def atom_folder_axis(root: Path) -> str | None:
    """Return the configured folder axis namespace for atoms, or None (flat)."""
    axis = DeskConfig.load(desk_root(root)).atom_folder_axis
    if axis is None:
        return None
    axis = str(axis).strip()
    if not axis:
        return None
    namespaces = load_namespaces(default_registry_path(root))
    if axis not in namespaces:
        raise ValueError(
            f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
            "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
        )
    return axis


def atom_doc_path(root: Path, atom_id: str, tags: list[str]) -> Path:
    base = desk_root(root) / "atoms"
    axis = atom_folder_axis(root)
    if axis is not None:
        value = folder_axis_value(tags, axis)
        if value is not None:
            return base / axis_folder_relpath(value) / f"{atom_id}.md"
    return base / f"{atom_id}.md"


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_selector(desk_root(root), [directory], doc_id, f"{doc_id}*.md", "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            directories,
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        if artifact_id != "artifact.review":
            raise
    # A review's id is the authority; its file is named `<kind>-<n>.md` under
    # `desk/reviews/<task-id>/`, so resolve it by the id its frontmatter carries
    # (TaskDoc precisión 4: nothing parses the id back out of the path).
    matches = [
        path
        for directory in directories
        if directory.exists()
        for path in sorted(directory.rglob("*.md"))
        if frontmatter_id(path) == selector
    ]
    if not matches:
        raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous {artifact_id} selector '{selector}': {names}")
    return matches[0]


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            [directory],
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        tracked = _tracked_task_paths(root) if artifact_id == "artifact.task" else set()
        if not tracked:
            raise
    # Tasks written before the `task-*` naming are still tracked TaskDocs.
    return resolve_selector(
        desk_root(root),
        [directory],
        selector,
        "*.md",
        artifact_id,
        recursive=True,
        keep=lambda path: path.resolve() in tracked,
    )


def _tracked_task_paths(root: Path) -> set[Path]:
    # Tasks are tracked under their type model (TaskCodeDoc, …) and, for pre-type
    # documents, under TaskDoc. Legacy file names resolve only through the tracked paths.
    from deskops.services.tasks import registered_task_types

    model_names = {"TaskDoc"}
    model_names.update(getattr(cls, "__name__") for cls in registered_task_types(root).values())
    tracked: set[Path] = set()
    for model_name in model_names:
        records = root / ".sldb" / "core" / "documents" / model_name
        if not records.is_dir():
            continue
        for record in records.glob("*.yaml"):
            try:
                path = (yaml.safe_load(record.read_text(encoding="utf-8")) or {}).get("path")
            except (OSError, yaml.YAMLError):
                continue
            if path:
                tracked.add((root / path).resolve())
    return tracked


def frontmatter_id(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        payload = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(payload, dict) or payload.get("id") is None:
        return None
    return str(payload["id"])


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    try:
        return resolve_artifact_selector(root, "artifact.ritual", directory, selector)
    except FileNotFoundError:
        pass
    # Ritual files are named by hand; accept the frontmatter id as well.
    matches = (
        [path for path in sorted(directory.glob("*.md")) if frontmatter_id(path) == selector]
        if directory.exists()
        else []
    )
    if not matches:
        raise FileNotFoundError(f"No artifact.ritual file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous artifact.ritual selector '{selector}': {names}")
    return matches[0]


def editable_artifact(root: Path, subject: str, selector: str) -> tuple[type[Any], Path, str]:
    """The model, file and kind of the document `deskops edit <subject> <selector>` names."""
    if subject == "task":
        try:
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "tasks", selector)
        except FileNotFoundError:
            # Drawer candidates are tasks too; an active task with the same
            # selector wins because it resolved before this fallback.
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "drawer" / "tasks", selector)
        return TaskDoc, path, "task"
    artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
    if subject not in artifact_subjects:
        raise ValueError(f"Unsupported edit subject: {subject}")
    artifact_id = artifact_subjects[subject]
    model = ARTIFACT_MODELS[artifact_id]
    if artifact_id == "artifact.ritual":
        return model, resolve_ritual_selector(root, selector), subject
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    path = resolve_artifact_selector_multi(root, artifact_id, directories, selector)
    return model, path, subject


# ---------------------------------------------------------------- tasks
def resolve_task_payload(root: Path, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
    """The normalized payload of a task with its inherited context (``effective_*``)."""
    if task_id in stack:
        chain = " -> ".join([*stack, task_id])
        raise ValueError(f"Task inheritance cycle detected: {chain}")
    path = resolve_glob(root, desk_root(root) / "tasks", task_id)
    payload = compile_task_spec(read_doc(path, TaskDoc), entry_node="").task_payload
    inherited_ids = coerce_list(payload.get("inherits_from") or [])
    inherited_payloads = [resolve_task_payload(root, parent_id, (*stack, task_id)) for parent_id in inherited_ids]

    payload["effective_references"] = merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
        payload.get("references", []),
    )
    payload["effective_pills"] = merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
        payload.get("pills", []),
    )
    payload["effective_tags"] = merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
        payload.get("atoms", []),
    )

    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = merge_unique(
            *[parent.get("effective_validation", parent.get("validation", [])) for parent in inherited_payloads],
            payload.get("validation", []),
        )
        parent_done_when = next(
            (
                str(parent.get("effective_done_when") or parent.get("done_when") or "")
                for parent in inherited_payloads
                if str(parent.get("effective_done_when") or parent.get("done_when") or "")
            ),
            "",
        )
        payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
    else:
        payload["effective_validation"] = coerce_list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    return payload


def hydrate_task(payload: dict[str, Any]) -> Task:
    return Task(
        id=payload["id"],
        title=payload["title"],
        status=payload["status"],
        summary=payload["goal"],
        tags=list(payload.get("tags") or []),
        current_node=payload.get("current_node", ""),
        history=list(payload.get("history") or []),
        goal=payload.get("goal", ""),
        scope=payload.get("scope", ""),
        references=list(payload.get("references") or []),
        depends_on=list(payload.get("depends_on") or []),
        pills=list(payload.get("pills") or []),
        files=list(payload.get("files") or []),
        implementation_path=payload.get("implementation_path", ""),
        validation=list(payload.get("validation") or []),
        done_when=payload.get("done_when", ""),
        task_type=payload.get("task_type", ""),
        inherits_from=list(payload.get("inherits_from") or []),
        inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
        atoms=list(payload.get("atoms") or []),
        from_drawer=payload.get("from_drawer") or "",
        closeout_evidence=list(payload.get("closeout_evidence") or []),
        effective_references=list(payload.get("effective_references") or payload.get("references") or []),
        effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
        effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
        effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
        effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
        effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
    )


def load_task(root: Path, task_id: str) -> Task:
    return hydrate_task(resolve_task_payload(root, task_id))


# ---------------------------------------------------------------- artifacts
def list_artifacts(root: Path, artifact_id: str) -> list[dict[str, Any]]:
    model = ARTIFACT_MODELS[artifact_id]
    directory = desk_root(root) / ARTIFACT_PATHS[artifact_id]
    if not directory.exists():
        if not desk_root(root).exists():
            raise FileNotFoundError(f"Desk root not found at {desk_root(root)}. Run 'deskops init' to initialize.")
        return []
    pattern = artifact_glob_pattern(artifact_id)
    results = []
    for path in sorted(directory.rglob(pattern)):
        try:
            results.append(read_doc(path, model))
        except Exception as e:
            print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
    return results


def show_artifact(root: Path, artifact_id: str, doc_id: str) -> dict[str, Any]:
    if not doc_id:
        raise ValueError(f"No {artifact_id} ID provided")
    model = ARTIFACT_MODELS[artifact_id]
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    return read_doc(resolve_artifact_selector_multi(root, artifact_id, directories, doc_id), model)


def create_artifact(root: Path, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
    ensure_workspace(root)
    model = ARTIFACT_MODELS[artifact_id]
    compiled = compile_artifact_spec(artifact_id, raw_payload, model_fields=model.model_fields.keys())
    validated(model, compiled.artifact_payload)
    doc_id = compiled.artifact_payload["id"]
    if artifact_id == "artifact.atom":
        tags = list(compiled.artifact_payload.get("tags") or [])
        validate_atom_tag_namespaces(tags, default_registry_path(root))
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(desk_root(root) / "atoms", tags)
        path = atom_doc_path(root, doc_id, tags)
    else:
        path = artifact_path(root, artifact_id, doc_id)
    with doc_io.DocTransaction(root):
        write_new_doc(root, path, model, compiled.artifact_payload)
        track_created_artifact(root, artifact_id, model, path, doc_id)
    return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=doc_id, path=path)


def edit_artifact_field(root: Path, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
    ensure_workspace(root)
    model, path, kind = editable_artifact(root, subject, selector)
    field_name = field.replace("-", "_")
    if field_name not in model.model_fields:
        raise ValueError(f"Unknown field '{field_name}' for {subject}")
    if field_name == "id":
        raise ValueError("Cannot edit immutable field 'id'")
    if subject == "task" and field_name in _TASK_OWNED_FIELDS:
        raise ValueError(
            f"{field_name} is not editable with edit task; "
            f"it is written by {_TASK_OWNED_FIELDS[field_name]}."
        )
    if subject == "review" and field_name in {"verdict", "reason", "disposed_at", "disposed_by"}:
        raise ValueError(
            "verdict is written by deskops review dispose (GC03); a new review is a new document"
        )
    payload = read_doc(path, model)
    payload[field_name] = _parse_field_value(model, field_name, raw_value)
    write_doc(root, path, model, payload)
    return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)


# ---------------------------------------------------------------- registry
def registered_repositories(root: Path) -> list[dict[str, Any]]:
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    repositories = []
    for path in sorted(registry_dir.glob("repo-*.md")):
        try:
            repositories.append(read_doc(path, RepositoryDoc))
        except Exception as e:
            print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
            continue
    return repositories


def repository_root(root: Path, repository: dict[str, Any]) -> Path:
    repo_path = Path(str(repository["path"]))
    if repo_path.is_absolute():
        return repo_path.resolve()
    return (root / repo_path).resolve()


def _resolve_repo_board_task_path(repo_root: Path, task_ref: str) -> Path | None:
    tasks_root = (repo_root / "desk" / "tasks").resolve()
    task_path = Path(task_ref)
    if not task_path.is_absolute():
        task_path = repo_root / task_path
    task_path = task_path.resolve()
    try:
        task_path.relative_to(tasks_root)
    except ValueError:
        return None
    if not task_path.name.startswith("task-") or task_path.suffix != ".md":
        return None
    if not task_path.is_file():
        return None
    return task_path


def _task_route_summary(task_path: Path) -> dict[str, str]:
    text = task_path.read_text(encoding="utf-8")
    payload: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                frontmatter = None
            if isinstance(frontmatter, dict):
                payload = frontmatter
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), task_path.stem)
    legacy_status = next((line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Status:")), "unknown")
    task_id = str(payload.get("id") or task_path.stem)
    if not task_id.startswith("task-"):
        raise ValueError(f"Routed task id must start with 'task-': {task_id}")
    return {
        "id": task_id,
        "status": str(payload.get("status") or legacy_status),
        "title": title,
    }


def list_repo_task_routes(root: Path) -> list[RepoTaskRoute]:
    routes: list[RepoTaskRoute] = []
    for repository in registered_repositories(root):
        repo_root = repository_root(root, repository)
        board_path = repo_root / "desk" / "tasks" / "Board.md"
        if not board_path.exists():
            continue
        try:
            board_payload = read_doc(board_path, BoardDoc)
        except Exception:
            continue
        for task_ref in board_payload.get("tasks") or []:
            task_path = _resolve_repo_board_task_path(repo_root, str(task_ref))
            if task_path is None:
                continue
            try:
                summary = _task_route_summary(task_path)
            except (OSError, UnicodeDecodeError, ValueError):
                continue
            routes.append(
                RepoTaskRoute(
                    repo_id=str(repository["id"]),
                    repo_root=repo_root,
                    task_id=summary["id"],
                    task_path=task_path,
                    board_path=board_path,
                    title=summary["title"],
                    status=summary["status"],
                )
            )
    return routes

FILE:deskops/cli/commands/message.py
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Any

import yaml
from sldb.cli.model_utils import registered_model
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.layout import project_root

from deskops import doc_io
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.config import DeskConfig
from deskops.identity import EcosystemIdentity
from deskops.identity import UNKNOWN_PROJECT_IDENTITY
from deskops.identity import find_context_root
from deskops.identity import find_local_store


def track_document(store, root, idx, model_type, entry, path, note_name, resolver, pythonpath):
    """Compatibility seam: the old positional sldb call signature delegates to doc_io."""
    doc_io.track(root, path, model_type, name=note_name, pythonpath=pythonpath)


def untrack_document(store, document, pythonpath=None):
    """Compatibility seam: untrack through doc_io instead of the sldb CLI class."""
    doc_io.untrack(project_root(Path(store)), document, pythonpath=pythonpath)


from deskops.models import InboxNoteDoc
from deskops.errors import UsageError


class MessageCLI:
    """Send, list, read, or acknowledge cross-desk messages.

    Canonical surface is `deskops message {send|list|read|ack}`. The legacy
    `deskops inbox` flag grammar routes through `_run_legacy` for backward
    compatibility.
    """

    def run(self, args: Any) -> int:
        try:
            if getattr(args, "message_command", None) is not None:
                return self._run_message_command(args)
            return self._run_legacy(args)
        except (SLDBStoreError, SLDBValidationError, ValueError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )

    def _run_message_command(self, args: Any) -> int:
        subcmd = args.message_command
        if subcmd == "send":
            args.message = args.body
            return self._deliver_note(args)
        if subcmd == "list":
            return self._list_notes(args)
        if subcmd == "read":
            args.show = args.selector
            return self._show_note(args)
        if subcmd == "ack":
            args.ack = args.selector
            return self._ack_note(args)
        return render_error(
            f"Unknown message command: {subcmd}",
            getattr(args, "format", "text"),
            type_name="DomainError",
        )

    def _run_legacy(self, args: Any) -> int:
        if getattr(args, "list", False):
            return self._list_notes(args)
        if getattr(args, "show", None):
            return self._show_note(args)
        if getattr(args, "ack", None):
            return self._ack_note(args)
        if not getattr(args, "message", None):
            return render_error(
                "Provide a message or use send/list/read/ack.",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )
        return self._deliver_note(args)

    def _deliver_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        inbox_dir = desk_root / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        created_at = datetime.now()
        title = args.title.strip() if args.title else self._derive_title(args.message)
        slug = self._slug(title)
        path = inbox_dir / f"{created_at.strftime('%Y%m%d-%H%M%S')}-{args.kind}-{slug}.md"
        sender_project = self._sender_project(args)
        payload = {
            "kind": args.kind,
            "sender_project": sender_project,
            "target_project": target_project,
            "created_at": created_at.isoformat(timespec="seconds"),
            "status": "open",
            "title": title,
            "body": args.message.strip(),
        }
        rendered = render_model_markdown(InboxNoteDoc, payload) + "\n"
        # Validate before writing: a note that cannot be read back should never
        # reach the target's inbox.
        valid, details = validate_model_input_roundtrip(InboxNoteDoc, rendered)
        if not valid:
            raise SLDBValidationError("Message failed validation", details)

        path.write_text(rendered, encoding="utf-8")

        # Tracking is a courtesy to the target's doctor. A foreign desk may keep
        # its models in a package this process cannot import, which must not turn
        # a delivered note into a reported failure.
        tracked_name = None
        try:
            tracked_name = self._verify_and_track_note(args, path, desk_root)
        except Exception as exc:
            print(
                f"Warning: delivered to {path} but could not track it in that store: {exc}",
                file=sys.stderr,
            )
        result = {
            "sender_project": sender_project,
            "target_project": target_project,
            "path": str(path),
            "tracked_name": tracked_name,
            "verified": tracked_name is not None,
        }
        return self._print_delivery_result(result, args.format)

    def _list_notes(self, args: Any) -> int:
        notes = self._iter_notes(self._desk_root(args))[: args.limit]
        payload = [self._note_summary(path) for path in notes]
        return self._print(payload, args.format, key="notes")

    def _show_note(self, args: Any) -> int:
        note = self._resolve_note(self._desk_root(args), args.show)
        if note is None:
            return render_error(
                f"Unknown message: {args.show}",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )
        payload = self._note_detail(note)
        return self._print(payload, args.format)

    def _ack_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        note = self._resolve_note(desk_root, args.ack)
        if note is None:
            return render_error(
                f"Unknown message: {args.ack}",
                getattr(args, "format", "text"),
                type_name="DomainError",
            )

        payload = extract_model_data(InboxNoteDoc, note.read_text(encoding="utf-8"))
        if payload.get("status") == "closed":
            raise ValueError(f"Message '{note.stem}' is already acknowledged.")

        acknowledged_at = datetime.now().isoformat(timespec="seconds")
        payload["status"] = "closed"
        payload["target_project"] = payload.get("target_project") or target_project
        payload["acknowledged_by"] = target_project
        payload["acknowledged_at"] = acknowledged_at
        original = note.read_text(encoding="utf-8")
        note.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
        try:
            tracked_name = self._verify_and_track_note(args, note, desk_root)
        except Exception:
            # Keep the note and the store agreeing when the ack cannot be tracked.
            note.write_text(original, encoding="utf-8")
            raise
        result = {
            "id": note.stem,
            "path": str(note),
            "status": "closed",
            "target_project": payload["target_project"],
            "acknowledged_by": target_project,
            "acknowledged_at": acknowledged_at,
            "tracked_name": tracked_name,
            "verified": True,
        }
        return self._print_ack_result(result, args.format)

    def _desk_root(self, args: Any) -> Path:
        if getattr(args, "desk_root", None):
            return Path(args.desk_root).resolve()

        if getattr(args, "repo", None):
            return self._resolve_repo_desk(args.repo, args.store, args.pythonpath)

        if getattr(args, "root", None):
            return (Path(args.root).resolve() / "desk").resolve()

        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()

        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()

        return (Path.cwd() / "desk").resolve()

    def _resolve_target(self, args: Any) -> tuple[str, Path]:
        desk_root = self._desk_root(args)
        repo_root = desk_root.parent.resolve()
        config = DeskConfig.load(desk_root) if desk_root.exists() else DeskConfig()

        target_project = None
        ecosystem = self._target_ecosystem(args, repo_root)
        if ecosystem is not None:
            target_project = ecosystem.what_repository_am_i_in(
                repo_root,
                require_registry_match=True,
                allow_unregistered=True,
                default_to_directory_name=True,
            )
        if target_project is None:
            config_identity = (config.project_identity or UNKNOWN_PROJECT_IDENTITY).strip() or UNKNOWN_PROJECT_IDENTITY
            target_project = (
                config_identity if config_identity != UNKNOWN_PROJECT_IDENTITY else repo_root.name
            )

        if config.project_identity.strip() in {"", UNKNOWN_PROJECT_IDENTITY}:
            print(
                f"Warning: target desk '{desk_root}' has no project_identity; "
                f"resolved it as '{target_project}' from its directory or registry.",
                file=sys.stderr,
            )
        return target_project, desk_root

    def _target_ecosystem(self, args: Any, repo_root: Path) -> EcosystemIdentity | None:
        """The ecosystem anchored at the target repo, never the sender's."""
        target_store = find_local_store(repo_root)
        if target_store is None and args.store:
            candidate = Path(args.store).resolve()
            if project_root(candidate).resolve() == repo_root:
                target_store = candidate
        if target_store is None:
            return None
        try:
            return EcosystemIdentity(str(target_store))
        except SLDBStoreError:
            return None

    def _sender_ecosystem(self) -> EcosystemIdentity | None:
        """The sender's own ecosystem; the target registry must never decide it."""
        try:
            return EcosystemIdentity(None)
        except SLDBStoreError:
            return None

    def _resolve_repo_desk(self, repo_name: str, store_arg: str | None, pythonpath: str | None) -> Path:
        _ = pythonpath
        return EcosystemIdentity(store_arg).how_do_i_find_another(repo_name)

    def _note_store_context(self, args: Any, desk_root: Path) -> tuple[Path, Path] | None:
        """The store that owns the target desk, or None when its repo has no store.

        ``--store`` may still describe the sender's store (for example with
        ``--to``/``--repo``), so it is honored only when it belongs to the
        target repo. The sender's store is never a fallback for the target.
        """
        repo_root = desk_root.parent.resolve()
        if args.store:
            store_path, root = get_store_context(args.store)
            if root.resolve() == repo_root:
                return store_path, root
        store_path = repo_root / ".sldb"
        if not store_path.is_dir():
            return None
        return store_path, repo_root

    def _iter_notes(self, desk_root: Path) -> list[Path]:
        inbox_dir = desk_root / "inbox"
        if not inbox_dir.exists():
            return []
        return sorted(inbox_dir.glob("*.md"), reverse=True)

    def _resolve_note(self, desk_root: Path, raw: str) -> Path | None:
        notes = self._iter_notes(desk_root)
        exact = next((path for path in notes if raw in {path.name, path.stem}), None)
        if exact is not None:
            return exact
        lowered = raw.lower()
        matches = [path for path in notes if lowered in path.stem.lower()]
        if len(matches) > 1:
            listing = ", ".join(path.stem for path in sorted(matches))
            raise UsageError(
                f"Ambiguous message selector '{raw}' matches {len(matches)} notes: {listing}. "
                "Pass the full filename or stem."
            )
        return matches[0] if matches else None

    def _note_summary(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, _ = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "kind": frontmatter.get("kind", ""),
            "sender_project": frontmatter.get("sender_project", ""),
            "target_project": frontmatter.get("target_project", ""),
            "status": frontmatter.get("status", ""),
            "created_at": frontmatter.get("created_at", ""),
            "acknowledged_by": frontmatter.get("acknowledged_by"),
            "acknowledged_at": frontmatter.get("acknowledged_at"),
            "title": title,
        }

    def _note_detail(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, body = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "title": title,
            "body": body,
            **frontmatter,
        }

    def _parse_note(self, path: Path) -> tuple[dict[str, str | None], str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, str | None] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else path.stem
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return frontmatter, title, content

    def _print(self, payload: Any, fmt: str, key: str | None = None) -> int:
        data = {key: payload} if key else payload
        if key == "notes":
            return render(data, fmt, lambda _data: self._format_note_list(payload))
        return render(data, fmt, lambda _data: self._format_note_detail(payload))

    @staticmethod
    def _format_note_list(payload: list[dict[str, Any]]) -> str:
        if not payload:
            return "No messages."
        return "\n".join(
            f"{item['id']} | {item['kind']} | {item['sender_project']} -> {item['target_project']} | {item['status']} | {item['title']}"
            for item in payload
        )

    @staticmethod
    def _format_note_detail(payload: dict[str, Any]) -> str:
        lines = [f"# {payload['title']}", ""]
        for meta in (
            "kind",
            "sender_project",
            "target_project",
            "created_at",
            "status",
            "acknowledged_by",
            "acknowledged_at",
            "path",
        ):
            if meta in payload and payload[meta] not in {None, ""}:
                lines.append(f"{meta}: {payload[meta]}")
        lines.append("")
        lines.append(payload.get("body", ""))
        return "\n".join(lines)

    def _print_delivery_result(self, payload: dict[str, Any], fmt: str) -> int:
        def text(data: dict[str, Any]) -> str:
            lines = [
                "Delivered message "
                f"from {data['sender_project']} to {data['target_project']} at {data['path']}"
            ]
            if data.get("tracked_name"):
                lines.append(f"Tracked '{data['tracked_name']}'")
            else:
                lines.append("Not tracked in the target store (see the warning above).")
            return "\n".join(lines)

        return render(payload, fmt, text)

    def _print_ack_result(self, payload: dict[str, Any], fmt: str) -> int:
        def text(data: dict[str, Any]) -> str:
            lines = [
                f"Acknowledged {data['id']} as {data['status']} "
                f"by {data['acknowledged_by']} at {data['acknowledged_at']}",
                f"Path: {data['path']}",
            ]
            if data.get("tracked_name"):
                lines.append(f"Tracked '{data['tracked_name']}'")
            else:
                lines.append("Not tracked in the target store (see the warning above).")
            return "\n".join(lines)

        return render(payload, fmt, text)

    def _derive_title(self, message: str) -> str:
        first = message.strip().splitlines()[0] if message.strip() else "Message"
        return first[:72]

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "note"

    def _sender_project(self, args: Any) -> str:
        sender_root = find_context_root()
        ecosystem = self._sender_ecosystem()
        config_identity = self._config_identity(sender_root)
        explicit = getattr(args, "sender", None)

        if explicit:
            registered = ecosystem is not None and any(
                entry.id == explicit for entry in ecosystem.entries
            )
            if registered or config_identity == explicit:
                return explicit
            if config_identity is None and (ecosystem is None or not ecosystem.entries):
                # No sender registry or config to check against; honor the explicit id.
                return explicit
            raise SLDBStoreError(
                f"Sender identity '{explicit}' is not the sender repo's identity "
                f"'{config_identity or UNKNOWN_PROJECT_IDENTITY}' and is not in its registry."
            )

        if ecosystem is not None:
            sender_project = ecosystem.what_repository_am_i_in(
                sender_root,
                require_registry_match=False,
                allow_unregistered=True,
            )
            if sender_project is not None:
                return sender_project
        if config_identity is not None:
            return config_identity
        raise SLDBStoreError(
            f"Unable to resolve sender identity for '{sender_root}'. Use --sender or register the repository canonically."
        )

    @staticmethod
    def _config_identity(repo_root: Path) -> str | None:
        desk_root = repo_root / "desk"
        if not desk_root.exists():
            return None
        identity = (DeskConfig.load(desk_root).project_identity or UNKNOWN_PROJECT_IDENTITY).strip()
        return identity if identity not in {"", UNKNOWN_PROJECT_IDENTITY} else None

    def _verify_and_track_note(self, args: Any, path: Path, desk_root: Path) -> str | None:
        context = self._note_store_context(args, desk_root)
        if context is None:
            print(
                f"Warning: no .sldb store at {desk_root.parent / '.sldb'}; "
                f"not tracking {path.name}.",
                file=sys.stderr,
            )
            return None
        store_path, root = context
        model_type, _entry, _idx = registered_model(store_path, "InboxNoteDoc", args.pythonpath)

        rendered = path.read_text(encoding="utf-8")
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Message failed validation", details)

        note_name = path.stem

        def track() -> None:
            track_document(
                store_path,
                root,
                _idx,
                model_type,
                _entry,
                path,
                note_name,
                None,
                args.pythonpath,
            )

        try:
            track()
        except SLDBStoreError as exc:
            if "already tracked" not in str(exc):
                raise
            # Re-sign an existing tracking entry instead of tracking it twice.
            untrack_document(store_path, note_name, args.pythonpath)
            track()
        return note_name

    def _store_context(self, args: Any) -> tuple[Path, Path] | None:
        if args.store:
            return get_store_context(args.store)
        local_store = find_local_store()
        if local_store is None:
            return None
        return local_store, project_root(local_store)

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
        for path in result.rewritten_paths:
            print(f"Rewrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import write_lifecycle_graph

            for change in write_lifecycle_graph(target_path):
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

        from deskops import lifecycle

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

        # The lifecycle graph's documents are managed seeds: a desk's copy that differs from the
        # package's is rewritten. A missing one is written with the rest of the scaffold.
        scaffold_plan = seed_desk(root, apply=False, restore_managed=True) if desk_dir.exists() else None
        lifecycle_rewrites = (
            [path.relative_to(root).as_posix() for path in scaffold_plan.rewritten_paths] if scaffold_plan else []
        )
        lifecycle_missing = bool(scaffold_plan) and any(
            path.relative_to(root).as_posix().startswith("desk/lifecycle/") for path in scaffold_plan.created_paths
        )

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

        if not lifecycle_rewrites and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not moved_contracts and not pending_local_types and not pending_migration:
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
        if lifecycle_rewrites:
            print(f"- Lifecycle documents to rewrite: {', '.join(lifecycle_rewrites)}")
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

        if missing_desk_files or lifecycle_rewrites or lifecycle_missing:
            scaffold = seed_desk(root, restore_managed=True)
            if missing_desk_files:
                print("Scaffolded missing desk structure.")
            for change in lifecycle.seed_changes(root, scaffold):
                print(f"Lifecycle graph: {change}")

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

        # Recomputed: the scaffold may have written declared documents (the lifecycle graph).
        untracked_docs = pending_desk_includes(root) if desk_dir.exists() and store_dir.exists() else []
        if untracked_docs:
            declared_models = {path: model_name for model_name, path in untracked_docs}
            try:
                tracked_paths = apply_desk_includes(root)
            except Exception as exc:
                print(f"Error: could not track the declared desk documents: {exc}")
                return 1
            for path in tracked_paths:
                model_name = declared_models.get(path, "its declared model")
                line = lifecycle.tracked_line(model_name, path)
                print(f"Lifecycle graph: {line}" if line else f"Tracked {path} as {model_name}.")

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

        return 0

FILE:deskops/cli/commands/repo.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from sldb.cli.model_utils import registered_model
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.layout import project_root

from deskops import doc_io
from deskops.identity import load_repository_registry, EcosystemIdentity
from deskops.identity import find_local_store


def track_document(store, root, idx, model_type, entry, path, note_name, resolver, pythonpath):
    """Compatibility seam: the old positional sldb call signature delegates to doc_io."""
    doc_io.track(root, path, model_type, name=note_name, pythonpath=pythonpath)


class RepoCLI:
    """Handle repository registration and discovery."""

    def run(self, args: Any) -> int:
        if args.repo_command == "register":
            return self.register(args)
        if args.repo_command == "whoami":
            return self.whoami(args)
        if args.repo_command == "remove":
            return self.remove(args)
        return 1

    def register(self, args: Any) -> int:
        name = args.name
        path = args.path_option or args.path
        if not path:
            print("Error: repository path is required. Use 'deskops repo register <name> --path <abs>' or provide the positional path.")
            return 1
        repo_id = args.id or self._slug(name)
        description = args.description or f"Repository for {name}."
        tags = [t.strip() for p in (args.tags or "").split(",") if (t := p.strip())]

        payload = {
            "name": name,
            "id": repo_id,
            "path": path,
            "status": "active",
            "description": description,
            "tags": tags,
        }

        # Preflight: resolve store context and model before any mutation
        try:
            store_path, root = self._store_context(args)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        try:
            model_type, entry, idx = registered_model(
                store_path, "RepositoryDoc", args.pythonpath
            )
        except SLDBStoreError:
            print("Error: RepositoryDoc model is not registered in the store.")
            print("Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>")
            return 1
        except (FileNotFoundError, OSError) as e:
            print(f"Error: cannot read store at {store_path}: {e}")
            return 1

        desk_root = self._desk_root(args)
        registry_dir = desk_root / "registry"
        filename = f"repo-{repo_id}.md"
        output_path = registry_dir / filename

        if output_path.exists():
            print(f"Error: Repository file already exists at {output_path}")
            return 1

        try:
            existing_entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        resolved_repo_root = self._resolve_registered_root(root, path)
        for existing_entry in existing_entries:
            if existing_entry.id == repo_id:
                print(
                    f"Error: Repository id '{repo_id}' is already registered by {existing_entry.source_path}."
                )
                return 1
            if existing_entry.repo_root is not None and resolved_repo_root == existing_entry.repo_root:
                print(
                    "Error: Repository root "
                    f"'{resolved_repo_root}' is already registered as '{existing_entry.id}' by {existing_entry.source_path}."
                )
                return 1

        from sldb.store.io import load_models_index, load_documents_index
        models_idx = load_models_index(root / entry.models_index)
        docs_idx = load_documents_index(root / models_idx.documents_index)
        if any(d.name == f"repo-{repo_id}" for d in docs_idx.documents):
            print(f"Error: Repository repo-{repo_id} is already registered in the store.")
            return 1

        rendered = render_model_markdown(model_type, payload)
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            print("Error: Repository registration failed validation.")
            for issue in details:
                print(f"  - {issue}")
            return 1

        # All prerequisites verified — mutate filesystem
        registry_dir.mkdir(parents=True, exist_ok=True)
        
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")

        # Track in store
        track_document(
            store_path,
            root,
            idx,
            model_type,
            entry,
            output_path,
            f"repo-{repo_id}",
            None,
            args.pythonpath,
        )
        print(f"Tracked 'repo-{repo_id}'")

        return 0

    def remove(self, args: Any) -> int:
        root = Path(args.root).resolve()
        desk_root = root / "desk"
        try:
            entries = load_repository_registry(desk_root, root)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1

        selector = args.selector
        matches = [
            entry
            for entry in entries
            if selector in {entry.id, entry.source_path.stem, f"repo-{entry.id}"}
        ]
        if not matches:
            known = ", ".join(sorted(entry.id for entry in entries)) or "(none)"
            print(f"Error: Repository '{selector}' is not registered. Registered ids: {known}")
            return 1
        if len(matches) > 1:
            paths = ", ".join(str(entry.source_path) for entry in matches)
            print(f"Error: Repository selector '{selector}' is ambiguous: {paths}")
            return 1

        entry = matches[0]
        with doc_io.DocTransaction(root) as transaction:
            transaction.delete(entry.source_path)
        print(entry.source_path)
        return 0

    def whoami(self, args: Any) -> int:
        try:
            project_id = EcosystemIdentity(args.store).what_repository_am_i_in(Path(args.root), require_registry_match=True)
        except SLDBStoreError as e:
            print(f"Error: {e}")
            return 1
        print(project_id)
        return 0

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "repo"

    def _desk_root(self, args: Any) -> Path:
        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()
        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()
        return (Path.cwd() / "desk").resolve()

    def _store_context(self, args: Any) -> tuple[Path, Path]:
        if args.store:
            try:
                return get_store_context(args.store)
            except (SLDBStoreError, FileNotFoundError, OSError) as e:
                raise SLDBStoreError(str(e))
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No store found to anchor the registry.")
        return local_store, project_root(local_store)

    def _resolve_registered_root(self, ecosystem_root: Path, repo_path: str) -> Path:
        candidate = Path(repo_path)
        if candidate.is_absolute():
            return candidate.resolve()
        return (ecosystem_root / candidate).resolve()

FILE:deskops/runtime/scion.py
"""Project a RoleDoc + its RuntimeProfileDoc onto a Scion agent template.

Scion (github.com/GoogleCloudPlatform/scion) launches an agent from a
*template* directory: ``scion-agent.yaml`` plus the prose files it points at
(``system-prompt.md``, ``agents.md``). A template describes the job, never the
environment: the harness-config decides image, auth and concrete model, and
the template only carries a portable model *size alias*.

This module is the Scion counterpart of ``materializers.roles`` (pi agent
files): the RoleDoc stays the tracked source and the template is a
materialization. Pure except for the two writers at the bottom; it never
calls ``scion``. Dispatch (``scion start``) is the supervisor's gesture.

Nothing is dropped silently: every RoleDoc setting the template cannot carry
is written into ``scion-agent.yaml`` as a comment that names the setting and
why it was left out.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from deskops import doc_io
from deskops.materializers.roles import iter_role_doc_paths, load_role_doc
from deskops.materializers.runtime_profiles import build_agent_spec_args, load_runtime_profiles
from deskops.models import RunDoc

#: RuntimeProfileDoc.kind -> Scion harness-config name. Only ``claude`` and
#: ``gemini`` ship installed; the rest need ``scion harness-config install``
#: (``pi`` needs a bundle of our own; see the scion fork's desk).
HARNESS_BY_KIND: dict[str, str] = {
    "claude": "claude",
    "codex": "codex",
    "antigravity": "antigravity",
    "gemini": "gemini",
    "opencode": "opencode",
    "pi": "pi",
}

#: Scion's portable model size aliases (``local/templates.md``).
MODEL_SIZE_ALIASES: tuple[str, ...] = ("small", "medium", "large", "extra-large")

#: ``medium`` by default: the owner's rule is that subagents never run on the
#: largest tier. Pass ``model_alias`` to change it per template.
DEFAULT_MODEL_ALIAS = "medium"
DEFAULT_MAX_TURNS = 200
DEFAULT_MAX_DURATION = "2h"
#: A coordinator waits blocked on its children and Scion counts that idle time,
#: so the executor's limit would kill it mid-review.
COORDINATOR_MAX_TURNS = 1000
COORDINATOR_MAX_DURATION = "24h"

#: Without this the Hub picks whichever credential it finds; a stale
#: ``CLAUDE_AUTH`` file beats a project token and the agent is not logged in.
HARNESS_AUTH: dict[str, str] = {"claude": "oauth-token"}

TEMPLATE_FILES: tuple[str, ...] = ("scion-agent.yaml", "system-prompt.md", "agents.md")


def pick_harness_config(runtime_kind: str) -> str:
    """Scion harness-config name for a RuntimeProfileDoc kind."""
    try:
        return HARNESS_BY_KIND[runtime_kind]
    except KeyError as exc:
        known = ", ".join(sorted(HARNESS_BY_KIND))
        raise ValueError(f"no Scion harness-config is known for runtime kind '{runtime_kind}' (known: {known})") from exc


def find_role_doc(root: Path, role_id: str) -> tuple[Path, dict[str, Any]]:
    """Locate a tracked RoleDoc by ``id`` or ``name`` (``role-x`` and ``x`` both resolve)."""
    wanted = {role_id, f"role-{role_id}"}
    for path in iter_role_doc_paths(root):
        role_doc = load_role_doc(path)
        if role_doc.get("id") in wanted or role_doc.get("name") in wanted:
            return path, role_doc
    raise ValueError(f"no RoleDoc with id or name '{role_id}' under {root / 'desk' / 'roles'}")


def template_dir_for(root: Path, role_doc: dict[str, Any], out_dir: Path | None = None) -> Path:
    """Default destination: ``<root>/.scion/templates/<role-name>/`` (a Scion project template)."""
    if out_dir is not None:
        return out_dir
    name = str(role_doc.get("name") or role_doc.get("id") or "").strip()
    if not name:
        raise ValueError("Role doc is missing a name")
    return root / ".scion" / "templates" / name


def _yaml_scalar(value: Any) -> str:
    """One-line YAML for a scalar or list: JSON is a YAML subset, and it never wraps."""
    return json.dumps(value, ensure_ascii=False)


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    """Role settings that only exist as CLI flags (today: ``tools``).

    Model and system prompt have template fields of their own, the session is
    Scion's, and the profile's ``extra_args`` describe a non-interactive
    invocation (``--print``) that Scion must not inherit. What is left is the
    tools vocabulary, folded through the profile's own flag.
    """
    stripped = dict(profile)
    stripped.update(model_flag="", fallback_models_flag="", system_prompt_flag="", session_flag="", extra_args=[])
    return list(build_agent_spec_args(role_doc, stripped))


def scion_template_files(
    role_doc: dict[str, Any],
    profile: dict[str, Any],
    *,
    harness: str,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    source: str | None = None,
    mode: str | None = None,
) -> dict[str, str]:
    """Render the three template files as ``{filename: text}``.

    ``source`` is a human-readable provenance line (role path + runtime path)
    written at the top of ``scion-agent.yaml``. ``mode`` picks the
    ``agents.md``: ``executor`` (one bounded task) or ``coordinator`` (owns a
    desk); by default a role whose name says supervisor/coordinator gets the
    coordinator instructions.
    """
    if mode not in (None, "executor", "coordinator"):
        raise ValueError(f"mode must be executor or coordinator, got '{mode}'")
    if model_alias not in MODEL_SIZE_ALIASES:
        raise ValueError(f"model alias must be one of {MODEL_SIZE_ALIASES}, got '{model_alias}'")
    if harness not in HARNESS_BY_KIND.values():
        raise ValueError(f"unknown Scion harness-config '{harness}' (known: {', '.join(sorted(set(HARNESS_BY_KIND.values())))})")

    role_name = str(role_doc.get("name") or role_doc.get("id") or "role")
    resolved_mode = mode or ("coordinator" if "supervisor" in role_name or "coordinator" in role_name else "executor")
    description = str(role_doc.get("description") or "").strip()
    body = str(role_doc.get("body") or "").strip()
    unsupported = set(profile.get("unsupported_role_fields") or [])

    lines: list[str] = []
    lines.append(f"# Generated by `deskops runtime template {role_doc.get('id') or role_name} --harness {harness}`.")
    if source:
        lines.append(f"# Source: {source}")
    lines.append("# Edit the RoleDoc / RuntimeProfileDoc and regenerate; do not edit this file by hand.")
    lines.append('schema_version: "1"')
    lines.append(f"description: {_yaml_scalar(description or role_name)}")
    lines.append("agent_instructions: agents.md")
    lines.append("system_prompt: system-prompt.md")
    lines.append(f"default_harness_config: {harness}")

    concrete_model = role_doc.get("model")
    if concrete_model:
        lines.append(
            f"# RoleDoc.model is {_yaml_scalar(concrete_model)}. A template carries a portable size alias; "
            f"the harness-config '{harness}' resolves it to a concrete model (Scion local/templates.md)."
        )
    lines.append(f"model: {model_alias}")
    if harness in HARNESS_AUTH:
        lines.append(f"auth_selectedType: {HARNESS_AUTH[harness]}")
    coordinator = resolved_mode == "coordinator"
    lines.append(f"max_turns: {COORDINATOR_MAX_TURNS if coordinator else DEFAULT_MAX_TURNS}")
    lines.append(f"max_duration: {COORDINATOR_MAX_DURATION if coordinator else DEFAULT_MAX_DURATION}")

    command_args = _command_args(role_doc, profile)
    if command_args:
        lines.append("# RoleDoc.tools, folded through the runtime profile's tools flag:")
        lines.append(f"command_args: {_yaml_scalar(command_args)}")

    omitted: list[str] = []
    fallback_models = role_doc.get("fallback_models") or []
    if fallback_models:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "fallback_models" in unsupported
            else "a Scion template has no field for it"
        )
        omitted.append(f"fallback_models: {_yaml_scalar(list(fallback_models))}  ({reason})")
    tools = role_doc.get("tools") or []
    if tools and not command_args:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "tools" in unsupported
            else f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' declares no tools_flag"
        )
        omitted.append(f"tools: {_yaml_scalar(list(tools))}  ({reason})")
    for key in ("system_prompt_mode", "inherit_project_context", "inherit_skills", "default_context"):
        if key in role_doc and role_doc.get(key) not in (None, ""):
            omitted.append(f"{key}: {_yaml_scalar(role_doc[key])}  (pi agent setting; Scion templates have no equivalent)")
    if omitted:
        lines.append("# Omitted on purpose (nothing is dropped silently):")
        lines.extend(f"#   {item}" for item in omitted)

    agent_yaml = "\n".join(lines) + "\n"
    system_prompt = (body or f"# {role_name}") + "\n"
    if resolved_mode == "coordinator":
        agents_md = _render_coordinator_agents_md(role_name, harness, task_repo)
    else:
        agents_md = _render_agents_md(role_name, harness, task_repo)
    return {"scion-agent.yaml": agent_yaml, "system-prompt.md": system_prompt, "agents.md": agents_md}


def _render_coordinator_agents_md(role_name: str, harness: str, task_repo: str | None) -> str:
    """Instructions for the long-lived agent that owns one desk.

    One coordinator per desk is the shape the owner chose (2026-10-29): it is
    the only writer of that ``desk/``, it dispatches short-lived executors
    through ``scion start``, waits blocked, reviews their evidence and closes.
    What needs the owner is never decided here.
    """
    repo = task_repo or "<repo>"
    return (
        f"# {role_name}: coordinator of the `{repo}` desk on Scion ({harness})\n"
        "\n"
        "You are the long-lived coordinator of ONE desk. The desk, not your memory, holds the state; every time you\n"
        "wake up, read it again. You are the only agent that writes `/workspace/" + repo + "/desk/`.\n"
        "\n"
        "## Each time you wake up\n"
        "\n"
        "```bash\n"
        f"cd /workspace/{repo}\n"
        "deskops show board Board --root .          # active tasks and their nodes\n"
        "deskops message list --root .              # inbox: incoming notes\n"
        "scion list                                 # executors you already dispatched\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## What you do\n"
        "\n"
        "1. **Triage the inbox.** Informational or duplicate -> `deskops message ack`. Bounded work for this repo ->\n"
        "   `deskops promote inbox-to-drawer-task`, then `deskops add task --from-drawer ...` when it is next.\n"
        "   Work for another repo -> `deskops message send --to <repo>`. A decision only the owner can make ->\n"
        "   leave the note open and say so with `sciontool status ask_user \"<the question>\"`.\n"
        "2. **Dispatch one executor per active task that has none.** Build the prompt from `deskops show task <id>`:\n"
        "   the task id, the repo, what to verify or implement, the validation command, the evidence files, and the\n"
        "   three prohibitions (no desk/ writes, no closeout, no commits unless the task says so). Then:\n"
        "   `scion start " + repo + "-<short-slug> \"<prompt>\" --type deskops-executor` and record it:\n"
        "   `deskops runtime template role-deskops-executor --harness " + harness + " --root /workspace/deskops --out /tmp/t"
        " --task <id> --agent " + repo + "-<short-slug> --task-root /workspace/" + repo + "`.\n"
        "3. **One executor per repository at a time.** Agents share the checkout; two writers on the same repo\n"
        "   collide in git. Different repositories may run in parallel.\n"
        "4. **Wait properly.** After dispatching: `sciontool status blocked \"waiting on <agent>\"`. Scion wakes you\n"
        "   when the child completes, stalls or asks for input. Do not poll in a loop.\n"
        "5. **Review before closing.** Read `runs/subagents/<run>/result-summary.md` and `validation.log`; re-run the\n"
        "   task's validation yourself; check `git status` shows only what the task scoped. Then\n"
        "   `deskops advance task <id>` through its gates and `deskops closeout commit --task <id> --run-dir <run>\n"
        "   --paths <files>`. If evidence is missing, message the executor or dispatch a new one; never fabricate it.\n"
        "   Then `scion stop <agent>`: an executor that reported completed keeps its container alive until stopped,\n"
        "   and Scion counts that idle time against its duration limit.\n"
        "6. **Do not push.** Commits stay local; the owner pushes. Report what you committed.\n"
        "7. **Report.** When the desk has nothing dispatchable left, `sciontool status task_completed \"<one-line summary>\"`.\n"
        "\n"
        "## Never\n"
        "\n"
        "- Never edit a tracked desk document by hand; always the `deskops` / `sldb` CLIs (`--help` first).\n"
        "- Never write outside `/workspace/" + repo + "` except `runs/` evidence and inbox notes sent through `deskops message send`.\n"
        "- Never decide for the owner: releases, policy, model design, anything a note marks as theirs.\n"
        "- Never answer an executor's question on the owner's behalf; surface it.\n"
    )


def _render_agents_md(role_name: str, harness: str, task_repo: str | None) -> str:
    repo_line = (
        f"- Your task lives in the repository `{task_repo}` under `/workspace`. Write only there."
        if task_repo
        else "- Your task names its repository under `/workspace`. Write only there; the other repositories are context."
    )
    return (
        f"# {role_name} on Scion ({harness})\n"
        "\n"
        "You are a deskops executor running as a Scion agent. The desk, not your memory, holds the state.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"{repo_line}\n"
        "- One bounded task. Do not route the board, touch other tasks, or close the task yourself.\n"
        "- The CLIs are `deskops` and `sldb`; learn them with `--help`. Never edit a tracked desk document by hand.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        "deskops show board Board --root <repo>\n"
        "deskops show task <task-id> --root <repo>\n"
        "deskops next <task-id> --root <repo>\n"
        "git -C <repo> status --short --branch\n"
        "```\n"
        "\n"
        "## Evidence\n"
        "\n"
        "Make `<repo>/runs/subagents/<YYYYMMDD-HHMMSS>-<task-id>/` first and snapshot the state you start from;\n"
        "`deskops closeout commit --run-dir` refuses a run dir without `board.txt` and `git-status.txt`:\n"
        "\n"
        "```bash\n"
        "RUN_DIR=<repo>/runs/subagents/$(date +%Y%m%d-%H%M%S)-<task-id>; mkdir -p \"$RUN_DIR\"\n"
        "deskops show board Board --root <repo> > \"$RUN_DIR/board.txt\"\n"
        "deskops show task <task-id> --root <repo> > \"$RUN_DIR/task.txt\"\n"
        "deskops next <task-id> --root <repo> > \"$RUN_DIR/next.txt\"\n"
        "git -C <repo> status --short --branch > \"$RUN_DIR/git-status.txt\"\n"
        "```\n"
        "\n"
        "- Then `validation.log` (the exact command and its exit code) and `result-summary.md`.\n"
        "- `result-summary.md` is the handoff: what you did, what you ran, what the supervisor must review.\n"
        "- Run the smallest relevant validation first.\n"
        "\n"
        "## When done\n"
        "\n"
        "- Leave the working tree committed or clearly described in `result-summary.md`; do not run `deskops closeout`.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`: Scion wakes the coordinator\n"
        "  on that status, not on `blocked`.\n"
    )


def materialize_scion_template(
    root: Path,
    role_id: str,
    *,
    harness: str | None = None,
    out_dir: Path | None = None,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    mode: str | None = None,
) -> Path:
    """Write the template for ``role_id`` and return its directory.

    The runtime profile is the one matching the role's ``kind`` unless
    ``harness`` names another installed kind; ``harness`` also decides
    ``default_harness_config``.
    """
    role_path, role_doc = find_role_doc(root, role_id)
    profiles = load_runtime_profiles(root)
    kind = harness or str(role_doc.get("kind") or "")
    profile = profiles.get(kind) or profiles.get(str(role_doc.get("kind") or ""))
    if profile is None:
        raise ValueError(f"no RuntimeProfileDoc for kind '{kind}' under {root / 'desk' / 'runtimes'}")
    harness_name = pick_harness_config(kind)
    source = f"{role_path.relative_to(root).as_posix()} + desk/runtimes/{profile.get('id', kind)}.md"
    files = scion_template_files(
        role_doc, profile, harness=harness_name, model_alias=model_alias, task_repo=task_repo, source=source, mode=mode
    )
    target = template_dir_for(root, role_doc, out_dir)
    target.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (target / name).write_text(text, encoding="utf-8")
    return target


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def record_scion_run(
    root: Path,
    *,
    task_id: str,
    role_id: str,
    kind: str,
    agent_slug: str,
    run_dir: str | None = None,
    outcome: str = "in_progress",
    summary: str = "",
) -> Path:
    """Write (and track, when the root has a store) a RunDoc for one Scion dispatch.

    The RunDoc lives at ``<run_dir>/run.md`` so the evidence directory and its
    record travel together. ``session_path`` carries ``scion://agent/<slug>``:
    the transcript is Scion's (``scion logs <slug>``), copied into ``run_dir``
    by the supervisor at closeout.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_dir = run_dir or f"runs/subagents/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{_slug(task_id)}"
    run_id = f"run-{_slug(agent_slug)}"
    payload = {
        "id": run_id,
        "title": f"Scion agent {agent_slug} on {task_id}",
        "summary": summary or f"Dispatched with `scion start {agent_slug}` from role {role_id} ({kind}).",
        "task_id": task_id,
        "role_id": role_id,
        "kind": kind,
        "run_dir": run_dir,
        "herdr_pane_id": "",
        "session_path": f"scion://agent/{agent_slug}",
        "session_sha256": "",
        "started_at": now,
        "ended_at": "" if outcome == "in_progress" else now,
        "outcome": outcome,
        "commit_sha": "",
        "tags": ["system:deskops", "runtime:scion"],
    }
    path = Path(run_dir) / "run.md"
    with doc_io.DocTransaction(root) as transaction:
        transaction.write(path, RunDoc, payload)
        transaction.track(path, RunDoc, name=run_id)
    return root / path

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
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False

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


def transitions_holding(root: Path, node: str, payload: dict[str, Any]) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False))


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).
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
    holding = transitions_holding(root, node, payload)
    if not holding:
        payload["current_node"] = node
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    payload.update(apply_effects(payload, transition.effects, model))
    history = payload.setdefault("history", [])
    if isinstance(history, list):
        history.append(transition.relation_type)
    target = COMPLETE if transition.terminal else transition.target
    payload["current_node"] = target
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


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds and restores one the desk changed
    (``workspace.seed_desk``), registers sldb's relation models when the store lacks them and
    tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        doc_io.init_relations_in(root, pythonpath=package_pythonpath())
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes

FILE:deskops/workspace.py
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
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
    #: Managed seeds whose bytes differed from the package's and were restored (the lifecycle graph).
    rewritten_paths: list[Path] = field(default_factory=list)

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths or self.rewritten_paths)


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

#: The declaration of the desk a repository gets; its ``file:`` seeds are relative to ``deskops/data/``
#: (``templates/`` for the desk's own files, ``lifecycle/`` for the lifecycle graph's documents).
DESK_DECLARATION_PATH = data_path("data", "desk_declaration.yaml")
DESK_DATA_PATH = data_path("data")
DESK_TEMPLATES_PATH = DESK_DATA_PATH / "templates"

#: The document seed whose ``system_prompt`` is code (``deskops.services.review.SYSTEM``), not
#: declaration data (CC36, f3).
_REVIEW_RUNTIME_SEED = "runtime-pi-deepseek-flash"


def desk_declaration(name: str) -> Any:
    """The desk declaration (``deskops/data/desk_declaration.yaml``) for a desk called ``name``.

    The ``folders`` and ``include`` rules are the file's; every seed comes back rendered as
    ``text`` with its ``mode``: ``file:`` templates read from ``deskops/data/`` and ``document:``
    payloads rendered through their deskops model, both with ``{desk_name}`` replaced. The bytes
    are the ones ``deskops init`` always wrote, and sldb only has to write them: its own
    ``document`` seed resolves the model from the store, which ``desk install`` and the first desk
    operation do not have yet. The lifecycle graph's seeds are ``managed``: a desk's copy that
    differs is rewritten.
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
        template = (DESK_DATA_PATH / seed.file).read_text(encoding="utf-8")
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


def seed_desk(target_path: Path, *, apply: bool = True, restore_managed: bool = False) -> DeskScaffoldResult:
    """Create the declared desk folders and seed files that are missing and, with
    ``restore_managed``, restore the managed ones that differ (``sldb.api.scaffold_store``).

    A desk's own files are ``if_missing`` seeds, so a desk that exists keeps them. The lifecycle
    graph's documents are ``managed``: ``deskops init`` and ``deskops desk update --apply`` restore
    a desk's copy that differs (``rewritten_paths``) and report it; every other scaffold (the first
    desk operation, ``doctor --repair``) only creates what is missing, so an edit to the desk's
    lifecycle is never undone silently. ``created_paths`` are the absolute paths of what was
    created, folders first and then seeds in declaration order; with ``apply=False`` nothing is
    written and both lists are what a run would do. A rewritten document the store tracks is
    reindexed (sldb's scaffold writes the file but does not rehash it).
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration
    from sldb.api import scaffold_store

    declaration = desk_declaration(target_path.name)
    if not restore_managed:
        declaration = StoreDeclaration(
            folders=declaration.folders,
            seeds=[Seed(path=seed.path, mode="if_missing", text=seed.text) for seed in declaration.seeds],
            include=declaration.include,
        )
    report = scaffold_store(target_path, declaration=declaration, apply=apply)
    if apply and report.rewritten and (target_path / ".sldb" / "core").exists():
        from deskops import doc_io
        from deskops.paths import package_pythonpath

        doc_io.update_store_indexes_in(target_path, pythonpath=package_pythonpath(), wait=False)
    return DeskScaffoldResult(
        created_paths=[target_path / relative for relative in report.created],
        rewritten_paths=[target_path / relative for relative in report.rewritten],
    )


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

FILE:deskops/bootstrap.py
from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

from sldb import StructuredNLDoc

from deskops import doc_io
from deskops import models as deskops_models
from deskops.paths import package_pythonpath


DESKOPS_STORE_LINK = "deskops"

#: Base classes that are never registered as models in a store.
BASE_MODEL_NAMES = frozenset({"PrimitiveDoc", "OperationalArtifactDoc"})

#: Every deskops model is inherited from the owner store by name and model ref.
MODEL_REFS = {
    name: f"deskops.models:{name}"
    for name in deskops_models.__all__
    if name not in BASE_MODEL_NAMES
    and isinstance(getattr(deskops_models, name, None), type)
    and issubclass(getattr(deskops_models, name), StructuredNLDoc)
}


class SLDBBootstrap:
    def ensure_sldb_available(self, *, allow_install: bool = False) -> int:
        """Check that sldb is importable.

        Only ``deskops bootstrap`` and ``deskops init`` may install it; every other
        command fails with the install hint instead of running pip behind the user's back.
        """
        if self._sldb_importable():
            if shutil.which("sldb") is None:
                print("sldb is importable but no shell entrypoint was found; using python -m sldb.")
            return 0

        if not allow_install:
            print(
                "Error: sldb is not installed. Run 'deskops bootstrap' or 'deskops init' to install it."
            )
            return 1

        install_path = self._resolve_sldb_checkout()
        if install_path is None:
            print("Error: sldb is not installed and no sibling checkout was found.")
            print(
                "Set DESKOPS_SLDB_PATH or keep the sibling checkout at ../sldb before running deskops init."
            )
            return 1
        print(f"Installing sldb from {install_path}...")
        try:
            self._run([
                sys.executable,
                "-m",
                "pip",
                "install",
                "-e",
                str(install_path),
            ])
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1
        importlib.invalidate_caches()

        return 0

    def ensure_machine_ready(self) -> int:
        ready = self.ensure_sldb_available(allow_install=True)
        if ready != 0:
            return ready

        return self.ensure_global_store_and_models()

    def default_pythonpath(self) -> str:
        return package_pythonpath()

    def ensure_global_store_and_models(self) -> int:
        global_store = Path.home() / ".sldb"
        if not global_store.exists():
            print(f"Initializing global store at {global_store}...")
            try:
                self._init_store(Path.home())
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        result = self._register_models(global_store)
        if result != 0:
            return result

        print("Global deskops model registry is ready.")
        return 0

    def init_local_store(self, target_path: Path) -> int:
        local_store = target_path / ".sldb"
        if local_store.exists():
            print(f"Local store already exists at {local_store}.")
        else:
            print(f"Initializing local store at {local_store}...")
            try:
                self._init_store(target_path)
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        return self._register_models(local_store)

    def _register_models(self, store_path: Path) -> int:
        """Link the deskops owner store and inherit the model set from it.

        A model registered here as a copy of the deskops class is converted in place by
        `inherit_model`, keeping its documents and signed contract. A regular (non-editable)
        install ships no owner store, so the models are registered directly from the
        installed package instead.
        """
        try:
            owner = self._deskops_owner_store()
            if owner is None:
                self._register_models_directly(store_path)
            else:
                link_state = self._ensure_owner_link(store_path, owner)
                if link_state is None:
                    # The name is already taken by another checkout. sldb cannot replace a
                    # link, so leave this store as it is instead of inheriting from it.
                    print(
                        f"Skipping model registration in {store_path}: '{DESKOPS_STORE_LINK}' is linked elsewhere."
                    )
                    return 0
                if link_state:
                    print(f"Linked {owner} as {DESKOPS_STORE_LINK} in {store_path}.")

                entries = self._registered_model_entries(store_path)
                for model_name, model_ref in MODEL_REFS.items():
                    entry = entries.get(model_name)
                    if entry is not None:
                        origin = getattr(entry, "origin", None)
                        if origin == DESKOPS_STORE_LINK:
                            continue
                        if origin or getattr(entry, "model_ref", None) != model_ref:
                            continue
                    print(f"Inheriting {model_name} in {store_path}...")
                    self._inherit_model(model_name, store_path)

            self._init_relations(store_path)
            self._update_store_indexes(store_path)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1

        return 0

    def _register_models_directly(self, store_path: Path) -> None:
        """Register the deskops models as copies when no owner store is installed."""
        owner = Path(package_pythonpath()) / ".sldb"
        print(
            f"No deskops owner store at {owner}; registering the models directly from the installed package."
        )
        entries = self._registered_model_entries(store_path)
        for model_name, model_ref in MODEL_REFS.items():
            if model_name in entries:
                continue
            print(f"Registering {model_name} in {store_path}...")
            self._register_model(model_ref, store_path)

    def _register_model(self, model_ref: str, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.register_model(store_path.parent, model_ref, pythonpath=package_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "models",
                "add",
                model_ref,
                "--store",
                str(store_path),
                "--pythonpath",
                package_pythonpath(),
            ])

    def _deskops_owner_store(self) -> Path | None:
        owner = Path(package_pythonpath()) / ".sldb"
        return owner if owner.exists() else None

    def _ensure_owner_link(self, store_path: Path, owner: Path) -> bool | None:
        """Link `owner` as `deskops`, repairing a broken link to it.

        Returns True when the link was added or repaired, False when it already points at
        `owner`, and None when the name is linked to a healthy different store (or the
        installed sldb cannot replace a link).
        """
        if self._sldb_importable():
            from sldb.api import store_links

            try:
                existing = next(
                    (link for link in store_links(store_path) if link["name"] == DESKOPS_STORE_LINK),
                    None,
                )
                if existing is not None:
                    target = Path(existing["resolved"])
                    if target == owner.resolve():
                        return False
                    if existing["status"] != "ok" and self._link_store_supports_replace():
                        doc_io.link_store_alias(
                            store_path.parent, owner, DESKOPS_STORE_LINK, replace=True
                        )
                        print(
                            f"Replaced broken '{DESKOPS_STORE_LINK}' link to {target} with {owner}."
                        )
                        return True
                    print(
                        f"Warning: {store_path} already links '{DESKOPS_STORE_LINK}' to {target}, "
                        f"not to {owner}."
                    )
                    return None
                doc_io.link_store_alias(store_path.parent, owner, DESKOPS_STORE_LINK)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            existing = self._store_link_names(store_path)
            if DESKOPS_STORE_LINK in existing:
                return False
            self.run_sldb([
                "stores",
                "add",
                str(owner),
                "--name",
                DESKOPS_STORE_LINK,
                "--store",
                str(store_path),
            ])
        return True

    def _inherit_model(self, model_name: str, store_path: Path) -> None:
        ref = f"{DESKOPS_STORE_LINK}:{model_name}"
        if self._sldb_importable():
            try:
                doc_io.inherit_model_from(store_path.parent, ref, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "models",
                "inherit",
                ref,
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _init_relations(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_relations_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "edges",
                "init",
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _update_store_indexes(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.update_store_indexes_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "update", "--store", str(store_path)])

    def run_sldb(self, args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        return self._run([sys.executable, "-m", "sldb", *args], capture_output=capture_output)

    def _init_store(self, target_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_store_at(target_path)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "init", "--path", str(target_path)])

    def _registered_model_entries(self, store_path: Path) -> dict[str, Any]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {m.name: m for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"]: entry for entry in payload.get("models", [])}

    def _store_link_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {link.name for link in idx.stores}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["stores", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("stores", [])}

    def _registered_model_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index
            try:
                idx = load_store_index(store_path)
                return {m.name for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("models", [])}

    def _link_store_supports_replace(self) -> bool:
        """Whether the installed sldb's `link_store` can re-point an existing link."""
        from inspect import signature

        from sldb.api import link_store

        return "replace" in signature(link_store).parameters

    def _sldb_importable(self) -> bool:
        return importlib.util.find_spec("sldb") is not None

    def _resolve_sldb_checkout(self) -> Path | None:
        candidates: list[Path] = []
        env_path = (os.environ.get("DESKOPS_SLDB_PATH") or "").strip()
        if env_path:
            candidates.append(Path(env_path).expanduser())

        package_root = Path(package_pythonpath())
        repo_root = package_root.parent
        candidates.append(repo_root.parent / "sldb")
        candidates.append(Path.cwd().resolve().parent / "sldb")

        seen: set[Path] = set()
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            if (resolved / "pyproject.toml").exists() and (resolved / "src" / "sldb").exists():
                return resolved
        return None

    def _run(self, command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=capture_output,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise RuntimeError(detail)
        return result

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
Cold-bundle de la tarea task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -rn 'doc_io\|DocTransaction' deskops/ vacío (a2)
- Fallo inyectado a mitad de atoms merge: sha256 de desk/ y .sldb/core/ y sldb stores check iguales antes y después (test, a6)
- Update con expected_source_hash viejo falla con el mensaje de conflicto de a5 (test)
- message send/ack dentro de la transacción, sin rollback manual (test)
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests de los archivos tocados (test_doc_io se reescribe o se borra con su módulo), test_atoms_*, test_message_cli, test_retire_cli, test_issue_cli, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- deskops doctor sin hallazgos nuevos en los 6 desks, con cwd neutro (a8)
- wc -l antes y después por archivo tocado
- CHANGELOG

