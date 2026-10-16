RESTATEMENT:
1. Open `deskops/operations.py`; locate `_resolve_glob` (~2612), `_resolve_artifact_selector_multi` (~2621), `_resolve_artifact_selector` (~2647), `_one_artifact_match` (~2738); record each one's current search mode (`glob` vs `rglob`), pattern, `what`-style label, and error wording.
2. Create `deskops/desk_paths.py` with `resolve_selector(desk_root: Path, directories: list[Path], selector: str, pattern: str, what: str, recursive: bool) -> Path`.
3. Implement the two-tier rule inside it: tier 1 exact `name`/`stem` equality; tier 2 unique `name`/`stem` startswith; 0 matches → `FileNotFoundError("No <what> file found for selector '<selector>'")`; >1 → `ValueError("Ambiguous <what> selector '<selector>': <candidates>")`, candidates = matching paths relative to `desk_root`, sorted, `', '`-joined.
4. Make the four methods one-line delegations to `resolve_selector`, preserving each caller's `glob`/`rglob` choice via `recursive` and each caller's `what` (`task`/`routine`/`edge`/`operator`/`checklist`/`condition` for glob callers; artifact id for artifact selectors).
5. Grep existing tests for assertions on the old message wording; update them; record each in the closeout notes.
6. Write `tests/test_desk_paths.py` covering tier 1, tier 2, zero matches, and ambiguity.
7. Run `pytest tests/test_desk_paths.py`, then `pytest tests`.
8. Run `grep -n 'glob(\|rglob(' deskops/operations.py` and confirm no selector-resolution loop outside the delegations.
9. Report updated tests and grep output; do not commit (supervisor commits).

AMBIGUITIES:
1. Role of the `pattern` parameter is undefined; the tier rule never states how the glob pattern combines with or constrains tier 1/tier 2 matching.
2. `_resolve_artifact_selector_multi` implies multiple results, but `resolve_selector` returns a single `Path` and raises on >1 — how it delegates is contradictory.
3. `_one_artifact_match` is named as one of the four resolvers but reads as a helper; whether/how it delegates is unspecified.
4. Origin of `desk_root` and its relation to `directories` in each caller is not stated.
5. `what` is "the artifact id" for artifact selectors, but the artifact id is not known at selector-resolution time — no source for that value is given.
6. Which existing tests assert the old wording is not enumerated; requires a repo search the task text does not bound.
7. Case sensitivity for `equals` and `startswith` is unspecified.
8. Sort key for `<candidates>` (full relative path vs basename) is unspecified.
9. Whether `<candidates>` lists all matches or only tier-2 ambiguous matches is unspecified.
10. Behavior when tier 1 yields more than one exact match is not stated (task says >1 raises, but tier 1 is described singularly).
11. Done When's grep may be unsatisfiable if `operations.py` has unrelated `glob(`/`rglob(` uses; unknown from the task.
12. Line numbers (2612/2621/2647/2738) are anchors only and may have drifted.
13. Scope says "two messages" change, but four methods each carry a message — which two are meant is unclear.
14. No acceptance criterion specifies that `FileNotFoundError`/`ValueError` types (versus messages alone) must be preserved per caller.
