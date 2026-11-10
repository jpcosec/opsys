---
sldb:
  by: agent
  at: '2026-11-10T10:31:35Z'
  authority: generated
  via: create_document
id: materialization-cc37-deskops-workspace
title: cc37 deskops workspace
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: code
target_identity: deskops/workspace.py
validation:
- pytest -q tests/test_task_lifecycle_validator.py
tags:
- system:deskops
- topic:lifecycle
---

# cc37 deskops workspace

## Intent

materializa atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc en deskops/workspace.py
