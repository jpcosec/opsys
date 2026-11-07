---
id: materialization-cc31-workflows-task-lifecycle-yaml
title: cc31 workflows task_lifecycle.yaml
source_atoms:
- atom-las-transiciones-del-ciclo-de-vida-de-una-tarea-son-aristas-con-efectos-declarados
target_kind: code
target_identity: deskops/spec/workflows/task_lifecycle.yaml
validation:
- pytest -q tests/test_lifecycle_graph.py tests/test_lifecycle_end_to_end.py
tags:
- system:deskops
- topic:lifecycle
---

# cc31 workflows task_lifecycle.yaml

## Intent

materializa atom-las-transiciones-del-ciclo-de-vida-de-una-tarea-son-aristas-con-efectos-declarados en deskops/spec/workflows/task_lifecycle.yaml
