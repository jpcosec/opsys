---
id: routine-task-noroottask
status: active
entrypoint: checklist-task-noroottask-execution-ready
decomposition:
- checklist-task-noroottask-execution-ready
- operator-task-noroottask-activate
- checklist-task-noroottask-testing-ready
- operator-task-noroottask-ready-for-testing
- checklist-task-noroottask-closeout-ready
- operator-task-noroottask-close
edges:
- edge-task-noroottask-execution-to-activate
- edge-task-noroottask-activate-to-testing
- edge-task-noroottask-testing-to-ready
- edge-task-noroottask-ready-to-closeout
- edge-task-noroottask-closeout-to-close
- edge-task-noroottask-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for NoRootTask

## Summary

Actionable routine for NoRootTask.
