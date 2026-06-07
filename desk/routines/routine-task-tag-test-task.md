# Routine for Tag Test Task

ID: routine-task-tag-test-task
Status: active

## Summary

Actionable routine for Tag Test Task.

## Entrypoint

checklist-task-tag-test-task-execution-ready

## Decomposition

- checklist-task-tag-test-task-execution-ready
- operator-task-tag-test-task-activate
- checklist-task-tag-test-task-testing-ready
- operator-task-tag-test-task-ready-for-testing
- checklist-task-tag-test-task-closeout-ready
- operator-task-tag-test-task-close

## Edges

- edge-task-tag-test-task-execution-to-activate
- edge-task-tag-test-task-activate-to-testing
- edge-task-tag-test-task-testing-to-ready
- edge-task-tag-test-task-ready-to-closeout
- edge-task-tag-test-task-closeout-to-close
- edge-task-tag-test-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
