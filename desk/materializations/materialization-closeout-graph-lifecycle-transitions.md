---
id: materialization-closeout-graph-lifecycle-transitions
title: closeout graph lifecycle transitions
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: deskops/lifecycle.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph lifecycle transitions

## Intent

Transitions read from the cached sldb edge index.
