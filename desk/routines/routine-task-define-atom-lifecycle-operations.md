---
id: routine-task-define-atom-lifecycle-operations
status: active
entrypoint: checklist-task-define-atom-lifecycle-operations-execution-ready
decomposition:
- checklist-task-define-atom-lifecycle-operations-execution-ready
- operator-task-define-atom-lifecycle-operations-activate
- checklist-task-define-atom-lifecycle-operations-testing-ready
- operator-task-define-atom-lifecycle-operations-ready-for-testing
- checklist-task-define-atom-lifecycle-operations-closeout-ready
- operator-task-define-atom-lifecycle-operations-close
edges:
- edge-task-define-atom-lifecycle-operations-execution-to-activate
- edge-task-define-atom-lifecycle-operations-activate-to-testing
- edge-task-define-atom-lifecycle-operations-testing-to-ready
- edge-task-define-atom-lifecycle-operations-ready-to-closeout
- edge-task-define-atom-lifecycle-operations-closeout-to-close
- edge-task-define-atom-lifecycle-operations-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Define atom lifecycle operations

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Define atom lifecycle operations.
