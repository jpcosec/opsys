---
id: routine-task-primitive-fields-test
status: active
entrypoint: checklist-task-primitive-fields-test-execution-ready
decomposition:
- checklist-task-primitive-fields-test-execution-ready
- operator-task-primitive-fields-test-activate
- checklist-task-primitive-fields-test-testing-ready
- operator-task-primitive-fields-test-ready-for-testing
- checklist-task-primitive-fields-test-closeout-ready
- operator-task-primitive-fields-test-close
edges:
- edge-task-primitive-fields-test-execution-to-activate
- edge-task-primitive-fields-test-activate-to-testing
- edge-task-primitive-fields-test-testing-to-ready
- edge-task-primitive-fields-test-ready-to-closeout
- edge-task-primitive-fields-test-closeout-to-close
- edge-task-primitive-fields-test-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Primitive Fields Test

## Summary

Actionable routine for Primitive Fields Test.
