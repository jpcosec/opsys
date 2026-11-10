---
sldb:
  by: agent
  at: '2026-11-10T10:31:31Z'
  authority: generated
  via: create_document
id: materialization-cc37-models-task
title: cc37 models task
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: code
target_identity: deskops/models/task.py
validation:
- pytest -q tests/test_task_lifecycle_validator.py
tags:
- system:deskops
- topic:lifecycle
---

# cc37 models task

## Intent

materializa atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc en deskops/models/task.py
