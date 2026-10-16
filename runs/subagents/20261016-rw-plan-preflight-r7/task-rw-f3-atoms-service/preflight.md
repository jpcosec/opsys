RESTATEMENT:
1. Read dependency `task-rw-f3-tasks-service` output and existing `deskops/services/*.py` to copy the established `Service(root)` pattern.
2. Read `deskops/operations.py`; enumerate all atom methods (`create`, `edit`, `split`, `merge`, `retarget`, `delete`) plus `_find_inbound_atom_references`/`_rewrite_inbound_atom_references`.
3. Read the doc_io module and `DocTransaction` to learn their exact import paths and call signatures.
4. Create `deskops/services/atoms.py` with `class AtomsService` and `__init__(self, root)`.
5. Move the atom method bodies from `operations.py` into the service; route every write through doc_io.
6. Wrap `merge_atom` body in a single `DocTransaction`; wrap `split_atom` body in a single `DocTransaction`.
7. Replace the atom methods in `operations.py` with delegating wrappers to `AtomsService(root)`.
8. Add failure-injection tests raising from the doc_io track step after the referrer rewrite (merge) and after the first new atom write (split); assert byte-equality of touched files vs originals and unchanged `sldb stores check`.
9. Run `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`.
10. Run `pytest tests`.
11. Run `grep -n 'def merge_atom' deskops/services/atoms.py`.

AMBIGUITIES:
1. `AtomsService(root)` — type/meaning of `root` (repo root, desk root, sldb root, `Path`) unspecified.
2. doc_io module path, function names, and "track step" API not named; cannot know what to make raise.
3. `DocTransaction` import path, constructor args, and usage (context manager vs explicit commit/rollback) unspecified.
4. Exact method list to move is not enumerated; "atom methods" beyond the six named in Goal is undefined.
5. Whether `_find_inbound_atom_references`/`_rewrite_inbound_atom_references` become service methods, module functions, or stay in operations.py is unspecified; other operations.py callers are not mapped.
6. Contradiction: Scope requires the four listed test files "pass unmodified," yet Step 3 adds failure-injection tests; no file path is given for the new tests, and `files:` lists only two test files.
7. Whether `tests/test_atoms_merge.py`/`tests/test_atoms_split.py` in `files:` are to be edited or only run is unclear (conflicts with "unmodified").
8. Failure-injection mechanism is undefined (monkeypatch, fake doc_io, injected seam) and no seam is named.
9. "After the referrer rewrite" and "after the first new atom is written" reference step order not specified in the doc; ordering must be inferred from existing code.
10. "Every touched file's bytes equal the originals" — set of touched files is not enumerated, nor how originals are snapshotted.
11. "`sldb stores check` is unchanged" — invocation method (subprocess vs API) and what "unchanged" compares (stdout, exit code, store bytes) unspecified.
12. Validation lists only the four named test files plus `pytest tests`; the Done When requires injection tests to pass but names no test file/path.
13. Wrapper contract in operations.py unspecified: whether signatures, names, and import surfaces must stay identical for existing tests.
14. Whether `create`/`edit`/`delete`/`retarget` need transactions is unspecified; Goal requires transactions only for merge and split (pill-012 covers create-op rollback).
15. Dependency `task-rw-f3-tasks-service` status and whether it defines a shared service base/interface to conform to is unknown.
16. Done When's grep checks only `def merge_atom`, leaving the other moved methods unverified.
17. Pill `pill-atom-lifecycle-preserves-provenance-and-materialization-links` is bound but no acceptance criterion in the task references provenance/materialization behavior.
