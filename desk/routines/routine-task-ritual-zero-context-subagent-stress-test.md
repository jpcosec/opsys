---
# routine-xxx
id: routine-task-ritual-zero-context-subagent-stress-test
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-ritual-zero-context-subagent-stress-test-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-ritual-zero-context-subagent-stress-test-execution-ready
- operator-task-ritual-zero-context-subagent-stress-test-activate
- checklist-task-ritual-zero-context-subagent-stress-test-testing-ready
- operator-task-ritual-zero-context-subagent-stress-test-ready-for-testing
- checklist-task-ritual-zero-context-subagent-stress-test-closeout-ready
- operator-task-ritual-zero-context-subagent-stress-test-close
# Edge identifiers composing the graph
edges:
- edge-task-ritual-zero-context-subagent-stress-test-execution-to-activate
- edge-task-ritual-zero-context-subagent-stress-test-activate-to-testing
- edge-task-ritual-zero-context-subagent-stress-test-testing-to-ready
- edge-task-ritual-zero-context-subagent-stress-test-ready-to-closeout
- edge-task-ritual-zero-context-subagent-stress-test-closeout-to-close
- edge-task-ritual-zero-context-subagent-stress-test-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Ritual: Zero-context subagent stress test

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Ritual: Zero-context subagent stress test.
