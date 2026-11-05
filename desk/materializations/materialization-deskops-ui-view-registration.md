---
id: materialization-deskops-ui-view-registration
title: deskops-ui view registration
source_atoms:
- atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
target_kind: code
target_identity: deskops/cli/registry.py
validation:
- pytest -q tests/test_desk_view.py
tags:
- system:deskops
- topic:ui
---

# deskops-ui view registration

## Intent

Registers the view command in the deskops CLI.
