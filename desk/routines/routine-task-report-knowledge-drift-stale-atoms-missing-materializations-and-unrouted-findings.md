---
# routine-xxx
id: routine-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-execution-ready
- operator-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-activate
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-testing-ready
- operator-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-ready-for-testing
- checklist-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-closeout-ready
- operator-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-close
# Edge identifiers composing the graph
edges:
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-execution-to-activate
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-activate-to-testing
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-testing-to-ready
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-ready-to-closeout
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-closeout-to-close
- edge-task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Report knowledge drift: stale atoms, missing materializations and unrouted findings

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Report knowledge drift: stale atoms, missing materializations and unrouted findings.
