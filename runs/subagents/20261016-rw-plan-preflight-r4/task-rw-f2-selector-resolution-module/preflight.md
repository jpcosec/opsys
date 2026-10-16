## RESTATEMENT

1. Open `deskops/operations.py` and read the current bodies, signatures, and all callers of `_resolve_glob` (~2612), `_resolve_artifact_selector_multi` (~2621), `_resolve_artifact_selector` (~2647), `_one_artifact_match` (~2738); record each method's search call (`glob` vs `rglob`), pattern used, current zero-match and multi-match messages, and the `what`/artifact-id value each caller would supply.
2. Create `deskops/desk_paths.py` with `def resolve_selector(desk_root: Path, directories: list[Path], selector: str, pattern: str, what: str, recursive: bool) -> Path`.
3. In it, gather candidates with `d.glob(pattern)` when `recursive=False` and `d.rglob(pattern)` when `recursive=True`, over all `directories`.
4. Tier 1: filter candidates where `p.name == selector` or `p.stem == selector`. Exactly one → return it. More than one → raise `ValueError(f"Ambiguous {what} selector '{selector}': {joined}")`.
5. Tier 2: filtered candidates where `p.name.startswith(selector)` or `p.stem.startswith(selector)`. Exactly one → return it. More than one → raise `ValueError` with the same format.
6. Zero matches at both tiers → raise `FileNotFoundError(f"No {what} file found for selector '{selector}'")`.
7. Build `<candidates>` as the matching paths made relative to `desk_root`, sorted, joined with `', '`.
8. Replace each of the four methods in `operations.py` with a one-line delegation to `resolve_selector`, preserving its existing signature so current callers/tests are unaffected, passing `recursive=False` for `_resolve_glob` and `recursive=True` for the artifact selectors, and passing `what` = artifact id for the artifact selectors and the directory kind (task, routine, edge, operator, checklist, condition) for `_resolve_glob` callers.
9. Find every test asserting the old message wording and update it to the new format; note each in the closeout.
10. Write `tests/test_desk_paths.py` covering: tier-1 exact name, tier-1 exact stem, tier-2 unique prefix, zero matches (`FileNotFoundError`), ambiguous tier (>1) (`ValueError`), for both `recursive=True` and `recursive=False`.
11. Run `pytest tests/test_desk_paths.py`.
12. Run `pytest tests` (must include `tests/test_cli_contract.py` passing unchanged).
13. Run `grep -n 'glob(\|rglob(' deskops/operations.py` and confirm no selector-resolution loop remains outside the delegations.

## AMBIGUITIES

1. `depends_on` lists only the three F1 tasks, but the Rationale depends on `task-rw-f0-reject-ambiguous-selectors`; that dependency is not declared.
2. `_resolve_artifact_selector_multi` (~2621) is named for returning multiple matches, yet `resolve_selector` returns one `Path` and raises on >1. A "one-line delegation" cannot preserve multi-match behavior; which semantics win is unspecified.
3. `_one_artifact_match` (~2738) is presumably a single-match helper, not a full resolver; whether it delegates, is deleted, or keeps distinct return/exception semantics is unspecified.
4. Where each artifact selector's `what` (artifact id) value comes from at runtime is unspecified; no source of that string is given.
5. The enumerated directory kinds "(task, routine, edge, operator, checklist, condition)" are asserted to cover `_resolve_glob` callers; whether that list is exhaustive, and which caller passes which, cannot be verified from the task text.
6. The `pattern` argument's exact value/form per caller (e.g. `'*.md'`) is not given.
7. Whether tier-1/tier-2 filtering also requires the candidate to match `pattern` (i.e. pattern applied before name/stem comparison) is unspecified.
8. When ambiguity appears, whether `<candidates>` lists the tier that produced the ambiguity or all matches across tiers is unspecified.
9. Behavior when a candidate is not under `desk_root` (`Path.relative_to` raises `ValueError`) is unspecified.
10. Whether `desk_paths.resolve_selector` is public API (exports, docs, FAQ mention) is unspecified.
11. Whether the four delegations must retain their exact current signatures, names, and return types is implied ("behavior unchanged") but not stated as a contract.
12. `tests/test_desk_paths.py` coverage is defined only as "both tiers, zero matches and ambiguity"; no required coverage for recursion variants, multiple directories, non-desk-root paths, or `what` string formatting.
13. Which existing tests assert the old wording is unknown from the task text, so "list each one in the closeout" cannot be pre-enumerated.
