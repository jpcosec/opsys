---
id: materialization-closeout-graph-v1-oracle
title: closeout graph v1 oracle
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: tests/closeout_graph_oracle.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph v1 oracle

## Intent

The old extract_* path kept as a test oracle.
