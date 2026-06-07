# Routine for JSON Task

ID: routine-task-json-task
Status: active

## Summary

Actionable routine for JSON Task.

## Entrypoint

checklist-task-json-task-execution-ready

## Decomposition

- checklist-task-json-task-execution-ready
- operator-task-json-task-activate
- checklist-task-json-task-testing-ready
- operator-task-json-task-ready-for-testing
- checklist-task-json-task-closeout-ready
- operator-task-json-task-close

## Edges

- edge-task-json-task-execution-to-activate
- edge-task-json-task-activate-to-testing
- edge-task-json-task-testing-to-ready
- edge-task-json-task-ready-to-closeout
- edge-task-json-task-closeout-to-close
- edge-task-json-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
