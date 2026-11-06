---
id: materialization-closeout-gates-task-types
title: closeout gates task types
source_atoms:
- atom-deskops-models-are-sldb-documents
- atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
target_kind: code
target_identity: deskops/models/task_types.py
validation:
- pytest -q tests/test_task_types.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates task types

## Intent

Task type hierarchy (TaskCodeDoc, TaskDocsDoc, ...) as sldb models with declared closeout evidence.
