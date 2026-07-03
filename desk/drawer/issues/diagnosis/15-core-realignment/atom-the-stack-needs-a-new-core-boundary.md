---
id: atom-the-stack-needs-a-new-core-boundary
title: The stack needs a new core boundary
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- system:kgdb
- system:hum
- topic:diagnosis
- topic:core-realignment
type: atom
description: Expected direction for reordering the current stack around its real emerging responsibilities.
---

# The stack needs a new core boundary

## Answer

The current stack likely needs a new boundary that distinguishes at least four layers: document infrastructure, knowledge nuclei and composition, workflow or execution orchestration, and agent interface or cognition. Without that realignment, deskops will continue to accumulate responsibilities that conceptually belong to a stronger document AST layer, a stronger knowledge graph or composition layer, or a HUM-facing persistent knowledge runtime.

## Evidence

- `README.md` still describes deskops mainly as a workflow-domain instance built on top of SLDB.
- The active board and diagnosis tree now cover concerns that go beyond a narrow workflow-domain layer: composition, provenance, runtime automation, drift, and cross-surface orchestration.
- `desk/drawer/issues/issue-integrate-kgdb-for-desk-source-knowledge-graph.md` and `issue-refactor-primitives-to-ast-driven-task-nodes.md` point to missing layers beneath the current deskops pressure.
