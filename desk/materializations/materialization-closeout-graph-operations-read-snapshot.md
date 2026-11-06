---
id: materialization-closeout-graph-operations-read-snapshot
title: closeout graph operations read snapshot
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/operations.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph operations read snapshot

## Intent

read_snapshot caches graph context, transitions and doc payloads for one view.
