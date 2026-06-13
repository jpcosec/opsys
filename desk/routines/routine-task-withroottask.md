---
id: routine-task-withroottask
status: active
entrypoint: checklist-task-withroottask-execution-ready
decomposition:
- checklist-task-withroottask-execution-ready
- operator-task-withroottask-activate
- checklist-task-withroottask-testing-ready
- operator-task-withroottask-ready-for-testing
- checklist-task-withroottask-closeout-ready
- operator-task-withroottask-close
edges:
- edge-task-withroottask-execution-to-activate
- edge-task-withroottask-activate-to-testing
- edge-task-withroottask-testing-to-ready
- edge-task-withroottask-ready-to-closeout
- edge-task-withroottask-closeout-to-close
- edge-task-withroottask-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for WithRootTask

## Summary

Actionable routine for WithRootTask.
