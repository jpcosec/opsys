---
id: routine-task-from-yaml-test-minimal
status: active
entrypoint: checklist-task-from-yaml-test-minimal-execution-ready
decomposition:
- checklist-task-from-yaml-test-minimal-execution-ready
- operator-task-from-yaml-test-minimal-activate
- checklist-task-from-yaml-test-minimal-testing-ready
- operator-task-from-yaml-test-minimal-ready-for-testing
- checklist-task-from-yaml-test-minimal-closeout-ready
- operator-task-from-yaml-test-minimal-close
edges:
- edge-task-from-yaml-test-minimal-execution-to-activate
- edge-task-from-yaml-test-minimal-activate-to-testing
- edge-task-from-yaml-test-minimal-testing-to-ready
- edge-task-from-yaml-test-minimal-ready-to-closeout
- edge-task-from-yaml-test-minimal-closeout-to-close
- edge-task-from-yaml-test-minimal-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for From YAML Test Minimal

## Summary

Actionable routine for From YAML Test Minimal.
