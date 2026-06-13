---
id: routine-task-explicitroottask
status: active
entrypoint: checklist-task-explicitroottask-execution-ready
decomposition:
- checklist-task-explicitroottask-execution-ready
- operator-task-explicitroottask-activate
- checklist-task-explicitroottask-testing-ready
- operator-task-explicitroottask-ready-for-testing
- checklist-task-explicitroottask-closeout-ready
- operator-task-explicitroottask-close
edges:
- edge-task-explicitroottask-execution-to-activate
- edge-task-explicitroottask-activate-to-testing
- edge-task-explicitroottask-testing-to-ready
- edge-task-explicitroottask-ready-to-closeout
- edge-task-explicitroottask-closeout-to-close
- edge-task-explicitroottask-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for ExplicitRootTask

## Summary

Actionable routine for ExplicitRootTask.
