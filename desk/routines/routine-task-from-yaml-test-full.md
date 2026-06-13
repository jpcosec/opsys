---
id: routine-task-from-yaml-test-full
status: active
entrypoint: checklist-task-from-yaml-test-full-execution-ready
decomposition:
- checklist-task-from-yaml-test-full-execution-ready
- operator-task-from-yaml-test-full-activate
- checklist-task-from-yaml-test-full-testing-ready
- operator-task-from-yaml-test-full-ready-for-testing
- checklist-task-from-yaml-test-full-closeout-ready
- operator-task-from-yaml-test-full-close
edges:
- edge-task-from-yaml-test-full-execution-to-activate
- edge-task-from-yaml-test-full-activate-to-testing
- edge-task-from-yaml-test-full-testing-to-ready
- edge-task-from-yaml-test-full-ready-to-closeout
- edge-task-from-yaml-test-full-closeout-to-close
- edge-task-from-yaml-test-full-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for From YAML Test Full

## Summary

Actionable routine for From YAML Test Full.
