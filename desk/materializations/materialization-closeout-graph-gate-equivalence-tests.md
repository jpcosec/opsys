---
id: materialization-closeout-graph-gate-equivalence-tests
title: closeout graph gate equivalence tests
source_atoms:
- atom-deskops-should-read-through-sldb-compositions
target_kind: code
target_identity: tests/test_closeout_gates.py
validation:
- pytest -q tests/test_closeout_gates.py
tags:
- system:deskops
- topic:closeout-graph
---

# closeout graph gate equivalence tests

## Intent

Gate results equal the v1 extractor oracle on fixtures.
