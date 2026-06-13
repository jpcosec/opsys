---
id: routine-task-json-task
status: active
entrypoint: checklist-task-json-task-execution-ready
decomposition:
- checklist-task-json-task-execution-ready
- operator-task-json-task-activate
- checklist-task-json-task-testing-ready
- operator-task-json-task-ready-for-testing
- checklist-task-json-task-closeout-ready
- operator-task-json-task-close
edges:
- edge-task-json-task-execution-to-activate
- edge-task-json-task-activate-to-testing
- edge-task-json-task-testing-to-ready
- edge-task-json-task-ready-to-closeout
- edge-task-json-task-closeout-to-close
- edge-task-json-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for JSON Task

## Summary

Actionable routine for JSON Task.
