---
id: routine-task-item
status: active
entrypoint: checklist-task-item-execution-ready
decomposition:
- checklist-task-item-execution-ready
- operator-task-item-activate
- checklist-task-item-testing-ready
- operator-task-item-ready-for-testing
- checklist-task-item-closeout-ready
- operator-task-item-close
edges:
- edge-task-item-execution-to-activate
- edge-task-item-activate-to-testing
- edge-task-item-testing-to-ready
- edge-task-item-ready-to-closeout
- edge-task-item-closeout-to-close
- edge-task-item-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for

## Summary

Actionable routine for .
