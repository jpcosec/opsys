---
id: routine-task-pills-as-string-task
status: active
entrypoint: checklist-task-pills-as-string-task-execution-ready
decomposition:
- checklist-task-pills-as-string-task-execution-ready
- operator-task-pills-as-string-task-activate
- checklist-task-pills-as-string-task-testing-ready
- operator-task-pills-as-string-task-ready-for-testing
- checklist-task-pills-as-string-task-closeout-ready
- operator-task-pills-as-string-task-close
edges:
- edge-task-pills-as-string-task-execution-to-activate
- edge-task-pills-as-string-task-activate-to-testing
- edge-task-pills-as-string-task-testing-to-ready
- edge-task-pills-as-string-task-ready-to-closeout
- edge-task-pills-as-string-task-closeout-to-close
- edge-task-pills-as-string-task-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Pills As String Task

## Summary

Actionable routine for Pills As String Task.
