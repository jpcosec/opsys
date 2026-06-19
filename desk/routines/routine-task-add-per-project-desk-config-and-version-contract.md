---
id: routine-task-add-per-project-desk-config-and-version-contract
status: active
entrypoint: checklist-task-add-per-project-desk-config-and-version-contract-execution-ready
decomposition:
- checklist-task-add-per-project-desk-config-and-version-contract-execution-ready
- operator-task-add-per-project-desk-config-and-version-contract-activate
- checklist-task-add-per-project-desk-config-and-version-contract-testing-ready
- operator-task-add-per-project-desk-config-and-version-contract-ready-for-testing
- checklist-task-add-per-project-desk-config-and-version-contract-closeout-ready
- operator-task-add-per-project-desk-config-and-version-contract-close
edges:
- edge-task-add-per-project-desk-config-and-version-contract-execution-to-activate
- edge-task-add-per-project-desk-config-and-version-contract-activate-to-testing
- edge-task-add-per-project-desk-config-and-version-contract-testing-to-ready
- edge-task-add-per-project-desk-config-and-version-contract-ready-to-closeout
- edge-task-add-per-project-desk-config-and-version-contract-closeout-to-close
- edge-task-add-per-project-desk-config-and-version-contract-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add per-project desk config and version contract

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add per-project desk config and version contract.
