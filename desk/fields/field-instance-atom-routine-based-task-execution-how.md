# How Field

ID: field-instance-atom-routine-based-task-execution-how
Status: active

## Summary

Compiled field instance for how.

## Field Key

how

## Value Type

string

## Owner Artifact

atom-routine-based-task-execution

## Value

When a task is created via the spec compiler, it generates a RoutineDoc with decomposition nodes and edges. Each node is a checklist or operator. Each edge has an optional condition_ref. Advancing evaluates the current node's checklists, checks edge conditions, and if all pass, transitions to the next node via the matching operator.

## Tags

- primitive:field
- field:how
- artifact:atom
