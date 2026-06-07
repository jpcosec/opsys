# Routine for Routine Ref Task

ID: routine-task-with-routine-ref
Status: active

## Summary

Actionable routine for Routine Ref Task.

## Entrypoint

checklist-task-with-routine-ref-execution-ready

## Decomposition

- checklist-task-with-routine-ref-execution-ready
- operator-task-with-routine-ref-activate
- checklist-task-with-routine-ref-testing-ready
- operator-task-with-routine-ref-ready-for-testing
- checklist-task-with-routine-ref-closeout-ready
- operator-task-with-routine-ref-close

## Edges

- edge-task-with-routine-ref-execution-to-activate
- edge-task-with-routine-ref-activate-to-testing
- edge-task-with-routine-ref-testing-to-ready
- edge-task-with-routine-ref-ready-to-closeout
- edge-task-with-routine-ref-closeout-to-close
- edge-task-with-routine-ref-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
