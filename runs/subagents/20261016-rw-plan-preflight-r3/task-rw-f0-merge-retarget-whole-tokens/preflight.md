RESTATEMENT:

1. Read `deskops/operations.py` around lines 2109-2165: `_find_inbound_atom_references` (~2109), `_rewrite_inbound_atom_references` (~2130), and confirm the `original_text.replace(needle, replacement)` call at ~2162.
2. Read `merge_atom` (~980) to confirm it is the only caller and to see how `needle`, `replacement`, and the referrer text are constructed.
3. Confirm `import re` exists in `deskops/operations.py`; add it if absent.
4. In `_rewrite_inbound_atom_references`, replace the `str.replace` call with `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, original_text)`.
5. Leave the `rewritten` (path:line) report construction untouched.
6. In `tests/test_atoms_merge.py`, add one test: create a referrer file containing both `atom:atom-foo` and `atom:atom-foo-bar`; merge `atom-foo` into a target atom; assert the referrer now contains `atom:<target>` where `atom:atom-foo` was, and still contains the literal `atom:atom-foo-bar` unchanged.
7. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`.
8. Run `pytest tests`.

AMBIGUITIES:

1. Dependency `task-rw-f0-reject-ambiguous-selectors` is not shown as closed; unclear whether the task may start.
2. Task `status: deferred` while the instructions say the supervisor promotes it before dispatch; promotion state is not observable from the document.
3. `replacement` may be built as a plain `f"atom:{target}"` or may contain regex-active characters (`\`, `\1`, group refs); with `re.sub` those become substitution syntax, so behavior depends on a construction not stated. A literal-safe path (e.g. `lambda m: replacement`) is not specified.
4. Where `needle` is built and whether it includes the `atom:` prefix is not stated; if `needle` is only the id, the proposed regex is wrong.
5. Lookbehind excludes `[A-Za-z0-9_.-]`, so a preceding `:` or `/` counts as a boundary and `x:atom:atom-foo` / `path/atom:atom-foo` would still be rewritten; it is unstated whether that is intended.
6. It is unstated whether the finder/rewrite mismatch case (`xatom:atom-foo` listed by the report but not rewritten) still leaves the `rewritten` report accurate; the report's derivation (finder lines vs actual substitutions) is not specified despite "unchanged" being required.
7. Test scaffolding is unspecified: whether to use the Operations API or the CLI, which sandbox desk root, how the referrer file is registered/tracked, and what the target atom's expected id/token is.
8. Existing tests in `tests/test_atoms_merge.py` may assert the old global-replace behavior; it is unstated whether modifying them is in scope ("one test" in Scope).
9. Line numbers and function signatures in the task may be stale; no acceptance criterion covers drift.
10. Done When requires the new test to fail before the fix and pass after; the ordering/evidence for the red run is not defined.
