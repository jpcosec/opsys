---
sldb:
  by: agent
  at: '2026-11-11T10:43:45Z'
  authority: generated
  via: save_document_payload
id: materialization-deskops-ui-view-tests
title: deskops-ui view tests
source_atoms:
- atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
target_kind: test
target_identity: tests/test_view.py
validation:
- pytest -q tests/test_view.py
tags:
- system:deskops
- topic:ui
---

# deskops-ui view tests

## Intent

Tests the view contract on real temporary desks, including no-write and unresolved-reference behavior.
