---
sldb:
  by: agent
  at: '2026-11-11T10:43:49Z'
  authority: generated
  via: save_document_payload
id: materialization-deskops-ui-view-service
title: deskops-ui view service
source_atoms:
- atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
target_kind: code
target_identity: deskops/cli/commands/view.py
validation:
- pytest -q tests/test_view.py
tags:
- system:deskops
- topic:ui
---

# deskops-ui view service

## Intent

Read-only service that composes the five UI views from DeskopsOperations; unresolved references go to errors.
