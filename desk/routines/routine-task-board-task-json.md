# Routine for Board task JSON

ID: routine-task-board-task-json
Status: active

## Summary

Actionable routine for Board task JSON.

## Entrypoint

checklist-task-board-task-json-execution-ready

## Decomposition

- checklist-task-board-task-json-execution-ready
- operator-task-board-task-json-activate
- checklist-task-board-task-json-testing-ready
- operator-task-board-task-json-ready-for-testing
- checklist-task-board-task-json-closeout-ready
- operator-task-board-task-json-close

## Edges

- edge-task-board-task-json-execution-to-activate
- edge-task-board-task-json-activate-to-testing
- edge-task-board-task-json-testing-to-ready
- edge-task-board-task-json-ready-to-closeout
- edge-task-board-task-json-closeout-to-close
- edge-task-board-task-json-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
