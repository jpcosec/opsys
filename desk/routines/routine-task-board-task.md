---
id: routine-task-board-task
status: active
entrypoint: checklist-task-board-task-execution-ready
decomposition:
- checklist-task-board-task-execution-ready
- operator-task-board-task-activate
- checklist-task-board-task-testing-ready
- operator-task-board-task-ready-for-testing
- checklist-task-board-task-closeout-ready
- operator-task-board-task-close
edges:
- edge-task-board-task-execution-to-activate
- edge-task-board-task-activate-to-testing
- edge-task-board-task-testing-to-ready
- edge-task-board-task-ready-to-closeout
- edge-task-board-task-closeout-to-close
- edge-task-board-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Board task

## Summary

Actionable routine for Board task.
