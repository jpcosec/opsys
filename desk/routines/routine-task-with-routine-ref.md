---
id: routine-task-with-routine-ref
status: active
entrypoint: checklist-task-with-routine-ref-execution-ready
decomposition:
- checklist-task-with-routine-ref-execution-ready
- operator-task-with-routine-ref-activate
- checklist-task-with-routine-ref-testing-ready
- operator-task-with-routine-ref-ready-for-testing
- checklist-task-with-routine-ref-closeout-ready
- operator-task-with-routine-ref-close
edges:
- edge-task-with-routine-ref-execution-to-activate
- edge-task-with-routine-ref-activate-to-testing
- edge-task-with-routine-ref-testing-to-ready
- edge-task-with-routine-ref-ready-to-closeout
- edge-task-with-routine-ref-closeout-to-close
- edge-task-with-routine-ref-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Routine Ref Task

## Summary

Actionable routine for Routine Ref Task.
