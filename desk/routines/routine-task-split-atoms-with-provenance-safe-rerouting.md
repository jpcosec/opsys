---
# routine-xxx
id: routine-task-split-atoms-with-provenance-safe-rerouting
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-split-atoms-with-provenance-safe-rerouting-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-split-atoms-with-provenance-safe-rerouting-execution-ready
- operator-task-split-atoms-with-provenance-safe-rerouting-activate
- checklist-task-split-atoms-with-provenance-safe-rerouting-testing-ready
- operator-task-split-atoms-with-provenance-safe-rerouting-ready-for-testing
- checklist-task-split-atoms-with-provenance-safe-rerouting-closeout-ready
- operator-task-split-atoms-with-provenance-safe-rerouting-close
# Edge identifiers composing the graph
edges:
- edge-task-split-atoms-with-provenance-safe-rerouting-execution-to-activate
- edge-task-split-atoms-with-provenance-safe-rerouting-activate-to-testing
- edge-task-split-atoms-with-provenance-safe-rerouting-testing-to-ready
- edge-task-split-atoms-with-provenance-safe-rerouting-ready-to-closeout
- edge-task-split-atoms-with-provenance-safe-rerouting-closeout-to-close
- edge-task-split-atoms-with-provenance-safe-rerouting-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Split atoms with provenance-safe rerouting

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Split atoms with provenance-safe rerouting.
