---
id: routine-task-task-lifecycle-enforce-phase-gates-during-advancement
status: active
entrypoint: checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-execution-ready
decomposition:
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-execution-ready
- operator-task-task-lifecycle-enforce-phase-gates-during-advancement-activate
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-testing-ready
- operator-task-task-lifecycle-enforce-phase-gates-during-advancement-ready-for-testing
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-closeout-ready
- operator-task-task-lifecycle-enforce-phase-gates-during-advancement-close
edges:
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-execution-to-activate
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-activate-to-testing
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-testing-to-ready
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-ready-to-closeout
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-closeout-to-close
- edge-task-task-lifecycle-enforce-phase-gates-during-advancement-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Task Lifecycle: Enforce phase gates during advancement

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Task Lifecycle: Enforce phase gates during advancement.
