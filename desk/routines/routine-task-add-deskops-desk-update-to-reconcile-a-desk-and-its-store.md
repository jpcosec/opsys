---
# routine-xxx
id: routine-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-execution-ready
- operator-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-activate
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-testing-ready
- operator-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-ready-for-testing
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-closeout-ready
- operator-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-close
# Edge identifiers composing the graph
edges:
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-execution-to-activate
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-activate-to-testing
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-testing-to-ready
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-ready-to-closeout
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-closeout-to-close
- edge-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add deskops desk update to reconcile a desk and its store

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add deskops desk update to reconcile a desk and its store.
