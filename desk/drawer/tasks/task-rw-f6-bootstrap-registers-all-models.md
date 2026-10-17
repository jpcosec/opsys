---
id: task-rw-f6-bootstrap-registers-all-models
status: deferred
references: []
depends_on:
- task-rw-f5-command-registry
pills:
- desk/contexts/pill-006-self-described-store-layout.md
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
files:
- deskops/bootstrap.py
- tests/test_doctor_model_registration.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f6
- topic:models
- topic:bootstrap
---

# Bootstrap registers every deskops model, and only bootstrap/init install sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S9: `MODEL_REFS` in deskops/bootstrap.py lists 12 models while the repo store registers 15 deskops models (plus sldb's RelationTypeDoc and RelationDoc, registered by the lifecycle graph), so a fresh `deskops init` does not register MaterializationContractDoc, RunDoc or RuntimeProfileDoc. `ensure_sldb_available` (bootstrap.py:36-62) can run `pip install -e ../sldb` from `list`, `show` or `add`.

Plan: phase F6 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`MODEL_REFS` stays a `dict[name, 'deskops.models:<Class>']`, built from every `StructuredNLDoc` subclass in `deskops.models.__all__` except the base classes `PrimitiveDoc` and `OperationalArtifactDoc`; a fresh init registers the same 15 deskops models as the repo store; only `bootstrap` and `init` may install sldb; other commands print the existing 'Error: sldb is not installed...' message and exit 1.

## Scope

_State what is in scope and what is out of scope._

In scope: bootstrap.py, its callers' install flag, and two tests (A and B below) in tests/test_doctor_model_registration.py. Out of scope: model contract changes. Importers rely on the dict shape (deskops/cli/commands/desk.py:142, doctor.py:118, domain_tree.py:249-250, tests/test_doctor_model_registration.py:17).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Build MODEL_REFS as described.
2. Add an `allow_install` parameter to `ensure_sldb_available`, true only from bootstrap and init.
3. Test A: `deskops init` in a `tmp_path` repo, then assert `<tmp>/.sldb/core/store_index.yaml` exists and its model-name set equals the set derived from `deskops.models.__all__` minus the two bases, plus `RelationTypeDoc` and `RelationDoc` that the lifecycle graph registers during init (no hard-coded count).
4. Test B (in-process, so monkeypatch works): monkeypatch sldb as not importable and spy on the install runner; `deskops list tasks` prints the error, exits 1, and the spy was not called.

## Validation

_List the checks required before this task can close._

- pytest tests/test_doctor_model_registration.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Tests A and B pass and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
