---
id: task-cc35d-resto-rbol-de-dominios-require-domain-parents-tag-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-cuando-sldb-resuelva-h1-h3
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

# CC35d resto: árbol de dominios, require_domain_parents, tag_namespaces y tag_folder por la API de tags de sldb, cuando sldb resuelva H1-H3

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-cc35d-resto-árbol-de-dominios-require-domain-parents-tag-namespaces-y-tag-folder-por-la-api-de-tags.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-cc35d-resto-árbol-de-dominios-require-domain-parents-tag-namespaces-y-tag-folder-por-la-api-de-tags.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Resto de CC35d, cortada por DO7 (decisiones.md de deskops-como-config). CC35d entregó solo a4: desk replace por sldb.replace_text (6d55bb40). Queda lo bloqueado por sldb, con hipótesis en el drawer de sldb 6b34cd5f:
- B1/H1: anchored_by con valor sin namespace. Sin eso CrossroadDoc.path no ancla domain:* y tag_tree da roots=[].
- B2/H2: tag_namespaces acotado por modelos. Sin eso, declarar tag-namespaces.yaml da 115 errores nuevos y on_write rechazaría tareas y pills.
- H3: tag_folder con segmentos vacíos.
Cuando H1 y H2 estén en sldb main, este nodo:
- pasa domain_tree (salvo la creación de crossroads y protoatoms), require_domain_parents y tag_namespaces a la API de sldb;
- suma doc_access.py, services/atoms.py y cli/commands/atoms.py a files (B3);
- resuelve b6 (test de tag_folder) según H3.
También reabre las filas 3 y 5 del inventario de CC38 que CC33b dejó en código por DO7. Informe de CC35d: runs/subagents/cc35d-worker-report.md (wt/cc35d 1b3ad660).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
