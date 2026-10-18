---
id: atom-operational-primitives-model
title: Task lifecycle is an sldb graph
five_wh_one_plus: what
tags:
- system:deskops
- topic:routines
- layer:runtime
---

# Task lifecycle is an sldb graph

## Answer

A task's lifecycle is part of the desk's sldb graph. Its states are the desk's rituals (RitualDoc ritual-execution, ritual-testing, ritual-closeout); its transitions are sldb RelationDoc edges between them, typed by a RelationTypeDoc that names the verb (task_activates, task_hands_to_closeout, task_completes) and guarded by a condition written as an sldb --where predicate on the task. deskops writes that graph once per desk (deskops init, deskops desk update --apply) from deskops/spec/workflows/task_lifecycle.yaml and reads it back from sldb's edge index; a task carries only current_node and status. There are no per-task routines, conditions, checklists, operators, edges or hooks: those deskops models were retired in favor of sldb's native graph.
