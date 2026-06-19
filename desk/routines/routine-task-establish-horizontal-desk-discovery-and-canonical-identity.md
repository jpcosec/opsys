---
id: routine-task-establish-horizontal-desk-discovery-and-canonical-identity
status: active
entrypoint: checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
decomposition:
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-ready
- operator-task-establish-horizontal-desk-discovery-and-canonical-identity-activate
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-testing-ready
- operator-task-establish-horizontal-desk-discovery-and-canonical-identity-ready-for-testing
- checklist-task-establish-horizontal-desk-discovery-and-canonical-identity-closeout-ready
- operator-task-establish-horizontal-desk-discovery-and-canonical-identity-close
edges:
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-execution-to-activate
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-activate-to-testing
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-testing-to-ready
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-ready-to-closeout
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-closeout-to-close
- edge-task-establish-horizontal-desk-discovery-and-canonical-identity-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Establish horizontal desk discovery and canonical identity

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Establish horizontal desk discovery and canonical identity.
