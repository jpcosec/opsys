---
id: routine-task-test-task
status: active
entrypoint: checklist-task-test-task-execution-ready
decomposition:
- checklist-task-test-task-execution-ready
- operator-task-test-task-activate
- checklist-task-test-task-testing-ready
- operator-task-test-task-ready-for-testing
- checklist-task-test-task-closeout-ready
- operator-task-test-task-close
edges:
- edge-task-test-task-execution-to-activate
- edge-task-test-task-activate-to-testing
- edge-task-test-task-testing-to-ready
- edge-task-test-task-ready-to-closeout
- edge-task-test-task-closeout-to-close
- edge-task-test-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Test task

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Test task.
