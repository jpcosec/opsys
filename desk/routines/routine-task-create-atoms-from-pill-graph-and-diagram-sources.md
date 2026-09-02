---
# routine-xxx
id: routine-task-create-atoms-from-pill-graph-and-diagram-sources
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-create-atoms-from-pill-graph-and-diagram-sources-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-create-atoms-from-pill-graph-and-diagram-sources-execution-ready
- operator-task-create-atoms-from-pill-graph-and-diagram-sources-activate
- checklist-task-create-atoms-from-pill-graph-and-diagram-sources-testing-ready
- operator-task-create-atoms-from-pill-graph-and-diagram-sources-ready-for-testing
- checklist-task-create-atoms-from-pill-graph-and-diagram-sources-closeout-ready
- operator-task-create-atoms-from-pill-graph-and-diagram-sources-close
# Edge identifiers composing the graph
edges:
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-execution-to-activate
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-activate-to-testing
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-testing-to-ready
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-ready-to-closeout
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-closeout-to-close
- edge-task-create-atoms-from-pill-graph-and-diagram-sources-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Create atoms from pill, graph, and diagram sources

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Create atoms from pill, graph, and diagram sources.
