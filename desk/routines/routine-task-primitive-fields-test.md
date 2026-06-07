# Routine for Primitive Fields Test

ID: routine-task-primitive-fields-test
Status: active

## Summary

Actionable routine for Primitive Fields Test.

## Entrypoint

checklist-task-primitive-fields-test-execution-ready

## Decomposition

- checklist-task-primitive-fields-test-execution-ready
- operator-task-primitive-fields-test-activate
- checklist-task-primitive-fields-test-testing-ready
- operator-task-primitive-fields-test-ready-for-testing
- checklist-task-primitive-fields-test-closeout-ready
- operator-task-primitive-fields-test-close

## Edges

- edge-task-primitive-fields-test-execution-to-activate
- edge-task-primitive-fields-test-activate-to-testing
- edge-task-primitive-fields-test-testing-to-ready
- edge-task-primitive-fields-test-ready-to-closeout
- edge-task-primitive-fields-test-closeout-to-close
- edge-task-primitive-fields-test-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
