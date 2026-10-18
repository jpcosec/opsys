---
id: task-init-links-federated-models-instead-of-copying
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/bootstrap.py
- deskops/cli/main.py
- deskops/cli/commands/desk.py
- deskops/lifecycle_migration.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- topic:sldb
- topic:models
---

# `deskops init` links the deskops models from their owner store instead of copying them

## Rationale

_Explain why this task exists or the business driver behind it._

sldb is implementing federated models (proposal ../sldb/docs/architecture/model-federation-on-the-graph.md, 2026-10-17, by the sldb agent): a model lives once, in the store that owns it (the deskops repo's `.sldb`), and other stores register an inherited entry that names the owner (`stores add` plus `deskops:TaskDoc`) instead of copying `model_ref` and an absolute `path`. Today `deskops init` copies the 16 deskops models into each new store with `models add`, which is how stores ended up pointing at a deleted checkout (graph_ui's store_index.yaml names /home/jp/proyectos/hum-ecosystem/tools/deskops/...).

## Goal

_Describe the concrete result this task must produce._

A store created by `deskops init` registers the deskops models as federated entries owned by the deskops store, and `deskops desk update --apply` converts an existing store's copied entries to federated ones.

## Scope

_State what is in scope and what is out of scope._

The model registration in bootstrap/init, the conversion in `desk update`, and tests. Out of scope: sldb itself.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. sldb main has it since 0463a9b/9d6cab2/9dbf568 (2026-10-18, announced by sldb-04). On a local store: `sldb.api.link_store(store, owner_store, "deskops")` with `owner_store` = the `.sldb` at the root of the deskops installation (CLI: `sldb stores add <deskops root>/.sldb --name deskops`), then `sldb.api.inherit_model(store, "deskops:<Model>")` for each deskops model the store uses (CLI: `sldb models inherit deskops:<Model>`), then `sldb edges init` (tracks `links_to`, makes `has_model` many_to_many). An inherited model imports from the owner repo's root, so no `--pythonpath` is needed. `models inherit` also converts an existing copy with the same model_ref in place, keeping documents and the signed contract. Read ../sldb/docs/architecture/model-federation-on-the-graph.md and the sldb.api signatures before coding. Replace every `models add` of a deskops model in deskops (bootstrap.py, cli/main.py init, cli/commands/desk.py) with link + inherit. The deskops repo's own store is the owner and keeps its registrations.
2. `desk update --apply` detects copied deskops model entries and converts them with `inherit_model` (in place), idempotently.
3. Tests: a fresh `deskops init` store has no copied `model_ref`/`path` for deskops models and `sldb stores check` passes; a store with copied entries is converted by `desk update --apply`.

## Validation

_List the checks required before this task can close._

- pytest tests
- sldb stores check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

`deskops init` registers no copied deskops model, existing stores convert through `desk update --apply`, and `pytest tests` is green.

## Resolved Decisions

- Requested by the SLDB_1 coordinator on 2026-10-18: register now, execute when sldb publishes federated models.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
