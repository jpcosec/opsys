---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f3-single-closure-path.md
- desk/tasks/task-tests-never-touch-the-real-global-store.md
- desk/tasks/task-rw-f5-output-renderer.md
- desk/tasks/task-rw-f6-taskdoc-contract-cleanup.md
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
- The test suite never writes to the user's real `~/.sldb` [draft] - Running `pytest tests` leaves `~/.sldb` byte-identical.
- One renderer for text, json and yaml output with an error envelope [draft] - Handlers return data; deskops/cli/render.py prints it as text, json or yaml; with `--format json` an error prints `{"ok": false, "error": {"code": <exit code>, "type": "<class name from deskops/errors.py, e.g. DomainError>", "message": "..."}}` and exits with that code. argparse usage errors keep argparse's stderr text and exit 2 and are never wrapped, because they happen before `--format` is known.
- TaskDoc contract cleanup [draft] - TaskDoc uses `extra: ignore`, drops the `frontmatter` field, its `_merge_frontmatter` validator and the `render_payload` override, declares each frontmatter field with its own template marker (as PillDoc does), keeps `from_drawer` as a plain field outside `__references__`, and the docstring says it keeps documents byte-identical, not the contract hash; tests/fixtures/model_contract_hashes.json is updated deliberately.
