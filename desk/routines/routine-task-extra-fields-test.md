---
id: routine-task-extra-fields-test
status: active
entrypoint: checklist-task-extra-fields-test-execution-ready
decomposition:
- checklist-task-extra-fields-test-execution-ready
- operator-task-extra-fields-test-activate
- checklist-task-extra-fields-test-testing-ready
- operator-task-extra-fields-test-ready-for-testing
- checklist-task-extra-fields-test-closeout-ready
- operator-task-extra-fields-test-close
edges:
- edge-task-extra-fields-test-execution-to-activate
- edge-task-extra-fields-test-activate-to-testing
- edge-task-extra-fields-test-testing-to-ready
- edge-task-extra-fields-test-ready-to-closeout
- edge-task-extra-fields-test-closeout-to-close
- edge-task-extra-fields-test-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Extra Fields Test

## Summary

Actionable routine for Extra Fields Test.
