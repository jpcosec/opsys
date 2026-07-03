---
id: atom-sldb-became-more-format-standardizer-than-document-ast-runtime
title: SLDB became more format standardizer than document AST runtime
five_wh_one_plus: what
tags:
- system:sldb
- system:deskops
- topic:diagnosis
- topic:core-realignment
type: atom
description: Diagnosis of how SLDB evolved relative to its stronger AST-oriented ambition.
---

# SLDB became more format standardizer than document AST runtime

## Answer

SLDB currently provides strong value as a structured Markdown contract, store, field, and query layer, but it has not yet become a broadly used document AST runtime that deskops can treat as its normal operational substrate. This gap matters because composition, structural editing, and semantically precise document access were expected to be deeper than frontmatter extraction and document normalization alone.

## Evidence

- `README.md` — defines SLDB as the structured document infrastructure beneath deskops.
- `.skills/sldb/SKILL.md` — emphasizes fields, tracked docs, queries, and structured operations, but current repo usage still falls back frequently to file-level operational behavior.
- `desk/drawer/issues/issue-refactor-primitives-to-ast-driven-task-nodes.md` — explicitly references AST-driven templates and markdown hooks as upstream missing capabilities.
