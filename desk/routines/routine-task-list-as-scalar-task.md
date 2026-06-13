---
id: routine-task-list-as-scalar-task
status: active
entrypoint: checklist-task-list-as-scalar-task-execution-ready
decomposition:
- checklist-task-list-as-scalar-task-execution-ready
- operator-task-list-as-scalar-task-activate
- checklist-task-list-as-scalar-task-testing-ready
- operator-task-list-as-scalar-task-ready-for-testing
- checklist-task-list-as-scalar-task-closeout-ready
- operator-task-list-as-scalar-task-close
edges:
- edge-task-list-as-scalar-task-execution-to-activate
- edge-task-list-as-scalar-task-activate-to-testing
- edge-task-list-as-scalar-task-testing-to-ready
- edge-task-list-as-scalar-task-ready-to-closeout
- edge-task-list-as-scalar-task-closeout-to-close
- edge-task-list-as-scalar-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for List As Scalar Task

## Summary

Actionable routine for List As Scalar Task.
