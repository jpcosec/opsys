---
id: task-rw-f4-coverage-extractor-decision
status: blocked
references: []
depends_on:
- task-rw-f4-single-snapshot-reader
- task-rw-f5-deprecated-aliases
pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/extract_coverage.py
- tests/test_graph_extract_coverage.py
- deskops/graph/snapshot.py
- tests/test_graph_snapshot.py
- deskops/cli/registry.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f4
- topic:graph
---

# Keep the coverage extractor as an optional report or delete it

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S13: deskops/graph/extract_coverage.py (907 lines) scores matches with fixed thresholds; the tag-overlap (0.65, line 693) and token-overlap (0.60, line 727) scores fall below the 0.70 cutoff at line 636 and can never win; `confidence="high"` is hard-coded at lines 192, 236, 248, 261 and 276 and written into snapshot edge metadata (snapshot.py:226); no deskops code reads it and no gate depends on the extractor.

Plan: phase F4 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

The owner's choice is applied (see Open Ambiguities).

## Scope

_State what is in scope and what is out of scope._

Blocked on the owner decision. The supervisor records the choice under Resolved Decisions and lifts `blocked` when promoting. It runs after the F5 chain (the keep option adds a registry entry, and every F5 task edits deskops/cli/registry.py, created by task-rw-f5-command-registry, an ancestor through task-rw-f5-deprecated-aliases); with the delete option the supervisor may drop that dependency.

## Implementation Path

_Outline the expected implementation route or affected surface._

Delete: remove the module, tests/test_graph_extract_coverage.py, its merge into the snapshot (snapshot.py:75-78) and its entry in `metadata.source_extractors` (snapshot.py:92, asserted by tests/test_graph_snapshot.py:43); update the golden snapshot. Keep: add `deskops graph coverage [--root] [--format text|json]` as a registry entry (task-rw-f5-command-registry) that prints one match per line (text) or a list (json) with fields element_id, atom_id, facet, score, basis, and always exits 0; remove coverage nodes, edges and the extractor entry from `graph build`; drop the two sub-cutoff scorers and the now-dead cutoff at line 636; compute `confidence` from the score (>=0.9 high, else medium).

## Validation

_List the checks required before this task can close._

- pytest tests
- deskops graph build --root .

## Done When

_Name the observable condition that makes the task complete._

Delete: `grep -rn extract_coverage deskops/` is empty. Keep: `deskops graph coverage --help` exits 0 and the snapshot has no coverage nodes. Either way `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

- Owner decision: delete extract_coverage.py, or keep it as an opt-in `deskops graph coverage` report (semantics in Implementation Path)?
