---
id: routine-task-12345
status: active
entrypoint: checklist-task-12345-execution-ready
decomposition:
- checklist-task-12345-execution-ready
- operator-task-12345-activate
- checklist-task-12345-testing-ready
- operator-task-12345-ready-for-testing
- checklist-task-12345-closeout-ready
- operator-task-12345-close
edges:
- edge-task-12345-execution-to-activate
- edge-task-12345-activate-to-testing
- edge-task-12345-testing-to-ready
- edge-task-12345-ready-to-closeout
- edge-task-12345-closeout-to-close
- edge-task-12345-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for 12345

## Summary

Actionable routine for 12345.
