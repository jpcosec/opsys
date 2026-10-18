---
id: task-message-delivery-resolves-unregistered-desks
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
- deskops/cli/commands/message.py
- deskops/identity.py
- tests/test_message_delivery.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `message send` and `message ack` work when the target desk does not register the sender or itself

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 while routing the store migration findings, and confirmed by the coordinator as deskops work. `deskops message send --root <repo>` failed in two repos. In /home/jp/Upla/paper_IEEE: "Desk config project_identity is not established (found unknown-project)". In /home/jp/proyectos/TraderBot, both without `--from` ("Unable to resolve sender identity") and with `--from deskops` ("Repository id deskops not found in registry at <target>/desk/registry (found: TraderBot)"). The supervisor had to deliver both notes by hand. sldb-04 reported a related failure: once sldb created a local desk/registry to register graph_ui, `message ack` in sldb stopped finding `sldb` itself until it registered itself too.

## Goal

_Describe the concrete result this task must produce._

A note can always be delivered and acknowledged. The sender identity comes from the sender's own desk config or registry, never from the target's registry. A target desk without project_identity takes its id from the directory name, with a warning. `ack` falls back to the repo's own desk config when a local registry does not list the repo itself.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/message.py and deskops/identity.py (sender and target resolution), tests for the three failure cases. Out of scope: rewriting other repos' configs.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce each case in a sandbox: a target with no project_identity; a target whose registry lists only itself, with and without --from; a repo whose local registry does not list itself, followed by `ack`. 2. Resolve the sender from the sending repo (cwd or --from checked against the sender's registry or config), not the target's. 3. For a target without project_identity, use the directory name and warn. 4. For ack, fall back to desk/config.json project_identity. 5. Tests in tests/test_inbox_promote_cli_gaps.py or a new tests/test_message_delivery.py.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_message_delivery.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The three cases deliver or acknowledge in tests, and `pytest tests` is green.
