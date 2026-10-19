---
id: task-migration-never-touches-kimun
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
- scripts/migrate_desk_stores.py
- tests/test_migrate_desk_stores.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# The store migration never touches /home/jp/proyectos/kimun

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-19 the coordinator reported that both migration passes over the 40 stores (05c4288, bf139a6) modified an archived store inside /home/jp/proyectos/kimun/docs/archive/architecture/spec2viz: 34 deleted, 3 modified and 5 untracked paths, none committed. The owner forbids touching kimun. The supervisor reverted that path: git restore, the 5 untracked paths removed, and the git-ignored .sldb restored from the pass-1 backup, verified identical with diff -rq. kimun's own docs/research and runs/research were left untouched. The discovery in scripts/migrate_desk_stores.py excludes only path segments such as .cache and tmp, so a future pass would touch kimun again.

## Goal

_Describe the concrete result this task must produce._

scripts/migrate_desk_stores.py never discovers a store under a protected root. kimun is protected relative to the discovery root (proyectos/kimun) and also as the absolute path /home/jp/proyectos/kimun. A test proves a TaskDoc-tracking store under <home>/proyectos/kimun/... is not discovered.

## Scope

_State what is in scope and what is out of scope._

In scope: scripts/migrate_desk_stores.py (a PROTECTED_ROOTS check in discover_stores, applied before descending into a directory), tests/test_migrate_desk_stores.py, and recording the incident in runs/planning/store-migration-20261018-pass2.md. Out of scope: kimun itself.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add PROTECTED_RELATIVE_ROOTS = ("proyectos/kimun",) and prune those directories during the walk (compare each directory's path relative to the discovery root). 2. Also refuse any resolved store path under /home/jp/proyectos/kimun. 3. Test: build <tmp>/proyectos/kimun/docs/archive/x/.sldb with core/models/TaskDoc.yaml inside a git repo, next to a normal repo, and assert discover_stores returns only the normal one. 4. Append an incident note to the pass-2 log.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_migrate_desk_stores.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The test passes, a dry-run of the script lists no kimun store, and `pytest tests` is green.
