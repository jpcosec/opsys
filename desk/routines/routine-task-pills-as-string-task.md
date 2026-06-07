# Routine for Pills As String Task

ID: routine-task-pills-as-string-task
Status: active

## Summary

Actionable routine for Pills As String Task.

## Entrypoint

checklist-task-pills-as-string-task-execution-ready

## Decomposition

- checklist-task-pills-as-string-task-execution-ready
- operator-task-pills-as-string-task-activate
- checklist-task-pills-as-string-task-testing-ready
- operator-task-pills-as-string-task-ready-for-testing
- checklist-task-pills-as-string-task-closeout-ready
- operator-task-pills-as-string-task-close

## Edges

- edge-task-pills-as-string-task-execution-to-activate
- edge-task-pills-as-string-task-activate-to-testing
- edge-task-pills-as-string-task-testing-to-ready
- edge-task-pills-as-string-task-ready-to-closeout
- edge-task-pills-as-string-task-closeout-to-close
- edge-task-pills-as-string-task-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
