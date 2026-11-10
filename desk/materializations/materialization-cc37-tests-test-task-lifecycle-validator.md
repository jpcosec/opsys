---
sldb:
  by: agent
  at: '2026-11-10T10:31:37Z'
  authority: generated
  via: create_document
id: materialization-cc37-tests-test-task-lifecycle-validator
title: cc37 tests test_task_lifecycle_validator
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: test
target_identity: tests/test_task_lifecycle_validator.py
validation:
- pytest -q tests/test_task_lifecycle_validator.py
tags:
- system:deskops
- topic:lifecycle
---

# cc37 tests test_task_lifecycle_validator

## Intent

materializa atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc en tests/test_task_lifecycle_validator.py
