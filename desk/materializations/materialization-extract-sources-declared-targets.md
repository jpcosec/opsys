---
sldb:
  by: agent
  at: '2026-11-10T05:42:16Z'
  authority: generated
  via: save_document_payload
id: materialization-extract-sources-declared-targets
title: Extract sources declared targets
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: source_file
target_identity: deskops/graph/desk_graph.py
validation:
- pytest tests/test_graph_extract_sources.py
tags: []
---

# Extract sources declared targets

## Intent

This file implements the declared materialization target extraction by reading target_identity from desk/materializations/**/*.md and creating source_file nodes for valid targets.
