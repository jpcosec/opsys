# Routine for Title with <html> & special chars

ID: routine-task-title-with-html-special-chars
Status: active

## Summary

Actionable routine for Title with <html> & special chars.

## Entrypoint

checklist-task-title-with-html-special-chars-execution-ready

## Decomposition

- checklist-task-title-with-html-special-chars-execution-ready
- operator-task-title-with-html-special-chars-activate
- checklist-task-title-with-html-special-chars-testing-ready
- operator-task-title-with-html-special-chars-ready-for-testing
- checklist-task-title-with-html-special-chars-closeout-ready
- operator-task-title-with-html-special-chars-close

## Edges

- edge-task-title-with-html-special-chars-execution-to-activate
- edge-task-title-with-html-special-chars-activate-to-testing
- edge-task-title-with-html-special-chars-testing-to-ready
- edge-task-title-with-html-special-chars-ready-to-closeout
- edge-task-title-with-html-special-chars-closeout-to-close
- edge-task-title-with-html-special-chars-close-to-complete

## Terminal Nodes

- complete

## Tags

- workspace:desk
- primitive:routine
