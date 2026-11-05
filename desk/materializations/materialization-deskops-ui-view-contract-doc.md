---
id: materialization-deskops-ui-view-contract-doc
title: deskops-ui view contract doc
source_atoms:
- atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
target_kind: doc
target_identity: docs/deskops-ui.md
validation:
- pytest -q tests/test_desk_view.py
tags:
- system:deskops
- topic:ui
---

# deskops-ui view contract doc

## Intent

Documents the view contract and the write path the UI must use.
