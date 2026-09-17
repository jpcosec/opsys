---
# routine-xxx
id: routine-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-execution-ready
- operator-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-activate
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-testing-ready
- operator-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-ready-for-testing
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-closeout-ready
- operator-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-close
# Edge identifiers composing the graph
edges:
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-execution-to-activate
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-activate-to-testing
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-testing-to-ready
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-ready-to-closeout
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-closeout-to-close
- edge-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for deskops rebuilt on pron (total refactor, fireproof test)

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for deskops rebuilt on pron (total refactor, fireproof test).
