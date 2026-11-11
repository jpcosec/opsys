---
id: task-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inv-lidas-en-el-mismo-modelo-ninguna-v-a-por-cli-escribe-sldb-h2
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

# Cerrar por CLI tareas que el modelo rechaza: resolved-by carga con el modelo, y con dos inválidas en el mismo modelo ninguna vía por CLI escribe (sldb H2)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inválidas-en-e.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-cerrar-por-cli-tareas-que-el-modelo-rechaza-resolved-by-carga-con-el-modelo-y-con-dos-inválidas-en-e.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Lo que deja abierto el task.debug de estados heredados (wt/legacy-status db337c1e, runs/subagents/legacy-worker-report.md). retire y supersede ya cargan y escriben por frontmatter una tarea que el modelo rechaza. Quedan dos huecos:
1. deskops closeout resolved-by sigue cargando la tarea con el modelo. No se probó; es hipótesis del worker. Una tarea inválida cuyo trabajo ya entró por un commit no tiene salida por resolved-by.
2. Con dos tareas inválidas en el mismo modelo, ninguna escritura por CLI pasa: sldb re-extrae el modelo entero en cada escritura y cae en la otra (H2 de la nota de sldb 3895e9f7). Es el caso de las 2 draft de /srv/repos/shared_llm-gateway (task-linea-base-de-lint-del-gateway y task-logs-de-llm-gateway-servir-sin-pii, draft con history [task_activates, task_hands_to_closeout]). Hoy el dueño tiene que decidir una a mano.
Hecho cuando: (1) resolved-by carga por frontmatter como retire y supersede, con test; (2) cuando sldb resuelva H2, un test con dos inválidas en el mismo modelo cierra las dos por CLI. Mientras no se resuelva, el mensaje de deskops en ese caso nombra H2 y la vía manual.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
