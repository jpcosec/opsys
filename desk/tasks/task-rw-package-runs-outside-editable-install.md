---
id: task-rw-package-runs-outside-editable-install
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f6-migrate-tracking-stores
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- pyproject.toml
- deskops/bootstrap.py
- deskops/lifecycle_migration.py
- deskops/lifecycle.py
- deskops/operations.py
- deskops/cli/main.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/faq.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-package-runs-outside-editable-install.md
---

# deskops works from a regular (non-editable) install

## Rationale

_Explain why this task exists or the business driver behind it._

Packaging audit of 2026-10-17 (desk/inbox/20261017-233236-suggestion-auditor-a-de-empaquetado-2026-10-17-kgdb-no-declarado-rutas-file-dependientes-del-checkout.md); the owner asked for it on 2026-10-18 through the SLDB_1 coordinator. Code locates files by `Path(__file__).resolve().parents[N]`, assuming the repo checkout: deskops/bootstrap.py:200 (`_package_root`), deskops/lifecycle_migration.py:137, deskops/lifecycle.py:24 (`SPEC_PATH`, spec/ lives at the repo root and is not packaged) and :112, deskops/operations.py:318 (`spec_root`), 1830, 1859, 2333, 2434, deskops/cli/main.py:8 (`PACKAGE_ROOT`), deskops/cli/commands/desk.py:251, 277, 290 and deskops/cli/commands/faq.py:29 (docs/faq.md). Another inbox note (20260928-213500-unclear-spec-no-se-empaqueta-promote-falla-fuera-del-repo.md) already reports that spec/ is not packaged.

## Goal

_Describe the concrete result this task must produce._

A wheel built from this repo and installed (not editable) into a fresh venv runs `deskops init`, `add task`, `advance`, `desk update` and `faq` in a sandbox repo outside the checkout.

## Scope

_State what is in scope and what is out of scope._

In scope: every `Path(__file__)` location in deskops/, packaging the data files deskops reads at runtime, and pyproject package-data. Out of scope: sldb and kgdb packaging. It runs last, after F6, because it moves spec/ and touches every module the F2-F5 refactors rewrite; the line numbers in Rationale are from 2026-10-18 and will have moved, so find the sites with `grep -rn "Path(__file__)" deskops/`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. One helper module (for example deskops/paths.py) owns location: `package_pythonpath()` (the directory that contains the `deskops` package, valid both editable and installed) for every `pythonpath=` passed to sldb, and `data_path(*parts)` for packaged data. Replace every site listed in Rationale; `grep -rn "Path(__file__)" deskops/` ends with only deskops/paths.py.
2. Package the runtime data: move `spec/` under the package (`git mv spec deskops/spec`), update every reference in code, tests and docs (`grep -rn "spec/"`), and declare it in `[tool.setuptools.package-data]`. For the FAQ, ship docs/faq.md as package data too (copy at build time is not available with setuptools; move or duplicate it under the package and keep docs/faq.md as the human copy only if a test pins both equal).
3. Verify: `python -m build --wheel` (or `pip wheel . --no-deps -w /tmp/...`), fresh venv under /tmp, install sldb from ../sldb, kgdb with `--no-deps` from git+https://github.com/jpcosec/kgdb.git@1247139, then the wheel; in a `git init` sandbox under /tmp (cwd outside the checkout, PYTHONPATH unset) run `deskops init .`, `deskops add task --root . --title T --goal g --scope s --implementation-path i --done-when d --validation pytest`, `deskops advance task <id> --root .`, `deskops desk update --root .`, `deskops faq`; all exit 0.

## Validation

_List the checks required before this task can close._

- pytest tests
- the step 3 non-editable smoke run

## Done When

_Name the observable condition that makes the task complete._

`grep -rn "Path(__file__)" deskops/` lists only the helper module, the step 3 smoke run passes from the installed wheel, and `pytest tests` is green.

## Resolved Decisions

- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): register and fix the checkout-dependent paths found by the packaging audit.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
