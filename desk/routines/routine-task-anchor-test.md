---
id: routine-task-anchor-test
status: active
entrypoint: checklist-task-anchor-test-execution-ready
decomposition:
- checklist-task-anchor-test-execution-ready
- operator-task-anchor-test-activate
- checklist-task-anchor-test-testing-ready
- operator-task-anchor-test-ready-for-testing
- checklist-task-anchor-test-closeout-ready
- operator-task-anchor-test-close
edges:
- edge-task-anchor-test-execution-to-activate
- edge-task-anchor-test-activate-to-testing
- edge-task-anchor-test-testing-to-ready
- edge-task-anchor-test-ready-to-closeout
- edge-task-anchor-test-closeout-to-close
- edge-task-anchor-test-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Anchor Test

## Summary

Actionable routine for Anchor Test.
