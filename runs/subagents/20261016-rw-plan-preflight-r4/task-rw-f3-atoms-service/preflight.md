RESTATEMENT:

1. Read `deskops/operations.py`; identify every atom-related function/method: create, edit, split, merge, retarget, delete, plus `_find_inbound_atom_references` and `_rewrite_inbound_atom_references`.
2. Create `deskops/services/atoms.py` defining `class AtomsService` with `__init__(self, root)`, following existing service patterns in `deskops/services/`.
3. Move the six atom operations and the two private helpers into `AtomsService`, routing every write through `doc_io`.
4. Replace the moved bodies in `operations.py` with thin wrappers that delegate to `AtomsService(root)` (same call signatures as before).
5. Import `DocTransaction` into `deskops/services/atoms.py`.
6. Wrap the entire body of `merge_atom` in one `with DocTransaction(...)`.
7. Wrap the entire body of `split_atom` in one `with DocTransaction(...)`.
8. Add a failure-injection test (merge): patch the `doc_io` track step to raise after the inbound-reference rewrite; assert byte-equality of every touched file vs originals; assert `sldb stores check` unchanged.
9. Add a failure-injection test (split): patch the `doc_io` track step to raise after the first new atom write; assert byte-equality of every touched file vs originals; assert `sldb stores check` unchanged.
10. Keep `tests/test_atoms_cli.py`, `tests/test_atoms_split.py`, `tests/test_atoms_create_from_source.py`, `tests/test_atoms_merge.py` unmodified.
11. Run `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`, then `pytest tests`.
12. Confirm `grep -n 'def merge_atom' deskops/services/atoms.py` matches and `operations.py` only delegates.
13. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:

1. "doc_io track step" is undefined: no module, function, or interface named; the injection seam (monkeypatch target) cannot be determined.
2. Failure-injection tests have no assigned file or names; `files:` lists both test files but does not map which test goes to which.
3. `DocTransaction` is not defined: no module, constructor, or semantics given; assumption that it exists and is rollback-capable.
4. Exact `AtomsService` method names are unspecified ("owns ... create, edit, split, merge, retarget and delete" vs `merge_atom` used in Done When).
5. Wrapper shape in `operations.py` is unspecified (names, signatures, how `root` is obtained, whether module-level functions).
6. Whether `_find_inbound_atom_references`/`_rewrite_inbound_atom_references` become `AtomsService` methods or stay module-level functions is not stated.
7. Which files are "touched" for the byte-equality assertion is not enumerated.
8. How to assert `sldb stores check` is "unchanged" (exit code, stdout diff, API call, subprocess) is unspecified.
9. Merge write ordering (source→target vs referrer rewrite) is only implied by the injection point; not stated.
10. Split write ordering and which atom is "first" are not defined.
11. `root` type/source for `AtomsService(root)` is unspecified.
12. Other callers of the atom methods outside `operations.py` are not enumerated; the move may break them and no criterion covers this.
13. "every write goes through doc_io" is asserted without defining `doc_io` or its interface.
14. Inventory item D7 (`runs/planning/deskops-rewrite-inventory.md`) is not included, so full intended scope cannot be confirmed.
15. Pill contents (pill-atom-lifecycle-..., pill-012-...) are not included, so the transaction/rollback contract cannot be verified.
16. Done When's grep only checks `merge_atom`; presence/correctness of the other moved operations is untestable from the stated criteria.
17. Whether `deskops/services/atoms.py` requires registration/export (e.g., in `deskops/services/__init__.py`) is not stated.
18. "Unchanged behavior" is anchored only to four named test files; CLI output/exit-code parity beyond those is undefined.
19. No assertion details or acceptance criteria are given for the two injection tests beyond "pass."
