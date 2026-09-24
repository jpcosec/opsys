---
# routine-xxx
id: routine-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-execution-ready
- operator-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-activate
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-testing-ready
- operator-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-ready-for-testing
- checklist-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-closeout-ready
- operator-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-close
# Edge identifiers composing the graph
edges:
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-execution-to-activate
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-activate-to-testing
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-testing-to-ready
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-ready-to-closeout
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-closeout-to-close
- edge-task-give-pilldoc-the-lifecycle-slots-its-commands-already-write-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Give PillDoc the lifecycle slots its commands already write

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Give PillDoc the lifecycle slots its commands already write.
