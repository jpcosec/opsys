RESTATEMENT:

1. Assume the doc is the already-promoted active task (per Resolved Decisions) and read `deskops/operations.py` around `_rewrite_inbound_atom_references` (~2109-2170) and its only caller `merge_atom` (~980); record the current signature, args (`needle`, `replacement`, `original_text`), return/report schema, and how `needle` is built (`atom:<source id>`).
2. Replace the whole-file `original_text.replace(needle, replacement)` at line ~2162 with per-line `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, line)`.
3. Build the `rewritten` report only from lines where the substituted text differs from the original line (keep existing `path:line` shape and existing keys).
4. Leave `_find_inbound_atom_references` unchanged; leave `split_atom` untouched; do not add rollback.
5. Add one test in `tests/test_atoms_merge.py`: create a valid target atom and source `atom-foo`, add a referrer doc containing both `atom:atom-foo` and `atom:atom-foo-bar`, invoke the merge, assert `atom:atom-foo-bar` is byte-identical and `atom:atom-foo` now references the target.
6. Confirm the new test fails against the pre-fix code path (e.g. stash the fix or run before editing).
7. Run `pytest tests/test_atoms_merge.py tests/test_atoms_split.py`, then `pytest tests`.
8. Report the diff; do not commit (supervisor owns promotion and closeout commits).

AMBIGUITIES:

1. Task `status: deferred` and `source:drawer`; Resolved Decisions says the supervisor promotes to `desk/tasks/` before dispatch — unclear whether promotion already happened, so unclear whether I should execute or stop.
2. `depends_on: task-rw-f0-reject-ambiguous-selectors`; no evidence it is closed, and no statement that this task is unblocked.
3. Whether `replacement` is the bare target id or the full `atom:<target>` token — the regex substitutes it verbatim, so the expected post-merge string in the test is undetermined.
4. Current signature of `_rewrite_inbound_atom_references` and the type/shape of its return value (`rewritten` report) are not given; exact `path:line` string format unstated.
5. Whether unchanged files must be skipped from writes at all, and whether a file whose only match is `atom:atom-foo-bar` must stay byte-identical (implied by Goal, not stated in Scope/Implementation Path).
6. Whether per-line substitution is required, or whole-text substitution plus a line-level diff is acceptable.
7. Whether the test must also assert the sub-token-only file is absent from the `rewritten` report.
8. Scope says "one test"; Validation lists `tests/test_atoms_split.py` — unclear whether that file is modified or only run.
9. Test harness not specified: how existing tests construct the desk root, the operations instance, and atom documents (fixtures/imports) is unknown.
10. `import re` presence in `deskops/operations.py` is unknown.
11. "merge `atom-foo` into a target" — target id, whether the source atom doc must exist/be valid, and how merge is invoked in tests are unspecified.
12. Whether `_find_inbound_atom_references` output for `xatom:atom-foo` is asserted anywhere; task calls it acceptable but no test-name/location is given.
13. How to demonstrate "fails before the fix" without reverting tracked files (stash/branch) is unspecified.
