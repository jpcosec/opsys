RESTATEMENT:
1. Read `deskops/bootstrap.py`: current `MODEL_REFS` (~lines 14-32, 17 entries), `ensure_sldb_available` (~36-62), and every call site of `ensure_sldb_available`.
2. Read `deskops/models.py` `__all__`; confirm which entries are `StructuredNLDoc` subclasses and that `PrimitiveDoc` and `OperationalArtifactDoc` are the only bases to exclude.
3. Inspect importers relying on dict shape: `deskops/cli/commands/desk.py:142`, `deskops/cli/commands/doctor.py:118`, `deskops/cli/commands/domain_tree.py:249-250`, `tests/test_doctor_model_registration.py:17`.
4. Rewrite `MODEL_REFS` as `dict[name, 'deskops.models:<Class>']` covering every `StructuredNLDoc` subclass in `__all__` except `PrimitiveDoc` and `OperationalArtifactDoc` (target 21 entries).
5. Add `allow_install` param to `ensure_sldb_available`; default False; pass True only from bootstrap and init call paths.
6. Update callers so non-bootstrap/init commands do not install: they print the existing `'Error: sldb is not installed...'` message and exit 1.
7. In `tests/test_doctor_model_registration.py`, add Test A copying `_make_repo`/`_cli` from `tests/test_lifecycle_end_to_end.py`: build tmp_path repo, run `deskops init`, assert `<tmp>/.sldb/core/store_index.yaml` exists and its model-name set equals the set from `deskops.models.__all__` minus the two bases (no hard-coded count).
8. Add Test B: monkeypatch sldb as not importable, spy on the install runner, run `deskops list tasks`, assert the error is printed, exit code 1, and the spy was not called.
9. Run `pytest tests/test_doctor_model_registration.py` then `pytest tests`.

AMBIGUITIES:
1. Scope says "one test" but Implementation Path defines Test A and Test B (two tests).
2. "bootstrap and init" are not mapped to concrete functions/commands; which call sites set `allow_install=True` must be guessed.
3. The "install runner" to spy on is unnamed (no function/module given).
4. Exact text/location of the existing `'Error: sldb is not installed...'` message is not given (only prefix).
5. `MODEL_REFS` key derivation (class name vs suffix-stripped name) is unspecified; must match the existing convention.
6. Schema of `.sldb/core/store_index.yaml` and how to extract its model-name set are unspecified.
7. How to make sldb "not importable" (sys.modules, importlib, env) is unspecified.
8. Whether `MODEL_REFS` must be a static literal of 21 entries or computed dynamically from `__all__` is not stated.
9. Done When names only "the fresh-init test", while Implementation Path requires both Test A and Test B.
10. Whether Test B lives in `tests/test_doctor_model_registration.py` (the only test file listed) or elsewhere is not stated.
11. `deskops init` and `deskops list tasks` exact subcommand syntax/being valid CLI forms is assumed, not verified in the task.
