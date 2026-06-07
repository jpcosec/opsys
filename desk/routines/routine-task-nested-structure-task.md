# Routine for Nested Structure Task

ID: routine-task-nested-structure-task
Status: active

## Summary

Actionable routine for Nested Structure Task.

## Entrypoint

checklist-task-nested-structure-task-execution-ready

## Decomposition

- checklist-task-nested-structure-task-execution-ready
- operator-task-nested-structure-task-activate
- checklist-task-nested-structure-task-testing-ready
- operator-task-nested-structure-task-ready-for-testing
- checklist-task-nested-structure-task-closeout-ready
- operator-task-nested-structure-task-close

## Edges

- edge-task-nested-structure-task-execution-to-activate
- edge-task-nested-structure-task-activate-to-testing
- edge-task-nested-structure-task-testing-to-ready
- edge-task-nested-structure-task-ready-to-closeout
- edge-task-nested-structure-task-closeout-to-close
- edge-task-nested-structure-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
