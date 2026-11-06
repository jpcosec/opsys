---
id: materialization-closeout-graph-snapshot
title: closeout graph snapshot
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/graph/snapshot.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph snapshot

## Intent

Graph snapshot built from the sldb project_graph instead of rescanning the repo.
