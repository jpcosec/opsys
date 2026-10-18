---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f3-single-closure-path.md
- desk/tasks/task-rw-f5-root-resolution-and-sandbox-guard.md
- desk/tasks/task-rw-f6-bootstrap-registers-all-models.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- One closure service behind every way of closing a task [draft] - `deskops/services/closure.py` performs every closure: gates (closeout_gates), Board update, bundle removal, exactly one commit with the route's trailers, and the index entry. `closeout commit` (both routes) uses it with its CLI unchanged.
- `--root` and the store resolve in one place, and the sandbox guard covers every mutating command [draft] - One resolver turns `--root`/`--store`/cwd into `(desk_root, store)` for every command and stops searching at the nearest ancestor that contains `desk/` or `.git`; the redirect keeps its current action (it changes the root, it does not refuse) but applies to every command the registry marks `mutates=True` and only when `--root` was not given explicitly.
- Bootstrap registers every deskops model, and only bootstrap/init install sldb [draft] - `MODEL_REFS` stays a `dict[name, 'deskops.models:<Class>']`, built from every `StructuredNLDoc` subclass in `deskops.models.__all__` except the base classes `PrimitiveDoc` and `OperationalArtifactDoc`; a fresh init registers the same 15 deskops models as the repo store; only `bootstrap` and `init` may install sldb; other commands print the existing 'Error: sldb is not installed...' message and exit 1.
