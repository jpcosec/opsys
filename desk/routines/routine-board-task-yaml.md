# Routine for Board task YAML

ID: routine-board-task-yaml
Status: active

## Summary

Actionable routine for Board task YAML.

## Entrypoint

checklist-board-task-yaml-execution-ready

## Decomposition

- checklist-board-task-yaml-execution-ready
- operator-board-task-yaml-activate
- checklist-board-task-yaml-testing-ready
- operator-board-task-yaml-ready-for-testing
- checklist-board-task-yaml-closeout-ready
- operator-board-task-yaml-close

## Edges

- edge-board-task-yaml-execution-to-activate
- edge-board-task-yaml-activate-to-testing
- edge-board-task-yaml-testing-to-ready
- edge-board-task-yaml-ready-to-closeout
- edge-board-task-yaml-closeout-to-close
- edge-board-task-yaml-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
