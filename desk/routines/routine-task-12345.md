# Routine for 12345

ID: routine-task-12345
Status: active

## Summary

Actionable routine for 12345.

## Entrypoint

checklist-task-12345-execution-ready

## Decomposition

- checklist-task-12345-execution-ready
- operator-task-12345-activate
- checklist-task-12345-testing-ready
- operator-task-12345-ready-for-testing
- checklist-task-12345-closeout-ready
- operator-task-12345-close

## Edges

- edge-task-12345-execution-to-activate
- edge-task-12345-activate-to-testing
- edge-task-12345-testing-to-ready
- edge-task-12345-ready-to-closeout
- edge-task-12345-closeout-to-close
- edge-task-12345-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
