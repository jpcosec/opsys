---
id: materialization-extract-sources-declared-targets
title: Extract sources declared targets
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: source_file
target_identity: deskops/graph/extract_sources.py
validation:
- pytest tests/test_graph_extract_sources.py
tags: []
---

# Extract sources declared targets

## Intent

This file implements the declared materialization target extraction by reading target_identity from desk/materializations/**/*.md and creating source_file nodes for valid targets.
