RESTATEMENT:
1. Read `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md` (bound pill).
2. Open `deskops/operations.py` and read `_find_inbound_atom_references` (line ~2109), `_rewrite_inbound_atom_references` (line ~2130), and its call in `merge_atom` (line ~980); confirm how `needle`, `replacement`, and the `rewritten` list are built.
3. Confirm `import re` exists in `deskops/operations.py`.
4. Replace the `original_text.replace(needle, replacement)` at line ~2162 with `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, original_text)`.
5. Change the `rewritten` report logic so a (path:line) is appended only when the substitution actually changed that line's text (compare pre/post per line).
6. Add one test in `tests/test_atoms_merge.py`: create/point at a referrer file containing `atom:atom-foo` and `atom:atom-foo-bar`; call `merge_atom` merging `atom-foo` into a target; assert `atom:atom-foo-bar` is unchanged and `atom:atom-foo` now references the target id.
7. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`, then `pytest tests`.
8. Verify the new test fails on the pre-fix code (stash/revert) and passes after.
9. Leave diff uncommitted; supervisor promotes, reviews, and commits.

AMBIGUITIES:
1. `merge_atom`'s exact signature, the `needle`/`replacement` construction, and how `rewritten` is currently shaped (list of tuples? strings? `.append` site?) are not given; the edit target is inferred from line numbers.
2. How referrer files are discovered/scanned by `merge_atom` (which directory or store) is unspecified, so the test's fixture setup for the referrer file is unknown.
3. Test helper conventions in `tests/test_atoms_merge.py` (existing fixtures, store setup, temp dirs) are not described.
4. `re.sub` replacement-string escaping: whether `replacement` can contain backslashes/group refs is not stated; a lambda replacement may be required but is not specified.
5. Whether `atom:atom-foo` uniquely identifies the source atom, and whether ids in referrers always use the `atom:` prefix, is assumed from the regex but not confirmed.
6. Whether the bounded rewrite should also apply inside `_find_inbound_atom_references` is left as "acceptable" divergence in the task, but the resulting mismatch between reported candidates and rewritten lines is not tested or asserted.
7. Acceptance "new test fails before the fix" has no stated procedure for demonstrating the pre-fix failure.
8. `depends_on: task-rw-f0-reject-ambiguous-selectors` status (closed/otherwise) is not stated.
9. `re` module availability in `deskops/operations.py` is assumed, not confirmed.
