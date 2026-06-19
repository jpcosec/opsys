---
id: routine-task-make-task-lifecycle-runnable-from-intake-to-closeout
status: active
entrypoint: checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
decomposition:
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
- operator-task-make-task-lifecycle-runnable-from-intake-to-closeout-activate
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-testing-ready
- operator-task-make-task-lifecycle-runnable-from-intake-to-closeout-ready-for-testing
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-closeout-ready
- operator-task-make-task-lifecycle-runnable-from-intake-to-closeout-close
edges:
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-to-activate
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-activate-to-testing
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-testing-to-ready
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-ready-to-closeout
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-closeout-to-close
- edge-task-make-task-lifecycle-runnable-from-intake-to-closeout-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Make task lifecycle runnable from intake to closeout

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Make task lifecycle runnable from intake to closeout.
