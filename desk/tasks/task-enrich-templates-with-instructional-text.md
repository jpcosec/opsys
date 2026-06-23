---
# task-xxx, unique task identifier
id: task-enrich-templates-with-instructional-text
# draft | active | blocked | closed
status: active
# Relevant file or doc paths
references:
- desk/contexts/pill-sldb-template-markers.md
- desk/contexts/pill-template-instructional-text.md
- tests/test_model_templates.py
# Task identifiers that must complete first
depends_on: []
# Pill identifiers required
pills:
- desk/contexts/pill-template-instructional-text.md
# Files expected to change
files:
- deskops/models/atom.py
- deskops/models/board.py
- deskops/models/checklist.py
- deskops/models/condition.py
- deskops/models/edge.py
- deskops/models/faq.py
- deskops/models/hook.py
- deskops/models/inbox.py
- deskops/models/operator.py
- deskops/models/pill.py
- deskops/models/repository.py
- deskops/models/ritual.py
- deskops/models/routine.py
- deskops/models/step.py
- deskops/models/task.py
# Routine identifier for operations
routine: routine-task-enrich-templates-with-instructional-text
# Checklist identifiers for verification
checklists:
- checklist-task-enrich-templates-with-instructional-text-execution-ready
- checklist-task-enrich-templates-with-instructional-text-testing-ready
- checklist-task-enrich-templates-with-instructional-text-closeout-ready
# Active routine node
current_node: complete
# Execution history references
history:
- 'created: 2026-06-21T00:00:00'
- status changed to active
- 'entered execution_gate: checklist-task-enrich-templates-with-instructional-text-execution-ready'
# e.g., system:deskops, topic:cli
tags:
- system:deskops
- topic:templates
- topic:documentation
---

# Enrich all deskops model templates with instructional fixed text

## Rationale

_Explain why this task exists or the business driver behind it._

Los templates actuales son esqueletos mínimos, no hay texto que explique qué va en cada campo al crear un documento nuevo.

## Goal

_Describe the concrete result this task must produce._

Que cada `__template__` en los modelos de deskops contenga texto fijo instructivo que guíe a quien escribe el documento sobre qué poner en cada campo.

## Scope

_State what is in scope and what is out of scope._

In scope: Todos los modelos en `deskops/models/*.py`. Solo texto instructivo fijo.
Out of scope: Cambios al motor de templates SLDB.

## Implementation Path

_Outline the expected implementation route or affected surface._

Agregar texto instructivo como comentarios YAML (#) en el frontmatter y texto en itálicas (_) en el markdown de cada template.

## Validation

_List the checks required before this task can close._

- `⸢rev•⸥` markers siguen presentes y funcionales
- Tests de roundtrip pasan (extract → render → extract)

## Done When

_Name the observable condition that makes the task complete._

All deskops models have instructional text in their templates and tests pass.
