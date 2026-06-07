# Routine for NoRootTask

ID: routine-task-noroottask
Status: active

## Summary

Actionable routine for NoRootTask.

## Entrypoint

checklist-task-noroottask-execution-ready

## Decomposition

- checklist-task-noroottask-execution-ready
- operator-task-noroottask-activate
- checklist-task-noroottask-testing-ready
- operator-task-noroottask-ready-for-testing
- checklist-task-noroottask-closeout-ready
- operator-task-noroottask-close

## Edges

- edge-task-noroottask-execution-to-activate
- edge-task-noroottask-activate-to-testing
- edge-task-noroottask-testing-to-ready
- edge-task-noroottask-ready-to-closeout
- edge-task-noroottask-closeout-to-close
- edge-task-noroottask-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
