RESTATEMENT:
1. Read context: `deskops/operations.py` atom methods, existing `deskops/services/*.py` pattern (from `task-rw-f3-tasks-service`), the `DocTransaction` implementation used by pill-012, the doc_io module, and the two bound pills.
2. Create `deskops/services/atoms.py` defining `AtomsService(root)` following the service conventions already used in `deskops/services/`.
3. Move into `AtomsService`: atom create, edit, split, merge, retarget, delete methods, plus `_find_inbound_atom_references` and `_rewrite_inbound_atom_references`, replacing any direct file/path writes with doc_io calls.
4. Wrap the body of `merge_atom` in exactly one `DocTransaction`; wrap the body of `split_atom` in exactly one `DocTransaction`.
5. Reduce `deskops/operations.py` atom functions to thin wrappers delegating to `AtomsService`.
6. Update internal call sites/imports that used the moved helpers, in the same change.
7. Add two failure-injection tests: (a) merge — make the doc_io track step raise after the inbound referrer rewrite, then assert every touched file's bytes equal originals and `sldb stores check` is unchanged; (b) split — raise after the first new atom is written, same assertions.
8. Run `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`, then `pytest tests`, without modifying existing tests in `tests/test_atoms_cli.py`, `tests/test_atoms_merge.py`, `tests/test_atoms_split.py`, `tests/test_atoms_create_from_source.py`.
9. Verify Done When: `grep -n 'def merge_atom' deskops/services/atoms.py` matches, `operations.py` only delegates, both injection tests pass, `pytest tests` green.
10. Do not commit; hand the diff to the supervisor for promotion/closeout.

AMBIGUITIES:
1. Contradiction: Scope says `tests/test_atoms_merge.py` and `tests/test_atoms_split.py` must pass unmodified, but the Implementation Path requires new failure-injection tests; where those tests live is unspecified, and adding them to those two files violates "unmodified".
2. `files:` lists no doc_io module, yet step 1 requires all writes to go through doc_io; the doc_io module/path and API are not given.
3. `DocTransaction` import path, constructor/context-manager form, touched-file registration, and whether nesting or reuse is allowed are unspecified.
4. Failure-injection mechanism unspecified: no name for "the doc_io track step", the referrer rewrite, or the first new-atom write, so the monkeypatch target is unknown.
5. How to assert `sldb stores check` is "unchanged" is unspecified: exact command, store path, sandbox root, and comparison method.
6. `AtomsService` signature, method naming (`merge_atom` vs `merge`), and error propagation are unspecified; the `depends_on` task's conventions are not quoted.
7. Goal lists retarget and delete as moved, but Scope and Implementation Path do not mention them, and no tests for them are named.
8. "operations.py keeps only wrappers" — wrapper signatures and whether the service or the wrapper opens the transaction are unspecified.
9. Whether existing CLI commands/tests must import `AtomsService` directly or keep going through `operations.py` is unspecified.
10. No acceptance check for "every write goes through doc_io"; cannot verify that clause.
11. `status: deferred` and Resolved Decisions say the supervisor promotes before dispatch; whether promotion has already occurred is not stated.
12. "inventory D7" is referenced but not included, so coverage of the partial rollbacks cannot be confirmed.
13. Whether retarget also needs transactional rollback (only merge and split are specified) is unspecified.
