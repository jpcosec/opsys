---
id: materialization-materialization-targets-outside-package-tests
title: Materialization targets outside package tests
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: test_file
target_identity: tests/test_materialization_targets_outside_package.py
validation:
- pytest tests/test_materialization_targets_outside_package.py
tags: []
---

# Materialization targets outside package tests

## Intent

This test file validates that declared materialization targets outside desk/ and deskops/ become graph nodes, that nonexistent targets stay missing, that materializations are tracked in the .sldb store, and that closeout verify accepts materialization coverage.
