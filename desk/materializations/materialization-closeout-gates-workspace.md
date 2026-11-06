---
id: materialization-closeout-gates-workspace
title: closeout gates workspace
source_atoms:
- atom-deskops-models-are-sldb-documents
target_kind: code
target_identity: deskops/workspace.py
validation:
- pytest -q tests/test_review_command.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates workspace

## Intent

Workspace layout knows desk/reviews and desk/runtimes and local task type modules.
