---
id: routine-task-my-custom-id
status: active
entrypoint: checklist-task-my-custom-id-execution-ready
decomposition:
- checklist-task-my-custom-id-execution-ready
- operator-task-my-custom-id-activate
- checklist-task-my-custom-id-testing-ready
- operator-task-my-custom-id-ready-for-testing
- checklist-task-my-custom-id-closeout-ready
- operator-task-my-custom-id-close
edges:
- edge-task-my-custom-id-execution-to-activate
- edge-task-my-custom-id-activate-to-testing
- edge-task-my-custom-id-testing-to-ready
- edge-task-my-custom-id-ready-to-closeout
- edge-task-my-custom-id-closeout-to-close
- edge-task-my-custom-id-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Custom ID Task

## Summary

Actionable routine for Custom ID Task.
