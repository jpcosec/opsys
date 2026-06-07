# Routine for Boolean Test

ID: routine-task-boolean-test
Status: active

## Summary

Actionable routine for Boolean Test.

## Entrypoint

checklist-task-boolean-test-execution-ready

## Decomposition

- checklist-task-boolean-test-execution-ready
- operator-task-boolean-test-activate
- checklist-task-boolean-test-testing-ready
- operator-task-boolean-test-ready-for-testing
- checklist-task-boolean-test-closeout-ready
- operator-task-boolean-test-close

## Edges

- edge-task-boolean-test-execution-to-activate
- edge-task-boolean-test-activate-to-testing
- edge-task-boolean-test-testing-to-ready
- edge-task-boolean-test-ready-to-closeout
- edge-task-boolean-test-closeout-to-close
- edge-task-boolean-test-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
