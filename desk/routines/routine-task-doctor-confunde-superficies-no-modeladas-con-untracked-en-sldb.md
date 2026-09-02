---
# routine-xxx
id: routine-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-execution-ready
- operator-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-activate
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-testing-ready
- operator-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-ready-for-testing
- checklist-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-closeout-ready
- operator-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-close
# Edge identifiers composing the graph
edges:
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-execution-to-activate
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-activate-to-testing
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-testing-to-ready
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-ready-to-closeout
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-closeout-to-close
- edge-task-doctor-confunde-superficies-no-modeladas-con-untracked-en-sldb-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Doctor confunde superficies no modeladas con untracked en sldb

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Doctor confunde superficies no modeladas con untracked en sldb.
