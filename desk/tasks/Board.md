---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-desk-replace-verb-for-unmodeled-files.md
- desk/tasks/task-doctor-accepts-a-repository-with-no-desk.md
- desk/tasks/task-pill-cli-gaps-track-yaml-and-board.md
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

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- `deskops desk replace` edits unmodeled desk files through the CLI with an exact text replacement [draft] - `deskops desk replace <path> --old <text> --new <text> [--count N] --root <repo>` replaces an exact substring in one file under desk/. By default the substring must occur exactly once, or exactly N times with --count. Otherwise the command refuses and the file stays untouched. A store-tracked document is re-tracked after the write. The command prints the path and the number of replacements.
- `deskops doctor` on a repository with no desk reports that there is no desk and exits 0 [draft] - When a root has neither desk/ nor desk/config.json, `deskops doctor` prints that it found no desk at the root (with the hint that `deskops init` creates one), suggests no repair, and exits 0. A partially present desk (config without desk/, desk/ missing required files) stays a finding with exit 1, as today. `doctor --repair` on a root with no desk does not scaffold one: scaffolding stays the job of `deskops init`.
- Pill CLI gaps: add pill tracks what it creates, --from-yaml needs no flags, retire unroutes the pill from the Board [draft] - `add pill` tracks the created PillDoc in the store. `add pill --from-yaml` accepts a payload without the per-field flags, as `add task --from-yaml` already does. `retire` on a pill removes it from every Board's `pills` list in the same transaction and reports that it did.
