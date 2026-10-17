---
id: task-rw-f0-declare-runtime-dependencies
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-008-kgdb-sldb-boundary.md
files:
- pyproject.toml
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-declare-runtime-dependencies.md
---

# pyproject declares kgdb as a dependency

## Rationale

_Explain why this task exists or the business driver behind it._

deskops imports `sldb` throughout and `kgdb` in deskops/graph/snapshot.py:119 and deskops/cli/main.py:251, but pyproject.toml lists only pydantic and PyYAML, so a clean install of deskops cannot import itself.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml declares `kgdb` with a lower-bound version next to the existing `structuredLanguageDB>=0.1.9`, and a fresh venv that installs the sibling sldb checkout, kgdb and deskops imports the CLI.

## Scope

_State what is in scope and what is out of scope._

In scope: the `dependencies` list in pyproject.toml. Out of scope: publishing, upper bounds, and `ensure_sldb_available` in deskops/bootstrap.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `dependencies` already holds `"structuredLanguageDB>=0.1.9"` (pyproject.toml:10, added by afdec7f); add `"kgdb>=0.1.0"` (the installed version) after it and change nothing else. In this machine's main environment the sldb metadata still says structuredLanguageDB 0.1.3 although `import sldb` loads ../sldb/src at 0.1.9, so `pip install -e .` there may need `pip install -e ../sldb` first; the throwaway venv below is the check that counts.
2. Verify in a throwaway venv under /tmp: `python -m venv /tmp/deskops-venv && /tmp/deskops-venv/bin/pip install ../sldb <kgdb source> . && /tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`. There is no sibling kgdb checkout; the installed kgdb 0.1.0 came from git (its dist-info `direct_url.json` records https://github.com/jpcosec/kgdb.git at commit 1247139), so `<kgdb source>` is `"git+https://github.com/jpcosec/kgdb.git@1247139"`. If that pip command exits non-zero, keep the declaration, and record the exact command and error in the closeout.

## Validation

_List the checks required before this task can close._

- python -m deskops --help
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

pyproject.toml declares kgdb, and the throwaway-venv import check succeeds (or the pip error is recorded).

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
