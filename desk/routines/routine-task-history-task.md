---
id: routine-task-history-task
status: active
entrypoint: checklist-task-history-task-execution-ready
decomposition:
- checklist-task-history-task-execution-ready
- operator-task-history-task-activate
- checklist-task-history-task-testing-ready
- operator-task-history-task-ready-for-testing
- checklist-task-history-task-closeout-ready
- operator-task-history-task-close
edges:
- edge-task-history-task-execution-to-activate
- edge-task-history-task-activate-to-testing
- edge-task-history-task-testing-to-ready
- edge-task-history-task-ready-to-closeout
- edge-task-history-task-closeout-to-close
- edge-task-history-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for History Task

## Summary

Actionable routine for History Task.
