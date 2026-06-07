# Routine for ExplicitRootTask

ID: routine-task-explicitroottask
Status: active

## Summary

Actionable routine for ExplicitRootTask.

## Entrypoint

checklist-task-explicitroottask-execution-ready

## Decomposition

- checklist-task-explicitroottask-execution-ready
- operator-task-explicitroottask-activate
- checklist-task-explicitroottask-testing-ready
- operator-task-explicitroottask-ready-for-testing
- checklist-task-explicitroottask-closeout-ready
- operator-task-explicitroottask-close

## Edges

- edge-task-explicitroottask-execution-to-activate
- edge-task-explicitroottask-activate-to-testing
- edge-task-explicitroottask-testing-to-ready
- edge-task-explicitroottask-ready-to-closeout
- edge-task-explicitroottask-closeout-to-close
- edge-task-explicitroottask-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
