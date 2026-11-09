---
sldb:
  by: agent
  at: '2026-11-09T19:12:00Z'
  authority: generated
  via: create_document
id: materialization-cc32-models-task-types
title: cc32 models task_types
source_atoms:
- atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla
target_kind: code
target_identity: deskops/models/task_types.py
validation:
- pytest -q tests/test_activation_rules.py
tags:
- system:deskops
- topic:lifecycle
---

# cc32 models task_types

## Intent

materializa atom-los-gates-de-activación-de-cada-tipo-de-tarea-son-ruledoc-semilla en deskops/models/task_types.py
