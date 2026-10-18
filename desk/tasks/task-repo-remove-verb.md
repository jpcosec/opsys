---
id: task-repo-remove-verb
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
- deskops/cli/commands/repo.py
- deskops/cli/registry.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops repo remove` takes a repository out of the registry so it can be registered again

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. graph_ui registered itself as `graph-ui` in its own desk/registry, while desk/config.json and the sldb and deskops registries say `graph_ui`. deskops now refuses writes to that desk ("Desk config project_identity graph_ui disagrees with registry root match graph-ui"), and spec2viz's note bounced. The CLI has no fix. `edit repository id` answers "Cannot edit immutable field id". `repo register graph_ui <path> --id graph_ui` answers "root already registered as graph-ui". There is no remove or rename verb.

## Goal

_Describe the concrete result this task must produce._

`deskops repo remove <id> --root <repo>` deletes desk/registry/repo-<id>.md, untracks its RepositoryDoc, and prints the path. Afterwards `repo register` can add the entry again under the right id. A missing id exits 1 with the ids that do exist.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/repo.py, deskops/cli/registry.py (register `repo remove` with mutates=True), the help goldens, tests. The removal goes through deskops/doc_io.py (transaction plus untrack). Out of scope: editing ids in place.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Resolve the registry entry by id, file stem, or repo-<id>. 2. Untrack its RepositoryDoc and delete the file in one DocTransaction. 3. Register the CLI verb and update the help goldens with --update-golden. 4. Tests: register graph-ui, remove it, register graph_ui at the same path, and check that `repo whoami` (or message target resolution) agrees with desk/config.json. Also a missing id exits 1.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_repo_identity.py tests/test_registry_robustness.py tests/test_command_registry.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The remove-then-register test passes, and `pytest tests` is green.
