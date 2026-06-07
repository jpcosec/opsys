# Routine for WithRootTask

ID: routine-task-withroottask
Status: active

## Summary

Actionable routine for WithRootTask.

## Entrypoint

checklist-task-withroottask-execution-ready

## Decomposition

- checklist-task-withroottask-execution-ready
- operator-task-withroottask-activate
- checklist-task-withroottask-testing-ready
- operator-task-withroottask-ready-for-testing
- checklist-task-withroottask-closeout-ready
- operator-task-withroottask-close

## Edges

- edge-task-withroottask-execution-to-activate
- edge-task-withroottask-activate-to-testing
- edge-task-withroottask-testing-to-ready
- edge-task-withroottask-ready-to-closeout
- edge-task-withroottask-closeout-to-close
- edge-task-withroottask-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
