---
id: task-adapter-deskops-a-scion-runtime-template
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- 3d50831
- tests/test_scion_runtime.py
- atom-role-prompts-are-tracked-documents-agent-files-are-materializations
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Adapter deskops a Scion: runtime template

## Rationale

_Explain why this task exists or the business driver behind it._

Scion ejecuta los executors de deskops desde templates; el RoleDoc y el RuntimeProfileDoc deben seguir siendo la fuente y el template una materialización, como ya pasa con los agentes pi.

## Goal

_Describe the concrete result this task must produce._

deskops runtime template <role> --harness <h> genera scion-agent.yaml, system-prompt.md y agents.md desde el desk, y con --task/--agent deja un RunDoc.

## Scope

_State what is in scope and what is out of scope._

deskops/runtime/scion.py, subcomando runtime template en cli/registry.py y cli/commands/runtime.py, tests/test_scion_runtime.py, goldens de help. No lanza scion.

## Implementation Path

_Outline the expected implementation route or affected surface._

commit 3d50831

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_scion_runtime.py
- python -m pytest -q tests/test_output_goldens.py -k help

## Done When

_Name the observable condition that makes the task complete._

Los 10 tests nuevos y los goldens pasan; deskops runtime template role-deskops-executor --harness claude --out DIR escribe los tres archivos.
