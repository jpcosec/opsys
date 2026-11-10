---
sldb:
  by: agent
  at: '2026-11-10T10:31:33Z'
  authority: generated
  via: create_document
id: materialization-cc37-models-task-lifecycle
title: cc37 models task_lifecycle
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: code
target_identity: deskops/models/task_lifecycle.py
validation:
- pytest -q tests/test_task_lifecycle_validator.py
tags:
- system:deskops
- topic:lifecycle
---

# cc37 models task_lifecycle

## Intent

materializa atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc en deskops/models/task_lifecycle.py
