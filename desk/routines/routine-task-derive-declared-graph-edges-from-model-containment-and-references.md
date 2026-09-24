---
# routine-xxx
id: routine-task-derive-declared-graph-edges-from-model-containment-and-references
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-derive-declared-graph-edges-from-model-containment-and-references-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-execution-ready
- operator-task-derive-declared-graph-edges-from-model-containment-and-references-activate
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-testing-ready
- operator-task-derive-declared-graph-edges-from-model-containment-and-references-ready-for-testing
- checklist-task-derive-declared-graph-edges-from-model-containment-and-references-closeout-ready
- operator-task-derive-declared-graph-edges-from-model-containment-and-references-close
# Edge identifiers composing the graph
edges:
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-execution-to-activate
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-activate-to-testing
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-testing-to-ready
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-ready-to-closeout
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-closeout-to-close
- edge-task-derive-declared-graph-edges-from-model-containment-and-references-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Derive declared graph edges from model containment and references

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Derive declared graph edges from model containment and references.
