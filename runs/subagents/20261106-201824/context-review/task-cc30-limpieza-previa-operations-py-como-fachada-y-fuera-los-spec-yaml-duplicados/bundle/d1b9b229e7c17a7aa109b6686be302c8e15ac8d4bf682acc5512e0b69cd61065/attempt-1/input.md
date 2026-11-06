FILE:desk/tasks/task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados.md
---
id: task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
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
- deskops/operations.py
- deskops/doc_access.py
- deskops/services/tasks.py
- deskops/services/atoms.py
- deskops/services/closure.py
- deskops/services/retire.py
- deskops/services/desk_view.py
- deskops/specs/__init__.py
- deskops/specs/compiler.py
- deskops/specs/loader.py
- deskops/specs/mermaid.py
- deskops/spec/artifacts/
- deskops/spec/fields/
- deskops/cli/model_introspection.py
- deskops/models/
- deskops/workflow/next_actions.py
- tests/test_specs.py
- tests/test_extension_points.py
- tests/test_desk_view.py
- tests/test_output_goldens.py
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC30: Limpieza previa - operations.py como fachada y fuera los spec YAML duplicados

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC30 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 2 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PF1. Depende de: nada. Gates requeridos: G_P0: P0 del árbol integrado en main de deskops y sldb (pending); G_GATES_FROZEN: gates-por-tipo congelado tras GC03 (DK2) (pending).

## Goal

_Describe the concrete result this task must produce._

