---
id: task-rw-f1-output-golden-files
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
- desk/contexts/pill-010-graph-runtime-output-policy.md
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
files:
- tests/test_output_goldens.py
- tests/fixtures/golden/
- tests/fixtures/golden_desk/
- tests/conftest.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f1
- topic:contract
- topic:graph
- topic:testing
---

# Golden files pin the graph snapshot, run index, closeout trailers and --help text

## Rationale

_Explain why this task exists or the business driver behind it._

Other tools read deskops outputs: `.sldb/runtime/graphs/deskops.kg.json` (schema `deskops_kgdb_graph_snapshot_v1`) and `deskops.nx.json`, `.sldb/runtime/self_reflection_findings.json`, `runs/subagents/index.jsonl`, and the trailers of closeout commits (`Task-Id`, `Run-Dir`, `Run-Id`, `Session-Sha256`, or `Closeout-Mode`/`Closeout-Reason` for `--no-run`). The CLI rewrite also needs every command's `--help` text pinned.

Plan: phase F1 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Tests compare those outputs, produced from a fixed fixture desk, against committed golden files with volatile values normalized.

## Scope

_State what is in scope and what is out of scope._

In scope: one fixture desk, the golden files listed below, the comparison tests, and a `--update-golden` pytest option. Out of scope: changing any output format.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Fixture desk tests/fixtures/golden_desk/ with 2 tasks, 2 atoms, 1 pill and 1 drawer task.
2. Copy it into `tmp_path`, git init, run `graph build`, `graph reflect` (the only writer of self_reflection_findings.json), a `closeout commit --run-dir` and a `closeout commit --no-run`; normalize timestamps to `<ts>`, absolute paths to `<root>`, commit hashes to `<sha>`.
3. Goldens in tests/fixtures/golden/: `graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (a list of `{route, trailers}` objects), and `help/deskops.txt` for the root plus `help/deskops_<sub>[_<subsub>].txt` for every command path reachable from `deskops --help`.
4. tests/test_output_goldens.py compares; `--update-golden` (registered in tests/conftest.py) rewrites them.

## Validation

_List the checks required before this task can close._

- pytest tests/test_output_goldens.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The golden tests pass, and fail when a key is renamed in the snapshot writer (check by hand, then revert).

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- tests/conftest.py already exists (the lifecycle_desk fixtures); add a `pytest_addoption` for `--update-golden` to it and keep the normalization helpers in tests/test_output_goldens.py.

## Open Ambiguities

None.
