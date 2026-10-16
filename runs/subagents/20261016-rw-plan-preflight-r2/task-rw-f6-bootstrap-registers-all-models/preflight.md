RESTATEMENT:

1. Read `deskops/bootstrap.py` in full; locate `MODEL_REFS` (~lines 14-32) and `ensure_sldb_available` (~lines 36-62).
2. Read `deskops/models/__init__.py` (or equivalent) to inspect `__all__` and confirm which entries are `StructuredNLDoc` subclasses vs. non-class exports.
3. Inspect importers to preserve the dict contract: `deskops/cli/commands/desk.py:142`, `deskops/cli/commands/doctor.py:118`, `deskops/cli/commands/domain_tree.py:249-250`, `tests/test_doctor_model_registration.py:17`.
4. Rewrite `MODEL_REFS` as a dict built at import time from `deskops.models.__all__`: keep entries where `issubclass(obj, StructuredNLDoc)`, drop `PrimitiveDoc` and `OperationalArtifactDoc`, map `name -> 'deskops.models:<ClassName>'`.
5. Add `allow_install` parameter to `ensure_sldb_available` (default `False`). When sldb is absent and `allow_install` is `False`, print the existing `Error: sldb is not installed...` message and exit with code 1; only run `pip install -e ../sldb` when `allow_install=True`.
6. Update call sites so only the bootstrap entry point and the `init` command pass `allow_install=True`; leave all other callers on the default.
7. Rewrite/extend `tests/test_doctor_model_registration.py`: use the `_make_repo` / `_cli` pattern from `tests/test_lifecycle_end_to_end.py` to create a throwaway repo in `tmp_path`, `git init` + one seed commit, run `desk install <root>`, then run `init`, and compare the generated store index's registered models against `.sldb/core/store_index.yaml`.
8. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.
9. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:

1. Key-name derivation for `MODEL_REFS` is unspecified: class name verbatim, snake_case, or the existing 17 keys' convention — no example given.
2. Static literal vs. dynamic `issubclass` discovery is not stated; dynamic discovery risks circular import (`deskops.models` importing `bootstrap`).
3. "except the base classes `PrimitiveDoc` and `OperationalArtifactDoc`" is ambiguous: exclude only the two classes themselves, or exclude every subclass of them (if all docs inherit from one, the rule as written could empty the dict or keep everything).
4. Non-class entries in `deskops.models.__all__` (enums, aliases, constants) have no filter rule.
5. `allow_install` default, position, and keyword-only-ness are unspecified; callers other than bootstrap/init are not named.
6. Which functions count as "bootstrap and init" is unstated — the exact call sites in `bootstrap.py` vs. a CLI `init` command are not identified.
7. Scope says "its callers' install flag" but the `files` list contains only `bootstrap.py` and the test; caller edits in `cli/commands/*` may be required but are not listed.
8. The exact `Error: sldb is not installed...` string and its mechanism (print+`sys.exit(1)` vs. raise) are not given, only that it is "existing".
9. Comparison target `.sldb/core/store_index.yaml` path resolution (repo root vs. cwd) and handling of a missing file are unspecified.
10. Whether the test must assert exact set equality or a count of 21 is unclear; hardcoding 21 conflicts with the "same as repo store" dynamic framing and will drift.
11. Whether the tmp-repo store index should exactly match the repo store (no extra models) is unstated.
12. No acceptance criterion states how to verify that non-init/non-bootstrap commands refuse to install sldb (only the message+exit-1 behavior is named, without a test target).
13. `tests/test_doctor_model_registration.py` is named for doctor registration but the described test is a fresh-init test; whether both behaviors must be covered is unclear.
14. `_make_repo`/`_cli` reuse: copy vs. import is unspecified; only "pattern to copy" is given.
