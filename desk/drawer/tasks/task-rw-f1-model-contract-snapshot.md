---
id: task-rw-f1-model-contract-snapshot
status: deferred
references: []
depends_on:
- task-rw-f0-closeout-amends-only-its-own-commit
- task-rw-f0-reject-ambiguous-selectors
- task-rw-f0-merge-retarget-whole-tokens
- task-rw-f0-closeout-commit-pathspec
- task-doctor-crashes-on-deskless-roots
- task-rw-f0-declare-runtime-dependencies
- task-rw-f0-graph-skips-vendored-trees
- task-rw-f0-pytest-collects-only-tests
- task-rw-f0-payload-from-drawer-resolves
pills:
- desk/contexts/pill-006-self-described-store-layout.md
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
files:
- tests/test_model_contract_snapshot.py
- tests/fixtures/model_contract_hashes.json
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f1
- topic:contract
- topic:testing
---

# A test pins the sldb contract hash of every deskops model

## Rationale

_Explain why this task exists or the business driver behind it._

24 stores on this machine track TaskDoc. sldb hashes each model's contract with `hash_model_contract` (../sldb/src/sldb/store/hashing.py:80, over field schemas with descriptions, `__template__`, `__family__`, semantics, base names, `__references__`, `__containment__`, `__compositions__`). An accidental change during the rewrite puts every one of those stores in FAIL, and nothing in deskops detects it today.

Plan: phase F1 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

A test fails, naming the model, whenever a deskops model's contract hash differs from a committed snapshot, or when a model is added to or removed from the registered set.

## Scope

_State what is in scope and what is out of scope._

In scope: one test module and its fixture. Out of scope: changing any model (F6). Import `sldb.store.hashing.hash_model_contract`; it is public by name although it is outside `sldb.api`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. The model set is `deskops.bootstrap.MODEL_REFS` (a dict name -> `module:Class`) united with the model names listed in `.sldb/core/store_index.yaml`; import each class from its `model_ref` (the MODEL_REFS value, or the store index's `model_ref`; RelationTypeDoc and RelationDoc are `sldb.models.*` classes registered by the lifecycle graph and are snapshotted too).
2. Fixture tests/fixtures/model_contract_hashes.json is a flat JSON object `{"<ModelName>": "<sha256 hex>"}` with sorted keys.
3. tests/test_model_contract_snapshot.py asserts the fixture's key set equals the discovered set (listing missing and extra names) and each hash matches (listing changed names). The failure message says a change requires a store migration (task-rw-f6-migrate-tracking-stores) and prints the new hashes so the fixture can be updated deliberately.
4. Generate the fixture once from the current code.

## Validation

_List the checks required before this task can close._

- pytest tests/test_model_contract_snapshot.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The test passes on the current code, and fails naming the model when a TaskDoc field description is edited locally (check by hand, then revert).

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
