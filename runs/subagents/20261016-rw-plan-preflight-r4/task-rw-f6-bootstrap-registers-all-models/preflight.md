RESTATEMENT:
1. Read `deskops/bootstrap.py`: current `MODEL_REFS` (lines 14–32), `ensure_sldb_available` (36–62), and its callers.
2. Rebuild `MODEL_REFS` as `dict[name, 'deskops.models:<Class>']` covering every `StructuredNLDoc` subclass in `deskops.models.__all__`, excluding `PrimitiveDoc` and `OperationalArtifactDoc` (target 21 entries).
3. Add an `allow_install` parameter to `ensure_sldb_available`; guard the `pip install -e ../sldb` path with it (default presumably `False`).
4. Set `allow_install=True` from bootstrap and init; leave list/show/add at the non-installing path.
5. Add Test A to `tests/test_doctor_model_registration.py`: build a throwaway repo via `_make_repo`/`_cli` helpers, run `python -m deskops init` in `tmp_path`, assert `<tmp>/.sldb/core/store_index.yaml` exists, derive expected set from `deskops.models.__all__` minus the two bases, assert store model-name set equals it (no hard-coded count).
6. Add Test B: monkeypatch sldb as unimportable, spy on the install runner, run `deskops list tasks`, assert the 'Error: sldb is not installed...' message prints, exit code is 1, and the spy was not called.
7. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.

AMBIGUITIES:
1. Whether `MODEL_REFS` should be built dynamically at import time (introspection over `deskops.models.__all__`) or remain a static literal that happens to match — "built from every subclass" reads both ways; Test A passes trivially under dynamic construction.
2. Which objects count as `StructuredNLDoc` subclasses: filter by `issubclass` over imported `__all__` entries, or by the two named bases only? Behavior for any other abstract/intermediate class is unspecified.
3. "bootstrap and init" as install-enabled callers: exact call graph unknown — is `bootstrap` a function that `init` calls (making the init flag redundant), and where does the top-level `deskops init` entrypoint live? Files list only `bootstrap.py`, but Scope says "its callers' install flag", so caller files may need edits not in the files list (contradiction).
4. Test B requires monkeypatching, which cannot cross a `subprocess.run` boundary, yet Resolved Decisions default to subprocess unless the task says "in-process" (it does not). Contradicts.
5. No install-runner function is named; "spy on the install runner" implies extracting `pip install -e ../sldb` into a patchable unit — its name, signature, and assertion target are unspecified.
6. Exact command spelling for Test B: `deskops list tasks` vs `deskops tasks list` (inventory mentions `list`, `show`, `add`); not fixed.
7. Exact error string to assert: text is elided as 'Error: sldb is not installed...' — exact-match vs prefix-match is unspecified, and the real message may differ.
8. Exact store-index path/filename assumed: `<tmp>/.sldb/core/store_index.yaml`; not verified against current layout, and the key/field within it that holds model names is unspecified.
9. `deskops init` in a fresh `tmp_path` repo: whether it prompts (install, git hooks, overwrite) and needs flags like `--force`/`--yes` is unknown; a prompt would hang the test.
10. Whether `init` needs a commit or additional setup before `.sldb/core/store_index.yaml` appears is unspecified (Resolved Decisions only say files are untracked until the test commits them).
11. Deriving "model-name set" from `deskops.models.__all__`: mapping from `__all__` attribute names to store model names and handling of non-class `__all__` entries is undefined.
12. "same 21 models as the repo store" is stated as a fact; unclear whether any test must assert equality against the repo's own `.sldb` or run `sldb stores check`, or whether 21 is only descriptive (Done When mentions only Tests A/B and `pytest tests`).
13. Default value and type of `allow_install` (bool default `False`) is implied but not stated.
14. Whether `_make_repo`/`_cli` must be imported from `tests/test_lifecycle_end_to_end.py` or duplicated locally is unspecified.
15. Invocation form (`python -m deskops init` vs `deskops init`) and whether top-level `init` exists as a command are not explicitly confirmed by the task text.
