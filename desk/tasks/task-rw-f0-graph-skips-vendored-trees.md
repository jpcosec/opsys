---
id: task-rw-f0-graph-skips-vendored-trees
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
- desk/contexts/pill-009-source-file-graph-traceability.md
files:
- deskops/graph/extract_coverage.py
- deskops/graph/extract_sources.py
- tests/test_graph_extract_coverage.py
- tests/test_graph_extract_sources.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-graph-skips-vendored-trees.md
---

# `graph build` ignores tools/, .tmp/ and .venv/

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding X4 (reproduced): `deskops graph build` puts 5 atoms from the untracked `tools/repopackage/` checkout into deskops' graph. Two walkers are involved: deskops/graph/extract_coverage.py excludes by `EXCLUDED_PATH_PARTS` (line 27, matched against any path part by `_is_excluded`, line 895), which lacks `tools` and `.tmp`; deskops/graph/extract_sources.py excludes by `EXCLUDED_DIRS` (lines 15-26), which lacks `tools` and `.tmp`.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

After `deskops graph build --root .`, no node in the snapshot has a path under `tools/` or `.tmp/` (`.venv/` stays excluded).

## Scope

_State what is in scope and what is out of scope._

In scope: adding `tools` and `.tmp` to both exclusion sets (any-path-part matching stays as it is), and one test per extractor. Out of scope: whether the coverage extractor survives the rewrite (task-rw-f4-coverage-extractor-decision).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add `"tools"` and `".tmp"` to `EXCLUDED_PATH_PARTS` in extract_coverage.py and to `EXCLUDED_DIRS` in extract_sources.py.
2. Tests: in tests/test_graph_extract_coverage.py, an atom under `tools/x/desk/atoms/` produces no node; in tests/test_graph_extract_sources.py, a `.py` file under `tools/x/` produces no `source_file:` node.
3. Rebuild and check: `python -m deskops graph build --root .`, then count snapshot nodes whose `semantics.path`, `identity.node_id` (after any `<kind>:` prefix) or any `source.provenance[*].path` starts with `tools/` or `.tmp/` (node layout: deskops/graph/snapshot.py:201-223); the count must be 0.

## Validation

_List the checks required before this task can close._

- pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py
- deskops graph build --root .
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both tests pass and the rebuilt snapshot has zero nodes under `tools/` or `.tmp/`.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
