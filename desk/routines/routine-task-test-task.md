# Routine for Test Task

ID: routine-task-test-task
Status: active

## Summary

Actionable routine for Test Task.

## Entrypoint

checklist-task-test-task-execution-ready

## Decomposition

- checklist-task-test-task-execution-ready
- operator-task-test-task-activate
- checklist-task-test-task-testing-ready
- operator-task-test-task-ready-for-testing
- checklist-task-test-task-closeout-ready
- operator-task-test-task-close

## Edges

- edge-task-test-task-execution-to-activate
- edge-task-test-task-activate-to-testing
- edge-task-test-task-testing-to-ready
- edge-task-test-task-ready-to-closeout
- edge-task-test-task-closeout-to-close
- edge-task-test-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
