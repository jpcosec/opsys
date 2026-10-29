---
id: materialization-board-portable-context
title: Board portable context
source_atoms:
- atom-board-context-uses-portable-document-names
target_kind: board
target_identity: desk/tasks/Board.md
validation:
- pytest -q tests/test_board_portable_references.py
tags:
- system:deskops
- topic:boards
---

# Board portable context

## Intent

The package Board names its pills and rituals by portable document name so linked consumer stores resolve them in this provider store.
