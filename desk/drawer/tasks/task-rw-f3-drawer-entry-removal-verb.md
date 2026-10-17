---
id: task-rw-f3-drawer-entry-removal-verb
status: blocked
references: []
depends_on:
- task-rw-f3-drawer-routing-service
pills:
- desk/contexts/pill-cli-gaps-become-tracked-work.md
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
files:
- deskops/services/drawer.py
- deskops/cli/parser.py
- tests/test_inbox_promote_cli_gaps.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f3
- topic:drawer
- topic:cli
---

# A CLI verb removes a drawer entry

## Rationale

_Explain why this task exists or the business driver behind it._

There is no deskops verb to delete a drawer entry. `deskops add task --from-drawer` keeps the entry 'for manual cleanup', so operators delete files by hand and nothing checks whether a task still records that entry in `from_drawer` (a provenance field that may dangle; see `PROVENANCE_FIELDS` in deskops/graph/extract_edges.py:31). desk/drawer/tasks/Board.md is hand-maintained prose: entries appear as bullets of the form ``- `<task-id>` — <summary>`` under several headings.

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

The approved verb removes one drawer file, untracks it if tracked, and deletes every Board.md bullet that starts with ``- `<its stem>` ``.

## Scope

_State what is in scope and what is out of scope._

Blocked on the owner decision (see Open Ambiguities). Uses `DrawerService` and `DocTransaction`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add the verb to deskops/cli/parser.py.
2. Implement removal in `DrawerService` inside a `DocTransaction`.
3. CLI test in a sandbox: the file is gone, its Board bullets are gone, other bullets are intact.

## Validation

_List the checks required before this task can close._

- pytest tests/test_inbox_promote_cli_gaps.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The verb removes the entry and its Board bullets and the test passes.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

- Owner decision: the verb's name (for example `deskops drawer remove <selector>`), and whether it refuses, warns, or proceeds silently when an active task's `from_drawer` points at the entry.
