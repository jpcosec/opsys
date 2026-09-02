---
# routine-xxx
id: routine-task-empaquetar-deskops-como-m-dulo-de-pi-subagents
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-execution-ready
- operator-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-activate
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-testing-ready
- operator-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-ready-for-testing
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-closeout-ready
- operator-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-close
# Edge identifiers composing the graph
edges:
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-execution-to-activate
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-activate-to-testing
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-testing-to-ready
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-ready-to-closeout
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-closeout-to-close
- edge-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Empaquetar deskops como módulo de pi-subagents

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Empaquetar deskops como módulo de pi-subagents.
