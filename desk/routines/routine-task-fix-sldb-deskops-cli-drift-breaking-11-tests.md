---
# routine-xxx
id: routine-task-fix-sldb-deskops-cli-drift-breaking-11-tests
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-execution-ready
- operator-task-fix-sldb-deskops-cli-drift-breaking-11-tests-activate
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-testing-ready
- operator-task-fix-sldb-deskops-cli-drift-breaking-11-tests-ready-for-testing
- checklist-task-fix-sldb-deskops-cli-drift-breaking-11-tests-closeout-ready
- operator-task-fix-sldb-deskops-cli-drift-breaking-11-tests-close
# Edge identifiers composing the graph
edges:
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-execution-to-activate
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-activate-to-testing
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-testing-to-ready
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-ready-to-closeout
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-closeout-to-close
- edge-task-fix-sldb-deskops-cli-drift-breaking-11-tests-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Fix sldb<->deskops CLI drift breaking 11 tests

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Fix sldb<->deskops CLI drift breaking 11 tests.
