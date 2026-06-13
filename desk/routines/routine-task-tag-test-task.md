---
id: routine-task-tag-test-task
status: active
entrypoint: checklist-task-tag-test-task-execution-ready
decomposition:
- checklist-task-tag-test-task-execution-ready
- operator-task-tag-test-task-activate
- checklist-task-tag-test-task-testing-ready
- operator-task-tag-test-task-ready-for-testing
- checklist-task-tag-test-task-closeout-ready
- operator-task-tag-test-task-close
edges:
- edge-task-tag-test-task-execution-to-activate
- edge-task-tag-test-task-activate-to-testing
- edge-task-tag-test-task-testing-to-ready
- edge-task-tag-test-task-ready-to-closeout
- edge-task-tag-test-task-closeout-to-close
- edge-task-tag-test-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Tag Test Task

## Summary

Actionable routine for Tag Test Task.
