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

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_output_goldens.py (test_help_goldens y test_command_output_goldens sin --update-golden)
- TMPDIR=/dev/shm pytest -q tests/test_specs.py tests/test_extension_points.py tests/test_desk_view.py
- TMPDIR=/dev/shm pytest -q sobre cada test de los archivos tocados (lista final en esta sección al cerrar)
- grep -rn 'spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS' deskops/ vacío
- grep -rn 'DeskopsOperations(' deskops/services/ vacío
- grep -rn 'def _normalize_task_payload\|def compile_task_spec' deskops/ devuelve una sola definición
- wc -l deskops/operations.py deskops/services/*.py antes (main dc1d2834) y después, registrado aquí
- deskops doctor y deskops view board en los 6 desks sin hallazgos nuevos

## Done When

_Name the observable condition that makes the task complete._

Goldens de ayuda y de salida idénticos (test_help_goldens, test_command_output_goldens sin --update-golden); grep -rn "spec/artifacts\|spec/fields\|SpecRegistry\|_ARTIFACT_DEFAULTS" deskops/ vacío; grep de "DeskopsOperations(" en deskops/services/ vacío; grep de "_normalize_task_payload\|compile_task_spec" devuelve una sola definición; los tests de los archivos tocados verdes (lista en la Validation del TaskDoc) y tests/test_desk_view.py verde incluido el cruce con graph_ui (:132); líneas de operations.py y de services/ antes y después en la Validation; CHANGELOG.
