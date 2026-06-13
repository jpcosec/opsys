---
id: routine-task-yaml-test-task
status: active
entrypoint: checklist-task-yaml-test-task-execution-ready
decomposition:
- checklist-task-yaml-test-task-execution-ready
- operator-task-yaml-test-task-activate
- checklist-task-yaml-test-task-testing-ready
- operator-task-yaml-test-task-ready-for-testing
- checklist-task-yaml-test-task-closeout-ready
- operator-task-yaml-test-task-close
edges:
- edge-task-yaml-test-task-execution-to-activate
- edge-task-yaml-test-task-activate-to-testing
- edge-task-yaml-test-task-testing-to-ready
- edge-task-yaml-test-task-ready-to-closeout
- edge-task-yaml-test-task-closeout-to-close
- edge-task-yaml-test-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for YAML test task

## Summary

Actionable routine for YAML test task.
