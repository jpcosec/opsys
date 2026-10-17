---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f0-declare-runtime-dependencies.md
- desk/tasks/task-rw-f0-pytest-collects-only-tests.md
- desk/tasks/task-rw-f0-graph-skips-vendored-trees.md
- desk/tasks/task-rw-f0-payload-from-drawer-resolves.md
- desk/tasks/task-rw-f0-reject-ambiguous-selectors.md
- desk/tasks/task-rw-f0-merge-retarget-whole-tokens.md
- desk/tasks/task-rw-f0-closeout-commit-pathspec.md
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

- pyproject declares kgdb as a dependency [draft] - pyproject.toml declares `kgdb` with a lower-bound version next to the existing `structuredLanguageDB>=0.1.9`, and a fresh venv that installs the sibling sldb checkout, kgdb and deskops imports the CLI.
- Bare `pytest` collects only the tests/ directory [draft] - Running `pytest` with no arguments from the repo root collects only `tests/`.
- `graph build` ignores tools/, .tmp/ and .venv/ [draft] - After `deskops graph build --root .`, no node in the snapshot has a path under `tools/` or `.tmp/` (`.venv/` stays excluded).
- `from_drawer` given in a YAML or JSON payload is resolved like the flag [draft] - A `from_drawer` value from the flag, a YAML payload or an inline JSON payload is resolved and stored as the same repo-relative drawer path; an unknown or ambiguous selector fails with exit 1 and creates nothing.
- Prefix selectors fail on ambiguity instead of picking the first match [draft] - `_resolve_glob` raises on more than one prefix match, naming every candidate, while an exact file name and a single prefix match keep resolving as today.
- Atom merge rewrites only whole `atom:<id>` tokens in referrers [draft] - `merge_atom` rewrites only exact `atom:<source id>` tokens in referrer files.
- The advance closeout commit contains only the closing task's paths [draft] - That commit includes exactly the removed task file, `desk/tasks/Board.md`, and those entries of the task's `files` list that have any change, new files included (`git status --porcelain -- <path>` prints something), with their working-tree content; unchanged listed paths are skipped; unrelated staged changes stay staged and out of the commit.
