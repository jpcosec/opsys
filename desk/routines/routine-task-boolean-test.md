---
id: routine-task-boolean-test
status: active
entrypoint: checklist-task-boolean-test-execution-ready
decomposition:
- checklist-task-boolean-test-execution-ready
- operator-task-boolean-test-activate
- checklist-task-boolean-test-testing-ready
- operator-task-boolean-test-ready-for-testing
- checklist-task-boolean-test-closeout-ready
- operator-task-boolean-test-close
edges:
- edge-task-boolean-test-execution-to-activate
- edge-task-boolean-test-activate-to-testing
- edge-task-boolean-test-testing-to-ready
- edge-task-boolean-test-ready-to-closeout
- edge-task-boolean-test-closeout-to-close
- edge-task-boolean-test-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Boolean Test

## Summary

Actionable routine for Boolean Test.
