---
# routine-xxx
id: routine-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-execution-ready
- operator-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-activate
- checklist-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-testing-ready
- operator-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-ready-for-testing
- checklist-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-closeout-ready
- operator-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-close
# Edge identifiers composing the graph
edges:
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-execution-to-activate
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-activate-to-testing
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-testing-to-ready
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-ready-to-closeout
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-closeout-to-close
- edge-task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Anti-pattern: Monolithic API endpoint in SLDB Viewer

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Anti-pattern: Monolithic API endpoint in SLDB Viewer.
