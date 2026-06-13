---
id: routine-task-nested-structure-task
status: active
entrypoint: checklist-task-nested-structure-task-execution-ready
decomposition:
- checklist-task-nested-structure-task-execution-ready
- operator-task-nested-structure-task-activate
- checklist-task-nested-structure-task-testing-ready
- operator-task-nested-structure-task-ready-for-testing
- checklist-task-nested-structure-task-closeout-ready
- operator-task-nested-structure-task-close
edges:
- edge-task-nested-structure-task-execution-to-activate
- edge-task-nested-structure-task-activate-to-testing
- edge-task-nested-structure-task-testing-to-ready
- edge-task-nested-structure-task-ready-to-closeout
- edge-task-nested-structure-task-closeout-to-close
- edge-task-nested-structure-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Nested Structure Task

## Summary

Actionable routine for Nested Structure Task.
