---
id: task-docs-y-readme-todav-a-nombran-spec-artifacts-y-spec-fields-borrados-en-cc30
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

# Docs y README todavía nombran spec/artifacts y spec/fields, borrados en CC30

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261106-183512-suggestion-docs-y-readme-todav-a-nombran-spec-artifacts-y-spec-fields-borrados-en-cc30.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261106-183512-suggestion-docs-y-readme-todav-a-nombran-spec-artifacts-y-spec-fields-borrados-en-cc30.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

CC30 (squash 93cc1943) borró deskops/spec/artifacts, deskops/spec/fields, SpecRegistry, deskops/specs/loader.py y deskops/specs/mermaid.py, y pasó id_pattern, status_default y tags por artefacto a atributos de clase de cada modelo (deskops/models). README.md y docs/ (vocabulario del grafo y diagramas de proceso, incluidas proyecciones de Spec2viz bajo docs/diagrams/) todavía los nombran. Arreglo: actualizar README y docs para que remitan a los atributos de clase de los modelos y a deskops/doc_access.py; regenerar las proyecciones de Spec2viz desde su spec en vez de editar el .mmd. Por la regla de docs como materialización de átomos, el cambio sustantivo se captura antes en un átomo. Aceptación: grep -rn 'spec/artifacts\|spec/fields\|SpecRegistry' README.md docs/ vacío, salvo el CHANGELOG histórico. Seguimiento del closeout de CC30, coordinador de proyecto, 2026-11-06.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
