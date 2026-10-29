---
id: task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-closeout-la-compuerta-tests-missing-tests-evidence-bloquea-tareas-que.md
---

# Closeout: la evidencia exigida depende de lo que la tarea toca, no es la misma para todo

## Rationale

_Explain why this task exists or the business driver behind it._

Tres notas (Chatbot_Infra 2026-10-22, deskops 2026-10-27, mepu_ocs_dev 2026-10-28) chocaron con lo mismo: closeout commit exige tests + commit + átomo/materialización para cualquier tarea, y eso bloquea tareas solo de specs/docs y tareas ejecutadas fuera del repo (LIN-1 en Linear). El dueño (2026-10-29): la regla está mal planteada; no se puede pedir la misma evidencia para todo.

## Goal

_Describe the concrete result this task must produce._

La evidencia de cierre se declara al crear la tarea y el closeout verifica exactamente eso. TaskDoc gana el campo closeout_evidence (lista con vocabulario cerrado: tests, commit, atom, materialization, document, external). deskops add task lo recibe con --evidence; si falta, lo rellena por task_type (code -> tests+commit+atom|materialization; docs|spec|design -> commit+document; external -> external); sin --evidence ni task_type falla con el mensaje de cómo declararla. closeout verify/commit comprueban solo lo declarado. Si el diff trae .py y la tarea no declaró tests, no bloquea: alerta visible (nunca silenciosa). La compuerta siempre imprime 'esta tarea declaró X; encontré Y'.

## Scope

_State what is in scope and what is out of scope._

deskops/models/task.py (campo closeout_evidence + template), deskops/cli/registry.py y cli/commands/core.py (add task --evidence, fallo sin evidencia ni task_type), deskops/services/closeout_gates.py y deskops/operations.py (verify_task_closeout lee lo declarado; alerta por .py sin tests), deskops/cli/commands/closeout.py (mensaje 'declaró X; encontré Y'), desk/rituals/closeout.md, un atom nuevo que enuncie la regla, tests en tests/ para las cuatro clases y para el fallo de add task. Las tareas existentes sin el campo se tratan como code (migración implícita, con alerta).

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (deskops-executor) implementa con tests; el supervisor revisa y cierra.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k closeout

## Done When

_Name the observable condition that makes the task complete._

pytest -q tests -k 'closeout or add_task' en verde; una tarea external con una URL en references cierra con closeout commit --no-run; una tarea code sin tests sigue bloqueada; una tarea docs cierra con commit + documento; add task sin --evidence ni --task-type falla explicando; el mensaje de la compuerta nombra lo declarado y lo encontrado; decisión del dueño 2026-10-29 registrada en el atom.
