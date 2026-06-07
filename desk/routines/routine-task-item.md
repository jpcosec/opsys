# Routine for

ID: routine-task-item
Status: active

## Summary

Actionable routine for .

## Entrypoint

checklist-task-item-execution-ready

## Decomposition

- checklist-task-item-execution-ready
- operator-task-item-activate
- checklist-task-item-testing-ready
- operator-task-item-ready-for-testing
- checklist-task-item-closeout-ready
- operator-task-item-close

## Edges

- edge-task-item-execution-to-activate
- edge-task-item-activate-to-testing
- edge-task-item-testing-to-ready
- edge-task-item-ready-to-closeout
- edge-task-item-closeout-to-close
- edge-task-item-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
