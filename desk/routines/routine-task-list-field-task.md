# Routine for List Field Task

ID: routine-task-list-field-task
Status: active

## Summary

Actionable routine for List Field Task.

## Entrypoint

checklist-task-list-field-task-execution-ready

## Decomposition

- checklist-task-list-field-task-execution-ready
- operator-task-list-field-task-activate
- checklist-task-list-field-task-testing-ready
- operator-task-list-field-task-ready-for-testing
- checklist-task-list-field-task-closeout-ready
- operator-task-list-field-task-close

## Edges

- edge-task-list-field-task-execution-to-activate
- edge-task-list-field-task-activate-to-testing
- edge-task-list-field-task-testing-to-ready
- edge-task-list-field-task-ready-to-closeout
- edge-task-list-field-task-closeout-to-close
- edge-task-list-field-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
