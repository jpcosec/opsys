---
id: task-desk-update-crea-desk-reviews-vac-o-y-git-no-lo-guarda-en-un-clon-limpio-el-dry-run-vuelve-a-dar-missing-desk-structure-desk-reviews
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

# desk update crea desk/reviews/ vacío y git no lo guarda: en un clon limpio el dry-run vuelve a dar 'Missing desk structure: desk/reviews/'

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-desk-update-crea-desk-reviews-vacío-y-git-no-lo-guarda-en-un-clon-limpio-el-dry-run-vuelve-a-dar-mis.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-desk-update-crea-desk-reviews-vacío-y-git-no-lo-guarda-en-un-clon-limpio-el-dry-run-vuelve-a-dar-mis.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Hallado por el worker de integración de graph_ui (2026-11-10, commit d98fcea en wt/deskops-ui de graph_ui). deskops desk update --apply crea desk/reviews/ vacío; git no versiona directorios vacíos, así que en un clon limpio de ese commit 'deskops desk update' (dry-run) vuelve a reportar 'Missing desk structure: desk/reviews/' con rc=1. Afecta a todo desk sin reviews todavía, CI incluido. Arreglo a elegir: el scaffold deja desk/reviews/.gitkeep (o un README gestionado), o desk update y doctor no exigen el directorio vacío y lo crean cuando escriben el primer recibo. Prueba: init en un repo, desk update --apply, commit, clon limpio y dry-run con rc=0.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
