# Routine for Missing Fields Test

ID: routine-task-missing-fields-test
Status: active

## Summary

Actionable routine for Missing Fields Test.

## Entrypoint

checklist-task-missing-fields-test-execution-ready

## Decomposition

- checklist-task-missing-fields-test-execution-ready
- operator-task-missing-fields-test-activate
- checklist-task-missing-fields-test-testing-ready
- operator-task-missing-fields-test-ready-for-testing
- checklist-task-missing-fields-test-closeout-ready
- operator-task-missing-fields-test-close

## Edges

- edge-task-missing-fields-test-execution-to-activate
- edge-task-missing-fields-test-activate-to-testing
- edge-task-missing-fields-test-testing-to-ready
- edge-task-missing-fields-test-ready-to-closeout
- edge-task-missing-fields-test-closeout-to-close
- edge-task-missing-fields-test-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
