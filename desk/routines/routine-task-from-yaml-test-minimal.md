# Routine for From YAML Test Minimal

ID: routine-task-from-yaml-test-minimal
Status: active

## Summary

Actionable routine for From YAML Test Minimal.

## Entrypoint

checklist-task-from-yaml-test-minimal-execution-ready

## Decomposition

- checklist-task-from-yaml-test-minimal-execution-ready
- operator-task-from-yaml-test-minimal-activate
- checklist-task-from-yaml-test-minimal-testing-ready
- operator-task-from-yaml-test-minimal-ready-for-testing
- checklist-task-from-yaml-test-minimal-closeout-ready
- operator-task-from-yaml-test-minimal-close

## Edges

- edge-task-from-yaml-test-minimal-execution-to-activate
- edge-task-from-yaml-test-minimal-activate-to-testing
- edge-task-from-yaml-test-minimal-testing-to-ready
- edge-task-from-yaml-test-minimal-ready-to-closeout
- edge-task-from-yaml-test-minimal-closeout-to-close
- edge-task-from-yaml-test-minimal-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
