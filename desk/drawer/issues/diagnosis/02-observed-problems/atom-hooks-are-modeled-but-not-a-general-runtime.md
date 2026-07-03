---
id: atom-hooks-are-modeled-but-not-a-general-runtime
title: Hooks are modeled but not a general runtime
five_wh_one_plus: what
tags:
- system:deskops
- topic:diagnosis
- topic:hooks
type: atom
description: Observed problem in the current hook layer.
---

# Hooks are modeled but not a general runtime

## Answer

Deskops already models hooks as workflow artifacts, but it does not yet expose a general runtime that resolves events, evaluates hook conditions, and dispatches hook targets consistently. As a result, some automatic behavior exists only as specialized code paths instead of as reusable hook-driven workflow automation.

## Related Tasks

- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`
- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`

## Evidence

- `deskops/models/hook.py` — defines hook documents as first-class modeled workflow artifacts.
- `deskops/cli/parser.py` and `deskops/cli/commands/operations.py` — expose add/show/list surfaces for hooks.
- `deskops/operations.py` — contains specific automation like `_auto_commit_task_closure()` but no general hook dispatcher that resolves hook docs by event and runs targets.
