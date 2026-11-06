---
id: materialization-closeout-gates-bootstrap
title: closeout gates bootstrap
source_atoms:
- atom-deskops-models-are-sldb-documents
target_kind: code
target_identity: deskops/bootstrap.py
validation:
- pytest -q tests/test_task_types.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates bootstrap

## Intent

Bootstrap registers the task type, review and runtime models in a new desk.
