RESTATEMENT:

1. Read `deskops/operations.py` around lines 2612, 2621, 2647, 2738 and read `_resolve_glob`, `_resolve_artifact_selector_multi`, `_resolve_artifact_selector`, `_one_artifact_match` in full, including their signatures, return types, and current messages.
2. Grep the repo for callers of those four methods to know return-type expectations and the `what` values in use.
3. Grep tests for assertions on the old message wording; record each affected test and file.
4. Read `tests/test_cli_contract.py` (F1 contract tests) to confirm it asserts the new wording and must pass unchanged.
5. Create `deskops/desk_paths.py` and implement `resolve_selector(directories: list[Path], selector: str, pattern: str, what: str) -> Path`.
6. Tier 1: find a file whose `name` or `stem` equals `selector`. Tier 2: find a unique file whose `name` or `stem` starts with `selector`.
7. Zero matches → raise `FileNotFoundError` with `No <what> file found for selector '<selector>'`. More than one → raise `ValueError` with `Ambiguous <what> selector '<selector>': <candidates>` where candidates are matching paths relative to the desk root, sorted, joined by `, `.
8. Replace each of the four method bodies with a one-line delegation to `resolve_selector`.
9. Update every existing test asserting the old wording; list each in the closeout.
10. Add `tests/test_desk_paths.py` covering both tiers, zero matches, and ambiguity.
11. Run `pytest tests/test_desk_paths.py`, then `pytest tests`.
12. Verify `grep -n 'glob(\|rglob(' deskops/operations.py` shows no selector-resolution loop outside the delegations.
13. Report the diff and the list of updated tests; do not commit (supervisor commits closeout).

AMBIGUITIES:

1. `pattern: str` is in the signature but its role is unspecified; unclear whether it globs per directory, is the file filter, or interacts with the tier logic.
2. Return type is `Path` (singular), but `_resolve_artifact_selector_multi` implies multi-match resolution; how a single `Path` replaces a multi-returning method is unspecified.
3. Candidates must be "relative to the desk root", but the function receives `directories: list[Path]`, not the desk root; how to derive the desk-root-relative form is unspecified.
4. `<what>` values each of the four callers should pass are not given.
5. Whether matching is case-sensitive is not stated.
6. Whether matching is recursive (`glob` vs `rglob` per directory) is not stated, though Done When mentions both.
7. Behavior when an exact match and a prefix match coexist (precedence, and whether the prefix match is excluded) is not stated beyond "exact first".
8. Whether zero-match/ambiguity errors apply to both tiers and to the multi variant is not stated.
9. "sorted" is unspecified: lexicographic string sort vs path-part sort.
10. Message wording for `_resolve_glob` given "No <what> file found" is phrased for files; unclear if non-file glob resolution shares it.
11. The exact existing tests asserting old wording are not enumerated; they must be discovered (scope of "any" is open).
12. Location of `ARTIFACT_PATHS` / desk layout constants is not stated, so the "stay where they are" boundary cannot be verified from the task alone.
13. Line numbers (2612/2621/2647/2738) may not match the current file; if not, method identification is by name only.
