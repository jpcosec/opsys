RESTATEMENT

1. Read `deskops/operations.py` around lines 850–900 (`_find_inbound_atom_references`), ~980 (`merge_atom`), and ~2130–2165 (`_rewrite_inbound_atom_references` to confirm the `needle` value (`atom:<id>`), the exact-token line check, and the `original_text.replace(needle, replacement)` call at ~2162.
2. Read `tests/test_atoms_merge.py` to learn existing fixture/helper patterns for building referrer files and invoking `merge_atom`.
3. In `_rewrite_inbound_atom_references`, replace the `str.replace` at ~2162 with `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, original_text)`.
4. Confirm `import re` is present in `deskops/operations.py`; add if missing.
5. Leave the `rewritten` (path:line) reporting logic unchanged.
6. Add one test in `tests/test_atoms_merge.py`: create a referrer containing both `atom:atom-foo` and `atom:atom-foo-bar`; run `merge_atom` merging `atom-foo` into a chosen target; assert `atom:atom-foo-bar` is byte-identical/untouched and `atom:atom-foo` now resolves to the target id.
7. Run the new test against unmodified code to confirm it fails, then with the fix to confirm it passes.
8. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`.
9. Run `pytest tests`.
10. Do not commit; leave the diff for supervisor review/closeout.

AMBIGUITIES

1. `replacement` is passed raw to `re.sub`; task does not say whether to escape it or use a lambda. Per the `atom:[a-zA-Z0-9_.-]+` grammar ids cannot contain backslashes, so raw is likely safe, but this is unspecified.
2. The concrete target atom id and the `merge_atom` invocation form (operation method vs CLI) for the new test are not specified.
3. Where/how to build the referrer fixture in `tests/test_atoms_merge.py` (existing helpers, file naming) is not described; requires reading the module.
4. "Fails before the fix" — the verification method (revert vs write-test-first) is not stated.
5. Whether `_find_inbound_atom_references` and `_rewrite_inbound_atom_references` must remain grammar-consistent is stated as unaffected/out of scope, so no action, but the task does not define behavior for a referrer like `xatom:atom-foo` (lookbehind suppresses the match); acceptance criteria do not cover it.