deskops/operations.py queda como fachada que solo delega; los helpers privados que piden los servicios viven en deskops/doc_access.py o en su servicio dueño; ningún servicio construye DeskopsOperations; _normalize_task_payload y compile_task_spec son una sola función; task_lifecycle.yaml se carga solo por lifecycle.load_lifecycle_spec; spec/artifacts y spec/fields (y SpecRegistry, specs/mermaid.py si solo lo usan tests) borrados, con id_pattern, status_default y tags por artefacto como atributo de clase de cada modelo. Sin cambio de comportamiento: goldens de ayuda y salida idénticos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/operations.py, deskops/doc_access.py (nuevo), deskops/services/ (tasks, atoms, closure, retire y el constructor de desk_view), deskops/specs/, deskops/spec/artifacts y deskops/spec/fields (borrados), deskops/cli/model_introspection.py, deskops/models/, deskops/workflow/next_actions.py, los tests que los cubren y CHANGELOG.md. Fuera: spec/workflows/task_lifecycle.yaml (lo reduce CC31); la vista de desk_view.py (la reemplaza CC34); graph_ui (sus imports privados se conservan como alias en la fachada); cualquier escritura en sldb; formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 2, CC30). SCOPE: (1) Dirección única de dependencias: los helpers privados que los servicios piden a operations (tasks.py:44-78 y atoms.py:51-79: _read_doc, _write_doc, _write_new_doc, _coerce_list, _hydrate_task, _resolve_glob, _resolve_task_payload, _normalize_task_payload, _add_closeout_facts y los demás que el grep delate) pasan a un módulo deskops/doc_access.py (lectura/escritura de documentos del desk) o al servicio dueño; los servicios dejan de construir DeskopsOperations (tasks.py:35-37, atoms.py:42-44, closure.py:63-65); DeskopsOperations queda como fachada que solo delega (ningún método con más de una llamada a servicio más el armado de argumentos). Los nombres privados que graph_ui importa (ops._read_doc, _resolve_glob, _registered_repositories, _repository_root: UIs/graph_ui/frontends/mindmap/deskops_routes.py:34,41,46,67; frontends/desk/serve.py:66-75) se conservan como alias en la fachada hasta CC34 y se marcan con un comentario que nombra CC34. (2) Duplicados: _normalize_task_payload (operations.py:537-567) y compile_task_spec (specs/compiler.py:25-61) quedan en una sola función; task_lifecycle.yaml se carga solo con lifecycle.load_lifecycle_spec (workflow/next_actions.py:9 la usa en lugar de su loader propio). (3) Specs: se borran spec/artifacts/*.yaml (10) y spec/fields/*.yaml (49), specs/loader.py (SpecRegistry) y specs/mermaid.py si solo los usan tests; id_pattern, status_default y tags por artefacto pasan a un atributo de clase de cada modelo (p. ej. __artifact__) que cli/model_introspection.py lee, y _ARTIFACT_DEFAULTS (model_introspection.py:302-349) se borra; compiler.py y operations.py:1118-1123 leen ese atributo; tests/test_specs.py y test_extension_points.py:44 se adaptan a los modelos. spec/workflows/task_lifecycle.yaml se queda (CC31 lo reduce). Sin cambio de comportamiento.

ACCEPTANCE: Goldens de ayuda y de salida idénticos (test_help_goldens, test_command_output_goldens sin --update-golden); grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/ vacío; grep de "DeskopsOperations(" en deskops/services/ vacío; grep de "_normalize_task_payload\|compile_task_spec" devuelve una sola definición; los tests de los archivos tocados verdes (lista en la Validation del TaskDoc) y tests/test_desk_view.py verde incluido el cruce con graph_ui (:132); líneas de operations.py y de services/ antes y después en la Validation; CHANGELOG.

OUTPUT_SCOPE: deskops/operations.py, deskops/doc_access.py, deskops/services/, deskops/specs/, deskops/spec/artifacts/ (borrado), deskops/spec/fields/ (borrado), deskops/cli/model_introspection.py, deskops/models/, deskops/workflow/next_actions.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (gates): requiere G_P0 y G_GATES_FROZEN, ambos pending en el dag. G_P0: el closeout de task-el-grafo-del-closeout-se-lee-del-índice-de-sldb-no-reescaneando-el-repo está en main (ce857e14). G_GATES_FROZEN: GC01, GC02, GC03 y GC06 están en main (9df4c82a), pero gates-por-tipo/dag.yaml no tiene todavía status frozen. Los marca el supervisor; el despacho espera a que ambos estén satisfechos.
q2 (desk_view.py): services/desk_view.py construye DeskopsOperations (:66) y cae en el grep de services/; este nodo solo cambia cómo obtiene el acceso a documentos (doc_access o la fachada recibida por parámetro), no la vista, que reemplaza CC34. services/retire.py:200 (DeskopsOperations(root)._write_doc) también entra.
q3 (líneas base): la base de la medición es main dc1d2834.
q4 (DK6): si al mover helpers aparece un chequeo de un documento fuera del modelo, no se mueve al modelo aquí: queda anotado para el inventario de CC38.

PRECISIONES DEL PREFLIGHT (review-task-cc30-...-preflight-1, 2026-11-06):
q5 (arranque): el ejecutor NO arranca mientras G_P0 o G_GATES_FROZEN estén pending en dag.yaml; el coordinador despacha solo cuando el supervisor los marca satisfechos.
q6 (destino de cada helper): un helper de lectura/escritura/resolución de documentos del desk que usan dos o más servicios o la fachada (_read_doc, _write_doc, _write_new_doc, _coerce_list, _resolve_glob, _resolve_artifact_selector, _resolve_artifact_selector_multi, _resolve_task_payload, _hydrate_task, _track_created_document, _track_created_artifact, _remove_created_file) va a deskops/doc_access.py como función de módulo que recibe root; un helper que usa un solo servicio (_normalize_task_payload, _append_task_to_board, _add_closeout_facts, _reference_points_to_atom, _transitions_from) va a ese servicio (o a lifecycle.py en el caso de _transitions_from).
q7 (inventario cerrado): el conjunto de helpers es exactamente la salida de grep -rhoE "operations\._[a-z_]+|ops\._[a-z_]+" deskops/services/ | sort -u sobre main dc1d2834 (los 17 nombres de q6); se registra aquí antes y después (después: vacío salvo desk_view.py, ver q9).
q8 (atributo de modelo): el atributo se llama __artifact__ y es un dict con las claves id_pattern, status_default y tags, con los mismos valores que hoy dan spec/artifacts/*.yaml y _ARTIFACT_DEFAULTS; model_introspection.py, specs/compiler.py y operations.py lo leen con getattr(model, "__artifact__", {}).
q9 (desk_view.py y retire.py): retire.py:200 escribe con doc_access.write_doc(root, ...). desk_view.py es consumidor de la fachada (la fachada no lo llama; lo construyen cli/commands/view.py y graph_ui serve.py:164 como DeskView(root)), no un servicio delegado: conserva su firma y su DeskopsOperations(self.root) por defecto; sus lecturas privadas (_read_doc, _resolve_task_payload, _transitions_from, _resolve_artifact_selector) pasan a doc_access/lifecycle. El grep de aceptación de "DeskopsOperations(" en deskops/services/ excluye services/desk_view.py, que CC34 borra.
q10 (specs/mermaid.py): se borra si grep -rn "specs.mermaid\|from deskops.specs import" deskops/ --include=*.py fuera de deskops/specs/ no lo importa; si algo de deskops/ lo importa, se conserva y se registra aquí. El mismo criterio vale para specs/loader.py tras quitar SpecRegistry.
q11 (tests fijados): los tests de los archivos tocados son tests/test_output_goldens.py, test_specs.py, test_extension_points.py, test_desk_view.py, test_atoms_transactions.py, test_board_portable_references.py, test_cli.py, test_closeout_gates.py, test_desk_replace.py, test_doc_io.py, test_materialization_contract.py, test_packaging.py, test_registry_robustness.py y test_review_doc.py (importan módulos tocados); fallas previas conocidas en main (test_board_portable_references::test_linked_board_context..., test_gitignore_policy::test_sldb_store_declaration...) se comparan contra main dc1d2834.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_output_goldens.py (help y output goldens sin --update-golden)
- TMPDIR=/dev/shm pytest -q tests/test_specs.py tests/test_extension_points.py tests/test_desk_view.py
- TMPDIR=/dev/shm pytest -q, uno a la vez, tests/test_atoms_transactions.py tests/test_board_portable_references.py tests/test_cli.py tests/test_closeout_gates.py tests/test_desk_replace.py tests/test_doc_io.py tests/test_materialization_contract.py tests/test_packaging.py tests/test_registry_robustness.py tests/test_review_doc.py (fallas previas comparadas contra main dc1d2834)
- grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/ vacío
- grep -rn "DeskopsOperations(" deskops/services/ vacío salvo services/desk_view.py (q9)
- grep -rn "def _normalize_task_payload\|def compile_task_spec" deskops/ devuelve una sola definición
- grep -rhoE "operations\._[a-z_]+|ops\._[a-z_]+" deskops/services/ antes y después (q7)
- wc -l deskops/operations.py deskops/services/*.py antes (main dc1d2834) y después
- deskops doctor y deskops view board en los 6 desks sin hallazgos nuevos

## Done When

_Name the observable condition that makes the task complete._

Goldens de ayuda y de salida idénticos (test_help_goldens, test_command_output_goldens sin --update-golden); grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/ vacío; grep de "DeskopsOperations(" en deskops/services/ vacío; grep de "_normalize_task_payload\|compile_task_spec" devuelve una sola definición; los tests de los archivos tocados verdes (lista en la Validation del TaskDoc) y tests/test_desk_view.py verde incluido el cruce con graph_ui (:132); líneas de operations.py y de services/ antes y después en la Validation; CHANGELOG.

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

FILE:deskops/services/tasks.py
"""Task lifecycle service: create, advance, and next.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Shared document storage helpers
(read/write/track, selector resolution, lifecycle facts) stay on
``DeskopsOperations``; the service delegates to the operations instance it is
bound to instead of duplicating them.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_io
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import TaskDoc
from deskops.models.task_types import canonical_task_type_name
from deskops.operations import TaskBundle
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import load_task_lifecycle_spec
from deskops.workflow.next_actions import match_workflow_state

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Shared document helpers stay in the operations layer.
    def ensure_workspace(self) -> None:
        self._ops.ensure_workspace()

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return self._ops._read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_doc(path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_new_doc(path, model, payload)

    def _track_created_document(self, model: type[Any], path: Path, doc_id: str) -> None:
        self._ops._track_created_document(model, path, doc_id)

    def _coerce_list(self, value: Any) -> list[str]:
        return self._ops._coerce_list(value)

    def _hydrate_task(self, payload: dict[str, Any]) -> Task:
        return self._ops._hydrate_task(payload)

    def _add_closeout_facts(self, payload: dict[str, Any]) -> None:
        self._ops._add_closeout_facts(payload)

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return self._ops._resolve_glob(directory, doc_id)

    def _normalize_task_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._ops._normalize_task_payload(payload)

    def _resolve_task_payload(self, task_id: str) -> dict[str, Any]:
        return self._ops._resolve_task_payload(task_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return self._ops._resolve_artifact_selector(artifact_id, directory, selector)

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        self.ensure_workspace()
        payload = self._normalize_task_payload(raw_payload)
        # A task's closeout evidence is declared by its type, not written into the task. The
        # task is stored under its type's model so `model <= TaskCodeDoc` finds it.
        raw_task_type = str(payload.get("task_type") or "").strip()
        registry = self._ops.registered_task_types()
        task_type = raw_task_type if raw_task_type in registry else canonical_task_type_name(raw_task_type)
        type_model = registry.get(task_type) or registry.get("task.code") or TaskDoc
        payload["task_type"] = task_type
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec(self._ops.spec_registry, payload, entry_node=spec.entry_node)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_io.DocTransaction(self.root):
            self._write_new_doc(task_path, type_model, compiled.task_payload)
            self._track_created_document(type_model, task_path, task_id)
            self._ops._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_ref = str(board_path.relative_to(self.root))
        if not task_selector:
            task_refs = list(self._read_doc(board_path, BoardDoc).get("tasks") or [])
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
                    payload = self._read_doc(path, TaskDoc)
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
        payload = self._resolve_task_payload(task_path.stem)
        spec = load_task_lifecycle_spec(self._ops.spec_root)
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

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = self._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = self._read_doc(task_path, TaskDoc)

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        self._add_closeout_facts(payload)
        result = lifecycle.advance(self.root, payload)
        for key in ("closeout_evidence_verified", "pill_graduation_verified"):
            payload.pop(key, None)
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return self._hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = self._hydrate_task(payload)
        if result.progressed:
            self._write_doc(task_path, TaskDoc, payload)
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

    def _auto_commit_task_closure(self, payload: dict[str, Any], task_path: Path) -> None:
        # Compatibility hook: closure logic lives in ClosureService.
        self._ops.closure.close_auto(payload, task_path)

    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return self._resolve_artifact_selector("artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = self._read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = self._read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]

FILE:deskops/services/atoms.py
"""Atom domain service: create, validate, reorganize, split, merge, retarget, delete.

Every atom write goes through ``doc_io``; split and merge each run inside one
``DocTransaction`` so a failure restores the original file bytes and store
entries. Shared document/path helpers stay on ``DeskopsOperations`` and this
service delegates to the operations instance it is bound to.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from deskops import doc_io
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import axis_values
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.models import AtomDoc
from deskops.models import PillDoc
from deskops.operations import AtomCreateResult
from deskops.operations import AtomMergeResult
from deskops.operations import AtomSplitResult
from deskops.operations import AtomValidationRecord
from deskops.operations import DocumentRecord
from deskops.operations import slugify
from deskops.paths import package_pythonpath

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class AtomsService:
    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Shared document helpers stay in the operations layer.
    def ensure_workspace(self) -> None:
        self._ops.ensure_workspace()

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return self._ops._read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_doc(path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_new_doc(path, model, payload)

    def _remove_created_file(self, path: Path) -> None:
        self._ops._remove_created_file(path)

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        self._ops._track_created_artifact(artifact_id, model, path, doc_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return self._ops._resolve_artifact_selector(artifact_id, directory, selector)

    def _reference_points_to_atom(self, reference: str) -> bool:
        return self._ops._reference_points_to_atom(reference)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return self._ops.list_artifacts(artifact_id)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return self._ops._resolve_artifact_selector_multi(artifact_id, directories, selector)

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
        untracked = doc_io.is_tracked(self.root, path)
        with doc_io.DocTransaction(self.root) as transaction:
            transaction.delete(path)
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
        if not self._is_valid_atom_slug(atom_id):
            raise ValueError(f"Atom id must follow slug convention atom-<slug>: {atom_id}")

        normalized_question = str(five_wh_one_plus).strip()
        if normalized_question not in {"what", "why", "how", "how_not", "when", "where", "for_whom"}:
            raise ValueError(f"Unsupported atom question '{normalized_question}'.")

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

        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        self._write_new_doc(path, AtomDoc, payload)
        try:
            self._track_created_artifact("artifact.atom", AtomDoc, path, atom_id)
        except Exception:
            self._remove_created_file(path)
            raise
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
        for target_id in normalized_ids:
            if not self._is_valid_atom_slug(target_id):
                raise ValueError(f"Atom split target id must follow slug convention atom-<slug>: {target_id}")

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])

        created: list[DocumentRecord] = []

        with doc_io.DocTransaction(self.root):
            for target_id in normalized_ids:
                heading, content = assignments[target_id]
                title = f"{payload['title']} — {heading}"
                new_payload = {
                    "id": target_id,
                    "title": title,
                    "five_wh_one_plus": payload["five_wh_one_plus"],
                    "answer": content,
                    "tags": list(payload.get("tags") or []),
                    "provenance": payload.get("provenance"),
                }
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                self._write_new_doc(new_path, AtomDoc, new_payload)
                self._track_created_artifact("artifact.atom", AtomDoc, new_path, target_id)
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

        if not self._is_valid_atom_slug(source_id):
            raise ValueError(f"Atom merge source id must follow slug convention atom-<slug>: {source_id}")
        if not self._is_valid_atom_slug(target_id):
            raise ValueError(f"Atom merge target id must follow slug convention atom-<slug>: {target_id}")

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        inbound_references = self._find_inbound_atom_references(source_id, excluded_path=source_path)
        rewritten_references: list[str] = []

        with doc_io.DocTransaction(self.root) as transaction:
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
        errors: list[str] = []
        doc_id = path.stem
        payload: dict[str, Any] | None = None
        try:
            payload = self._read_doc(path, AtomDoc)
            doc_id = str(payload.get("id") or path.stem)
            AtomDoc(**payload)
        except Exception as exc:
            errors.append(f"model validation failed: {exc}")
            return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")
        if not self._is_valid_atom_slug(doc_id):
            errors.append("atom id must follow slug convention atom-<slug>")

        try:
            validate_atom_tag_namespaces(
                list(payload.get("tags") or []),
                default_registry_path(self.root),
            )
        except ValueError as exc:
            errors.append(str(exc))

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

    def _is_valid_atom_slug(self, atom_id: str) -> bool:
        if not atom_id.startswith("atom-"):
            return False
        slug = atom_id.removeprefix("atom-")
        return bool(slug) and slug == slugify(slug)

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
        transaction: doc_io.DocTransaction | None = None,
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

        pythonpath = package_pythonpath()
        changed = False
        for atom_id, new_path in retargets.items():
            try:
                doc_io.untrack(self.root, atom_id, pythonpath=pythonpath)
                doc_io.track(self.root, self.root / new_path, AtomDoc, name=atom_id, pythonpath=pythonpath)
            except Exception:
                continue
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        if not (self.root / ".sldb").is_dir():
            return False
        try:
            doc_io.untrack(self.root, atom_id, pythonpath=package_pythonpath())
        except Exception:
            return False
        return True

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        axis = DeskConfig.load(self.desk_root).atom_folder_axis
        if axis is None:
            return None
        axis = str(axis).strip()
        if not axis:
            return None
        namespaces = load_namespaces(default_registry_path(self.root))
        if axis not in namespaces:
            raise ValueError(
                f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
                "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
            )
        return axis

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        base = self.desk_root / "atoms"
        axis = self.atom_folder_axis()
        if axis is not None:
            value = folder_axis_value(tags, axis)
            if value is not None:
                return base / axis_folder_relpath(value) / f"{atom_id}.md"
        return base / f"{atom_id}.md"

FILE:deskops/services/closure.py
"""One closure path for task bundles.

Every way of closing a task ends here: ``deskops closeout commit`` (run-linked
and manual routes), ``deskops closeout supersede``, ``deskops closeout retire``,
and the legacy ``_auto_commit_task_closure`` hook. The
service owns the whole closure: closeout gates for a board-routed task, Board
update, store untracking, bundle removal, exactly one closing commit carrying
the route's trailers, and the append-only index entry.

``advance`` no longer closes: it refuses at the closeout node and points here.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
from typing import TYPE_CHECKING

import yaml

from deskops import doc_io
from deskops.models import BoardDoc
from deskops.models import TaskDoc

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class ClosureCommitError(RuntimeError):
    """The closing commit could not be made; the desk was restored."""


@dataclass
class ClosureOutcome:
    """What one closure did, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


class ClosureService:
    """Build the closing commit and its run-index entry as one clean unit.

    ``runs/subagents/index.jsonl`` records ``task_id``, ``run_dir`` and the
    route fields, but not the closing commit hash: the index line is written
    after the commit exists and folded into that same commit with one
    ``git commit --amend --no-edit``, which changes the hash. ``commit`` is
    therefore always null in new entries. Readers resolve the closing commit
    with ``git log -1 --grep 'Task-Id: <task_id>'``, using the trailer every
    closing commit already carries. The amend is limited to the index path so
    the working tree is clean when the command returns.
    """

    REQUIRED_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]

    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self._gate_notes: list[str] = []

    # ---------------------------------------------------------------- routes
    def close_manual(
        self,
        task_id: str,
        *,
        reason: str,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["--no-run needs a non-empty --reason saying why the task closes without a subagent run."],
            )
        subject = message or self._default_subject(task_id)
        trailers = [f"Task-Id: {task_id}", "Closeout-Mode: manual", f"Closeout-Reason: {reason}"]
        return self._close(
            task_id,
            route="manual",
            subject=subject,
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=paths is not None,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "manual",
            },
            success_line=f"Closing commit {{commit}} made manually (no run): {reason}",
        )

    def close_superseded(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Close a task whose subject no longer exists, from any lifecycle node.

        No evidence gates run: tests, atoms and a run would all describe work
        that was never done. The reason and at least one resolvable ref (an
        ancestor commit or an existing path) are the evidence instead, and the
        closing commit says ``Closeout-Mode: superseded``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Supersede needs a non-empty --reason saying why the task's subject no longer exists."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Supersede needs at least one --ref naming an ancestor commit or an existing path."],
            )
        unresolved = [ref for ref in cleaned_refs if not self._ref_resolves(ref)]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need an ancestor commit or an existing path)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        original = task_path.read_bytes()
        payload = self._ops._read_doc(task_path, TaskDoc)
        payload["status"] = "superseded"
        payload["history"] = [*(payload.get("history") or []), "superseded"]
        try:
            self._ops._write_doc(task_path, TaskDoc, payload)
        except Exception as exc:  # noqa: BLE001 - a task that cannot record superseded is not closed
            task_path.write_bytes(original)
            return ClosureOutcome(1, [f"Could not record superseded status on {task_id}: {exc}"])

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: superseded",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        try:
            outcome = self._close(
                task_id,
                route="superseded",
                subject=message or self._default_subject(task_id),
                trailers=trailers,
                paths=list(paths or []),
                explicit_paths=True,
                run_gates=False,
                index_entry={
                    "task_id": task_id,
                    "run_id": None,
                    "run_dir": None,
                    "session_sha256": None,
                    "mode": "superseded",
                },
                success_line=f"Closing commit {{commit}} made in superseded mode: {reason}",
            )
        except Exception:
            task_path.write_bytes(original)
            raise
        if outcome.exit_code != 0:
            task_path.write_bytes(original)
        return outcome

    def close_retired(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Remove a task that was already resolved before the ritual lifecycle.

        The task keeps its status: it is not made ``superseded`` and no evidence
        gates run. A resolved-family status plus a reason and at least one ref
        that is HEAD or an ancestor commit are the evidence instead, and the
        closing commit says ``Closeout-Mode: legacy-resolved``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Retire needs a non-empty --reason saying why the task is already resolved."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Retire needs at least one --ref naming a commit that is HEAD or an ancestor."],
            )
        unresolved = [
            ref for ref in cleaned_refs if not self._ops.closeout_gates.reference_points_to_commit(ref)
        ]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need a commit that is HEAD or an ancestor)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        payload = self._ops._read_doc(task_path, TaskDoc)
        status = str(payload.get("status") or "").strip().lower()
        if status not in {"resolved", "closed", "done", "complete"}:
            return ClosureOutcome(
                1,
                [
                    f"Task {task_id} has status '{payload.get('status') or ''}'; only resolved, "
                    "closed, done or complete tasks can be retired."
                ],
            )

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: legacy-resolved",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        return self._close(
            task_id,
            route="legacy-resolved",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=True,
            run_gates=False,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "legacy-resolved",
            },
            success_line=f"Closing commit {{commit}} made in legacy-resolved mode: {reason}",
        )

    def _ref_resolves(self, reference: str) -> bool:
        if self._ops.closeout_gates.reference_points_to_commit(reference):
            return True
        path = Path(reference)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def close_with_run(
        self,
        task_id: str,
        *,
        run_dir: str | Path,
        paths: list[str] | None = None,
        run_id: str | None = None,
        session: str | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        root = self.root
        resolved_run_dir = Path(run_dir)
        if not resolved_run_dir.is_absolute():
            resolved_run_dir = (root / resolved_run_dir).resolve()

        if not self._is_under(resolved_run_dir, root / "runs" / "subagents"):
            return ClosureOutcome(1, [f"Run dir must live under runs/subagents/: {resolved_run_dir}"])
        if not resolved_run_dir.is_dir():
            return ClosureOutcome(1, [f"Run dir not found: {resolved_run_dir}"])

        missing = [name for name in self.REQUIRED_EVIDENCE if not (resolved_run_dir / name).exists()]
        if missing:
            return ClosureOutcome(
                1,
                [f"Missing required evidence in {resolved_run_dir}: {', '.join(missing)}"],
            )

        manifest_path = resolved_run_dir / "run.yaml"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

        run_id = run_id or manifest.get("run_id")
        session = session or manifest.get("session")
        session_sha256 = manifest.get("session_sha256")
        session_path = Path(str(session)) if session else None
        if session_path and session_path.is_file():
            session_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()

        rel_run_dir = resolved_run_dir.relative_to(root).as_posix()
        manifest.update(
            {
                "task_id": task_id,
                "run_dir": rel_run_dir,
                "run_id": run_id,
                "session": session,
                "session_sha256": session_sha256,
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")

        staged_paths = list(paths) if paths is not None else list(manifest.get("touched") or [])
        trailers = [f"Task-Id: {task_id}", f"Run-Dir: {rel_run_dir}"]
        if run_id:
            trailers.append(f"Run-Id: {run_id}")
        if session_sha256:
            trailers.append(f"Session-Sha256: {session_sha256}")

        return self._close(
            task_id,
            route="run",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=staged_paths,
            explicit_paths=True,
            extra_stage_paths=[rel_run_dir],
            index_entry={
                "task_id": task_id,
                "run_id": run_id,
                "run_dir": rel_run_dir,
                "session_sha256": session_sha256,
            },
            success_line=f"Closing commit {{commit}} linked to run {rel_run_dir}",
        )

    def close_auto(self, payload: dict[str, Any], task_path: Path) -> None:
        """Legacy hook used by ``DeskopsOperations._auto_commit_task_closure``."""
        task_id = payload.get("id", "unknown-task")
        files = [str(item) for item in payload.get("files") or []]
        try:
            self._close(
                task_id,
                route="legacy",
                subject=self._default_subject(task_id, task_path),
                trailers=[f"Task-Id: {task_id}"],
                paths=files,
                explicit_paths=True,
                task_path=task_path,
                run_gates=False,
                index_entry={},
                success_line="",
            )
        except ClosureCommitError as exc:
            raise RuntimeError(
                f"Failed to commit task closure for {task_id}. The bundle was not deleted "
                f"and the desk was left unchanged. Git output: {exc}"
            ) from exc

    # ---------------------------------------------------------------- internals
    def _close(
        self,
        task_id: str,
        *,
        route: str,
        subject: str,
        trailers: list[str],
        paths: list[str],
        explicit_paths: bool,
        index_entry: dict[str, Any],
        success_line: str,
        task_path: Path | None = None,
        extra_stage_paths: list[str] | None = None,
        run_gates: bool = True,
    ) -> ClosureOutcome:
        self._gate_notes = []
        task_path = task_path or self._task_path(task_id)
        task_rel = self._relative(task_path)
        board_path = self.desk_root / "tasks" / "Board.md"
        board_before = board_path.read_text(encoding="utf-8") if board_path.exists() else None
        routed = self._board_routes(board_path, task_id, task_path) if board_before is not None else False

        if run_gates and task_path.exists() and routed:
            gate_outcome = self._gate_outcome(task_id)
            if gate_outcome is not None:
                return gate_outcome

        staged_before = self._git("diff", "--cached", "--name-only", check=False)
        if explicit_paths:
            for path in paths:
                self._git("add", "-A", "--", path, check=False)
            for path in extra_stage_paths or []:
                self._git("add", "-A", "--", path, check=False)
        elif not staged_before:
            if route == "manual":
                return ClosureOutcome(1, ["Nothing staged and no paths given. Pass --paths."])
            return ClosureOutcome(
                1,
                ["Nothing staged and no paths given. Pass --paths or record 'touched' in run.yaml."],
            )

        commit_paths: list[str] = []
        if explicit_paths:
            commit_paths.extend(paths)
            commit_paths.extend(extra_stage_paths or [])

        def add_commit_path(path: str) -> None:
            if path not in commit_paths:
                commit_paths.append(path)

        task_bytes = task_path.read_bytes() if task_path.exists() else None
        paths_to_remove: list[Path] = []

        try:
            if task_bytes is not None:
                # A task created and closed between two commits never reached HEAD.
                # Record its body first so the closing commit does not erase it.
                self._record_uncommitted_task(task_id, task_path, task_rel)

            with doc_io.DocTransaction(self.root) as transaction:
                if routed and board_before is not None:
                    board_payload = self._ops._read_doc(board_path, BoardDoc)
                    references = [
                        str(item)
                        for item in board_payload.get("tasks") or []
                        if not self._board_reference_matches(str(item), task_id, task_rel)
                    ]
                    board_payload["tasks"] = references
                    self._ops._write_doc(board_path, BoardDoc, board_payload)
                    self._git("add", "--", "desk/tasks/Board.md", check=False)
                    add_commit_path("desk/tasks/Board.md")

                if task_bytes is not None:
                    transaction.untrack(task_path)

                sldb_status = self._git("status", "--porcelain", "--", ".sldb", check=False)
                if sldb_status:
                    self._git("add", "-A", "--", ".sldb", check=False)
                    add_commit_path(".sldb")

                if task_bytes is not None:
                    # Committed means present in HEAD, not merely staged: a directory in
                    # --paths can stage a task created in this cycle, and HEAD never had it.
                    in_head = self._in_head(task_rel)
                    if not in_head:
                        self._git("rm", "--cached", "-q", "--ignore-unmatch", "--", task_rel, check=False)
                    if in_head:
                        removed = subprocess.run(
                            ["git", "rm", "-f", "--", task_rel],
                            cwd=self.root,
                            capture_output=True,
                            text=True,
                        )
                        if removed.returncode != 0:
                            raise ClosureCommitError(
                                removed.stderr.strip() or removed.stdout.strip() or f"git rm failed for {task_rel}"
                            )
                        add_commit_path(task_rel)
                    else:
                        paths_to_remove.append(task_path)

                message = subject + "\n\n" + "\n".join(trailers) + "\n"

                head_task_id = self._git(
                    "log", "-1", "--format=%(trailers:key=Task-Id,valueonly)", check=False
                )
                head_mode = self._git(
                    "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)", check=False
                )
                pathspec = list(dict.fromkeys(commit_paths)) if explicit_paths else None
                if pathspec:
                    # A path git knows neither in the index nor in HEAD (a directory whose
                    # only file was the never-committed task) would fail the whole commit.
                    pathspec = [path for path in pathspec if self._git_knows(path)]
                    if not pathspec:
                        raise ClosureCommitError("None of the --paths match a file git knows; nothing to commit.")
                if head_task_id == task_id and head_mode != "record":
                    argv = ["commit", "--amend", "--no-edit"]
                else:
                    argv = ["commit", "-m", message]
                if pathspec:
                    argv.extend(["--", *pathspec])

                result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
                if result.returncode != 0:
                    raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

            # The commit exists; only now remove an untracked bundle from disk.
            for path in paths_to_remove:
                if path.exists():
                    path.unlink()
        except Exception:
            self._restore_index(commit_paths, task_rel)
            if task_bytes is not None:
                task_path.parent.mkdir(parents=True, exist_ok=True)
                task_path.write_bytes(task_bytes)
            if board_before is not None:
                board_path.write_text(board_before, encoding="utf-8")
            raise

        commit = self._git("rev-parse", "HEAD")
        messages: list[str] = []
        if index_entry:
            index_path = self.root / "runs" / "subagents" / "index.jsonl"
            index_rel = index_path.relative_to(self.root).as_posix()
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_before = index_path.read_bytes() if index_path.exists() else None
            entry = {**index_entry, "commit": None}
            with index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            try:
                # A project that ignores the run index keeps it local: the entry is written,
                # but neither staged nor folded into the closing commit (the trailer is enough).
                if not self._git_ignores(index_rel):
                    self._git("add", "--", index_rel)
                    self._git("commit", "--amend", "--no-edit", "--", index_rel)
            except Exception:
                if index_before is None:
                    index_path.unlink(missing_ok=True)
                else:
                    index_path.write_bytes(index_before)
                self._git("restore", "--staged", "--", index_rel, check=False)
                raise
            commit = self._git("rev-parse", "HEAD")
            messages.append(f"Index: {index_path}")
        messages = [*self._gate_notes, *messages] if run_gates else messages
        if success_line:
            messages.insert(0, success_line.format(commit=commit[:12]))
        return ClosureOutcome(0, messages)

    def _gate_outcome(self, task_id: str) -> ClosureOutcome | None:
        """Run the declared-evidence gate; its declared/found line and alerts are always reported."""
        self._gate_notes = []
        try:
            report = self._ops.verify_task_closeout(task_id)
        except Exception as exc:  # noqa: BLE001 - a gate that cannot run blocks closure
            return ClosureOutcome(1, [f"Closeout verify failed for {task_id}; the closing commit was not made.", f"- {exc}"])
        notes = [f"Closeout gate: {report.get('summary', '')}"]
        for alert in report.get("alerts") or []:
            notes.append(f"ALERTA {alert.get('code', 'alert')}: {alert.get('message', '')}")
        self._gate_notes = notes
        if report.get("ok"):
            return None
        messages = [f"Closeout verify failed for {task_id}; the closing commit was not made.", *notes]
        for finding in report.get("findings") or []:
            code = finding.get("code", "finding")
            detail = finding.get("message") or finding.get("path") or ""
            messages.append(f"- {code}: {detail}")
        messages.append(f"Run 'deskops closeout verify --task {task_id}' for the full report.")
        return ClosureOutcome(1, messages)

    def _task_path(self, task_id: str) -> Path:
        try:
            return self._ops._resolve_glob(self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return self.desk_root / "tasks" / f"{task_id}.md"

    def _default_subject(self, task_id: str, task_path: Path | None = None) -> str:
        """Name the task file, so ``git log`` says what closed, not just its id."""
        path = task_path or self._task_path(task_id)
        return f"closeout: {path.stem}"

    def _board_routes(self, board_path: Path, task_id: str, task_path: Path) -> bool:
        try:
            payload = self._ops._read_doc(board_path, BoardDoc)
        except Exception:
            return False
        task_rel = self._relative(task_path)
        return any(
            self._board_reference_matches(str(item), task_id, task_rel)
            for item in payload.get("tasks") or []
        )

    @staticmethod
    def _board_reference_matches(reference: str, task_id: str, task_rel: str) -> bool:
        return reference in {
            task_rel,
            f"desk/tasks/{task_id}",
            f"desk/tasks/{task_id}.md",
        }

    def _restore_index(self, commit_paths: list[str], task_rel: str) -> None:
        for path in dict.fromkeys([*commit_paths, task_rel]):
            self._git("restore", "--staged", "--", path, check=False)

    def _relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    @staticmethod
    def _is_under(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _in_head(self, path: str) -> bool:
        """Whether `path` is already committed in HEAD."""
        return subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{path}"],
            cwd=self.root,
            capture_output=True,
        ).returncode == 0

    def _record_uncommitted_task(self, task_id: str, task_path: Path, task_rel: str) -> None:
        """Commit the body of a task HEAD never saw, before the closing commit removes it.

        The record commit carries ``Closeout-Mode: record`` so the closing commit does
        not fold itself into it through the same-Task-Id amend.
        """
        if self._in_head(task_rel):
            return
        message = f"desk: registra {task_path.stem}\n\nTask-Id: {task_id}\nCloseout-Mode: record\n"
        added = subprocess.run(
            ["git", "add", "--", task_rel], cwd=self.root, capture_output=True, text=True
        )
        if added.returncode != 0:
            raise ClosureCommitError(added.stderr.strip() or added.stdout.strip() or f"git add failed for {task_rel}")
        result = subprocess.run(
            ["git", "commit", "-m", message, "--", task_rel],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

    def _git_ignores(self, path: str) -> bool:
        """Whether `path` is excluded by the project's ignore rules (a tracked file never is)."""
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=self.root,
                                capture_output=True, text=True)
        return result.returncode == 0

    def _git_knows(self, path: str) -> bool:
        """Whether `path` matches anything in the index or in HEAD."""
        for argv in (["ls-files", "--", path], ["ls-tree", "-r", "--name-only", "HEAD", "--", path]):
            listed = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
            if listed.returncode == 0 and listed.stdout.strip():
                return True
        return False

    def _git(self, *argv: str, check: bool = True) -> str:
        result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise ClosureCommitError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result.stdout.strip()

FILE:deskops/services/retire.py
"""Retire one obsolete desk document, leaving the reason for the commit that removes it.

Kinds with their own lifecycle keep their own verb: tasks close through closeout,
drawer entries through ``drawer remove``, atoms through ``atoms delete`` and registry
entries through ``repo remove``. Everything else under desk/ (pills, inbox notes,
steps, roles, runtimes, faq, logbook, materializations, leftover files) retires here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops import doc_io
from deskops.errors import DomainError
from deskops.models import BoardDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

_DEDICATED_VERBS = (
    ("desk/tasks/", "deskops closeout commit|supersede|retire"),
    ("desk/drawer/", "deskops drawer remove"),
    ("desk/atoms/", "deskops atoms delete"),
    ("desk/registry/", "deskops repo remove"),
)
_REFERENCE_SURFACES = ("desk", "docs")
_REFERENCE_FILES = ("README.md", "AGENTS.md")
#: Paths `deskops doctor` and `deskops desk update` require as the desk's structure.
_REQUIRED_STRUCTURE = frozenset(
    {
        "desk/config.json",
        "desk/drawer",
        "desk/rituals/phase.md",
        "desk/tasks/Board.md",
    }
)


@dataclass(frozen=True)
class RetireResult:
    path: str
    reason: str
    refs: tuple[str, ...]
    boards: tuple[str, ...] = ()


def retire_document(
    root: Path,
    target: str,
    reason: str,
    refs: list[str],
    *,
    force: bool = False,
    ref_resolves=None,
) -> RetireResult:
    """Delete one file under desk/ (and its store record) after checking the reason, refs and inbound links."""
    root = root.resolve()
    path = Path(target)
    path = (path if path.is_absolute() else root / path).resolve()
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError as exc:
        raise DomainError(f"{target} is not inside {root}") from exc
    if not relative.startswith("desk/"):
        raise DomainError(f"{relative} is not a file under desk/")
    closed_issue = _is_retirable_drawer_issue(path, relative)
    for prefix, verb in _DEDICATED_VERBS:
        if relative.startswith(prefix) and not closed_issue:
            if relative.startswith("desk/drawer/issues/"):
                verb = "deskops issue close (open issues), then deskops retire"
            raise DomainError(f"{relative} has its own retirement verb: use `{verb}`.")
    if relative in _REQUIRED_STRUCTURE:
        raise DomainError(
            f"{relative} is required desk structure: `deskops doctor` repairs it, so it cannot be retired."
        )
    if not path.is_file():
        raise DomainError(f"{relative} is not a file under desk/")

    reason = " ".join(reason.split())
    if not reason:
        raise DomainError("--reason must not be empty.")
    clean_refs = tuple(ref.strip() for ref in refs if ref.strip())
    if not clean_refs:
        raise DomainError("Give at least one --ref: the commit or file that replaces or resolves this document.")
    unresolved = [ref for ref in clean_refs if not _ref_resolves(root, ref, ref_resolves)]
    if unresolved:
        raise DomainError(f"Unresolvable --ref: {', '.join(unresolved)} (use an ancestor commit or an existing path).")

    updates = _board_pill_updates(root, path, relative)
    drawer_board = root / "desk" / "drawer" / "tasks" / "Board.md"
    unrouted_drawer = closed_issue and drawer_board.is_file() and _drawer_bullets_removed(drawer_board, path.stem) is not None
    if not force:
        skip = _handled_boards(root, updates, path, relative)
        if unrouted_drawer:
            skip.add(drawer_board.resolve())
        inbound = _inbound_references(root, path, relative, skip=skip)
        if inbound:
            raise DomainError(
                f"Refusing to retire {relative}: still referenced by {', '.join(inbound)}. "
                "Update those first, or pass --force."
            )

    with doc_io.DocTransaction(root) as transaction:
        for board_path, payload in updates:
            _write_board(root, board_path, payload)
        if unrouted_drawer:
            transaction.record(drawer_board)
            drawer_board.write_text(_drawer_bullets_removed(drawer_board, path.stem), encoding="utf-8")
        transaction.delete(path)
    boards = [board_path.relative_to(root).as_posix() for board_path, _ in updates]
    if unrouted_drawer:
        boards.append(drawer_board.relative_to(root).as_posix())
    return RetireResult(path=relative, reason=reason, refs=clean_refs, boards=tuple(boards))


def _is_retirable_drawer_issue(path: Path, relative: str) -> bool:
    """A drawer issue that is already closed or resolved, or an archived record."""
    if not relative.startswith("desk/drawer/issues/") or path.suffix != ".md" or not path.is_file():
        return False
    from deskops.services.issues import issue_status

    text = path.read_text(encoding="utf-8")
    if issue_status(text) in {"closed", "resolved"}:
        return True
    return _frontmatter_record(text)


def _frontmatter_record(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    import yaml

    try:
        block = text.split("---\n", 2)[1]
        loaded = yaml.safe_load(block)
    except (IndexError, yaml.YAMLError):
        return False
    return isinstance(loaded, dict) and loaded.get("record") is True


def _drawer_bullets_removed(board: Path, stem: str) -> str | None:
    """The drawer Board without its ``- `<stem>` `` bullets, or None when it has none."""
    text = board.read_text(encoding="utf-8")
    prefix = f"- `{stem}`"
    kept = "".join(line for line in text.splitlines(keepends=True) if not line.startswith(prefix))
    return kept if kept != text else None


def _pill_reference_matches(reference: str, relative: str, stem: str) -> bool:
    return reference in {
        relative,
        f"desk/contexts/{stem}",
        f"desk/contexts/{stem}.md",
        stem,
    }


def _board_pill_updates(root: Path, path: Path, relative: str) -> list[tuple[Path, dict]]:
    """Boards whose ``pills`` list routes ``relative``, with that entry removed."""
    if not relative.startswith("desk/contexts/"):
        return []
    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    updates: list[tuple[Path, dict]] = []
    for board_path in sorted(tasks_dir.glob("*.md")):
        if board_path.name != "Board.md" and not board_path.stem.startswith("board-"):
            continue
        try:
            payload = extract_model_data(BoardDoc, board_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        payload.setdefault("id", board_path.stem)
        pills = [str(item) for item in payload.get("pills") or []]
        kept = [item for item in pills if not _pill_reference_matches(item, relative, path.stem)]
        if kept == pills:
            continue
        payload["pills"] = kept
        updates.append((board_path, payload))
    return updates


def _handled_boards(root: Path, updates: list[tuple[Path, dict]], path: Path, relative: str) -> set[Path]:
    """Boards whose rewrite removes every textual reference to the retired pill."""
    needles = {relative, path.stem}
    handled: set[Path] = set()
    for board_path, payload in updates:
        try:
            rewritten = render_model_markdown(BoardDoc, payload) + "\n"
        except ValueError:
            continue
        if not any(needle in rewritten for needle in needles):
            handled.add(board_path.resolve())
    return handled


def _write_board(root: Path, board_path: Path, payload: dict) -> None:
    from deskops.operations import DeskopsOperations

    DeskopsOperations(root)._write_doc(board_path, BoardDoc, payload)


def _ref_resolves(root: Path, ref: str, ref_resolves) -> bool:
    if ref_resolves is not None:
        return ref_resolves(ref)
    if (root / ref).exists():
        return True
    from deskops.services.closeout_gates import CloseoutGatesService

    return CloseoutGatesService(root).reference_points_to_commit(ref)


def _inbound_references(root: Path, path: Path, relative: str, *, skip: set[Path] | None = None) -> list[str]:
    skip = skip or set()
    needles = {relative}
    if path.suffix == ".md":
        needles.add(path.stem)
    found: list[str] = []
    candidates: list[Path] = []
    for surface in _REFERENCE_SURFACES:
        base = root / surface
        if base.is_dir():
            candidates.extend(sorted(base.rglob("*.md")))
    candidates.extend(root / name for name in _REFERENCE_FILES if (root / name).is_file())
    for candidate in candidates:
        if candidate.resolve() == path or candidate.resolve() in skip:
            continue
        try:
            text = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(needle in text for needle in needles):
            found.append(candidate.relative_to(root).as_posix())
    return found

FILE:deskops/services/desk_view.py
"""Read-only views of one desk for the deskops UI.

Each view composes existing operations (``show_task``, ``verify_task_closeout``,
``next_action_report``, the drawer and inbox readers, the Herdr runtime and the
run index) into one JSON-ready dict. Nothing here writes: a reference that does
not resolve lands in the view's ``errors`` list with its cause, never as data.

The contract of every view is written in ``docs/deskops-ui.md``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shlex
from typing import Any, Callable

from deskops import lifecycle
from deskops.models import BoardDoc
from deskops.models import InboxNoteDoc
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations

CONTRACT_VERSION = 1
BOARD_REF = Path("desk") / "tasks" / "Board.md"
RUN_INDEX = Path("runs") / "subagents" / "index.jsonl"
DEFAULT_RUNS_LIMIT = 20
EXCERPT_LINES = 3
_TEMPLATE_HINT = re.compile(r"^_.*_$")
_NOTE_STAMP = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-")


class DeskViewError(RuntimeError):
    """The view cannot be produced at all (no desk, unknown task)."""


def task_revision(board_path: Path, task_path: Path) -> str:
    """The advance guard: sha256 of Board.md bytes, a NUL byte, and the task file bytes.

    Same formula as graph_ui's ``DeskRoutes.detail``.
    """
    return hashlib.sha256(board_path.read_bytes() + b"\0" + task_path.read_bytes()).hexdigest()


def note_revision(path: Path) -> str:
    """The guard for inbox actions: sha256 of the note file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DeskView:
    def __init__(
        self,
        root: Path,
        *,
        operations: DeskopsOperations | None = None,
        runs_limit: int = DEFAULT_RUNS_LIMIT,
        herdr: str = "herdr",
        workers_provider: Callable[[], list[dict[str, Any]]] | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.board_path = self.root / BOARD_REF
        if not self.board_path.is_file():
            raise DeskViewError(f"No desk board at {self.board_path}; run 'deskops init' first.")
        self.ops = operations or DeskopsOperations(self.root)
        self.runs_limit = runs_limit
        self.herdr = herdr
        self._workers_provider = workers_provider
        self._spec = lifecycle.load_lifecycle_spec()

    # ------------------------------------------------------------ helpers
    def _rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    @staticmethod
    def _error(errors: list[dict[str, str]], reference: str, cause: str, task: str | None = None) -> None:
        item = {"reference": reference, "cause": cause}
        if task:
            item["task"] = task
        if item not in errors:
            errors.append(item)

    def _lifecycle_nodes(self) -> list[dict[str, Any]]:
        nodes = []
        for state in self._spec.states:
            node = str(state.get("current_node") or "")
            if not node or node == lifecycle.COMPLETE:
                continue
            nodes.append(
                {
                    "node": node,
                    "phase": str(state.get("phase") or ""),
                    "purpose": str(state.get("purpose") or ""),
                }
            )
        known = {item["node"] for item in nodes}
        for node in self._spec.rituals:
            if node not in known:
                nodes.append({"node": node, "phase": "", "purpose": ""})
        return nodes

    def _board_payload(self) -> dict[str, Any]:
        return self.ops._read_doc(self.board_path, BoardDoc)

    def _board_task_paths(self, errors: list[dict[str, str]]) -> list[Path]:
        tasks_dir = (self.root / "desk" / "tasks").resolve()
        paths: list[Path] = []
        for ref in self._board_payload().get("tasks") or []:
            path = (self.root / str(ref)).resolve()
            if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md":
                self._error(errors, str(ref), "Board reference is outside desk/tasks/ or is not a task file.")
                continue
            if not path.is_file():
                self._error(errors, str(ref), "Board reference points to a missing task file.")
                continue
            if path in paths:
                self._error(errors, str(ref), "Task listed twice in the Board.")
                continue
            paths.append(path)
        return paths

    def _resolve_pill(self, pill_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.pill", pill_id)
        except Exception:
            return None

    def _resolve_atom(self, atom_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.atom", atom_id)
        except Exception:
            return None

    def _pills(
        self, refs: list[tuple[str, str]], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        pills = []
        for pill_id, source in refs:
            doc = self._resolve_pill(pill_id)
            if doc is None:
                self._error(
                    errors,
                    pill_id,
                    f"Pill referenced by the {source} does not resolve to a PillDoc.",
                    task if source == "task" else None,
                )
                continue
            item = {"id": pill_id, "title": str(doc.get("title") or ""), "source": source}
            if detail:
                item.update({key: str(doc.get(key) or "") for key in ("what", "when", "how_not")})
            pills.append(item)
        return pills

    def _atoms(
        self, ids: list[str], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        atoms = []
        for atom_id in ids:
            doc = self._resolve_atom(atom_id)
            if doc is None:
                self._error(errors, atom_id, "Atom referenced by the task does not resolve to an AtomDoc.", task)
                continue
            item = {"id": atom_id, "title": str(doc.get("title") or "")}
            if detail:
                item["question"] = str(doc.get("five_wh_one_plus") or "")
                item["answer"] = str(doc.get("answer") or "")
            atoms.append(item)
        return atoms

    @staticmethod
    def _atom_ids(payload: dict[str, Any]) -> list[str]:
        ids = [str(item) for item in payload.get("effective_atoms") or payload.get("atoms") or []]
        ids += [
            str(ref)
            for ref in payload.get("effective_references") or payload.get("references") or []
            if str(ref).startswith("atom-")
        ]
        return list(dict.fromkeys(ids))

    def _closeout(self, task_id: str, node: str, errors: list[dict[str, str]]) -> dict[str, Any] | None:
        try:
            report = self.ops.verify_task_closeout(task_id)
        except Exception as exc:
            self._error(errors, task_id, f"verify_task_closeout failed: {exc}")
            return None
        at_closeout = node == "ritual-closeout"
        evidence = []
        for name, gate in report.get("gates", {}).items():
            state = "holds" if gate.get("ok") else ("failing" if at_closeout else "pending")
            evidence.append(
                {
                    "gate": name,
                    "state": state,
                    "evidence": list(gate.get("evidence") or []),
                    "findings": list(gate.get("findings") or []),
                }
            )
        for finding in report.get("findings", []):
            if finding.get("code") == "unknown_closeout_evidence":
                evidence.append({"gate": "unknown", "state": "failing", "evidence": [], "findings": [finding]})
        return {
            "ok": bool(report.get("ok")),
            "declared": list(report.get("declared") or []),
            "found": list(report.get("found") or []),
            "summary": report.get("summary"),
            "implicit_code": bool(report.get("implicit_code")),
            "alerts": list(report.get("alerts") or []),
            "evidence": evidence,
        }

    def _card(
        self, path: Path, board_pills: list[str], errors: list[dict[str, str]], *, detail: bool = False
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        stem = path.stem
        payload = self.ops._resolve_task_payload(stem)
        task_id = str(payload.get("id") or stem)
        task, gates = self.ops.show_task(stem)
        node = str(payload.get("current_node") or "")
        if task is not None and not gates and node and node != lifecycle.COMPLETE:
            try:
                self.ops._transitions_from(node)
                cause = f"The desk lifecycle graph declares no transition leaving {node}."
            except Exception as exc:
                cause = f"Lifecycle gates unavailable: {exc}"
            self._error(errors, task_id, cause)
        pill_refs = [(str(p), "task") for p in payload.get("effective_pills") or payload.get("pills") or []]
        pill_refs += [(p, "board") for p in board_pills if p not in {ref for ref, _ in pill_refs}]
        card = {
            "id": task_id,
            "title": str(payload.get("title") or ""),
            "status": str(payload.get("status") or ""),
            "current_node": node,
            "task_type": str(payload.get("task_type") or ""),
            "path": self._rel(path),
            "gates": [dict(gate) for gate in gates],
            "gates_holding": sum(1 for gate in gates if gate.get("holds")),
            "gates_total": len(gates),
            "closeout": self._closeout(stem, node, errors),
            "pills": self._pills(pill_refs, errors, detail=detail, task=task_id),
            "atoms": self._atoms(self._atom_ids(payload), errors, detail=detail, task=task_id),
        }
        return card, payload

    # ------------------------------------------------------------ views
    def board(self) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._board_view()

    def _board_view(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        board = self._board_payload()
        board_pills = [str(p) for p in board.get("pills") or []]
        nodes = self._lifecycle_nodes()
        columns = {item["node"]: {**item, "in_lifecycle": True, "count": 0, "tasks": []} for item in nodes}
        for path in self._board_task_paths(errors):
            try:
                card, _ = self._card(path, board_pills, errors)
            except Exception as exc:
                self._error(errors, self._rel(path), f"Task does not load: {exc}")
                continue
            node = card["current_node"]
            if node not in columns:
                self._error(errors, card["id"], f"current_node '{node}' is not a node of the task lifecycle.")
                columns[node] = {"node": node, "phase": "", "purpose": "", "in_lifecycle": False, "count": 0, "tasks": []}
            columns[node]["tasks"].append(card)
            columns[node]["count"] += 1
        cards = [card for column in columns.values() for card in column["tasks"]]
        return {
            "view": "board",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "board": {
                "path": self._rel(self.board_path),
                "pills": self._pills([(p, "board") for p in board_pills], errors, detail=False),
            },
            "columns": list(columns.values()),
            "counts": {
                "tasks": len(cards),
                "by_node": {node: column["count"] for node, column in columns.items()},
                "gates_holding": sum(card["gates_holding"] for card in cards),
                "gates_total": sum(card["gates_total"] for card in cards),
            },
            "errors": errors,
        }

    def task(self, selector: str) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._task_view(selector)

    def _task_view(self, selector: str) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        try:
            path = self.ops._resolve_artifact_selector("artifact.task", self.ops.desk_root / "tasks", selector)
        except (FileNotFoundError, ValueError) as exc:
            raise DeskViewError(f"Task '{selector}' does not resolve: {exc}") from exc
        board_paths = self._board_task_paths([])
        board_pills = [str(p) for p in self._board_payload().get("pills") or []]
        card, payload = self._card(path, board_pills, errors, detail=True)
        try:
            report = self.ops.next_action_report(path.stem)
            next_info = {
                "phase": report.get("phase", ""),
                "ritual": report.get("ritual", ""),
                "next_actions": list(report.get("next_actions") or []),
                "advance_when": list(report.get("advance_when") or []),
            }
        except Exception as exc:
            next_info = None
            self._error(errors, card["id"], f"next_action_report failed: {exc}")
        return {
            "view": "task",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "task": {
                **card,
                "on_board": path.resolve() in board_paths,
                "why": str(payload.get("why") or ""),
                "goal": str(payload.get("goal") or ""),
                "scope": str(payload.get("scope") or ""),
                "implementation_path": str(payload.get("implementation_path") or ""),
                "validation": [str(v) for v in payload.get("effective_validation") or payload.get("validation") or []],
                "done_when": str(payload.get("effective_done_when") or payload.get("done_when") or ""),
                "references": [str(r) for r in payload.get("effective_references") or payload.get("references") or []],
                "files": [str(f) for f in payload.get("files") or []],
                "depends_on": [str(d) for d in payload.get("depends_on") or []],
                "inherits_from": [str(i) for i in payload.get("inherits_from") or []],
                "from_drawer": str(payload.get("from_drawer") or ""),
                "history": [str(h) for h in payload.get("history") or []],
            },
            "next": next_info,
            "revision": task_revision(self.board_path, path),
            "errors": errors,
        }

    def drawer(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        drawer_dir = self.root / "desk" / "drawer" / "tasks"
        index_files = self.ops.drawer.DRAWER_INDEX_FILES
        entries = []
        files = sorted(p for p in drawer_dir.glob("*.md") if p.name not in index_files) if drawer_dir.is_dir() else []
        for path in files:
            rel = self._rel(path)
            try:
                text = self.ops.drawer._read_markdown(path)
            except Exception as exc:
                self._error(errors, rel, f"Drawer file does not parse: {exc}")
                continue
            try:
                doc = self.ops._read_doc(path, TaskDoc)
            except Exception as exc:
                doc = {}
                self._error(errors, rel, f"Drawer file is not a valid TaskDoc: {exc}")
            lines = [
                line.strip()
                for line in text["body"].splitlines()
                if line.strip() and not line.lstrip().startswith("#") and not _TEMPLATE_HINT.match(line.strip())
            ]
            entries.append(
                {
                    "id": str(doc.get("id") or path.stem),
                    "markdown": path.read_text(encoding="utf-8"),
                    "title": text["title"],
                    "status": str(doc["status"]) if doc.get("status") else None,
                    "excerpt": lines[:EXCERPT_LINES],
                    "path": rel,
                    "command": "deskops add task --root . --from-drawer "
                    + shlex.quote(rel)
                    + " --title "
                    + shlex.quote(text["title"]),
                }
            )
        return {
            "view": "drawer",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "tasks": entries,
            "count": len(entries),
            "errors": errors,
        }

    def inbox(self) -> dict[str, Any]:
        from deskops.cli.commands.message import MessageCLI

        errors: list[dict[str, str]] = []
        reader = MessageCLI()
        notes = []
        for path in reader._iter_notes(self.root / "desk"):
            rel = self._rel(path)
            try:
                detail = reader._note_detail(path)
            except Exception as exc:
                self._error(errors, rel, f"Inbox note does not parse: {exc}")
                continue
            try:
                body = str(self.ops._read_doc(path, InboxNoteDoc).get("body") or "")
            except Exception as exc:
                body = str(detail.get("body") or "")
                self._error(errors, rel, f"Inbox note is not a valid InboxNoteDoc; body shown raw: {exc}")
            match = _NOTE_STAMP.match(path.name)
            date = "{}-{}-{}T{}:{}:{}".format(*match.groups()) if match else None
            if date is None:
                self._error(errors, rel, "Inbox note filename carries no YYYYMMDD-HHMMSS stamp.")
            status = str(detail.get("status") or "")
            notes.append(
                {
                    "id": path.stem,
                    "path": rel,
                    "kind": str(detail.get("kind") or ""),
                    "title": str(detail.get("title") or ""),
                    "sender": str(detail.get("sender_project") or ""),
                    "target": str(detail.get("target_project") or ""),
                    "date": date,
                    "status": status,
                    "acknowledged": status == "closed",
                    "acknowledged_by": detail.get("acknowledged_by"),
                    "acknowledged_at": detail.get("acknowledged_at"),
                    "body": body,
                    "revision": note_revision(path),
                }
            )
        return {
            "view": "inbox",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "notes": notes,
            "count": len(notes),
            "open": sum(1 for note in notes if not note["acknowledged"]),
            "errors": errors,
        }

    def _list_workers(self) -> list[dict[str, Any]]:
        if self._workers_provider is not None:
            agents = self._workers_provider()
        else:
            from deskops.runtime.herdr import HerdrClient, HerdrProvider

            agents = HerdrProvider(HerdrClient(self.herdr)).list_agents()
        from deskops.cli.commands.runtime import RuntimeCLI

        return [RuntimeCLI._project_agent(agent) for agent in agents]

    def agents(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        workers: list[dict[str, Any]] | None
        workers_error = None
        try:
            workers = self._list_workers()
        except Exception as exc:
            workers = None
            workers_error = f"{type(exc).__name__}: {exc}"
            self._error(errors, "runtime workers", f"Herdr runtime unavailable: {workers_error}")
        board_ids = set()
        for path in self._board_task_paths([]):
            try:
                board_ids.add(str(self.ops._read_doc(path, TaskDoc).get("id") or path.stem))
            except Exception:
                continue
        runs: list[dict[str, Any]] = []
        index = self.root / RUN_INDEX
        total = 0
        if index.is_file():
            lines = index.read_text(encoding="utf-8").splitlines()
            parsed = []
            for number, line in enumerate(lines, start=1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if not isinstance(entry, dict):
                        raise ValueError("entry is not an object")
                except ValueError as exc:
                    self._error(errors, f"{RUN_INDEX.as_posix()}:{number}", f"Run index line does not parse: {exc}")
                    continue
                parsed.append(entry)
            total = len(parsed)
            for entry in reversed(parsed[-self.runs_limit :] if self.runs_limit > 0 else []):
                task_id = str(entry.get("task_id") or "")
                runs.append(
                    {
                        "task_id": task_id,
                        "run_id": entry.get("run_id"),
                        "run_dir": entry.get("run_dir"),
                        "commit": entry.get("commit"),
                        "mode": entry.get("mode"),
                        "on_board": task_id in board_ids,
                    }
                )
        return {
            "view": "agents",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "workers": workers,
            "workers_error": workers_error,
            "live_workers": None if workers is None else len(workers),
            "runs": runs,
            "runs_total": total,
            "runs_limit": self.runs_limit,
            "errors": errors,
        }


# ---------------------------------------------------------------- text rendering
def _errors_text(view: dict[str, Any]) -> list[str]:
    return [f"! {item['reference']}: {item['cause']}" for item in view.get("errors") or []]


def render_text(view: dict[str, Any]) -> str:
    kind = view.get("view")
    lines: list[str] = []
    if kind == "board":
        for column in view["columns"]:
            lines.append(f"{column['node']} ({column['count']})")
            for card in column["tasks"]:
                lines.append(f"  {card['id']} [{card['status']}] gates {card['gates_holding']}/{card['gates_total']} - {card['title']}")
    elif kind == "task":
        task = view["task"]
        lines += [f"{task['id']} [{task['status']}] {task['current_node']}", task["title"], f"revision {view['revision']}"]
        for gate in task["gates"]:
            lines.append(f"  gate {gate['relation_type']} -> {gate['target']}: {'holds' if gate['holds'] else 'pending'} ({gate['condition'] or 'no condition'})")
        for item in (task.get("closeout") or {}).get("evidence", []):
            lines.append(f"  evidence {item['gate']}: {item['state']}")
    elif kind == "drawer":
        for entry in view["tasks"]:
            lines.append(f"{entry['id']} [{entry['status'] or '-'}] {entry['title']}")
    elif kind == "inbox":
        for note in view["notes"]:
            lines.append(f"{note['id']} [{'ack' if note['acknowledged'] else 'open'}] {note['sender']} -> {note['target']}: {note['title']}")
    elif kind == "agents":
        if view["workers"] is None:
            lines.append(f"workers unavailable: {view['workers_error']}")
        else:
            lines.append(f"live workers: {view['live_workers']}")
            for worker in view["workers"]:
                lines.append(f"  {worker.get('pane')} | {worker.get('kind')} | {worker.get('status')} | {worker.get('cwd') or ''}")
        lines.append(f"runs (latest {len(view['runs'])} of {view['runs_total']}):")
        for run in view["runs"]:
            lines.append(f"  {run['task_id']} | {run['mode'] or '-'} | {run['run_dir'] or '-'}")
    return "\n".join([*lines, *_errors_text(view)])

FILE:deskops/specs/__init__.py
from .compiler import CompiledArtifactSpec
from .compiler import CompiledTaskSpec
from .compiler import compile_artifact_spec
from .compiler import compile_task_spec
from .loader import SpecRegistry
from .mermaid import render_artifact_structure_mermaid

__all__ = [
    "CompiledArtifactSpec",
    "CompiledTaskSpec",
    "SpecRegistry",
    "compile_artifact_spec",
    "compile_task_spec",
    "render_artifact_structure_mermaid",
]

FILE:deskops/specs/compiler.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from collections.abc import Collection

from pydantic.fields import PydanticUndefined

from deskops.cli.model_introspection import artifact_id_pattern
from deskops.cli.model_introspection import artifact_tags_default
from deskops.cli.model_introspection import DEFAULT_FACTORY
from .loader import SpecRegistry


@dataclass(slots=True)
class CompiledTaskSpec:
    task_payload: dict[str, Any]


@dataclass(slots=True)
class CompiledArtifactSpec:
    artifact_payload: dict[str, Any]


def compile_task_spec(
    registry: SpecRegistry,
    raw_payload: dict[str, Any],
    *,
    entry_node: str,
) -> CompiledTaskSpec:
    """Compile a task payload. The task starts at ``entry_node`` of the lifecycle graph
    (deskops/lifecycle.py); no per-task primitives or routine are generated."""
    artifact = registry.artifacts["artifact.task"]
    title = str(raw_payload["title"]).strip()
    slug = _slugify(title)
    task_id = str(raw_payload.get("id") or artifact["data"]["doc"]["id_pattern"].format(slug=slug))
    task_payload = {
        "title": title,
        "id": task_id,
        "status": str(raw_payload.get("status") or artifact["data"]["doc"].get("status_default", "draft")),
        "why": str(raw_payload.get("why") or "Not provided."),
        "goal": str(raw_payload.get("goal") or ""),
        "scope": str(raw_payload.get("scope") or ""),
        "references": _coerce_list(raw_payload.get("references") or []),
        "depends_on": _coerce_list(raw_payload.get("depends_on") or []),
        "pills": _coerce_list(raw_payload.get("pills") or []),
        "files": _coerce_list(raw_payload.get("files") or []),
        "implementation_path": str(raw_payload.get("implementation_path") or ""),
        "validation": _coerce_list(raw_payload.get("validation") or []),
        "done_when": str(raw_payload.get("done_when") or ""),
        "history": _coerce_list(raw_payload.get("history") or []),
        "tags": _coerce_list(raw_payload.get("tags") or artifact["data"]["doc"].get("tags", [])),
        "task_type": str(raw_payload.get("task_type") or ""),
        "inherits_from": _coerce_list(raw_payload.get("inherits_from") or []),
        "inherit_acceptance_context": bool(raw_payload.get("inherit_acceptance_context") or False),
        "atoms": _coerce_list(raw_payload.get("atoms") or []),
        "from_drawer": str(raw_payload.get("from_drawer") or ""),
        "closeout_evidence": _coerce_list(raw_payload.get("closeout_evidence") or []),
    }
    task_payload["current_node"] = str(raw_payload.get("current_node") or entry_node)
    return CompiledTaskSpec(task_payload=task_payload)


def compile_artifact_spec(
    registry: SpecRegistry,
    artifact_id: str,
    raw_payload: dict[str, Any],
    *,
    model_fields: Collection[str] | None = None,
) -> CompiledArtifactSpec:
    """Compile a raw payload into an artifact payload using the Pydantic model.

    The Pydantic model is the single source of truth for which fields exist and
    their defaults. The YAML spec (via registry) is consulted only for artifact-
    level config: id_pattern and status_default.
    """
    from deskops.operations import ARTIFACT_MODELS

    artifact = registry.artifacts[artifact_id]
    display_value = raw_payload.get("title") or raw_payload.get("name") or raw_payload.get("id")
    if display_value is None:
        raise KeyError(f"Payload for {artifact_id} must include 'title', 'name', or 'id'")
    title = str(display_value).strip()
    if not title:
        raise ValueError(f"Payload for {artifact_id} has empty title/name/id after stripping whitespace")
    slug = _slugify(title)

    # id_pattern from model_introspection (was in YAML doc section)
    id_pattern = artifact_id_pattern(artifact_id)
    doc_id = str(raw_payload.get("id") or id_pattern.format(slug=slug))

    supported = set(model_fields or [])
    payload: dict[str, Any] = {"id": doc_id}
    if "title" in supported:
        payload["title"] = title

    model = ARTIFACT_MODELS.get(artifact_id)
    if model is not None:
        for field_name, field_info in model.model_fields.items():
            if field_name == "id":
                continue  # already handled

            # Value from raw_payload overrides everything
            if field_name in raw_payload and raw_payload[field_name] is not None:
                payload[field_name] = raw_payload[field_name]
                continue

            # Apply defaults from the Pydantic model
            default = field_info.default
            if default is PydanticUndefined:
                factory = getattr(field_info, "default_factory", None)
                if factory is not None:
                    payload[field_name] = []  # default_factory=list
                # else: required field, leave as None (model validation handles it)
            elif isinstance(default, str):
                payload[field_name] = default
            elif isinstance(default, (list, tuple)):
                payload[field_name] = list(default)
            # else: other default types — leave for model validation

    # Handle status_default from artifact config (not in model)
    if "status" in supported and "status" not in payload:
        status_default = str(artifact["data"]["doc"].get("status_default", "active"))
        payload["status"] = status_default

    # Handle tags default — prefer model factory, fall back to artifact config
    if "tags" in supported and "tags" not in payload:
        # Check if model has default_factory for tags
        if model is not None and "tags" in model.model_fields:
            field_info = model.model_fields["tags"]
            factory = getattr(field_info, "default_factory", None)
            if factory is not None:
                payload["tags"] = []
            else:
                payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))
        else:
            payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))

    return CompiledArtifactSpec(artifact_payload=payload)


def _coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")

FILE:deskops/specs/loader.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class SpecRegistry:
    root: Path
    fields: dict[str, dict[str, Any]]
    artifacts: dict[str, dict[str, Any]]

    @classmethod
    def load(cls, root: Path) -> "SpecRegistry":
        root = root.resolve()
        return cls(
            root=root,
            fields=_load_spec_dir(root / "fields"),
            artifacts=_load_spec_dir(root / "artifacts"),
        )


def _load_spec_dir(directory: Path) -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        specs[str(payload["id"])] = payload
    return specs

FILE:deskops/specs/mermaid.py
from __future__ import annotations

from .loader import SpecRegistry


def render_artifact_structure_mermaid(registry: SpecRegistry, artifact_id: str) -> str:
    artifact = registry.artifacts[artifact_id]
    lines = ["flowchart TD"]
    lines.append(f"  {artifact_id}[{artifact['title']}]")
    for field_id in artifact["data"].get("fields", []):
        lines.append(f"  {field_id}[{field_id}]")
        lines.append(f"  {artifact_id} --> {field_id}")
    return "\n".join(lines)

FILE:deskops/cli/model_introspection.py
"""Introspect Pydantic models to extract CLI-ready field metadata.

Replaces YAML-spec-driven CLI arg generation. The Pydantic model is the
single source of truth for field names, types, defaults, help text, and
validation rules.
"""
from __future__ import annotations

import typing
from dataclasses import dataclass, field as dataclass_field
from typing import Any, Collection

from pydantic import BaseModel, TypeAdapter
from pydantic.fields import FieldInfo, PydanticUndefined


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class CliFieldMeta:
    """Metadata for one CLI-exposed model field."""

    name: str  # Python field name (e.g. "five_wh_one_plus")
    cli_name: str  # CLI flag without dashes (e.g. "five-wh-one-plus")
    help: str  # argparse help text
    is_required: bool  # True when the model has no default
    is_list: bool  # True when the field is a list type
    choices: tuple[str, ...] | None  # Enum choices, if applicable
    default: Any  # Resolved default value or sentinel
    pattern: str | None  # Regex pattern from JSON schema, if any

    @property
    def cli_option(self) -> str:
        """The --flag name for argparse."""
        return f"--{self.cli_name.replace('_', '-')}"


DEFAULT_FACTORY = object()  # sentinel for fields with default_factory=list
REQUIRED = object()  # sentinel for fields with no default at all

# Mirror a small set of field defaults that are part of the operator-facing CLI
# contract for selected models. This keeps argparse metadata aligned with the
# model contract when these fields are intentionally optional/backward-compatible.
_MODEL_FIELD_DEFAULT_OVERRIDES: dict[tuple[str, str], Any] = {
    ("InboxNoteDoc", "target_project"): None,
    ("InboxNoteDoc", "acknowledged_by"): None,
    ("InboxNoteDoc", "acknowledged_at"): None,
}


# ---------------------------------------------------------------------------
# List detection
# ---------------------------------------------------------------------------


def _is_list_annotation(annotation: Any) -> bool:
    """Return True if annotation is list[...] or typing.List[...].
    
    Handles:
      - list[str]
      - typing.List[str]
      - Annotated[..., ...] wrapping a list
    """
    # Direct list origin
    origin = getattr(annotation, "__origin__", None)
    if origin is list or origin is typing.List:
        return True

    # Check Annotated[list[str], ...]
    if hasattr(annotation, "__metadata__"):
        # Walk the Annotated args looking for a list type
        args = getattr(annotation, "__args__", ())
        if args and _is_list_annotation(args[0]):
            return True

    return False


# ---------------------------------------------------------------------------
# Default resolution
# ---------------------------------------------------------------------------


def _resolve_field_default(field: FieldInfo) -> Any:
    """Return the resolved default for a Pydantic field.

    Returns DEFAULT_FACTORY when the field uses default_factory.
    Returns the actual default value when set explicitly (including None).
    Returns REQUIRED when there is no default (required field).
    """
    default = field.default
    if default is PydanticUndefined:
        factory = getattr(field, "default_factory", None)
        if factory is not None:
            return DEFAULT_FACTORY
        return REQUIRED
    return default


# ---------------------------------------------------------------------------
# Enum choice extraction
# ---------------------------------------------------------------------------


def _extract_enum_choices(
    model: type[BaseModel], field_name: str
) -> tuple[str, ...] | None:
    """Extract enum member values from a string enum field via JSON schema.

    Returns None when the field is not a string enum.
    """
    try:
        schema = TypeAdapter(model).json_schema()
    except Exception:
        return None

    props = schema.get("properties", {})
    field_schema = props.get(field_name, {})

    # Follow $ref if present
    ref = field_schema.get("$ref", "")
    if ref:
        defs = schema.get("$defs", {})
        key = ref.split("/")[-1]
        enum_def = defs.get(key, {})
        members = enum_def.get("enum")
        if members is not None and all(isinstance(v, str) for v in members):
            return tuple(str(v) for v in members)
        return None

    # Inline enum (rare)
    enum = field_schema.get("enum")
    if enum is not None:
        return tuple(str(v) for v in enum)

    return None


# ---------------------------------------------------------------------------
# Pattern extraction
# ---------------------------------------------------------------------------


def _extract_pattern(
    model: type[BaseModel], field_name: str
) -> str | None:
    """Extract the first regex pattern found in a field's JSON schema.

    Useful for Annotated fields like AtomTag that carry a pattern.
    """
    try:
        schema = TypeAdapter(model).json_schema()
    except Exception:
        return None

    props = schema.get("properties", {})
    field_schema = props.get(field_name, {})

    # Check top-level pattern
    pat = field_schema.get("pattern")
    if pat:
        return str(pat)

    # Check items level (for list types)
    items = field_schema.get("items", {})
    if isinstance(items, dict):
        pat = items.get("pattern")
        if pat:
            return str(pat)

    return None


# ---------------------------------------------------------------------------
# Core introspection
# ---------------------------------------------------------------------------

# Fields that are operational state or internal — never exposed as CLI args.
# These are managed by the runtime, not set by users at creation time.
_INTERNAL_FIELDS: frozenset[str] = frozenset({
    "id",
    "current_node",
    "history",
})

# Fields managed via a dedicated CLI flag rather than a generic --field option.


def introspect_model(model: type[BaseModel]) -> list[CliFieldMeta]:
    """Return CLI-ready metadata for every user-facing field in a Pydantic model.

    Fields are ordered as they appear in the model definition.

    Skipped fields:
    - ``id`` — generated by slugification
    - ``current_node``, ``history`` — managed by the lifecycle graph (deskops/lifecycle.py)
    - ``status`` — managed by lifecycle transitions on operational artifacts
    """
    results: list[CliFieldMeta] = []
    for name, fInfo in model.model_fields.items():
        if name in _INTERNAL_FIELDS:
            continue
        # status is internal for operational artifacts (TaskDoc, PillDoc, BoardDoc, etc.)
        # but a normal user-settable field for simple artifacts (RepositoryDoc).
        if name == "status":
            from deskops.models.base import OperationalArtifactDoc
            if issubclass(model, OperationalArtifactDoc):
                continue

        is_list = _is_list_annotation(fInfo.annotation)
        choices = _extract_enum_choices(model, name)
        pattern = _extract_pattern(model, name)
        default = _MODEL_FIELD_DEFAULT_OVERRIDES.get(
            (model.__name__, name),
            _resolve_field_default(fInfo),
        )
        is_required = default is REQUIRED

        # Use field description as help text
        help_text = fInfo.description or f"{name.replace('_', ' ').capitalize()}."

        results.append(
            CliFieldMeta(
                name=name,
                cli_name=name,
                help=help_text,
                is_required=is_required,
                is_list=is_list,
                choices=choices,
                default=default,
                pattern=pattern,
            )
        )

    return results


def model_cli_fields(
    model: type[BaseModel],
    *,
    include_special: bool = False,
) -> list[CliFieldMeta]:
    """Return CLI fields for a given model.

    The `include_special` flag controls exclusion of fields that have dedicated
    hardcoded CLI flags on the task subcommand (--depends-on, --validation).
    For non-task artifacts, these fields are normal user-settable fields and
    are always included.
    """
    metas = introspect_model(model)
    if include_special:
        # Task subcommand has hardcoded --depends-on and --validation flags.
        # Exclude them from generated args to avoid duplication.
        return [m for m in metas if m.name not in frozenset({"depends_on", "validation"})]
    return metas


def artifact_model_fields() -> dict[str, type[BaseModel]]:
    """Map artifact_id -> Pydantic model class for all artifact subjects.

    This is the authoritative mapping used by CLI arg generation.
    """
    from deskops.operations import ARTIFACT_MODELS
    from deskops.models import (
        AtomDoc,
        BoardDoc,
        DeskFAQDoc,
        InboxNoteDoc,
        MaterializationContractDoc,
        PillDoc,
        RepositoryDoc,
        RitualDoc,
        StepDoc,
    )

    return {
        "artifact.atom": AtomDoc,
        "artifact.board": BoardDoc,
        "artifact.faq": DeskFAQDoc,
        "artifact.inbox_note": InboxNoteDoc,
        "artifact.materialization": MaterializationContractDoc,
        "artifact.pill": PillDoc,
        "artifact.repository": RepositoryDoc,
        "artifact.ritual": RitualDoc,
        "artifact.step": StepDoc,
        # artifact.task uses a separate bundle creation path (not this path)
    }


# ---------------------------------------------------------------------------
# Spec-level defaults (the only YAML concern we keep)
# ---------------------------------------------------------------------------

# Artifact-level defaults that live in YAML and are not in the model.
# These are id_pattern, status_default, and tags defaults.
# The YAML spec is the source of truth here because these are
# artifact-level configuration, not field-level schema.

_ARTIFACT_DEFAULTS: dict[str, dict[str, Any]] = {
    "artifact.atom": {
        "id_pattern": "atom-{slug}",
        "status_default": None,
        "tags": ["system:deskops", "topic:atoms"],
    },
    "artifact.board": {
        "id_pattern": "board-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:board"],
    },
    "artifact.faq": {
        "id_pattern": "faq-{slug}",
        "status_default": "active",
        "tags": ["workspace:docs", "artifact:faq"],
    },
    "artifact.inbox_note": {
        "id_pattern": "inbox-note-{slug}",
        "status_default": "open",
        "tags": ["workspace:desk", "artifact:inbox-note"],
    },
    "artifact.materialization": {
        "id_pattern": "materialization-{slug}",
        "status_default": None,
        "tags": ["system:deskops", "topic:materialization"],
    },
    "artifact.pill": {
        "id_pattern": "pill-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:pill"],
    },
    "artifact.repository": {
        "id_pattern": "repo-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:repository"],
    },
    "artifact.ritual": {
        "id_pattern": "ritual-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:ritual"],
    },
    "artifact.step": {
        "id_pattern": "step-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:step"],
    },
}


def artifact_id_pattern(artifact_id: str) -> str:
    """Return the id_pattern for an artifact. E.g. 'atom-{slug}'."""
    return _ARTIFACT_DEFAULTS.get(artifact_id, {}).get(
        "id_pattern", "{slug}"
    )


def artifact_status_default(artifact_id: str) -> str | None:
    """Return the status_default for an artifact, or None if status is not managed."""
    return _ARTIFACT_DEFAULTS.get(artifact_id, {}).get("status_default")


def artifact_tags_default(artifact_id: str) -> list[str]:
    """Return the default tags for an artifact when none are provided."""
    return list(_ARTIFACT_DEFAULTS.get(artifact_id, {}).get("tags", []))

FILE:deskops/workflow/next_actions.py
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_task_lifecycle_spec(spec_root: Path) -> dict[str, Any]:
    path = spec_root / "workflows" / "task_lifecycle.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Workflow spec must be a mapping: {path}")
    payload["_path"] = path
    return payload


def match_workflow_state(spec: dict[str, Any], current_node: str) -> dict[str, Any]:
    node = current_node or ""
    for state in spec.get("states") or []:
        if not isinstance(state, dict):
            continue
        if state.get("current_node") == node:
            return state
    if not node:
        return _first_state(spec)
    raise ValueError(f"No workflow state in {spec.get('_path')} matches current node '{current_node}'")


def render_workflow_mermaid(spec: dict[str, Any]) -> str:
    """Mermaid of the lifecycle graph: one node per state, one arrow per transition,
    labelled with its relation type and condition."""
    states = [state for state in spec.get("states") or [] if isinstance(state, dict)]
    by_node = {str(state.get("current_node")): str(state["id"]) for state in states}
    lines = ["flowchart TD"]
    for state in states:
        state_id = str(state["id"])
        label = str(state.get("phase") or state_id).replace('"', "'")
        lines.append(f'    {state_id}["{label}"]')
    for transition in spec.get("transitions") or []:
        source = by_node.get(str(transition["source"]), str(transition["source"]))
        target_node = "complete" if transition.get("terminal") else str(transition["target"])
        target = by_node.get(target_node, target_node)
        label = str(transition["relation_type"])
        if transition.get("condition"):
            label += f": {transition['condition']}"
        lines.append(f'    {source} -->|"{label.replace(chr(34), chr(39))}"| {target}')
    return "\n".join(lines)


def _first_state(spec: dict[str, Any]) -> dict[str, Any]:
    states = [state for state in spec.get("states") or [] if isinstance(state, dict)]
    if not states:
        raise ValueError(f"Workflow spec has no states: {spec.get('_path')}")
    return states[0]

FILE:tests/test_specs.py
from __future__ import annotations

from pathlib import Path

from deskops.paths import data_path
from deskops.specs.compiler import compile_task_spec
from deskops.specs.loader import SpecRegistry
from deskops.specs.mermaid import render_artifact_structure_mermaid


ROOT = Path(__file__).resolve().parents[1]
SPEC_ROOT = data_path("spec")


def test_spec_registry_loads_fields_and_artifacts() -> None:
    registry = SpecRegistry.load(SPEC_ROOT)

    assert "field.goal" in registry.fields
    assert "field.validation" in registry.fields
    assert not hasattr(registry, "primitives"), "per-task primitive specs are gone; the lifecycle is a graph"
    assert "artifact.task" in registry.artifacts
    assert "artifact.pill" in registry.artifacts
    assert "artifact.ritual" in registry.artifacts
    assert "artifact.board" in registry.artifacts
    assert "artifact.atom" in registry.artifacts
    assert "artifact.repository" in registry.artifacts
    assert "artifact.inbox_note" in registry.artifacts
    assert "artifact.faq" in registry.artifacts
    assert "artifact.step" in registry.artifacts
    assert "field.description" in registry.fields
    assert "field.related_atoms" in registry.fields
    assert "field.created_at" in registry.fields


def test_task_spec_compiler_builds_only_the_task_at_the_lifecycle_entry() -> None:
    registry = SpecRegistry.load(SPEC_ROOT)
    compiled = compile_task_spec(
        registry,
        {
            "title": "Spec authored task",
            "goal": "Drive task creation from YAML specs.",
            "scope": "Task pipeline only.",
            "implementation_path": "Compile artifact spec into runtime-ready docs.",
            "done_when": "The task is produced from specs.",
            "validation": ["pytest"],
        },
        entry_node="ritual-execution",
    )

    assert compiled.task_payload["id"] == "task-spec-authored-task"
    assert compiled.task_payload["current_node"] == "ritual-execution"
    assert "routine" not in compiled.task_payload
    assert "checklists" not in compiled.task_payload
    assert "field_refs" not in compiled.task_payload
    assert compiled.task_payload["title"] == "Spec authored task"
    assert compiled.task_payload["goal"] == "Drive task creation from YAML specs."
    assert compiled.task_payload["scope"] == "Task pipeline only."
    assert compiled.task_payload["implementation_path"] == "Compile artifact spec into runtime-ready docs."
    assert compiled.task_payload["validation"] == ["pytest"]
    assert compiled.task_payload["done_when"] == "The task is produced from specs."


def test_mermaid_views_render_from_task_specs() -> None:
    registry = SpecRegistry.load(SPEC_ROOT)
    structure = render_artifact_structure_mermaid(registry, "artifact.task")

    assert "artifact.task[Task Artifact]" in structure
    assert "field.goal[field.goal]" in structure

FILE:tests/test_extension_points.py
"""The public extension registries must agree as one contract.

Models, spec artifacts, artifact maps, and CLI handlers are declared in separate
places and maintained by convention. These tests fail when one of them drifts,
so a new model or command cannot land half-registered.
"""

from __future__ import annotations

import importlib

from sldb import StructuredNLDoc

from deskops import models
from deskops.bootstrap import MODEL_REFS
from deskops.cli.registry import command_registry
from deskops.operations import ARTIFACT_MODELS
from deskops.operations import ARTIFACT_PATHS
from deskops.operations import ARTIFACT_SUBJECTS
from deskops.paths import data_path
from deskops.specs import SpecRegistry

TASK_ARTIFACT = "artifact.task"


def test_every_artifact_model_has_a_path() -> None:
    assert set(ARTIFACT_MODELS) <= set(ARTIFACT_PATHS)
    assert set(ARTIFACT_PATHS) <= set(ARTIFACT_MODELS)


def test_every_artifact_except_task_has_a_subject() -> None:
    assert set(ARTIFACT_MODELS) - set(ARTIFACT_SUBJECTS) == {TASK_ARTIFACT}
    assert set(ARTIFACT_SUBJECTS) <= set(ARTIFACT_MODELS)


def test_model_refs_are_exported_structured_documents() -> None:
    for name in MODEL_REFS:
        assert name in models.__all__, f"{name} is registered but not exported"
        model = getattr(models, name)
        assert isinstance(model, type)
        assert issubclass(model, StructuredNLDoc)


def test_every_spec_artifact_resolves_to_an_artifact_model() -> None:
    artifacts = SpecRegistry.load(data_path("spec")).artifacts

    for artifact_id in artifacts:
        assert artifact_id in ARTIFACT_MODELS or artifact_id == TASK_ARTIFACT


def test_every_command_handler_resolves() -> None:
    commands = command_registry()
    assert commands

    for command in commands:
        module_name, separator, attribute = command.handler.partition(":")
        assert separator and module_name and attribute, (
            f"{command.path} handler is not module:attribute: {command.handler}"
        )
        module = importlib.import_module(module_name)
        handler = getattr(module, attribute)
        assert callable(handler), f"{command.path} handler is not callable: {command.handler}"

FILE:tests/test_desk_view.py
"""deskops view: the read-only views the deskops UI draws, over real temporary desks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations
from deskops.services.desk_view import DeskView
from deskops.services.desk_view import DeskViewError


def _task(operations: DeskopsOperations, title: str, **extra: object) -> str:
    payload = {
        "title": title,
        "goal": f"goal of {title}",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest -q tests/test_x.py"],
        "task_type": "code",
        **extra,
    }
    return operations.create_task_bundle(payload).task_id


def _pill(operations: DeskopsOperations, title: str) -> str:
    record = operations.create_artifact(
        "artifact.pill",
        {
            "title": title,
            "what": "what text",
            "why": "why text",
            "when": "when text",
            "where": "where text",
            "how": "how text",
            "how_not": "how not text",
            "tags": ["topic:view"],
        },
    )
    return record.doc_id


def _atom(operations: DeskopsOperations, title: str) -> str:
    record = operations.create_artifact(
        "artifact.atom",
        {"title": title, "five_wh_one_plus": "what", "answer": "the answer", "tags": ["topic:view"]},
    )
    return record.doc_id


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def _cli_json(capsys: pytest.CaptureFixture[str], *argv: str) -> dict:
    capsys.readouterr()
    assert main(list(argv)) == 0
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def desk(lifecycle_desk: Path) -> dict:
    ops = DeskopsOperations(lifecycle_desk)
    pill = _pill(ops, "Guardrail: view pill")
    atom = _atom(ops, "Atom for the view")
    first = _task(ops, "First task", pills=[pill], atoms=[atom])
    second = _task(ops, "Second task", pills=["pill-does-not-exist"], atoms=["atom-does-not-exist"])
    ops.advance_task(second)
    return {"root": lifecycle_desk, "ops": ops, "first": first, "second": second, "pill": pill, "atom": atom}


def test_board_groups_by_current_node_in_spec_order_and_counts_gates_like_show_task(desk: dict) -> None:
    view = DeskView(desk["root"]).board()

    assert [column["node"] for column in view["columns"]] == ["ritual-execution", "ritual-testing", "ritual-closeout"]
    by_node = {column["node"]: [card["id"] for card in column["tasks"]] for column in view["columns"]}
    assert by_node == {"ritual-execution": [desk["first"]], "ritual-testing": [desk["second"]], "ritual-closeout": []}
    assert view["counts"]["by_node"] == {"ritual-execution": 1, "ritual-testing": 1, "ritual-closeout": 0}
    for column in view["columns"]:
        for card in column["tasks"]:
            _, gates = desk["ops"].show_task(card["id"])
            assert card["gates"] == gates
            assert card["gates_holding"] == sum(1 for gate in gates if gate["holds"])
            assert card["gates_total"] == len(gates)
            report = desk["ops"].verify_task_closeout(card["id"])
            assert card["closeout"]["declared"] == report["declared"]
            assert card["closeout"]["found"] == report["found"]


def test_unresolvable_pill_and_atom_go_to_errors_not_to_the_card(desk: dict) -> None:
    view = DeskView(desk["root"]).board()
    cards = {card["id"]: card for column in view["columns"] for card in column["tasks"]}

    first, second = cards[desk["first"]], cards[desk["second"]]
    assert [p["id"] for p in first["pills"]] == [desk["pill"]]
    assert first["pills"][0]["title"] == "Guardrail: view pill"
    assert [a["id"] for a in first["atoms"]] == [desk["atom"]]
    assert second["pills"] == [] and second["atoms"] == []
    references = {item["reference"]: item.get("task") for item in view["errors"]}
    assert references["pill-does-not-exist"] == desk["second"]
    assert references["atom-does-not-exist"] == desk["second"]
    assert all(item["cause"] for item in view["errors"])


def test_task_view_carries_the_fields_and_the_graph_ui_revision(desk: dict) -> None:
    root = desk["root"]
    view = DeskView(root).task(desk["first"])
    task = view["task"]

    for key in ("goal", "scope", "implementation_path", "validation", "done_when", "why", "references", "files",
                "depends_on", "inherits_from", "gates", "closeout", "pills", "atoms"):
        assert key in task
    assert task["goal"] == "goal of First task"
    assert task["pills"][0]["what"] == "what text" and task["pills"][0]["when"] == "when text"
    assert task["pills"][0]["how_not"] == "how not text"
    assert task["atoms"][0]["answer"] == "the answer"
    assert view["next"]["next_actions"] and view["next"]["advance_when"]
    task_path = root / task["path"]
    expected = hashlib.sha256((root / "desk/tasks/Board.md").read_bytes() + b"\0" + task_path.read_bytes()).hexdigest()
    assert view["revision"] == expected


def test_task_view_revision_matches_graph_ui_desk_routes_when_available(desk: dict) -> None:
    routes = pytest.importorskip("frontends.mindmap.deskops_routes", reason="graph_ui is not importable here")
    detail = routes.DeskRoutes(desk["root"]).detail(desk["first"])
    assert DeskView(desk["root"]).task(desk["first"])["revision"] == detail["revision"]


def test_unknown_task_raises(desk: dict) -> None:
    with pytest.raises(DeskViewError):
        DeskView(desk["root"]).task("task-nope")


def test_drawer_inbox_and_agents_return_what_is_on_disk(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = desk["root"]
    assert main(["message", "send", "--root", str(root), "--title", "Deferred idea", "--kind", "suggestion", "Body of the idea"]) == 0
    assert main(["message", "send", "--root", str(root), "--title", "Open question", "--kind", "unclear", "Question body"]) == 0
    deferred = next(p for p in (root / "desk/inbox").glob("*.md") if "deferred-idea" in p.name)
    assert main(["promote", "inbox-to-drawer-task", deferred.stem, "--root", str(root)]) == 0
    question = next((root / "desk/inbox").glob("*.md"))
    assert main(["message", "ack", question.stem, "--root", str(root)]) == 0
    runs = root / "runs/subagents/index.jsonl"
    runs.parent.mkdir(parents=True)
    runs.write_text(
        json.dumps({"task_id": desk["first"], "run_id": None, "run_dir": None, "mode": "manual", "commit": None}) + "\n"
        + json.dumps({"task_id": "task-gone", "run_id": "r1", "run_dir": "runs/subagents/x", "commit": None}) + "\n",
        encoding="utf-8",
    )
    view = DeskView(root, workers_provider=lambda: [{"pane_id": "w1:p1", "agent": "pi", "agent_status": "idle", "cwd": str(root)}])

    drawer = view.drawer()
    files = sorted(p for p in (root / "desk/drawer/tasks").glob("*.md") if p.name not in {"Board.md", "README.md"})
    assert [entry["path"] for entry in drawer["tasks"]] == [p.relative_to(root).as_posix() for p in files]
    entry = drawer["tasks"][0]
    assert entry["title"] == "Deferred idea" and entry["status"] == "deferred"
    assert entry["markdown"] == (root / entry["path"]).read_text(encoding="utf-8")
    assert entry["command"].startswith(f"deskops add task --root . --from-drawer {entry['path']} --title ")

    inbox = view.inbox()
    listed = _cli_json(capsys, "message", "list", "--root", str(root), "--format", "json")["notes"]
    assert [note["id"] for note in inbox["notes"]] == [note["id"] for note in listed]
    assert inbox["notes"][0]["title"] == "Open question" and inbox["notes"][0]["acknowledged"]
    assert inbox["notes"][0]["body"] == "Question body"
    assert inbox["open"] == 0 and inbox["notes"][0]["date"]
    note_path = root / inbox["notes"][0]["path"]
    assert inbox["notes"][0]["revision"] == hashlib.sha256(note_path.read_bytes()).hexdigest()

    agents = view.agents()
    assert agents["live_workers"] == 1 and agents["workers"][0]["pane"] == "w1:p1"
    assert [run["task_id"] for run in agents["runs"]] == ["task-gone", desk["first"]]
    assert [run["on_board"] for run in agents["runs"]] == [False, True]


def test_agents_without_herdr_reports_the_cause(desk: dict) -> None:
    def broken() -> list:
        raise RuntimeError("herdr not running")

    agents = DeskView(desk["root"], workers_provider=broken).agents()
    assert agents["workers"] is None and "herdr not running" in agents["workers_error"]
    assert agents["errors"][0]["reference"] == "runtime workers"


def test_no_view_writes(desk: dict) -> None:
    root = desk["root"]
    view = DeskView(root, workers_provider=lambda: [])
    before = _tree_hash(root)
    view.board()
    view.task(desk["first"])
    view.drawer()
    view.inbox()
    view.agents()
    assert _tree_hash(root) == before


def test_cli_view_json_matches_the_service(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = str(desk["root"])
    assert _cli_json(capsys, "view", "board", "--root", root, "--format", "json") == DeskView(desk["root"]).board()
    task = _cli_json(capsys, "view", "task", desk["first"], "--root", root, "--format", "json")
    assert task == DeskView(desk["root"]).task(desk["first"])
    capsys.readouterr()
    assert main(["view", "board", "--root", root]) == 0
    assert desk["first"] in capsys.readouterr().out


def test_view_is_registered_read_only() -> None:
    from deskops.cli.registry import command_registry

    view_commands = [command for command in command_registry() if command.path[0] == "view"]
    assert {command.path for command in view_commands} == {
        ("view",), ("view", "board"), ("view", "task"), ("view", "drawer"), ("view", "inbox"), ("view", "agents")
    }
    assert not any(command.mutates for command in view_commands)

FILE:tests/test_output_goldens.py
"""Golden files pin the machine-readable outputs other tools depend on.

The fixture desk is copied into a throwaway git repository. The real CLI then
builds the graph snapshot, writes the self-reflection report, and makes one
closeout commit per route (run-linked and manual). Volatile values (root paths,
timestamps, commit hashes) are normalized before comparison.

Run ``pytest tests/test_output_goldens.py --update-golden`` to rewrite the
committed goldens after an intentional output change.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
FIXTURE_DESK = TESTS_DIR / "fixtures" / "golden_desk"
GOLDEN_DIR = TESTS_DIR / "fixtures" / "golden"

GRAPH_SNAPSHOT = Path(".sldb/runtime/graphs/deskops.kg.json")
GRAPH_NETWORKX = Path(".sldb/runtime/graphs/deskops.nx.json")
SELF_REFLECTION = Path(".sldb/runtime/self_reflection_findings.json")

RUN_DIR = "runs/subagents/golden-run"
RUN_ID = "run-golden-001"
SESSION_SHA256 = "1" * 64

POSITIONAL_ARGUMENT_RE = re.compile(r"^    (?P<name>\S+)(?:\s{2,}|$)")
ISO_TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b"
)
COMMIT_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TRAILER_RE = re.compile(r"^(?P<key>[A-Z][A-Za-z0-9-]+): (?P<value>.+)$")


def _env(home: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env["COLUMNS"] = "80"
    if home is not None:
        env["HOME"] = str(home)
        env["XDG_CACHE_HOME"] = str(home / ".cache")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) + (os.pathsep + existing if existing else "")
    return env


def _cli(
    cwd: Path, *argv: str, home: Path | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=cwd,
        env=_env(home),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def _git(cwd: Path, *argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _normalize_text(text: str, root: Path) -> str:
    text = text.replace(str(root), "<root>")
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return text


def _normalize_json(value: Any, root: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: "<sha>" if key == "commit" else _normalize_json(item, root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_normalize_json(item, root) for item in value]
    if isinstance(value, str):
        return _normalize_text(value, root)
    return value


def _json_document(value: Any, root: Path) -> str:
    return json.dumps(_normalize_json(value, root), indent=2, sort_keys=True) + "\n"


def _check_golden(relative_path: str, actual: str, request: pytest.FixtureRequest) -> None:
    path = GOLDEN_DIR / relative_path
    update = request.config.getoption("--update-golden")
    if not actual.endswith("\n"):
        actual += "\n"
    if update:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    assert path.exists(), f"missing golden {path}; run pytest --update-golden"
    expected = path.read_text(encoding="utf-8")
    if relative_path.startswith("help/"):
        # argparse wraps the usage block differently across Python versions
        # (3.12 vs 3.13); its words, not its line breaks, are the contract.
        actual, expected = _unwrap_usage(actual), _unwrap_usage(expected)
    assert actual == expected, f"golden mismatch: {relative_path}"


_SHORT_OPTION_METAVAR_RE = re.compile(r"(?m)^(\s+-\w) (\S+), (--[\w-]+) \2$")


def _unwrap_usage(text: str) -> str:
    """Collapse the leading `usage:` block into one line and use 3.13 option spelling.

    3.12 lists a short option with its metavar (`-m MESSAGE, --message MESSAGE`);
    3.13 lists it once (`-m, --message MESSAGE`).
    """
    text = _SHORT_OPTION_METAVAR_RE.sub(r"\1, \3 \2", text)
    if not text.startswith("usage:"):
        return text
    usage, sep, rest = text.partition("\n\n")
    return " ".join(usage.split()) + sep + rest


def _make_fixture_repo(destination: Path) -> Path:
    root = destination / "repo"
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    return root


def _write_run_evidence(root: Path) -> Path:
    run_dir = root / RUN_DIR
    run_dir.mkdir(parents=True)
    for name in ("board.txt", "task.txt", "git-status.txt", "result-summary.md"):
        (run_dir / name).write_text(f"{name} evidence\n", encoding="utf-8")
    (run_dir / "run.yaml").write_text(
        "\n".join(
            [
                f"run_id: {RUN_ID}",
                f"session_sha256: {SESSION_SHA256}",
                "touched:",
                f"- {RUN_DIR}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return run_dir


def _trailers(root: Path) -> dict[str, str]:
    message = _git(root, "log", "-1", "--format=%B")
    trailers: dict[str, str] = {}
    for line in message.splitlines():
        match = TRAILER_RE.match(line)
        if match:
            trailers[match.group("key")] = match.group("value")
    return trailers


@pytest.fixture(scope="module")
def golden_outputs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = _make_fixture_repo(tmp_path_factory.mktemp("golden-output"))

    _cli(root, "graph", "build", "--root", str(root))
    _cli(root, "graph", "reflect", "--root", str(root))

    snapshot = json.loads((root / GRAPH_SNAPSHOT).read_text(encoding="utf-8"))
    networkx = json.loads((root / GRAPH_NETWORKX).read_text(encoding="utf-8"))
    self_reflection = json.loads((root / SELF_REFLECTION).read_text(encoding="utf-8"))

    _write_run_evidence(root)
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-alpha",
        "--run-dir",
        RUN_DIR,
    )
    run_trailers = _trailers(root)

    note = root / "notes" / "golden-note.txt"
    note.parent.mkdir(parents=True)
    note.write_text("manual closeout note\n", encoding="utf-8")
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-beta",
        "--no-run",
        "--reason",
        "golden manual closeout",
        "--paths",
        "notes/golden-note.txt",
    )
    no_run_trailers = _trailers(root)

    return {
        "root": root,
        "graph_snapshot": snapshot,
        "graph_networkx": networkx,
        "self_reflection": self_reflection,
        "closeout_trailers": [
            {"route": "run-dir", "trailers": run_trailers},
            {"route": "no-run", "trailers": no_run_trailers},
        ],
    }


def test_graph_snapshot_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_snapshot"], golden_outputs["root"])
    _check_golden("graph_snapshot.kg.json", actual, request)


def test_graph_networkx_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_networkx"], golden_outputs["root"])
    _check_golden("graph_snapshot.nx.json", actual, request)


def test_self_reflection_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["self_reflection"], golden_outputs["root"])
    _check_golden("self_reflection_findings.json", actual, request)


def test_run_index_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    root = golden_outputs["root"]
    index_path = root / "runs" / "subagents" / "index.jsonl"
    entries = [
        _normalize_json(json.loads(line), root)
        for line in index_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    actual = "".join(json.dumps(entry, sort_keys=True) + "\n" for entry in entries)
    _check_golden("run_index.jsonl", actual, request)


def test_closeout_trailers_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["closeout_trailers"], golden_outputs["root"])
    _check_golden("closeout_trailers.json", actual, request)


def _positional_names(help_text: str) -> list[str]:
    names: list[str] = []
    in_positionals = False
    for line in help_text.splitlines():
        if line.strip() == "positional arguments:":
            in_positionals = True
            continue
        if not in_positionals:
            continue
        if line and not line.startswith(" "):
            break
        match = POSITIONAL_ARGUMENT_RE.match(line)
        if match:
            names.append(match.group("name"))
    return names


def _help(prefix: list[str]) -> str:
    result = _cli(REPO_ROOT, *prefix, "--help")
    assert result.stdout.startswith("usage: deskops"), result.stdout
    return result.stdout


def _collect_help() -> dict[str, str]:
    outputs: dict[str, str] = {}
    pending: list[list[str]] = [[]]
    while pending:
        prefix = pending.pop(0)
        name = "_".join(["deskops", *prefix])
        text = _help(prefix)
        outputs[f"help/{name}.txt"] = text
        for candidate in _positional_names(text):
            if candidate in {"-h", "--help"}:
                continue
            child = [*prefix, candidate]
            result = _cli(REPO_ROOT, *child, "--help")
            if result.stdout.startswith("usage: deskops"):
                pending.append(child)
    return outputs


def test_help_goldens(request: pytest.FixtureRequest) -> None:
    outputs = _collect_help()
    update = request.config.getoption("--update-golden")
    if update:
        help_dir = GOLDEN_DIR / "help"
        for stale in help_dir.glob("*.txt"):
            if f"help/{stale.name}" not in outputs:
                stale.unlink()
    for relative_path, actual in sorted(outputs.items()):
        _check_golden(relative_path, actual, request)


# --- command output goldens -------------------------------------------------

STAMP_RE = re.compile(r"\b\d{8}-\d{6}\b")
FORMATS_TEXT_JSON = ("text", "json")
FORMATS_TEXT_JSON_YAML = ("text", "json", "yaml")

OUTPUT_FIXTURE_DOCS = (
    (
        "ritual",
        (
            ["--title", "Golden ritual"],
            ["--purpose", "Golden purpose"],
            ["--trigger", "Golden trigger"],
            ["--completion", "Golden completion"],
        ),
    ),
    (
        "board",
        (
            ["--title", "Golden board"],
            ["--scope", "golden scope"],
            ["--purpose", "Golden purpose"],
        ),
    ),
    (
        "materialization",
        (
            ["--title", "Golden materialization"],
            ["--target-kind", "document"],
            ["--target-identity", "atom-golden-one"],
            ["--intent", "Golden intent"],
        ),
    ),
    (
        "repository",
        (
            ["--name", "Golden repository"],
            ["--description", "Golden description"],
        ),
    ),
    (
        "inbox-note",
        (
            ["--kind", "unclear"],
            ["--created-at", "2026-01-01T00:00:00"],
            ["--status", "open"],
            ["--title", "Golden inbox note"],
            ["--body", "Golden body"],
        ),
    ),
    (
        "faq-doc",
        (
            ["--title", "Golden FAQ"],
            ["--body", "What is golden?\n\nGolden output."],
        ),
    ),
    (
        "step",
        (
            ["--title", "Golden step"],
            ["--action", "Golden action"],
            ["--outcome", "Golden outcome"],
        ),
    ),
)

SHOW_SUBJECTS = (
    ("task", "task-golden-alpha"),
    ("pill", "pill-golden-rule"),
    ("ritual", "ritual-golden-ritual"),
    ("board", "board-golden-board"),
    ("atom", "atom-golden-one"),
    ("materialization", "materialization-golden-materialization"),
    ("repository", "repo-golden-repository"),
    ("inbox-note", "inbox-note-golden-inbox-note"),
    ("faq-doc", "faq-golden-faq"),
    ("step", "step-golden-step"),
)

LIST_SUBJECTS = (
    "tasks",
    "pills",
    "rituals",
    "boards",
    "atoms",
    "materializations",
    "repositories",
    "inbox-notes",
    "faq-docs",
    "steps",
)

FAKE_HERDR = """#!/usr/bin/env python3
import json
import sys

if sys.argv[1:3] == ["workspace", "list"]:
    payload = {
        "result": {
            "workspaces": [
                {
                    "workspace_id": "w-1",
                    "label": "golden",
                    "number": 1,
                    "agent_status": "active",
                    "pane_count": 1,
                    "focused": True,
                }
            ]
        }
    }
elif sys.argv[1:3] == ["agent", "list"]:
    payload = {
        "result": {
            "agents": [
                {
                    "pane_id": "w-1:p-1",
                    "agent": "pi",
                    "name": "executor",
                    "agent_status": "idle",
                    "cwd": "/tmp/golden-work",
                    "workspace_id": "w-1",
                    "tab_id": "t-1",
                    "terminal_title_stripped": "deskops executor",
                    "state_change_seq": 7,
                    "focused": True,
                }
            ]
        }
    }
else:
    payload = {"result": {}}
print(json.dumps(payload))
"""


def _normalize_output(text: str, replacements: tuple[tuple[str, str], ...]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return STAMP_RE.sub("<stamp>", text)


def _prepare_output_repo(root: Path, home: Path) -> None:
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    for subject, arguments in OUTPUT_FIXTURE_DOCS:
        argv = ["add", subject, "--root", str(root)]
        for argument in arguments:
            argv.extend(argument)
        _cli(root, *argv, home=home)
    (root / "faq.md").write_text(
        "# Golden FAQ\n\n## What is golden?\n\nGolden output stays stable.\n\n"
        "## Why keep goldens?\n\nSibling tools parse the CLI.\n",
        encoding="utf-8",
    )


def _prepare_message_repos(base: Path, home: Path) -> tuple[Path, Path]:
    sender = base / "sender-repo"
    target = base / "target-repo"
    sender.mkdir()
    target.mkdir()
    _cli(sender, "init", str(sender), home=home)
    _cli(target, "init", str(target), home=home)
    return sender, target


def _reset_inbox(target: Path) -> None:
    for note in (target / "desk" / "inbox").glob("*.md"):
        note.unlink()


def _only_note(target: Path) -> Path:
    notes = sorted((target / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1, notes
    return notes[0]


@pytest.fixture(scope="module")
def output_golden_env(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    base = tmp_path_factory.mktemp("command-output-goldens")
    home = base / "home"
    home.mkdir()

    repo = base / "repo"
    _prepare_output_repo(repo, home)

    sender, target = _prepare_message_repos(base, home)

    herdr = base / "fake-herdr"
    herdr.write_text(FAKE_HERDR, encoding="utf-8")
    herdr.chmod(0o755)

    return {"base": base, "home": home, "repo": repo, "sender": sender, "target": target, "herdr": herdr}


def _collect_command_output_goldens(env: dict[str, Path]) -> dict[str, str]:
    home = env["home"]
    repo = env["repo"]
    sender = env["sender"]
    target = env["target"]
    repo_replacements = ((str(repo), "<root>"), (str(home), "<home>"))
    message_replacements = (
        (str(target), "<target>"),
        (str(sender), "<sender>"),
        (str(home), "<home>"),
    )
    outputs: dict[str, str] = {}

    def capture(
        name: str,
        fmt: str,
        argv: list[str],
        cwd: Path,
        replacements: tuple[tuple[str, str], ...],
    ) -> None:
        completed = _cli(cwd, *argv, "--format", fmt, home=home)
        outputs[f"{name}.{fmt}"] = _normalize_output(completed.stdout, replacements)

    for subject in LIST_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"list_{subject}",
                fmt,
                ["list", subject, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for subject, selector in SHOW_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"show_{subject}",
                fmt,
                ["show", subject, selector, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for name, argv in (
        ("atoms_list", ["atoms", "list", "--root", str(repo)]),
        ("atoms_show", ["atoms", "show", "atom-golden-one", "--root", str(repo)]),
        ("atoms_tree", ["atoms", "tree", "--root", str(repo)]),
    ):
        for fmt in FORMATS_TEXT_JSON:
            capture(name, fmt, argv, repo, repo_replacements)

    for fmt in FORMATS_TEXT_JSON_YAML:
        capture(
            "faq",
            fmt,
            ["faq", "--faq-path", str(repo / "faq.md")],
            repo,
            repo_replacements,
        )

    for fmt in FORMATS_TEXT_JSON_YAML:
        _reset_inbox(target)
        capture(
            "message_send",
            fmt,
            [
                "message",
                "send",
                f"Golden message for {fmt}.",
                "--title",
                f"Golden message {fmt}",
                "--kind",
                "suggestion",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )
        note = _only_note(target)
        capture(
            "message_list",
            fmt,
            ["message", "list", "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_read",
            fmt,
            ["message", "read", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_ack",
            fmt,
            ["message", "ack", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )

        _reset_inbox(target)
        capture(
            "inbox",
            fmt,
            [
                "inbox",
                f"Legacy golden message for {fmt}.",
                "--title",
                f"Legacy golden {fmt}",
                "--kind",
                "unclear",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )

    for fmt in FORMATS_TEXT_JSON:
        capture(
            "runtime_workers",
            fmt,
            [
                "runtime",
                "workers",
                "--root",
                str(repo),
                "--herdr",
                str(env["herdr"]),
            ],
            repo,
            repo_replacements,
        )

    return outputs


def test_command_output_goldens(
    output_golden_env: dict[str, Path], request: pytest.FixtureRequest
) -> None:
    outputs = _collect_command_output_goldens(output_golden_env)
    update = request.config.getoption("--update-golden")
    if update:
        output_dir = GOLDEN_DIR / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        for stale in output_dir.glob("*"):
            if f"output/{stale.name}" not in outputs:
                stale.unlink()
    for name, actual in sorted(outputs.items()):
        _check_golden(f"output/{name}", actual, request)

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

- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.

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
Cold-bundle de la tarea task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/test_output_goldens.py (help y output goldens sin --update-golden)
- TMPDIR=/dev/shm pytest -q tests/test_specs.py tests/test_extension_points.py tests/test_desk_view.py
- TMPDIR=/dev/shm pytest -q, uno a la vez, tests/test_atoms_transactions.py tests/test_board_portable_references.py tests/test_cli.py tests/test_closeout_gates.py tests/test_desk_replace.py tests/test_doc_io.py tests/test_materialization_contract.py tests/test_packaging.py tests/test_registry_robustness.py tests/test_review_doc.py (fallas previas comparadas contra main dc1d2834)
- grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/ vacío
- grep -rn "DeskopsOperations(" deskops/services/ vacío salvo services/desk_view.py (q9)
- grep -rn "def _normalize_task_payload\|def compile_task_spec" deskops/ devuelve una sola definición
- grep -rhoE "operations\._[a-z_]+|ops\._[a-z_]+" deskops/services/ antes y después (q7)
- wc -l deskops/operations.py deskops/services/*.py antes (main dc1d2834) y después
- deskops doctor y deskops view board en los 6 desks sin hallazgos nuevos

