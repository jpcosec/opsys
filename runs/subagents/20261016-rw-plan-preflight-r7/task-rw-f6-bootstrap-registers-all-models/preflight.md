RESTATEMENT:

1. Read `deskops/bootstrap.py` (lines 14-32, 36-62), `deskops/models/__init__.py` (confirm `__all__` exists and what it contains), and consumers `deskops/cli/commands/desk.py:142`, `deskops/cli/commands/doctor.py:118`, `deskops/cli/domain_tree.py:249-250`, `tests/test_doctor_model_registration.py:17` to confirm the `dict[name, 'deskops.models:<Class>']` contract.
2. Replace the hard-coded 17-entry `MODEL_REFS` literal with a dynamically built dict: iterate `deskops.models.__all__`, `getattr(deskops.models, name)`, keep entries that are classes and `issubclass(cls, StructuredNLDoc)` and `cls is not PrimitiveDoc` and `cls is not OperationalArtifactDoc`, map to `{name: f'deskops.models:{cls.__name__}'}`, preserving dict shape/type.
3. Change `ensure_sldb_available` signature to accept an `allow_install` flag and gate the `pip install -e ../sldb` subprocess on it.
4. Find every caller of `ensure_sldb_available`; pass `allow_install=True` only from the bootstrap and init paths, `False` (or default) everywhere else, including `list`, `show`, `add`.
5. Add Test A in `tests/test_doctor_model_registration.py`: create a throwaway repo under `tmp_path` (using the `_make_repo`/`_cli` pattern from `tests/test_lifecycle_end_to_end.py` or inline git init + seed commit), run `deskops init`, assert `<tmp>/.sldb/core/store_index.yaml` exists, parse it, and assert its model-name set equals the set derived from `deskops.models.__all__` filtered by `StructuredNLDoc` minus `PrimitiveDoc`/`OperationalArtifactDoc` (no hard-coded count).
6. Add Test B in the same file, in-process: call `deskops.cli.main.main(['list', 'tasks'])` under `capsys`; monkeypatch so sldb resolves as not importable; install a spy on the install runner; assert stdout/stderr contains `Error: sldb is not installed`, exit code is 1, and the spy was not called.
7. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.

AMBIGUITIES:

1. The function that consumes `MODEL_REFS` to register store models is never named; unclear how the dict is handed to sldb, so "registers every model" cannot be traced in code.
2. `deskops.models.__all__` contents are assumed; unknown whether the base classes are included in it and whether indirect (non-direct) `StructuredNLDoc` subclasses must be included.
3. Exclusion of `PrimitiveDoc`/`OperationalArtifactDoc` by name vs identity is unspecified.
4. `dict` key semantics: unknown whether the key must equal `cls.__name__` or some other store model name, and whether insertion order matters to consumers.
5. Default value of the new `allow_install` parameter is unspecified.
6. The exact set of callers of `ensure_sldb_available` is not enumerated; "bootstrap and init" vs "list, show, add" may be incomplete.
7. Whether "bootstrap" is a CLI command, a module function, or an internal call site is not stated, so the `True` call sites cannot be pinned.
8. The install runner to spy on in Test B is not named; unknown function/subprocess target to monkeypatch.
9. Mechanism for making sldb "not importable" in Test B is unspecified (sys.modules, `importlib.util.find_spec`, etc.).
10. `store_index.yaml` schema is not given; unknown which field holds model names or how to read them.
11. Whether `deskops init` requires a prior scaffolded `desk/` (per resolved decisions using `desk install`) or runs standalone in an empty tmp repo is unclear.
12. Whether Test A should reuse `_make_repo`/`_cli` from `tests/test_lifecycle_end_to_end.py` (cross-file import) or be self-contained is unspecified.
13. Whether `deskops.cli.main.main` returns an int or raises `SystemExit`, and how "exits 1" is asserted in-process, is unspecified.
14. Test B repo/setup preconditions (does a fresh repo need `init` first) are unspecified.
15. Whether the goal's "same 21 models as the repo store" requires an assertion against the repo's own store, or is purely informational, is unclear.
16. The bound pill `pill-doctor-separates-desk-repair-from-sldb-health` implies doctor behavior, but the task text gives no doctor-specific acceptance criteria.
