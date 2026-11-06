---
id: materialization-closeout-gates-desk-command
title: closeout gates desk command
source_atoms:
- atom-deskops-models-are-sldb-documents
- atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
target_kind: code
target_identity: deskops/cli/commands/desk.py
validation:
- pytest -q tests/test_task_types.py::test_legacy_task_type_migrates_idempotently
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates desk command

## Intent

desk update --apply migrates legacy task types, registers local types and seeds desk/reviews and runtimes.
