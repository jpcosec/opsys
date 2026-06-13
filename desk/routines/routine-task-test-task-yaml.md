---
id: routine-task-test-task-yaml
status: active
entrypoint: checklist-task-test-task-yaml-execution-ready
decomposition:
- checklist-task-test-task-yaml-execution-ready
- operator-task-test-task-yaml-activate
- checklist-task-test-task-yaml-testing-ready
- operator-task-test-task-yaml-ready-for-testing
- checklist-task-test-task-yaml-closeout-ready
- operator-task-test-task-yaml-close
edges:
- edge-task-test-task-yaml-execution-to-activate
- edge-task-test-task-yaml-activate-to-testing
- edge-task-test-task-yaml-testing-to-ready
- edge-task-test-task-yaml-ready-to-closeout
- edge-task-test-task-yaml-closeout-to-close
- edge-task-test-task-yaml-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Test Task YAML

## Summary

Actionable routine for Test Task YAML.
