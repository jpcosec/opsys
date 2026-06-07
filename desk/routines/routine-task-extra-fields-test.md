# Routine for Extra Fields Test

ID: routine-task-extra-fields-test
Status: active

## Summary

Actionable routine for Extra Fields Test.

## Entrypoint

checklist-task-extra-fields-test-execution-ready

## Decomposition

- checklist-task-extra-fields-test-execution-ready
- operator-task-extra-fields-test-activate
- checklist-task-extra-fields-test-testing-ready
- operator-task-extra-fields-test-ready-for-testing
- checklist-task-extra-fields-test-closeout-ready
- operator-task-extra-fields-test-close

## Edges

- edge-task-extra-fields-test-execution-to-activate
- edge-task-extra-fields-test-activate-to-testing
- edge-task-extra-fields-test-testing-to-ready
- edge-task-extra-fields-test-ready-to-closeout
- edge-task-extra-fields-test-closeout-to-close
- edge-task-extra-fields-test-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
