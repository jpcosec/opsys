---
# routine-xxx
id: routine-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-execution-ready
- operator-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-activate
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-testing-ready
- operator-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-ready-for-testing
- checklist-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-closeout-ready
- operator-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-close
# Edge identifiers composing the graph
edges:
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-execution-to-activate
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-activate-to-testing
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-testing-to-ready
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-ready-to-closeout
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-closeout-to-close
- edge-task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Drive sldb in process during bootstrap instead of one subprocess per model

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Drive sldb in process during bootstrap instead of one subprocess per model.
