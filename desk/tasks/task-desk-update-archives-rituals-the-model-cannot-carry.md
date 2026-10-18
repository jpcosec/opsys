---
id: task-desk-update-archives-rituals-the-model-cannot-carry
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
- deskops/lifecycle.py
- deskops/workspace.py
- tests/test_lifecycle_graph.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `desk update --apply` archives legacy rituals RitualDoc cannot carry and writes the default ones

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 while running the store migration (task-rw-f6-apply-store-migration) on the 39 stores. 13 of them failed with exit 3: their lifecycle rituals predate RitualDoc. They have no frontmatter `id` (an old `deskops init`), `steps` with another shape (paper_IEEE), or hand-written sections RitualDoc does not declare (TraderBot, which sldb then refuses to track as structural noise). The 2026-10-18 decision "re-render, and fail with an error if still unreadable" left those desks without a lifecycle graph.

## Goal

_Describe the concrete result this task must produce._

When a lifecycle ritual cannot round-trip through RitualDoc, `desk update --apply` moves it byte for byte to `desk/drawer/rituals/legacy-<name>.md` (not modeled), writes the ritual `deskops init` writes in its place, tracks that, and reports both paths.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/lifecycle.py (`_archive_legacy_ritual`, structural-noise check in `_ensure_ritual_readable`), deskops/workspace.py (`default_ritual_text`), tests in tests/test_lifecycle_graph.py. Out of scope: merging a legacy ritual's text into the new one (its owner decides).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `_ensure_ritual_readable` also refuses rituals with undeclared headings. 2. On LifecycleGraphMissing from it, `ensure_lifecycle_graph` archives the file and writes `default_ritual_text(ritual_id, repo name)`, then re-checks. 3. Tests: a ritual without frontmatter and one with its own sections are archived intact and replaced; `doctor` passes.

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_graph.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both new tests fail on the unfixed code and pass here, `pytest tests` is green, and the stores that failed for this reason migrate.
