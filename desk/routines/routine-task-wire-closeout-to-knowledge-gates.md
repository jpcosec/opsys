---
id: routine-task-wire-closeout-to-knowledge-gates
status: active
entrypoint: checklist-task-wire-closeout-to-knowledge-gates-execution-ready
decomposition:
- checklist-task-wire-closeout-to-knowledge-gates-execution-ready
- operator-task-wire-closeout-to-knowledge-gates-activate
- checklist-task-wire-closeout-to-knowledge-gates-testing-ready
- operator-task-wire-closeout-to-knowledge-gates-ready-for-testing
- checklist-task-wire-closeout-to-knowledge-gates-closeout-ready
- operator-task-wire-closeout-to-knowledge-gates-close
edges:
- edge-task-wire-closeout-to-knowledge-gates-execution-to-activate
- edge-task-wire-closeout-to-knowledge-gates-activate-to-testing
- edge-task-wire-closeout-to-knowledge-gates-testing-to-ready
- edge-task-wire-closeout-to-knowledge-gates-ready-to-closeout
- edge-task-wire-closeout-to-knowledge-gates-closeout-to-close
- edge-task-wire-closeout-to-knowledge-gates-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Wire closeout to knowledge gates

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Wire closeout to knowledge gates.
