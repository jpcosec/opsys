---
# routine-xxx
id: routine-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-execution-ready
- operator-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-activate
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-testing-ready
- operator-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-ready-for-testing
- checklist-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-closeout-ready
- operator-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-close
# Edge identifiers composing the graph
edges:
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-execution-to-activate
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-activate-to-testing
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-testing-to-ready
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-ready-to-closeout
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-closeout-to-close
- edge-task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Prevent promotion from nesting structured source sections into active task fields

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Prevent promotion from nesting structured source sections into active task fields.
