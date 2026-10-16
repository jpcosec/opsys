RESTATEMENT:
1. Open `deskops/operations.py` and read `_rewrite_inbound_atom_references` (~line 2130–2170) to learn its signature, how the target `atom:<id>` and its replacement are supplied, how lines are iterated, and how the `rewritten` (path:line) list is built.
2. Locate the matcher that identifies exact `atom:<id>` tokens in that function (or its helper) and confirm the real token grammar; if it differs from the regex given in the task, reconcile before editing.
3. Build a compiled pattern: `re.compile(r'(?<![A-Za-z0-9_.-])atom:' + re.escape(target_id) + r'(?![A-Za-z0-9_.-])')`.
4. Replace the global `original_text.replace(needle, replacement)` at ~line 2162 with `pattern.sub(<repl>, original_text)`; use a `lambda m: replacement` (or an escaped replacement) so the replacement text is treated literally, not as a regex group reference.
5. Keep the `rewritten` report (path:line) semantics unchanged: still detect/record a line only when a real `atom:<id>` token was matched, preserving existing line numbering.
6. Add a test in `tests/test_atoms_merge.py`: build a referrer document containing both `atom:atom-foo` and `atom:atom-foo-bar`; invoke the retarget/rename path for `atom-foo`; assert `atom:atom-foo` becomes the new token and `atom:atom-foo-bar` is untouched.
7. Confirm the new test fails before the fix, then passes after (run the single test against unfixed code, then fixed).
8. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`, then `pytest`.

AMBIGUITIES:
1. Signature of `_rewrite_inbound_atom_references` is not given: unknown parameters, return type, how target id and replacement are derived.
2. The "matcher" and its actual token grammar are asserted but not cited; if it differs from the task's regex, which grammar is authoritative.
3. Whether the existing loop is per-line or whole-file is not stated; affects whether `re.sub` runs per line or on the whole text, and thus line-number accounting for `rewritten`.
4. Replacement escaping is unspecified: whether to use a `lambda` or escape backslashes in the replacement string; unclear if ids can contain `\` or group-like sequences.
5. Exact semantics of "keep the `rewritten` report unchanged" is not defined — unclear whether a line matching only `atom:atom-foo-bar` must remain unreported, or whether that behavior is even currently covered.
6. Test fixture/helper API in `tests/test_atoms_merge.py` is unknown (existing helper names, how to invoke the retarget path, how atoms are constructed).
7. `depends_on: task-rw-f0-reject-ambiguous-selectors` status is not provided; cannot verify the dependency is closed.
8. Whether renaming, merging, and splitting all route through this same function, or only one path does, is not stated.
9. No defined id character constraints; unclear whether the given lookbehind/lookahead char class `[A-Za-z0-9_.-]` is exhaustive.
10. Acceptance threshold for "all atom tests stay green" is unspecified (full `pytest` vs. named files only; whether unrelated failures block).
11. The referenced pill file content is not included, so any constraint it imposes is unknown.
12. `status: deferred` with a full implementation path: unclear whether this task should be executed now or only restated.
