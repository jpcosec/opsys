RESTATEMENT:

1. Read `deskops/bootstrap.py`: locate `MODEL_REFS` and `ensure_sldb_available` (lines ~36-62), and read `deskops.models.__all__`.
2. Grep for callers of `ensure_sldb_available` in `deskops/cli/` (commands `list`, `show`, `add`, plus bootstrap/init) to identify every call site.
3. Rebuild `MODEL_REFS` as `{name: 'deskops.models:<Name>'}` over every entry in `deskops.models.__all__` that is a `StructuredNLDoc` subclass, excluding the bases `PrimitiveDoc` and `OperationalArtifactDoc`. Keep it a `dict[name, str]`.
4. Add an `allow_install` parameter to `ensure_sldb_available`; guard the `pip install -e ../sldb` path so it runs only when `allow_install` is true; otherwise print `Error: sldb is not installed...` and exit 1.
5. Pass `allow_install=True` only from the bootstrap entrypoint and the `init` command; all other callers use false/default.
6. Confirm `MODEL_REFS` consumers still index by name and get a string: `deskops/cli/commands/desk.py:142`, `doctor.py:118`, `domain_tree.py:249-250`, `tests/test_doctor_model_registration.py:17`.
7. Add Test A to `tests/test_doctor_model_registration.py`: create `tmp_path` repo (per Resolved Decisions: `git init`, one empty seed commit), run `subprocess.run([sys.executable,'-m','deskops','init',str(root)], cwd=root)`; assert `<root>/.sldb/core/store_index.yaml` exists; parse its model-name set; build expected set = (`deskops.models.__all__` minus `PrimitiveDoc`, `OperationalArtifactDoc`) plus `RelationTypeDoc`, `RelationDoc`; assert set equality with no hard-coded count.
8. Add Test B in-process: monkeypatch sldb as not importable, install a spy on the install runner, call `deskops.cli.main.main(['list','tasks'])` under `capsys`; assert the 'Error: sldb is not installed...' message is printed, exit code 1, and the spy was not called.
9. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.
10. Do not commit and do not touch the repo's tracked `desk/`; report the diff for supervisor closeout.

AMBIGUITIES:

1. The call sites of `ensure_sldb_available` are not enumerated; how many callers exist and which need explicit changes vs a defaulted parameter is unknown.
2. `allow_install` default value/kind (default `False` vs required keyword-only) is not specified.
3. Contradiction: Goal states 15 deskops models, but Test A must derive the set from `__all__` with no hard-coded count; which is authoritative if they differ is unstated.
4. How to filter `__all__` is not specified: whether every entry is a class, whether all non-base entries are `StructuredNLDoc` subclasses, and behavior for any other entries is unknown.
5. It is unstated whether `init` registers exactly `RelationTypeDoc` and `RelationDoc` and nothing else besides the deskops models; the expected non-deskops set for Test A is only asserted, not verifiable from the doc.
6. Test A execution mode is not stated (only Test B is called in-process); whether `init` requires a `git init`/seed commit to succeed is not stated.
7. Test B: the mechanism to make sldb "not importable" and the identity/name of the "install runner" to spy on are not given.
8. Exact error-message text and whether the assertion is substring vs exact match is not given; whether exit 1 comes from `sys.exit`/`SystemExit` vs CLI framework is unknown.
9. Exact CLI form `deskops list tasks` (vs `deskops list --kind tasks`) is not specified.
10. Which function in `bootstrap.py` is "bootstrap", and whether `init` is a distinct call site or goes through bootstrap, is not stated.
11. Whether `store_index.yaml` model-name keys match `MODEL_REFS` keys exactly (so set comparison is valid) is not stated.
