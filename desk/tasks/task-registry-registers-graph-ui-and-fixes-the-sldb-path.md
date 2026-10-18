---
id: task-registry-registers-graph-ui-and-fixes-the-sldb-path
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- desk/registry/repo-sldb.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# The repo registry knows graph_ui and spec2viz and points sldb at its current checkout

## Rationale

_Explain why this task exists or the business driver behind it._

graph-ui-59 reported on 2026-10-18 that `deskops message send --root <deskops> --from graph_ui` fails with "Repository id 'graph_ui' not found in registry (found: deskops, sldb)". It also noted that desk/registry/repo-sldb.md still points at /home/jp/proyectos/hum-ecosystem/tools/sldb; sldb now lives in /home/jp/proyectos/SLDB_1/sldb. The 2026-09-24 sldb handoff note reported the same broken registration.

## Goal

_Describe the concrete result this task must produce._

desk/registry lists graph_ui and spec2viz with their current paths, repo-sldb points at /home/jp/proyectos/SLDB_1/sldb, and `message send --from graph_ui` resolves.

## Scope

_State what is in scope and what is out of scope._

In scope: `deskops repo register` for graph_ui and spec2viz, and `deskops edit repository` for repo-sldb's path. Out of scope: registry code changes.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `deskops repo register graph_ui --path /home/jp/proyectos/SLDB_1/UIs/graph_ui`. 2. The same for spec2viz. 3. `deskops edit repository repo-sldb path /home/jp/proyectos/SLDB_1/sldb`. 4. Check with `deskops repo list` and a `message send` dry check.

## Validation

_List the checks required before this task can close._

- deskops repo list --root .
- sldb stores check --store .sldb
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`deskops repo list` shows deskops, sldb, graph_ui and spec2viz at their current paths, and the store check passes.
