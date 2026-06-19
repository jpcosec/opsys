---
id: routine-task-add-desk-health-and-recovery-surface-deskops-slice
status: active
entrypoint: checklist-task-add-desk-health-and-recovery-surface-deskops-slice-execution-ready
decomposition:
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-execution-ready
- operator-task-add-desk-health-and-recovery-surface-deskops-slice-activate
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-testing-ready
- operator-task-add-desk-health-and-recovery-surface-deskops-slice-ready-for-testing
- checklist-task-add-desk-health-and-recovery-surface-deskops-slice-closeout-ready
- operator-task-add-desk-health-and-recovery-surface-deskops-slice-close
edges:
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-execution-to-activate
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-activate-to-testing
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-testing-to-ready
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-ready-to-closeout
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-closeout-to-close
- edge-task-add-desk-health-and-recovery-surface-deskops-slice-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add desk health and recovery surface (deskops slice)

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add desk health and recovery surface (deskops slice).
