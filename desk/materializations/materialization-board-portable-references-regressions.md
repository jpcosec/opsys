---
id: materialization-board-portable-references-regressions
title: Board portable references regressions
source_atoms:
- atom-board-context-uses-portable-document-names
target_kind: test_file
target_identity: tests/test_board_portable_references.py
validation:
- pytest -q tests/test_board_portable_references.py
tags:
- system:deskops
- topic:boards
- topic:materialization
---

# Board portable references regressions

## Intent

Prove linked provider/consumer resolution with colliding paths and the local graph, next, show and retirement on portable Board context.
