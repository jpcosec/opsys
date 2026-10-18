---
id: task-graph-uses-sldb-graph-api-instead-of-kgdb
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
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- pyproject.toml
- deskops/cli/main.py
- deskops/graph/snapshot.py
- tests/test_graph_snapshot.py
- tests/test_graph_cli.py
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- runs/planning/rewrite-plan/gen.py
- runs/planning/deskops-rewrite-inventory.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-graph-uses-sldb-graph-api-instead-of-kgdb.md
---

# deskops reads and validates graphs through sldb, with no kgdb dependency

## Rationale

_Explain why this task exists or the business driver behind it._

Owner correction (2026-10-18, through the SLDB_1 coordinator): kgdb no longer exists as a project. Its graph layer was merged into sldb (sldb merge 6deb222, ADR 2026-09-20). The public API is `sldb.api.graph.snapshot` (`snapshot_load`, `GraphSnapshot`), with `load_graph`/`save_graph` in `sldb.store.graph.graph_io`. The kgdb 0.1.0 in the anaconda base environment is a leftover and must not be a dependency. task-rw-f0-declare-runtime-dependencies (closed in 9b56113) added `"kgdb>=0.1.0"` to pyproject.toml on a false premise. Today deskops still imports kgdb in deskops/cli/main.py:251-252 (`from kgdb.graph import load_graph, save_graph`), deskops/graph/snapshot.py:119 (`from kgdb.contracts.io import GraphSnapshot`, with the error text "install kgdb before running `deskops graph build`") and tests/test_graph_snapshot.py:6. The supervisor checked that `sldb.store.graph.snapshot.GraphSnapshot.model_validate` accepts the current deskops snapshot (539 nodes) and that `sldb.store.graph.graph_io.load_graph`/`save_graph` round-trip it.

## Goal

_Describe the concrete result this task must produce._

No deskops code, test or packaging metadata imports or declares kgdb. `deskops graph build` validates and writes through sldb, and in a fresh venv without kgdb `pytest tests` passes and `deskops graph build` works.

## Scope

_State what is in scope and what is out of scope._

In scope:
- remove `"kgdb>=0.1.0"` from pyproject.toml;
- the three import sites and their tests (tests/test_graph_snapshot.py, and tests/test_graph_cli.py:165 `test_graph_build_reports_missing_kgdb_capability`, which simulates kgdb missing; rewrite it to simulate the sldb graph API being unavailable, or delete it if that path no longer exists);
- the correction notes listed in Implementation Path.

Out of scope:
- snapshot format identifiers such as `deskops_kgdb_graph_snapshot_v1`, `deskops_kgdb_snapshot_v1`, `desk_kgdb_coverage_v1` and the `.kgdb.json` suffixes. They are output contract that the F1 goldens pin; renaming them is separate work.
- historical prose in desk/drawer/.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. pyproject.toml: delete the `"kgdb>=0.1.0",` line; change nothing else.
2. deskops/graph/snapshot.py `_validate_graph_snapshot`: `from sldb.api.graph.snapshot import GraphSnapshot`. If that import fails, raise `GraphSnapshotCapabilityError` with a message that names sldb (for example "sldb graph API unavailable (sldb.api.graph.snapshot); upgrade structuredLanguageDB"), not kgdb.
3. deskops/cli/main.py graph build: replace the kgdb imports with `from sldb.api.graph.snapshot import snapshot_load` and `from sldb.store.graph.graph_io import save_graph`, and call `save_graph(snapshot_load(output_path), networkx_path_for_snapshot(output_path))`.
4. tests/test_graph_snapshot.py: import `GraphSnapshot` from `sldb.api.graph.snapshot`; update tests/test_graph_cli.py:165 as described in Scope.
5. `grep -rn "kgdb" --include=*.py deskops tests | grep -v "_kgdb_\|kgdb_graph_snapshot\|kgdb_snapshot\|kgdb_coverage\|\.kgdb\.json\|integrate-kgdb\|write-kgdb"` returns nothing. Function and identifier names may stay. Any remaining `import kgdb` or `from kgdb` fails this step.
6. Rewrite desk/contexts/pill-008-kgdb-sldb-boundary.md to the current boundary: the graph layer is part of sldb (`sldb.api.graph`), deskops builds its snapshot and validates it with sldb's `GraphSnapshot`, and there is no kgdb dependency. Keep the file name (other documents link it); fix the title, What, Why, When and How, and drop the `system:kgdb` tag.
7. runs/planning/rewrite-plan/gen.py: in the declare-runtime-dependencies entry, record that it was a false premise and that kgdb was dropped by this task (the generator is frozen, so fix the text only). In runs/planning/deskops-rewrite-inventory.md, add a short note under Estado. Add runs/subagents/20261017-task-rw-f0-declare-runtime-dependencies/correction.md saying the same.
8. Fresh venv check:
   - `python -m venv /tmp/rw/f0/venv-nokgdb`;
   - `/tmp/rw/f0/venv-nokgdb/bin/pip install /home/jp/proyectos/SLDB_1/sldb -e . pytest pytest-asyncio` (add the other test plugins that tests/ needs, if any);
   - confirm `python -c "import kgdb"` fails there;
   - then, from this worktree, run `/tmp/rw/f0/venv-nokgdb/bin/python -m pytest tests -q` and `/tmp/rw/f0/venv-nokgdb/bin/python -m deskops graph build --root .`.
   Use PYTHONPATH=<worktree>, as for every run.

## Validation

_List the checks required before this task can close._

- pytest tests/test_graph_snapshot.py tests/test_graph_cli.py
- deskops graph build --root .
- pytest tests
- the step 8 fresh-venv run (pytest tests and graph build, kgdb absent)

## Done When

_Name the observable condition that makes the task complete._

The step 5 grep is empty, pyproject has no kgdb, and the fresh venv without kgdb runs `pytest tests` green and `deskops graph build` exit 0.

## Resolved Decisions

- Owner decision (2026-10-18): kgdb is gone; use sldb's graph API.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
