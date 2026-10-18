---
id: task-rw-f1-cli-contract-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
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
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
files:
- tests/test_cli_contract.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f1-cli-contract-tests.md
---

# Every CLI surface without a test gets one through main(argv)

## Rationale

_Explain why this task exists or the business driver behind it._

The rewrite must not change the CLI. These subcommands have no test through `main` today (checked 2026-10-16 by grepping tests/): `add faq-doc`, `atoms list`, `atoms show`, and `runtime init|status|attach|stop|supervise` (deskops/cli/parser.py:67-89). Already covered and out of this task: `add board|ritual|step` (tests/test_cli.py), `closeout commit` (tests/test_closeout.py), `bind pill` (tests/test_cli.py:1124), `atoms type` (tests/test_domain_tree.py:104) and `runtime workers` (tests/test_cli.py:2402).

Plan: phase F1 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Each listed subcommand has one in-process test that calls `deskops.cli.main.main([...])` inside a sandbox repo and asserts the exit code and one stable line of output.

## Scope

_State what is in scope and what is out of scope._

In scope: new tests only, one test per subcommand (parametrize where the shape repeats). Out of scope: fixing what the tests reveal: record each surprise as a new drawer task file and mark its test `pytest.mark.xfail(strict=True, reason='<task id>')`. `runtime` tests must not start Herdr: stub the Herdr client the way tests/test_herdr_runtime.py does.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. tests/test_cli_contract.py using the `lifecycle_desk` fixture from tests/conftest.py (a sandbox repo as `deskops init` leaves it).
2. One test per subcommand listed in Rationale, calling `main([...])` with `--root <sandbox>`, capturing stdout/stderr via `capsys`.
3. These tests call `main` in-process (like tests/test_cli.py:1124), not through a subprocess; the sandbox repo is still built as described in Resolved Decisions.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli_contract.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Each of the 8 uncovered subcommands named in Rationale has its own test (a strict xfail tied to a new drawer task counts), and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
