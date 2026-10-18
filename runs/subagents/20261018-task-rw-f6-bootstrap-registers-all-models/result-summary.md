# Result summary — task-rw-f6-bootstrap-registers-all-models

## Changed

- `deskops/bootstrap.py`
  - `MODEL_REFS` is now derived from `deskops.models.__all__`: every `StructuredNLDoc`
    subclass except `PrimitiveDoc` and `OperationalArtifactDoc` maps to
    `deskops.models:<Class>` (currently 15 entries, includes `MaterializationContractDoc`,
    `RunDoc`, `RuntimeProfileDoc`).
  - `SLDBBootstrap.ensure_sldb_available(allow_install: bool = False)`: installs sldb only
    when `allow_install=True`; otherwise prints
    `Error: sldb is not installed. Run 'deskops bootstrap' or 'deskops init' to install it.`
    and returns 1 without resolving a checkout or running pip.
  - `SLDBBootstrap.ensure_machine_ready()` passes `allow_install=True` (only `bootstrap`
    and `init` reach it).
  - `SLDBBootstrap._ensure_owner_link()` now verifies that an existing `deskops` link
    resolves to the current owner store. If it points to a different (stale) store it
    returns `None`; `_register_models()` then prints a warning, skips registration for
    that store, and lets init continue. sldb has no public unlink/replace-link API.
- `tests/test_doctor_model_registration.py`
  - Added `test_init_registers_every_deskops_model` (Test A): subprocess
    `python -m deskops init` in a throwaway git repo with isolated `HOME`; asserts
    `.sldb/core/store_index.yaml` exists and its model-name set equals
    `set(deskops.models.__all__) - {PrimitiveDoc, OperationalArtifactDoc}` plus
    `RelationTypeDoc` and `RelationDoc` (17 names; no hard-coded count).
  - Added `test_non_bootstrap_command_does_not_install_sldb` (Test B, in-process):
    patches `_sldb_importable` to false and `_resolve_sldb_checkout` to a fake path,
    spies on `_run`, then asserts `deskops list tasks` exits 1, prints
    `Error: sldb is not installed`, and never calls the install runner.

## Validation

- `PYTHONPATH=/tmp/rw/wt/bootall python -m pytest tests/test_doctor_model_registration.py`
  - `6 passed in 19.14s`
- `PYTHONPATH=/tmp/rw/wt/bootall python -m pytest tests -q`
  - `412 passed, 3 skipped in 359.31s (0:05:59)`
- `PYTHONPATH=/tmp/rw/wt/bootall python -c "from deskops.bootstrap import MODEL_REFS; print(len(MODEL_REFS))"`
  - `15`

### Against the unfixed code

Temporarily restored `deskops/bootstrap.py` from `HEAD` (test file kept new) and ran:

- `PYTHONPATH=/tmp/rw/wt/bootall python -m pytest tests/test_doctor_model_registration.py::test_init_registers_every_deskops_model tests/test_doctor_model_registration.py::test_non_bootstrap_command_does_not_install_sldb -q`
  - `2 failed in 5.67s`
  - Test A failed because the fresh store lacked `MaterializationContractDoc`,
    `RuntimeProfileDoc` and `RunDoc`.
  - Test B failed because the old `ensure_sldb_available` ran
    `pip install -e <fake checkout>` (the spy was called) and exited 3.
- Fixed file was restored immediately after (`git diff --stat` shows only the two intended files).

## Task points that were wrong or ambiguous

- The cited `bootstrap.py:36-62` line range is stale; the function now starts around line 38
  after the derived `MODEL_REFS`.
- The task says the repo store has 15 deskops models. Correct: 15 deskops models plus
  `RelationTypeDoc`/`RelationDoc`, i.e. 17 entries in `.sldb/core/store_index.yaml`.
- Test A needed an isolated `HOME`; otherwise `init` registers models in the real
  `~/.sldb` of the test runner.
- Test B as literally described would have passed on the unfixed code in this environment
  (no sibling checkout existed, so the old code printed the no-checkout error without
  calling `_run`). I also patched `_resolve_sldb_checkout` to a fake path so the test
  actually detects an install attempt.
- `ensure_sldb_available` keeps the no-argument call in `deskops/cli/main.py`, so existing
  monkeypatched `lambda self: 0` stubs keep working; `allow_install` defaults to false.

## sldb issue observed (not fixed)

A stale store link from a previous worktree run remains in the real global store:

- File: `/home/jp/.sldb/core/store_index.yaml`
- Entry: `- name: deskops` → `path: ../../tmp/rw/wt/federated/.sldb` (target no longer exists)
- Command/output that exposed it (before the bootstrap guard):
  - `python -m deskops init <tmp repo>`
  - `Inheriting MaterializationContractDoc in /home/jp/.sldb...`
  - `Error: No store is linked as 'deskops' (see sldb stores add).`
- sldb has no public API to unlink or replace an existing link:
  `sldb.api.link_store` → `record_store_link` calls `_check_store_linked`, which raises
  `Store '<name>' already linked.`; there is no `unlink_store`/`remove_store` export and
  `sldb stores add` has no `--force`.
