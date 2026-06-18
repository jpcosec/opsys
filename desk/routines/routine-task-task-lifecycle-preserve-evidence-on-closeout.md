---
id: routine-task-task-lifecycle-preserve-evidence-on-closeout
status: active
entrypoint: checklist-task-task-lifecycle-preserve-evidence-on-closeout-execution-ready
decomposition:
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-execution-ready
- operator-task-task-lifecycle-preserve-evidence-on-closeout-activate
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-testing-ready
- operator-task-task-lifecycle-preserve-evidence-on-closeout-ready-for-testing
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-closeout-ready
- operator-task-task-lifecycle-preserve-evidence-on-closeout-close
edges:
- edge-task-task-lifecycle-preserve-evidence-on-closeout-execution-to-activate
- edge-task-task-lifecycle-preserve-evidence-on-closeout-activate-to-testing
- edge-task-task-lifecycle-preserve-evidence-on-closeout-testing-to-ready
- edge-task-task-lifecycle-preserve-evidence-on-closeout-ready-to-closeout
- edge-task-task-lifecycle-preserve-evidence-on-closeout-closeout-to-close
- edge-task-task-lifecycle-preserve-evidence-on-closeout-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Task Lifecycle: Preserve evidence on closeout

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Task Lifecycle: Preserve evidence on closeout.
