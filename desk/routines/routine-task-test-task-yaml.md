# Routine for Test Task YAML

ID: routine-task-test-task-yaml
Status: active

## Summary

Actionable routine for Test Task YAML.

## Entrypoint

checklist-task-test-task-yaml-execution-ready

## Decomposition

- checklist-task-test-task-yaml-execution-ready
- operator-task-test-task-yaml-activate
- checklist-task-test-task-yaml-testing-ready
- operator-task-test-task-yaml-ready-for-testing
- checklist-task-test-task-yaml-closeout-ready
- operator-task-test-task-yaml-close

## Edges

- edge-task-test-task-yaml-execution-to-activate
- edge-task-test-task-yaml-activate-to-testing
- edge-task-test-task-yaml-testing-to-ready
- edge-task-test-task-yaml-ready-to-closeout
- edge-task-test-task-yaml-closeout-to-close
- edge-task-test-task-yaml-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
