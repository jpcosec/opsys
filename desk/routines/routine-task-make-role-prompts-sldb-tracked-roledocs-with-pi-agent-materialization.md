---
# routine-xxx
id: routine-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-execution-ready
- operator-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-activate
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-testing-ready
- operator-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-ready-for-testing
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-closeout-ready
- operator-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-close
# Edge identifiers composing the graph
edges:
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-execution-to-activate
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-activate-to-testing
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-testing-to-ready
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-ready-to-closeout
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-closeout-to-close
- edge-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Make role prompts sldb-tracked RoleDocs with pi-agent materialization

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Make role prompts sldb-tracked RoleDocs with pi-agent materialization.
