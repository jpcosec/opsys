# Routine for Title with
newline

ID: routine-task-title-with-newline
Status: active

## Summary

Actionable routine for Title with
newline.

## Entrypoint

checklist-task-title-with-newline-execution-ready

## Decomposition

- checklist-task-title-with-newline-execution-ready
- operator-task-title-with-newline-activate
- checklist-task-title-with-newline-testing-ready
- operator-task-title-with-newline-ready-for-testing
- checklist-task-title-with-newline-closeout-ready
- operator-task-title-with-newline-close

## Edges

- edge-task-title-with-newline-execution-to-activate
- edge-task-title-with-newline-activate-to-testing
- edge-task-title-with-newline-testing-to-ready
- edge-task-title-with-newline-ready-to-closeout
- edge-task-title-with-newline-closeout-to-close
- edge-task-title-with-newline-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
