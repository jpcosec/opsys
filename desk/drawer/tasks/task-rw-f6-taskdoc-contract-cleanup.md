---
id: task-rw-f6-taskdoc-contract-cleanup
status: blocked
references: []
depends_on:
- task-rw-f6-bootstrap-registers-all-models
- task-rw-f4-graph-on-sldb-edge-index
- task-rw-f1-model-contract-snapshot
pills:
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
- desk/contexts/pill-006-self-described-store-layout.md
files:
- deskops/models/task.py
- tests/fixtures/model_contract_hashes.json
- tests/test_graph_declared_edges.py
- runs/planning/taskdoc-unknown-keys.md
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f6
- topic:models
- topic:contract
---

# TaskDoc contract cleanup

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S10, in deskops/models/task.py (afdec7f already dropped `routine` and `checklists` and pointed `current_node` at RitualDoc): TaskDoc sets `extra: allow`; the `frontmatter` field (`exclude=True`) is repopulated by `render_payload` from a hand-kept body-field list, the only deskops model using the dict-frontmatter template marker; `from_drawer` sits in `__references__` although it is provenance; and the `_omit_unset_from_drawer` docstring claims that omitting an empty `from_drawer` kept the contract hash stable, which is false (the field itself is hashed).

Plan: phase F6 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

TaskDoc uses `extra: ignore`, drops the `frontmatter` field, its `_merge_frontmatter` validator and the `render_payload` override, declares each frontmatter field with its own template marker (as PillDoc does), keeps `from_drawer` as a plain field outside `__references__`, and the docstring says it keeps documents byte-identical, not the contract hash; tests/fixtures/model_contract_hashes.json is updated deliberately.

## Scope

_State what is in scope and what is out of scope._

Blocked on the owner deciding that F6 enters this cycle. The store migration is task-rw-f6-migrate-tracking-stores. `PROVENANCE_FIELDS` in deskops/graph/extract_edges.py stays: it also stops the line scanner from reading the `from_drawer` path (lines 340-346).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Before changing the model, save `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` for every file in desk/tasks/*.md and desk/drawer/tasks/*.md except Board.md, and every task file in the golden fixture desk (the round trip used in tests/test_composition.py:66).
2. Pre-scan the stores found by task-rw-f6-migrate-tracking-stores' discovery rule for TaskDoc files with top-level frontmatter keys not in `TaskDoc.model_fields` (null values count) and list them in runs/planning/taskdoc-unknown-keys.md; with `extra: ignore` those keys are dropped, so those files are exempt from the byte-identical check and handled by the migration task.
3. Change the model. Removing `from_drawer` from `__references__` drops the frontmatter `from_drawer` edge (deskops/graph/extract_edges.py:181-190); update tests/test_graph_declared_edges.py:131 to expect no edge.
4. Run tests/test_model_contract_snapshot.py and copy the printed TaskDoc hash into the fixture.
5. Re-render and compare with step 1; every file not listed in step 2 must be byte-identical.

## Validation

_List the checks required before this task can close._

- pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py
- deskops graph missing --root .
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`pytest tests` is green with the updated fixture and every TaskDoc not listed in runs/planning/taskdoc-unknown-keys.md renders byte-identically.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

- Owner decision: does F6 (TaskDoc contract change plus migrating the 24 stores that track it) enter this cycle, or is it postponed?
