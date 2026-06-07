# Routine for Board task

ID: routine-task-board-task
Status: active

## Summary

Actionable routine for Board task.

## Entrypoint

checklist-task-board-task-execution-ready

## Decomposition

- checklist-task-board-task-execution-ready
- operator-task-board-task-activate
- checklist-task-board-task-testing-ready
- operator-task-board-task-ready-for-testing
- checklist-task-board-task-closeout-ready
- operator-task-board-task-close

## Edges

- edge-task-board-task-execution-to-activate
- edge-task-board-task-activate-to-testing
- edge-task-board-task-testing-to-ready
- edge-task-board-task-ready-to-closeout
- edge-task-board-task-closeout-to-close
- edge-task-board-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
