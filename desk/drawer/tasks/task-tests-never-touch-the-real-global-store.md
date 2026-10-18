---
id: task-tests-never-touch-the-real-global-store
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- tests/conftest.py
- deskops/bootstrap.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:testing
- topic:sldb
---

# The test suite never writes to the user's real `~/.sldb`

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18. `pytest tests` modifies `/home/jp/.sldb/core/store_index.yaml`, the user's global store: `deskops init` and `bootstrap` run `ensure_global_store_and_models` against `Path.home() / ".sldb"`, and tests spawn them without an isolated HOME. One worktree run of task-init-links-federated-models-instead-of-copying left the global store's `deskops` link pointing at a temporary worktree (`../../tmp/rw/wt/federated/.sldb`). The supervisor backed up the file (/tmp/rw/global-store_index.yaml.bak) and repaired the link by hand to /home/jp/proyectos/SLDB_1/deskops/.sldb. The next suite run then inherited three more models into it (MaterializationContractDoc, RunDoc, RuntimeProfileDoc). task-rw-f6-bootstrap-registers-all-models (66f81ff) stops overwriting a link that points elsewhere, but tests still write there. Only tests/test_doctor_model_registration.py isolates HOME.

## Goal

_Describe the concrete result this task must produce._

Running `pytest tests` leaves `~/.sldb` byte-identical.

## Scope

_State what is in scope and what is out of scope._

In scope: an autouse fixture in tests/conftest.py, and any test or subprocess env that bypasses it. Out of scope: changing where deskops keeps its global store at runtime.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Autouse fixture in tests/conftest.py: `monkeypatch.setenv("HOME", str(tmp_path_factory.mktemp("home")))`, set once per test. Subprocesses inherit the environment. Check that `Path.home()` and `os.path.expanduser` honor it, and that git still finds a user identity: write a minimal `.gitconfig` with user.name and user.email into the fake HOME, or set `GIT_AUTHOR_*` and `GIT_COMMITTER_*`.
2. Find code that reads the global store some other way (`grep -rn "home()\|expanduser\|\.sldb" deskops/bootstrap.py deskops/cli`) and make sure the fixture covers it.
3. Guard test: run a representative subset (`deskops init` in a sandbox), record a hash of the real `~/.sldb/core/store_index.yaml` before and after, and assert they are equal. Use the real home taken from `pwd.getpwuid(os.getuid()).pw_dir`, not `HOME`.

## Validation

_List the checks required before this task can close._

- sha256sum ~/.sldb/core/store_index.yaml before and after `pytest tests` (equal)
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The real global store index is byte-identical before and after the full suite, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
