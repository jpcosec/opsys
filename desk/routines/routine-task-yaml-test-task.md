# Routine for YAML test task

ID: routine-task-yaml-test-task
Status: active

## Summary

Actionable routine for YAML test task.

## Entrypoint

checklist-task-yaml-test-task-execution-ready

## Decomposition

- checklist-task-yaml-test-task-execution-ready
- operator-task-yaml-test-task-activate
- checklist-task-yaml-test-task-testing-ready
- operator-task-yaml-test-task-ready-for-testing
- checklist-task-yaml-test-task-closeout-ready
- operator-task-yaml-test-task-close

## Edges

- edge-task-yaml-test-task-execution-to-activate
- edge-task-yaml-test-task-activate-to-testing
- edge-task-yaml-test-task-testing-to-ready
- edge-task-yaml-test-task-ready-to-closeout
- edge-task-yaml-test-task-closeout-to-close
- edge-task-yaml-test-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
