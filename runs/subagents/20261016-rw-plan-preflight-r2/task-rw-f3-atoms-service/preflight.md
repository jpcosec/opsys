RESTATEMENT:

1. Confirm `task-rw-f3-tasks-service` is closed; do not start while deferred/unmet.
2. Read `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md` and `desk/contexts/pill-012-create-operations-transactional-rollback.md`.
3. Create `deskops/services/atoms.py` defining `AtomsService(root)` with `__init__(self, root)`.
4. Move atom `create`, `edit`, `split`, `merge`, `retarget`, `delete` from `deskops/operations.py` into `AtomsService`.
5. Move helpers `_find_inbound_atom_references` and `_rewrite_inbound_atom_references` into the same module.
6. Route every write in those methods through `doc_io`.
7. Wrap `merge_atom` body in exactly one `DocTransaction`.
8. Wrap `split_atom` body in exactly one `DocTransaction`.
9. In `deskops/operations.py`, keep the same public functions but make them delegate to `AtomsService`.
10. Add failure-injection test: merge — raise from the doc_io track step after the referrer rewrite; assert every touched file's bytes equal originals and `sldb stores check` unchanged.
11. Add failure-injection test: split — raise from the doc_io track step after the first new atom is written; same byte/store assertions.
12. Run `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`.
13. Run `pytest tests`.
14. Verify `grep -n 'def merge_atom' deskops/services/atoms.py` matches and `operations.py` only delegates.
15. Do not commit; leave diff for supervisor closeout.

AMBIGUITIES:

1. Dependency `task-rw-f3-tasks-service` status is unknown; task is `deferred` and cannot be assumed unblocked.
2. `doc_io` is not defined/referenced as an existing module; its API and the exact "track step" call to inject failure into are unstated.
3. `DocTransaction` location, constructor/context-manager API, and multi-file rollback guarantees are unstated; "one DocTransaction each" cannot be verified against an unknown interface.
4. How to capture and compare "every touched file's bytes" and what set of files counts as touched is unspecified.
5. "`sldb stores check` is unchanged" — no comparator defined (output text, exit code, snapshot).
6. Which test files hold the two failure-injection tests is not stated; files list implies `tests/test_atoms_merge.py` and `tests/test_atoms_split.py` but does not say so.
7. Scope names `tests/test_atoms_cli.py` as must-pass unmodified, but it is absent from the Validation command list and from the files list.
8. `retarget` and `delete` have no named test coverage; "unchanged behavior" for them is unverifiable.
9. Wrapper signatures/names in `operations.py` and whether CLI callers/imports need updating are unstated.
10. Meaning of `AtomsService(root)` — what `root` denotes (store root, desk root, repo root) is unspecified.
11. "Every write goes through doc_io" has no acceptance criterion or test enforcing it.
12. `Done When` grep `def merge_atom` does not prove service ownership or that operations.py delegates.
