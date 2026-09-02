---
# routine-xxx
id: routine-task-add-promote-no-trackean-el-bundle-generado-en-el-store
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-execution-ready
- operator-task-add-promote-no-trackean-el-bundle-generado-en-el-store-activate
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-testing-ready
- operator-task-add-promote-no-trackean-el-bundle-generado-en-el-store-ready-for-testing
- checklist-task-add-promote-no-trackean-el-bundle-generado-en-el-store-closeout-ready
- operator-task-add-promote-no-trackean-el-bundle-generado-en-el-store-close
# Edge identifiers composing the graph
edges:
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-execution-to-activate
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-activate-to-testing
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-testing-to-ready
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-ready-to-closeout
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-closeout-to-close
- edge-task-add-promote-no-trackean-el-bundle-generado-en-el-store-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for add/promote no trackean el bundle generado en el store

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for add/promote no trackean el bundle generado en el store.
