---
id: task-guard-extension-points
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- tests/test_extension_points.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Guard the declared deskops extension points

## Rationale

_Explain why this task exists or the business driver behind it._

Models, spec artifacts, CLI commands, artifact maps, and command handlers are separate registries.
They are maintained by convention but not asserted as one contract, so a new model or command can
land half-registered.

## Goal

_Describe the concrete result this task must produce._

Add one test that proves the public extension registries agree with each other and that every CLI
handler resolves, without changing runtime behavior.

## Scope

_State what is in scope and what is out of scope._

In scope: one test module and fixes limited to genuine registry mismatches. Out of scope: new
extension APIs, plugin loading, CLI changes, and model contract changes.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `tests/test_extension_points.py`.
2. Assert every key in `deskops.operations.ARTIFACT_MODELS` exists in
   `deskops.operations.ARTIFACT_PATHS`.
3. Assert `set(ARTIFACT_MODELS) - set(ARTIFACT_SUBJECTS) == {"artifact.task"}` and that no other
   artifact is missing a subject.
4. Assert every `deskops.bootstrap.MODEL_REFS` name is in `deskops.models.__all__` and resolves to
   a `StructuredNLDoc` subclass.
5. Assert every artifact id in `SpecRegistry.load(deskops.paths.data_path("spec")).artifacts`
   resolves through `ARTIFACT_MODELS` or is the task-only artifact.
6. Assert every `command_registry()` handler string imports as `module:attribute` and that the
   attribute is callable.
7. If a real mismatch appears, fix only the registry entry; do not change command behavior or model
   fields.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_extension_points.py -q
- python -m pytest tests/test_specs.py tests/test_command_registry.py tests/test_federated_models.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

The test enumerates and verifies models, spec artifacts, artifact maps, and CLI handlers as one
contract, and `pytest` is green with no behavior changes.
