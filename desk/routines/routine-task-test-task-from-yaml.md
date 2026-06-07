# Routine for Test task from YAML

ID: routine-task-test-task-from-yaml
Status: active

## Summary

Actionable routine for Test task from YAML.

## Entrypoint

checklist-task-test-task-from-yaml-execution-ready

## Decomposition

- checklist-task-test-task-from-yaml-execution-ready
- operator-task-test-task-from-yaml-activate
- checklist-task-test-task-from-yaml-testing-ready
- operator-task-test-task-from-yaml-ready-for-testing
- checklist-task-test-task-from-yaml-closeout-ready
- operator-task-test-task-from-yaml-close

## Edges

- edge-task-test-task-from-yaml-execution-to-activate
- edge-task-test-task-from-yaml-activate-to-testing
- edge-task-test-task-from-yaml-testing-to-ready
- edge-task-test-task-from-yaml-ready-to-closeout
- edge-task-test-task-from-yaml-closeout-to-close
- edge-task-test-task-from-yaml-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
