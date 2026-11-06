---
id: materialization-closeout-graph-desk-config
title: closeout graph desk config
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/graph/desk_graph.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph desk config

## Intent

Declares the desk's ProjectGraphConfig; the graph itself is read from sldb project_graph.
