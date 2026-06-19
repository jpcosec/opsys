---
id: routine-task-add-drift-check-review-loop
status: active
entrypoint: checklist-task-add-drift-check-review-loop-execution-ready
decomposition:
- checklist-task-add-drift-check-review-loop-execution-ready
- operator-task-add-drift-check-review-loop-activate
- checklist-task-add-drift-check-review-loop-testing-ready
- operator-task-add-drift-check-review-loop-ready-for-testing
- checklist-task-add-drift-check-review-loop-closeout-ready
- operator-task-add-drift-check-review-loop-close
edges:
- edge-task-add-drift-check-review-loop-execution-to-activate
- edge-task-add-drift-check-review-loop-activate-to-testing
- edge-task-add-drift-check-review-loop-testing-to-ready
- edge-task-add-drift-check-review-loop-ready-to-closeout
- edge-task-add-drift-check-review-loop-closeout-to-close
- edge-task-add-drift-check-review-loop-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add drift check review loop

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add drift check review loop.
