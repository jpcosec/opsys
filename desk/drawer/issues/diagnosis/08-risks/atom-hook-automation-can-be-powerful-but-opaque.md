---
id: atom-hook-automation-can-be-powerful-but-opaque
title: Hook automation can be powerful but opaque
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:diagnosis
- topic:risks
type: atom
description: Risk to control when activating automatic hooks.
---

# Hook automation can be powerful but opaque

## Answer

Hook automation should not become an invisible side-effect machine. If hooks begin dispatching executors or creating commits automatically, deskops must also provide clear event logs, dry-run inspection, condition visibility, and evidence capture so operators can understand why automation fired and what it changed.

## Related Tasks

- `desk/tasks/task-wire-closeout-to-knowledge-gates.md`
- `desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md`

## Evidence

- `_auto_commit_task_closure()` in `deskops/operations.py` shows how impactful automatic workflow side effects can already be.
- `docs/diagrams/process/llm-tasks-vs-automatic-routines.md` says automatic routines should block or return work rather than invent semantic decisions.
- `.agents/skills/workflow-supervisor/SKILL.md` emphasizes evidence review and truthful routing, which opaque automation could undermine.
