---
sldb:
  by: agent
  at: '2026-11-10T10:31:29Z'
  authority: generated
  via: create_document
id: materialization-cc37-deskops-lifecycle
title: cc37 deskops lifecycle
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: code
target_identity: deskops/lifecycle.py
validation:
- pytest -q tests/test_task_lifecycle_validator.py
tags:
- system:deskops
- topic:lifecycle
---

# cc37 deskops lifecycle

## Intent

materializa atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc en deskops/lifecycle.py
