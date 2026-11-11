---
id: task-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-c-digo-vive-en-otro-repo
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

# una task.code no puede cerrar en un desk cuando su código vive en otro repo

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-código-vive-en-otro-repo.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-una-task-code-no-puede-cerrar-en-un-desk-cuando-su-código-vive-en-otro-repo.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Caso de AntonIA (2026-11-11): task-el-almacén-sellado-del-kit-no-guarda-lotes-de-más-de-9300-filas vive en el desk de Governance y su código en Chatbot_Infra (#400, 87671716). advance se frena en task_hands_to_closeout (nonempty(validation)); closeout verify da missing_tests_evidence y missing_commit_evidence porque ni el commit ni el test existen en el repo del desk; resolved-by exige un commit ancestro local y un test .py del repo. Vía actual (decisión del coordinador, revisable): tarea espejo en el desk del repo del código cerrada con resolved-by, supersede en el desk coordinador apuntando a ella, y task.external para lo que viene. Falta en deskops: (a) que desk update o add task sugiera task.external cuando files o references apuntan a otro repo; (b) o que la evidencia commit/tests acepte referencias calificadas por repo (repo:sha, repo:path) verificadas contra un repo registrado (deskops repo register).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
