RESTATEMENT:
1. Read `deskops/operations.py` `_rewrite_inbound_atom_references` (~line 1706, replace at ~1738) and its only caller `merge_atom` (~line 924) to capture current logic: per-line `needle in line` check, whole-file `original_text.replace(needle, replacement)`, and how `rewritten` (path:line) entries are built.
2. Replace the `str.replace` call with `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, original_text)`; confirm `re` is imported in the module.
3. Rebuild the `rewritten` report so it appends a `path:line` entry only for lines whose text the substitution changed (compare pre/post line text, or run the sub per line / capture which lines changed from the file-level result).
4. Add one test in `tests/test_atoms_merge.py`: build a referrer file containing a line with `atom:atom-foo` and a line with `atom:atom-foo-bar`; call `merge_atom("atom-foo", <target>)`; assert the `atom:atom-foo-bar` line is byte-identical after merge and the `atom:atom-foo` token now names the target.
5. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`, then `pytest tests`.
6. Confirm the new test fails against the pre-fix code (e.g. stash the `operations.py` edit and rerun) and passes after.
7. Leave the change uncommitted; report the diff to the supervisor for the closeout commit.

AMBIGUITIES:
1. Rationale claims the bounded regex leaves `xatom:atom-foo` alone, but with `(?<![A-Za-z0-9_.-])` the preceding `:` is not in the excluded set, so that substring **would** be rewritten. Contradiction between rationale and the given regex.
2. No spec for the `rewritten` report when a single line has multiple changed lines/tokens, nor whether entry ordering/dedup must be preserved from current behavior.
3. Whether the substitution must run once on the whole file text or per line is not fixed; only the regex and the "changed lines only" reporting rule are given, and the two must be reconciled.
4. Test construction details are unspecified: fixture/desk setup helpers, referrer file path, target atom id, and the exact assertion form for "now names the target".
5. `depends_on: task-rw-f0-reject-ambiguous-selectors` is listed but no precondition/behavior is stated if that task is not yet merged (it touches selector handling in the same operation surface).
6. Task `status: deferred`; promotion to `desk/tasks/` is a supervisor step per Resolved Decisions, but it is not stated whether execution may start before promotion/dependency completion.
