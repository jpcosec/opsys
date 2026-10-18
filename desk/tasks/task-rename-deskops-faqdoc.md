---
id: task-rename-deskops-faqdoc
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f6-apply-store-migration
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/models/faq.py
- deskops/models/__init__.py
- deskops/bootstrap.py
- tests/fixtures/model_contract_hashes.json
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rename-deskops-faqdoc.md
---

# deskops' FAQ model gets its own name instead of `FAQDoc`

## Rationale

_Explain why this task exists or the business driver behind it._

sldb-04 reported on 2026-10-18 that the deskops store registers `FAQDoc` as `deskops.models:FAQDoc`, while sldb has its own `FAQDoc` (`docs.models:FAQDoc`). With federated models there is one graph node per model name, so the two get mixed and `sldb stores check` warns. sldb's rule: to override or specialize a model, use a subclass with its own name (recorded as `extends`), never the same name.

## Goal

_Describe the concrete result this task must produce._

The deskops FAQ model has a distinct name (for example `DeskFAQDoc`), and every store that tracks FAQ documents with the old name is migrated, with `sldb stores check` PASS.

## Scope

_State what is in scope and what is out of scope._

In scope:
- the model class and its exports;
- MODEL_REFS;
- the contract-hash fixture;
- the store migration of tracked FAQ documents in this repo's store and in the stores that task-rw-f6-migrate-tracking-stores discovers.

Out of scope: sldb's FAQDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Rename the class, keeping fields and template, so documents stay byte-identical.
2. Re-register the model under the new name in each store. Use sldb's model rename or move if sldb.api has one; otherwise register the new name, retrack the FAQ documents under it, and remove the old one. Do the same in other stores through the F6 migration script.
3. Update the hash fixture.

## Validation

_List the checks required before this task can close._

- pytest tests
- sldb stores check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

No store registers `deskops.models:FAQDoc` under the name `FAQDoc`, `sldb stores check` passes, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
