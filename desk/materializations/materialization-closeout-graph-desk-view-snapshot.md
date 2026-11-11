---
sldb:
  by: agent
  at: '2026-11-11T10:43:37Z'
  authority: generated
  via: save_document_payload
id: materialization-closeout-graph-desk-view-snapshot
title: closeout graph desk view snapshot
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/cli/commands/view.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph desk view snapshot

## Intent

board and task views run inside one read_snapshot.
