# Routine for JSON Test Task

ID: routine-task-json-test-task
Status: active

## Summary

Actionable routine for JSON Test Task.

## Entrypoint

checklist-task-json-test-task-execution-ready

## Decomposition

- checklist-task-json-test-task-execution-ready
- operator-task-json-test-task-activate
- checklist-task-json-test-task-testing-ready
- operator-task-json-test-task-ready-for-testing
- checklist-task-json-test-task-closeout-ready
- operator-task-json-test-task-close

## Edges

- edge-task-json-test-task-execution-to-activate
- edge-task-json-test-task-activate-to-testing
- edge-task-json-test-task-testing-to-ready
- edge-task-json-test-task-ready-to-closeout
- edge-task-json-test-task-closeout-to-close
- edge-task-json-test-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
