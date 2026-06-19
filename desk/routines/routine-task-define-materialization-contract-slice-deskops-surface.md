---
id: routine-task-define-materialization-contract-slice-deskops-surface
status: active
entrypoint: checklist-task-define-materialization-contract-slice-deskops-surface-execution-ready
decomposition:
- checklist-task-define-materialization-contract-slice-deskops-surface-execution-ready
- operator-task-define-materialization-contract-slice-deskops-surface-activate
- checklist-task-define-materialization-contract-slice-deskops-surface-testing-ready
- operator-task-define-materialization-contract-slice-deskops-surface-ready-for-testing
- checklist-task-define-materialization-contract-slice-deskops-surface-closeout-ready
- operator-task-define-materialization-contract-slice-deskops-surface-close
edges:
- edge-task-define-materialization-contract-slice-deskops-surface-execution-to-activate
- edge-task-define-materialization-contract-slice-deskops-surface-activate-to-testing
- edge-task-define-materialization-contract-slice-deskops-surface-testing-to-ready
- edge-task-define-materialization-contract-slice-deskops-surface-ready-to-closeout
- edge-task-define-materialization-contract-slice-deskops-surface-closeout-to-close
- edge-task-define-materialization-contract-slice-deskops-surface-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Define materialization contract slice (deskops surface)

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Define materialization contract slice (deskops surface).
