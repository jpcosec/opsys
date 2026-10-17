RESTATEMENT:
1. Open `deskops/bootstrap.py`; locate `MODEL_REFS` and `ensure_sldb_available` (lines ~36-62).
2. Inspect `deskops.models.__all__` to enumerate every `StructuredNLDoc` subclass and identify the base classes `PrimitiveDoc` and `OperationalArtifactDoc`.
3. Rebuild `MODEL_REFS` at import time as a `dict[name, 'deskops.models:<Class>']`, including every `StructuredNLDoc` subclass from `__all__` except the two bases.
4. Confirm the dict-shape consumers still resolve: `deskops/cli/commands/desk.py:142`, `doctor.py:118`, `domain_tree.py:249-250`, `tests/test_doctor_model_registration.py:17`.
5. Add an `allow_install` parameter (default false) to `ensure_sldb_available`; gate the `pip install -e ../sldb` call on it.
6. When install is not allowed and sldb is missing, print the existing `'Error: sldb is not installed...'` message and exit 1.
7. Update call sites so only `bootstrap` and `init` pass `allow_install=True`; leave `list`, `show`, `add` (and any other callers) false.
8. Test A in `tests/test_doctor_model_registration.py`: build a throwaway repo in `tmp_path` (git init, one empty seed commit; use `_make_repo`/`_cli` from `tests/test_lifecycle_end_to_end.py` or the `lifecycle_desk` fixture), run `python -m deskops init <root>` via subprocess with `cwd=root`.
9. Test A assertions: `<root>/.sldb/core/store_index.yaml` exists; parse it; model-name set equals the set derived from `deskops.models.__all__` minus `PrimitiveDoc` and `OperationalArtifactDoc` (no hard-coded count).
10. Test B in-process: monkeypatch sldb as not importable, spy on the install runner, call `deskops.cli.main.main(['list','tasks'])` with `capsys`; assert the error message prints, exit is 1, and the spy was not called.
11. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.

AMBIGUITIES:
1. `init`'s implementation module is not named in `files:` (only `bootstrap.py` and the test file), so the location to pass `allow_install=True` must be guessed.
2. The `allow_install` default is not stated explicitly; I inferred default false.
3. The install runner's exact symbol to spy on in Test B is not named.
4. "Monkeypatch sldb as not importable" mechanism is unspecified (`sys.modules['sldb']=None` vs import hook).
5. Whether `main([...])` returns an int, raises `SystemExit`, or both, and how Test B should assert exit 1, is unspecified.
6. `MODEL_REFS` key convention is unspecified: SLDB model `name` attribute vs class name, and how that maps to the names in `store_index.yaml`.
7. Which attribute of `store_index.yaml` holds model names, and how to parse it, is unspecified.
8. How to derive the expected model-name set from `__all__` (attribute vs class name, and whether `__all__` contains non-`StructuredNLDoc` entries) is unspecified.
9. The full list of `ensure_sldb_available` call sites that must pass `allow_install=False` is not enumerated.
10. Test A says "`deskops init` in a `tmp_path` repo" but not whether to use subprocess helpers or the `lifecycle_desk` fixture.
11. Whether tests A/B are added to the existing `tests/test_doctor_model_registration.py` and whether its existing tests/`MODEL_REFS` import need updating is not stated.
12. Task `status: deferred` / `source:drawer`; task text does not contradict the Resolved Decision that the supervisor promotes before dispatch.
