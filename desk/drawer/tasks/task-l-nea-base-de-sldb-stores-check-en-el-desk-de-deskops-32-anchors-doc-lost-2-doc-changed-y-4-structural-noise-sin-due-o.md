---
id: task-l-nea-base-de-sldb-stores-check-en-el-desk-de-deskops-32-anchors-doc-lost-2-doc-changed-y-4-structural-noise-sin-due-o
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

# Línea base de sldb stores check en el desk de deskops: 32 anchors/doc_lost, 2 doc_changed y 4 structural-noise sin dueño

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-línea-base-de-sldb-stores-check-en-el-desk-de-deskops-32-anchors-doc-lost-2-doc-changed-y-4-structur.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-línea-base-de-sldb-stores-check-en-el-desk-de-deskops-32-anchors-doc-lost-2-doc-changed-y-4-structur.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Medido el 2026-11-10 en main (desk 94e1f819) con sldb main 41a98dbc: sldb stores check --store .sldb da rc 0 con 38 alertas. Ninguna tenía tarea ni nota. Regla del dueño: un fallo conocido sin tarea no existe.

1. anchors/doc_lost (32). ReviewDocs cuyo subject es una tarea cerrada y destrackeada por closeout commit; el recibo sigue trackeado con un ancla a un documento que ya no está en el store. 23 tareas distintas, por ejemplo: review-task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados-bundle-1 -> TaskRefactorDoc task-cc30-... (lost); review-task-test-gitignore-policy-quedó-viejo-sldb-core-se-versiona-entero-preflight-1 y -2; review-task-review-record-recibos-reproduction-goldens-y-owner-sin-modelo-seguimiento-de-cc32-preflight-1; también versiones pinneadas (@sha256) de cc37, main-en-verde, closeout-resolved-by y manual-sin-atoms-split. Causa probable: closeout commit destrackea la TaskDoc pero no sus recibos (desk/reviews/<task>/). Decidir: closeout destrackea o archiva los recibos con la tarea, o las alertas de ancla excluyen recibos de tareas cerradas. Conecta con CC33a/CC33b (recibos evidence anclados al contrato de la tarea; informe cc33a, Desvíos 1).

2. anchors/doc_changed (2). review-task-cc33a-...-bundle-1 y -preflight-1: la TaskDoc de CC33a cambió después (disposiciones) y existen -2 al día. Esperado para recibos superados; decidir si un recibo superado por otro posterior del mismo kind deja de alertar.

3. store/structural-noise (4). AtomDocs con encabezados que el modelo no declara: atom-desk-health-delegates-store-diagnostics-to-sldb (Boundary Rationale, Delegation Pattern, Evidence, Tags), atom-desk-health-is-measured-by-cli-diagnostics (Diagnostic Surface, Repairability, Evidence, Tags), atom-desk-health-is-workspace-integrity-state (Evidence, Related Atoms, Tags), atom-desk-repair-is-owned-by-deskops (Owned Operations, Not Owned, Evidence, Tags). Arreglo: llevar ese contenido a fields del AtomDoc con deskops/sldb (no a mano) o declarar las secciones.

Reproducir: en deskops, PYTHONPATH=<sldb>/src:. python -m sldb stores check --store .sldb y contar los códigos [..].

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
