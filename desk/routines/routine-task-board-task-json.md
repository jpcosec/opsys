---
id: routine-task-board-task-json
status: active
entrypoint: checklist-task-board-task-json-execution-ready
decomposition:
- checklist-task-board-task-json-execution-ready
- operator-task-board-task-json-activate
- checklist-task-board-task-json-testing-ready
- operator-task-board-task-json-ready-for-testing
- checklist-task-board-task-json-closeout-ready
- operator-task-board-task-json-close
edges:
- edge-task-board-task-json-execution-to-activate
- edge-task-board-task-json-activate-to-testing
- edge-task-board-task-json-testing-to-ready
- edge-task-board-task-json-ready-to-closeout
- edge-task-board-task-json-closeout-to-close
- edge-task-board-task-json-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Board task JSON

## Summary

Actionable routine for Board task JSON.
