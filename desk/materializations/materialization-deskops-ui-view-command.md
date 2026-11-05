---
id: materialization-deskops-ui-view-command
title: deskops-ui view command
source_atoms:
- atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
target_kind: code
target_identity: deskops/cli/commands/view.py
validation:
- pytest -q tests/test_desk_view.py
tags:
- system:deskops
- topic:ui
---

# deskops-ui view command

## Intent

The deskops view subcommand exposing board, task, drawer, inbox and agents as json or text.
