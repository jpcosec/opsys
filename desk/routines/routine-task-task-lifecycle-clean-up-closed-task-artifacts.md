---
id: routine-task-task-lifecycle-clean-up-closed-task-artifacts
status: active
entrypoint: checklist-task-task-lifecycle-clean-up-closed-task-artifacts-execution-ready
decomposition:
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-execution-ready
- operator-task-task-lifecycle-clean-up-closed-task-artifacts-activate
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-testing-ready
- operator-task-task-lifecycle-clean-up-closed-task-artifacts-ready-for-testing
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-closeout-ready
- operator-task-task-lifecycle-clean-up-closed-task-artifacts-close
edges:
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-execution-to-activate
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-activate-to-testing
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-testing-to-ready
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-ready-to-closeout
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-closeout-to-close
- edge-task-task-lifecycle-clean-up-closed-task-artifacts-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Task Lifecycle: Clean up closed task artifacts

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Task Lifecycle: Clean up closed task artifacts.
