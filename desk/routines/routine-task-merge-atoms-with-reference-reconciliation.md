---
# routine-xxx
id: routine-task-merge-atoms-with-reference-reconciliation
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-merge-atoms-with-reference-reconciliation-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-merge-atoms-with-reference-reconciliation-execution-ready
- operator-task-merge-atoms-with-reference-reconciliation-activate
- checklist-task-merge-atoms-with-reference-reconciliation-testing-ready
- operator-task-merge-atoms-with-reference-reconciliation-ready-for-testing
- checklist-task-merge-atoms-with-reference-reconciliation-closeout-ready
- operator-task-merge-atoms-with-reference-reconciliation-close
# Edge identifiers composing the graph
edges:
- edge-task-merge-atoms-with-reference-reconciliation-execution-to-activate
- edge-task-merge-atoms-with-reference-reconciliation-activate-to-testing
- edge-task-merge-atoms-with-reference-reconciliation-testing-to-ready
- edge-task-merge-atoms-with-reference-reconciliation-ready-to-closeout
- edge-task-merge-atoms-with-reference-reconciliation-closeout-to-close
- edge-task-merge-atoms-with-reference-reconciliation-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Merge atoms with reference reconciliation

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Merge atoms with reference reconciliation.
