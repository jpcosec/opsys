---
id: routine-board-task-yaml
status: active
entrypoint: checklist-board-task-yaml-execution-ready
decomposition:
- checklist-board-task-yaml-execution-ready
- operator-board-task-yaml-activate
- checklist-board-task-yaml-testing-ready
- operator-board-task-yaml-ready-for-testing
- checklist-board-task-yaml-closeout-ready
- operator-board-task-yaml-close
edges:
- edge-board-task-yaml-execution-to-activate
- edge-board-task-yaml-activate-to-testing
- edge-board-task-yaml-testing-to-ready
- edge-board-task-yaml-ready-to-closeout
- edge-board-task-yaml-closeout-to-close
- edge-board-task-yaml-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Board task YAML

## Summary

Actionable routine for Board task YAML.
