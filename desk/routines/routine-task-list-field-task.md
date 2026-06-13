---
id: routine-task-list-field-task
status: active
entrypoint: checklist-task-list-field-task-execution-ready
decomposition:
- checklist-task-list-field-task-execution-ready
- operator-task-list-field-task-activate
- checklist-task-list-field-task-testing-ready
- operator-task-list-field-task-ready-for-testing
- checklist-task-list-field-task-closeout-ready
- operator-task-list-field-task-close
edges:
- edge-task-list-field-task-execution-to-activate
- edge-task-list-field-task-activate-to-testing
- edge-task-list-field-task-testing-to-ready
- edge-task-list-field-task-ready-to-closeout
- edge-task-list-field-task-closeout-to-close
- edge-task-list-field-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for List Field Task

## Summary

Actionable routine for List Field Task.
