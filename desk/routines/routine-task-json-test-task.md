---
id: routine-task-json-test-task
status: active
entrypoint: checklist-task-json-test-task-execution-ready
decomposition:
- checklist-task-json-test-task-execution-ready
- operator-task-json-test-task-activate
- checklist-task-json-test-task-testing-ready
- operator-task-json-test-task-ready-for-testing
- checklist-task-json-test-task-closeout-ready
- operator-task-json-test-task-close
edges:
- edge-task-json-test-task-execution-to-activate
- edge-task-json-test-task-activate-to-testing
- edge-task-json-test-task-testing-to-ready
- edge-task-json-test-task-ready-to-closeout
- edge-task-json-test-task-closeout-to-close
- edge-task-json-test-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for JSON Test Task

## Summary

Actionable routine for JSON Test Task.
