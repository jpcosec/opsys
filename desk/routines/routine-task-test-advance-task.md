# Routine for Test advance task

ID: routine-task-test-advance-task
Status: active

## Summary

Actionable routine for Test advance task.

## Entrypoint

checklist-task-test-advance-task-execution-ready

## Decomposition

- checklist-task-test-advance-task-execution-ready
- operator-task-test-advance-task-activate
- checklist-task-test-advance-task-testing-ready
- operator-task-test-advance-task-ready-for-testing
- checklist-task-test-advance-task-closeout-ready
- operator-task-test-advance-task-close

## Edges

- edge-task-test-advance-task-execution-to-activate
- edge-task-test-advance-task-activate-to-testing
- edge-task-test-advance-task-testing-to-ready
- edge-task-test-advance-task-ready-to-closeout
- edge-task-test-advance-task-closeout-to-close
- edge-task-test-advance-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
