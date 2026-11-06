---
id: materialization-closeout-gates-models-package
title: closeout gates models package
source_atoms:
- atom-deskops-models-are-sldb-documents
target_kind: code
target_identity: deskops/models/__init__.py
validation:
- pytest -q tests/test_model_contract_snapshot.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates models package

## Intent

Exports the task type models, ReviewDoc and RuntimeProfileDoc so bootstrap registers them.
