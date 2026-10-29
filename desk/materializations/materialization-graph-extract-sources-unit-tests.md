---
id: materialization-graph-extract-sources-unit-tests
title: Graph extract sources unit tests
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: test_file
target_identity: tests/test_graph_extract_sources.py
validation:
- pytest tests/test_graph_extract_sources.py
tags: []
---

# Graph extract sources unit tests

## Intent

This test file validates the extract_source_file_nodes function including the new declared materialization target extraction.
