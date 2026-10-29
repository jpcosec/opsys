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

closeout verify/commit exigen evidencia según la naturaleza de la tarea: una tarea que cambia código (.py en los paths cerrados o en el diff) exige tests + commit + átomo o materialización como hoy; una tarea de docs/spec/diseño exige commit y el documento entregado; una tarea externa exige una referencia externa verificable (URL o id de ticket) en references. La compuerta dice siempre qué clase de tarea detectó y qué evidencia pidió por eso.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closeout_gates.py, deskops/operations.py (verify_task_closeout, _has_verified_task_closeout_evidence), deskops/cli/commands/closeout.py; usar TaskDoc.task_type (code|docs|design|spec|external; default code) y, si no está declarado, inferir por los archivos tocados. Tests en tests/ para las cuatro clases. Actualizar desk/rituals/closeout.md y el atom que describa la regla (crear uno nuevo con deskops add atom si no existe).

## Implementation Path

_Outline the expected implementation route or affected surface._

Agente Scion (deskops-executor) implementa con tests; el supervisor revisa y cierra.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests -k closeout

## Done When

_Name the observable condition that makes the task complete._

Los tests de las cuatro clases pasan; reproducir el caso LIN-1 (tarea external con una URL en references) cierra con closeout commit --no-run; una tarea code sin tests sigue bloqueada; el mensaje de la compuerta nombra la clase detectada.
