---
# routine-xxx
id: routine-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-execution-ready
- operator-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-activate
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-testing-ready
- operator-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-ready-for-testing
- checklist-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-closeout-ready
- operator-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-close
# Edge identifiers composing the graph
edges:
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-execution-to-activate
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-activate-to-testing
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-testing-to-ready
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-ready-to-closeout
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-closeout-to-close
- edge-task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Make cross-repo inbox delivery work from a canonical identity

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Make cross-repo inbox delivery work from a canonical identity.
