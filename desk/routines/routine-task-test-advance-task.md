---
id: routine-task-test-advance-task
status: active
entrypoint: checklist-task-test-advance-task-execution-ready
decomposition:
- checklist-task-test-advance-task-execution-ready
- operator-task-test-advance-task-activate
- checklist-task-test-advance-task-testing-ready
- operator-task-test-advance-task-ready-for-testing
- checklist-task-test-advance-task-closeout-ready
- operator-task-test-advance-task-close
edges:
- edge-task-test-advance-task-execution-to-activate
- edge-task-test-advance-task-activate-to-testing
- edge-task-test-advance-task-testing-to-ready
- edge-task-test-advance-task-ready-to-closeout
- edge-task-test-advance-task-closeout-to-close
- edge-task-test-advance-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Test advance task

## Summary

Actionable routine for Test advance task.
