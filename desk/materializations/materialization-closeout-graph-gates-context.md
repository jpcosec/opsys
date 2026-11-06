---
id: materialization-closeout-graph-gates-context
title: closeout graph gates context
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/services/closeout_gates.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph gates context

## Intent

build_closeout_graph_context consults sldb project_graph.
