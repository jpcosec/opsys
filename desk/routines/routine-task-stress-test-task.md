# Routine for Stress test task

ID: routine-task-stress-test-task
Status: active

## Summary

Actionable routine for Stress test task.

## Entrypoint

checklist-task-stress-test-task-execution-ready

## Decomposition

- checklist-task-stress-test-task-execution-ready
- operator-task-stress-test-task-activate
- checklist-task-stress-test-task-testing-ready
- operator-task-stress-test-task-ready-for-testing
- checklist-task-stress-test-task-closeout-ready
- operator-task-stress-test-task-close

## Edges

- edge-task-stress-test-task-execution-to-activate
- edge-task-stress-test-task-activate-to-testing
- edge-task-stress-test-task-testing-to-ready
- edge-task-stress-test-task-ready-to-closeout
- edge-task-stress-test-task-closeout-to-close
- edge-task-stress-test-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
