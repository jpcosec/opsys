---
id: atom-dirty-worktree-and-stale-board-state-come-from-mixed-lanes-and-diverged-truth-surfaces
title: Dirty worktree and stale board state come from mixed lanes and diverged truth surfaces
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:workspace-health
- topic:drift
- topic:routing
type: atom
description: Diagnosis of why dirty git state and stale board/task routing accumulated together.
---

# Dirty worktree and stale board state come from mixed lanes and diverged truth surfaces

## Answer

The dirty git state accumulated because execution stopped respecting single-lane cleanup boundaries. The evidence bundle shows multiple unrelated strands living in the same worktree at once: active `doctor` implementation work, bulk atom/template mutation residue, operational agent/tooling additions, diagnosis drafting, inbox intake, run artifacts, and generated scratch files. That mix left unreverted or generated residue in place, so later work started on top of an already-dirty tree instead of first isolating or cleaning the earlier lane.

The stale board and task state accumulated because deskops currently lets several sources of truth drift independently: board frontmatter routing, board prose notes, task-file frontmatter such as `status`, task runtime state such as `current_node`, and the actual commit history. The evidence bundle shows all of those disagreeing at once. `desk/tasks/Board.md` routes one set of task files in frontmatter, its prose notes still advertise additional `[active]` work, some task files still read as `status: active` even when `current_node: complete`, and git history already contains commits that look like closeout points for some of those surfaces. `deskops list tasks` makes that drift more visible because it currently scans `desk/tasks/task-*.md` directly rather than only the board-routed task set, so any lingering task file can still appear active even when board routing and commit history say something else.

This is not only a documentation inconsistency. It is a workflow failure mode that sits directly between desk health and recovery, drift review, task lifecycle execution, and the eventual operator manual/routing contract. Until those tasks define one authoritative routing and cleanup model, the repo can keep recreating dirty worktrees and stale board state even after individual fixes land.

## Related Tasks

- `desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

## Evidence

- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/git-status.txt` — shows a mixed dirty worktree with tracked modifications plus untracked agent/tooling, diagnosis, inbox, and run-evidence residue.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/git-triage-report.md` — groups the dirt into multiple unrelated execution lanes and calls out unreverted/generated residue plus incomplete cleanup boundaries.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/cleanup-result-summary.md` — shows that even after targeted cleanup, the remaining tree still had several separate lanes, proving the cleanup contract was only partial.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/board.txt` — shows divergence between board frontmatter task routing and prose notes, including prose-only active items.
- `runs/subagents/20260702-070320-drawer-diagnosis-dirty-board-and-git/list-tasks.txt` — shows `deskops list tasks` reporting `task-enrich-templates-with-instructional-text | active | complete`, which is not a board-routed active task.
- `deskops/operations.py` — `list_tasks` iterates `desk/tasks/task-*.md`, so file presence currently drives task listing more than board routing does.
- `desk/tasks/task-enrich-templates-with-instructional-text.md` — still says `status: active` while `current_node: complete`, showing task-file state can remain stale on its own.
- `desk/tasks/Board.md` and the commit history summarized in `git-triage-report.md` — show that board prose, routed task references, and landed closeout-style commits can tell different stories at the same time.
