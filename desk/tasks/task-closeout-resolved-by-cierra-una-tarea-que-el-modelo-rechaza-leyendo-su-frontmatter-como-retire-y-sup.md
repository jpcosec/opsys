---
sldb:
  by: agent
  at: '2026-11-11T17:51:25Z'
  authority: generated
  via: save_document_payload
id: task-closeout-resolved-by-cierra-una-tarea-que-el-modelo-rechaza-leyendo-su-frontmatter-como-retire-y-sup
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
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- deskops/workspace.py
- tests/
- docs/operator-manual.md
- docs/workflow-policy-reference.md
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inv-lidas-en-el-mismo-modelo-ninguna-v-a-por-cli-escribe-sldb-h2.md
---

# closeout resolved-by cierra una tarea que el modelo rechaza leyendo su frontmatter, como retire y supersede (huecos de legacy, parte 1)

## Rationale

_Explain why this task exists or the business driver behind it._

Una tarea heredada inválida (por ejemplo, draft con history [task_activates, task_hands_to_closeout], como las 2 draft de shared_llm-gateway) cuyo trabajo ya entró por un commit no tiene salida por resolved-by: carga la tarea con el modelo y sale con Validation error. retire y supersede ya leen por frontmatter (task.debug de estados heredados, wt/legacy-status, informe runs/subagents/legacy-worker-report.md). Prioridad del coordinador: es lo que más destraba.

## Goal

_Describe the concrete result this task must produce._

deskops closeout resolved-by de una tarea que el modelo rechaza la cierra por CLI, con el mismo commit, los mismos trailers (Closeout-Mode: resolved-by) y las mismas compuertas de ref y test que una tarea válida, leyéndola por frontmatter como supersede; con store y otra tarea inválida en el mismo modelo, rechaza antes de escribir y nombra sldb H2 y la vía manual.

## Scope

_State what is in scope and what is out of scope._

En alcance: closeout resolved-by (deskops/services/closure.py close_resolved_by y lo que comparte con close_superseded), su CLI, sus tests, docs (operator-manual, workflow-policy-reference) y CHANGELOG. Fuera: cerrar dos inválidas en el mismo modelo, que depende de sldb H2 (nota de sldb 3895e9f7, sin resolver); no se escribe en sldb. Una tarea que el modelo sí lee sigue la ruta de hoy sin cambios.

## Implementation Path

_Outline the expected implementation route or affected surface._

Drawer de origen 75e33dab (huecos de legacy, coord2), parte 1.

REPRODUCCIÓN (coordinador, deskops main 60f1ec37; runs/subagents/20261111-repro-resolvedby/repro.log y test_repro_resolved_by_invalid.py, armado igual que test_closeout.py::test_closeout_supersede_closes_a_task_whose_lifecycle_the_model_rejects): 'deskops closeout resolved-by --task task-x --reason ... --ref <HEAD> --test <un archivo de test del repo de prueba>' sobre una draft con history [task_activates, task_hands_to_closeout] sale rc 1 con 'Validation error: 1 validation error for TaskDoc ... lifecycle is inconsistent: status draft does not follow history task_hands_to_closeout'.

CAUSA (a confirmar): close_resolved_by carga la tarea con el modelo (read_doc con TaskDoc) para leer files y escribir status resolved. close_superseded ya tiene la rama de respaldo: si read_doc falla, lee el frontmatter, escribe solo status e history con workspace.rewrite_task_fields, revalida con TaskDoc y restaura si falla, y con store rechaza antes de escribir si hay otra tarea inválida en el modelo (H2).

ARREGLO (r1-r5):
r1: resolved-by usa la misma rama de respaldo que supersede: si el modelo rechaza la tarea, lee files y el resto del frontmatter sin el modelo, escribe status resolved e history [..., <el evento de cierre que corresponda>] línea a línea, revalida y restaura si falla. El código compartido con supersede se factoriza; no se duplica.
r2: las compuertas de --ref y --test son las de hoy y se aplican igual a una tarea inválida (el gate de tests usa los files del frontmatter).
r3: con store, si hay otra tarea inválida en el mismo modelo, resolved-by rechaza antes de escribir nada, con un mensaje que nombra sldb H2 y la vía manual (decidir la otra a mano o con supersede/retire cuando quede sola). Mismo chequeo que supersede y retire.
r4: tests: resolved-by de una inválida sin store (mismo commit y trailers que una válida, árbol limpio); con store y una sola inválida, cierra y stores check queda en rc 0; con store y dos inválidas, rechazo limpio con el mensaje de H2 y árbol intacto. La UNMIGRATABLE_SUGGESTION de doctor ya ofrece resolved-by: su golden no cambia, salvo que la ayuda o la salida cambien a propósito (dilo en el informe).
r5: los tests existentes de closeout (test_closeout.py, test_closeout_resolved_by.py, test_legacy_task_states.py y los goldens de salida) siguen verdes. Docs y CHANGELOG.

VALIDACIÓN: el worker corre de a uno los tests que toca y los de closeout relacionados (grep). Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: resolved-by de una tarea que el modelo rechaza cierra con Closeout-Mode: resolved-by, sin store y con store (stores check rc 0)
- Test nuevo: con dos inválidas en el mismo modelo, rechazo limpio que nombra sldb H2, árbol intacto
- test_closeout, test_closeout_resolved_by, test_legacy_task_states y goldens de salida verdes, de a uno
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r5 hechos, con la causa raíz escrita en el informe antes del arreglo y los tests verdes; docs y CHANGELOG actualizados.
