---
id: atom-declared-materialization-targets-are-graph-nodes
title: Declared materialization targets are graph nodes
five_wh_one_plus: how
tags:
- system:deskops
- topic:materialization
- topic:closeout
- topic:graph
---

# Declared materialization targets are graph nodes

## Answer

A MaterializationContractDoc whose target_identity is a plain repo-relative POSIX path to an existing regular file makes that file a source_file graph node. The extractor reads desk/materializations/**/*.md frontmatter for target_identity, strips leading './', rejects absolute paths, '..' segments, and kind:id values, verifies the file exists and is not already a node (from path rules or doc rules), and emits a source_file node with source_kind 'declared_materialization_target'. Excluded paths (.tmp/, tools/, etc.) remain missing_declared_target.
