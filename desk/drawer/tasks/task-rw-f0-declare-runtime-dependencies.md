---
id: task-rw-f0-declare-runtime-dependencies
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-008-kgdb-sldb-boundary.md
files:
- pyproject.toml
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:packaging
---

# pyproject declares sldb and kgdb as dependencies

## Rationale

_Explain why this task exists or the business driver behind it._

deskops imports `sldb` throughout and `kgdb` in deskops/graph/snapshot.py:119 and deskops/cli/main.py:249, but pyproject.toml lists only pydantic and PyYAML, so a clean install of deskops cannot import itself.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml declares sldb (distribution name `structuredLanguageDB`) and `kgdb` with lower-bound versions, and a fresh venv that installs the sibling sldb checkout, kgdb and deskops imports the CLI.

## Scope

_State what is in scope and what is out of scope._

In scope: the `dependencies` list in pyproject.toml. Out of scope: publishing, upper bounds, and `ensure_sldb_available` in deskops/bootstrap.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add `"structuredLanguageDB>=0.1.4"` and `"kgdb>=0.1.0"` to `dependencies`. The import name is `sldb` but its distribution is `structuredLanguageDB` (../sldb/pyproject.toml:2); 0.1.4 is the release that fixed `sldb fields update`; kgdb 0.1.0 is the installed version. In this machine's main environment the metadata still says structuredLanguageDB 0.1.3 (plus a stale `sldb 0.1.0` editable entry) although `import sldb` loads ../sldb/src at 0.1.4, so `pip install -e .` there may need `pip install -e ../sldb` first; the throwaway venv below is the check that counts.
2. Verify in a throwaway venv under /tmp: `python -m venv /tmp/deskops-venv && /tmp/deskops-venv/bin/pip install ../sldb <kgdb source> . && /tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`. There is no sibling kgdb checkout; the installed kgdb 0.1.0 came from git (its dist-info `direct_url.json` records https://github.com/jpcosec/kgdb.git at commit 1247139), so `<kgdb source>` is `"git+https://github.com/jpcosec/kgdb.git@1247139"`. If that pip command exits non-zero, keep the declaration, and record the exact command and error in the closeout.

## Validation

_List the checks required before this task can close._

- python -m deskops --help
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

pyproject.toml declares both packages and the throwaway-venv import check succeeds (or the missing kgdb source is reported).

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
