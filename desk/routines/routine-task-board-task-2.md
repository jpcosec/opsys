# Routine for Board task 2

ID: routine-task-board-task-2
Status: active

## Summary

Actionable routine for Board task 2.

## Entrypoint

checklist-task-board-task-2-execution-ready

## Decomposition

- checklist-task-board-task-2-execution-ready
- operator-task-board-task-2-activate
- checklist-task-board-task-2-testing-ready
- operator-task-board-task-2-ready-for-testing
- checklist-task-board-task-2-closeout-ready
- operator-task-board-task-2-close

## Edges

- edge-task-board-task-2-execution-to-activate
- edge-task-board-task-2-activate-to-testing
- edge-task-board-task-2-testing-to-ready
- edge-task-board-task-2-ready-to-closeout
- edge-task-board-task-2-closeout-to-close
- edge-task-board-task-2-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
