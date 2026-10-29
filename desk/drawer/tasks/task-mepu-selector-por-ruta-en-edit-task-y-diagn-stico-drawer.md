---
id: task-mepu-selector-por-ruta-en-edit-task-y-diagn-stico-drawer
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# MEPU: selector por ruta en edit task y diagnóstico drawer

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261028-055156-unclear-mepu-selector-por-ruta-en-edit-task-y-diagn-stico-drawer.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261028-055156-unclear-mepu-selector-por-ruta-en-edit-task-y-diagn-stico-drawer.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Para equipo deskops, desde MEPU (coordinador repos-9f). Fricción observada, no reparada aquí:
deskops edit task desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md scope '<contenido>' --root .
Error: No artifact.task file found for selector 'desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md'
deskops desk replace desk/drawer/tasks/task-homologaci-n-procedencia-del-parseo-reglas-expl-citas-de-conflictos-y-evidencia-en-el-front.md --old '<Scope anterior>' --new '<Scope con evidencia>' --root .
Error: archivo modelado; use deskops edit task <selector> <field> <value>.
Diagnóstico: edit task SÍ soporta drawer/tasks. El selector admite basename/stem/prefijo, no ruta. Repetir con el stem funcionó. Mejora solicitada: error que explique la diferencia o aceptar rutas contenidas en desk; ejemplo drawer en help. No presentar como bug de soporte de drawer.
Además promote retira inbox origen y conserva su referencia junto a placeholders en el Scope, aunque copia el cuerpo completo. Mejorar legibilidad para no parecer vacío o perdido.
Envío inicial --to deskops falló: Repository id 'deskops' not found in registry at '/home/jp/AntonIA/repos/legacy/mepu/mepu/desk/registry' (found: none). Se usa destino explícito --desk-root; no se cambia registro global.
Sin cambios de código, commit ni reparación.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
