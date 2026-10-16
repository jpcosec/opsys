RESTATEMENT:
1. Open `deskops/operations.py` and locate `_resolve_glob` (~2612), `_resolve_artifact_selector_multi` (~2621), `_resolve_artifact_selector` (~2647), `_one_artifact_match` (~2738); confirm each currently implements "exact name/stem, then unique prefix, else ambiguity".
2. Create `deskops/desk_paths.py` with `resolve_selector(directories: list[Path], selector: str, pattern: str, what: str) -> Path`.
3. Implement tier 1: return the file in `directories` whose `name` or `stem` equals `selector`.
4. Implement tier 2: return the sole file whose `name` or `stem` starts with `selector`.
5. Zero matches → raise `FileNotFoundError`; more than one → raise `ValueError(f"Ambiguous {what} selector '{selector}' in {dir}: {candidates}")`.
6. Reduce the four `operations.py` methods to one-line delegations calling `resolve_selector`.
7. Add `tests/test_desk_paths.py` covering tier 1, tier 2, zero matches (`FileNotFoundError`), and ambiguity (`ValueError`).
8. Run `pytest tests/test_desk_paths.py`.
9. Run `pytest tests` (must include F1 `tests/test_cli_contract.py`, pass unchanged).
10. Run `grep -n 'glob(\|rglob(' deskops/operations.py` and confirm no selector-resolution loop remains outside the delegations.
11. Leave the diff uncommitted for supervisor closeout.

AMBIGUITIES:
1. Role of `pattern` param is undefined: is it a glob applied inside each directory, a suffix filter, or unused? Not stated how it combines with name/stem matching.
2. `directories` is a list but the ValueError message uses singular `<dir>`; unclear which directory is printed when matches span multiple directories.
3. Multi-directory semantics undefined: are matches aggregated across all directories, or searched per-directory in order, or must be unique within each?
4. `<candidates>` formatting unspecified: basenames vs full paths, sorted or not, separator.
5. `FileNotFoundError` message text unspecified.
6. `_resolve_artifact_selector_multi` name implies multi-match return, but the new function returns a single `Path`; how it delegates without changing its signature/return type is not stated, contradicting "behavior is unchanged".
7. Existing methods may currently raise exception types other than `FileNotFoundError`/`ValueError`; "behavior is unchanged except the ambiguity message" contradicts prescribing these exceptions.
8. Behavior for empty `directories` list unspecified.
9. Whether tier 2 should also return exact matches (a name equal to selector also starts with it) or exclude them.
10. Case sensitivity of name/stem comparison unspecified.
11. Per-caller `what` values (e.g., "artifact", "task") not given.
12. Whether the F1 dependency tasks must exist/be complete before running `pytest tests` is not specified; task status is `deferred`.
13. Line numbers for the four methods may be stale; no acceptance criterion addresses drift.
