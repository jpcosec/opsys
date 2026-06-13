---
id: routine-task-board-task-2
status: active
entrypoint: checklist-task-board-task-2-execution-ready
decomposition:
- checklist-task-board-task-2-execution-ready
- operator-task-board-task-2-activate
- checklist-task-board-task-2-testing-ready
- operator-task-board-task-2-ready-for-testing
- checklist-task-board-task-2-closeout-ready
- operator-task-board-task-2-close
edges:
- edge-task-board-task-2-execution-to-activate
- edge-task-board-task-2-activate-to-testing
- edge-task-board-task-2-testing-to-ready
- edge-task-board-task-2-ready-to-closeout
- edge-task-board-task-2-closeout-to-close
- edge-task-board-task-2-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Board task 2

## Summary

Actionable routine for Board task 2.
