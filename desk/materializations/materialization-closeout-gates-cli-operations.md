---
id: materialization-closeout-gates-cli-operations
title: closeout gates cli operations
source_atoms:
- atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
target_kind: code
target_identity: deskops/cli/commands/operations.py
validation:
- pytest -q tests/test_cli_escape_hatches.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates cli operations

## Intent

CLI handlers for add task --task-type and the edit task refusal of lifecycle fields.
