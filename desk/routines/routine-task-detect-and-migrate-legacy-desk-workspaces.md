---
id: routine-task-detect-and-migrate-legacy-desk-workspaces
status: active
entrypoint: checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
decomposition:
- checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
- operator-task-detect-and-migrate-legacy-desk-workspaces-activate
- checklist-task-detect-and-migrate-legacy-desk-workspaces-testing-ready
- operator-task-detect-and-migrate-legacy-desk-workspaces-ready-for-testing
- checklist-task-detect-and-migrate-legacy-desk-workspaces-closeout-ready
- operator-task-detect-and-migrate-legacy-desk-workspaces-close
edges:
- edge-task-detect-and-migrate-legacy-desk-workspaces-execution-to-activate
- edge-task-detect-and-migrate-legacy-desk-workspaces-activate-to-testing
- edge-task-detect-and-migrate-legacy-desk-workspaces-testing-to-ready
- edge-task-detect-and-migrate-legacy-desk-workspaces-ready-to-closeout
- edge-task-detect-and-migrate-legacy-desk-workspaces-closeout-to-close
- edge-task-detect-and-migrate-legacy-desk-workspaces-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Detect and migrate legacy desk workspaces

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Detect and migrate legacy desk workspaces.
