# Routine for None

ID: routine-task-none
Status: active

## Summary

Actionable routine for None.

## Entrypoint

checklist-task-none-execution-ready

## Decomposition

- checklist-task-none-execution-ready
- operator-task-none-activate
- checklist-task-none-testing-ready
- operator-task-none-ready-for-testing
- checklist-task-none-closeout-ready
- operator-task-none-close

## Edges

- edge-task-none-execution-to-activate
- edge-task-none-activate-to-testing
- edge-task-none-testing-to-ready
- edge-task-none-ready-to-closeout
- edge-task-none-closeout-to-close
- edge-task-none-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
