---
id: materialization-closeout-gates-task-model
title: closeout gates task model
source_atoms:
- atom-deskops-models-are-sldb-documents
- atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
target_kind: code
target_identity: deskops/models/task.py
validation:
- pytest -q tests/test_task_types.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates task model

## Intent

TaskDoc carries task_type and closeout_evidence; the type model declares the evidence that closes it.
