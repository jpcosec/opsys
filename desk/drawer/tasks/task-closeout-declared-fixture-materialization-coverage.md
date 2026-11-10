---
id: task-closeout-declared-fixture-materialization-coverage
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ''
history: []
references:
- deskops/graph/desk_graph.py
- tests/fixtures/golden/help/deskops_runtime_template.txt
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Closeout coverage for explicitly declared fixture artifacts

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Allow an explicit atom-backed materialization of a genuine fixture/golden file to be recognized by closeout while preserving broad fixture exclusions.

## Scope

_State what is in scope and what is out of scope._

Graph contract and closeout coverage for explicitly declared targets only; no workaround in Scion runtime.

## Implementation Path

_Outline the expected implementation route or affected surface._

Review deskops/graph/desk_graph.py EXCLUSIONS tests/fixtures against MATERIALIZATION_TARGETS; route a bounded task before implementation.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

A regression covers a declared .txt golden under tests/fixtures and undeclared fixture noise remains excluded.
