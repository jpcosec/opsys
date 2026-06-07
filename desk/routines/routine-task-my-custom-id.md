# Routine for Custom ID Task

ID: routine-task-my-custom-id
Status: active

## Summary

Actionable routine for Custom ID Task.

## Entrypoint

checklist-task-my-custom-id-execution-ready

## Decomposition

- checklist-task-my-custom-id-execution-ready
- operator-task-my-custom-id-activate
- checklist-task-my-custom-id-testing-ready
- operator-task-my-custom-id-ready-for-testing
- checklist-task-my-custom-id-closeout-ready
- operator-task-my-custom-id-close

## Edges

- edge-task-my-custom-id-execution-to-activate
- edge-task-my-custom-id-activate-to-testing
- edge-task-my-custom-id-testing-to-ready
- edge-task-my-custom-id-ready-to-closeout
- edge-task-my-custom-id-closeout-to-close
- edge-task-my-custom-id-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
