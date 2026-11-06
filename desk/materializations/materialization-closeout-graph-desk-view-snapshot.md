---
id: materialization-closeout-graph-desk-view-snapshot
title: closeout graph desk view snapshot
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/services/desk_view.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph desk view snapshot

## Intent

board and task views run inside one read_snapshot.
