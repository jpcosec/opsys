# Routine for History Task

ID: routine-task-history-task
Status: active

## Summary

Actionable routine for History Task.

## Entrypoint

checklist-task-history-task-execution-ready

## Decomposition

- checklist-task-history-task-execution-ready
- operator-task-history-task-activate
- checklist-task-history-task-testing-ready
- operator-task-history-task-ready-for-testing
- checklist-task-history-task-closeout-ready
- operator-task-history-task-close

## Edges

- edge-task-history-task-execution-to-activate
- edge-task-history-task-activate-to-testing
- edge-task-history-task-testing-to-ready
- edge-task-history-task-ready-to-closeout
- edge-task-history-task-closeout-to-close
- edge-task-history-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
