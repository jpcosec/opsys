---
id: routine-task-formalize-phase-layer-workflow
status: active
entrypoint: checklist-task-formalize-phase-layer-workflow-execution-ready
decomposition:
- checklist-task-formalize-phase-layer-workflow-execution-ready
- operator-task-formalize-phase-layer-workflow-activate
- checklist-task-formalize-phase-layer-workflow-testing-ready
- operator-task-formalize-phase-layer-workflow-ready-for-testing
- checklist-task-formalize-phase-layer-workflow-closeout-ready
- operator-task-formalize-phase-layer-workflow-close
edges:
- edge-task-formalize-phase-layer-workflow-execution-to-activate
- edge-task-formalize-phase-layer-workflow-activate-to-testing
- edge-task-formalize-phase-layer-workflow-testing-to-ready
- edge-task-formalize-phase-layer-workflow-ready-to-closeout
- edge-task-formalize-phase-layer-workflow-closeout-to-close
- edge-task-formalize-phase-layer-workflow-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Formalize phase-layer workflow

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Formalize phase-layer workflow.
