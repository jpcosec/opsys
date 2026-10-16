RESTATEMENT:
1. Verify dependency `task-rw-f3-tasks-service` is closed, then promote/activate this task (currently `status: deferred`) per the phase-gated flow.
2. Read the two bound pills: `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md` and `desk/contexts/pill-012-create-operations-transactional-rollback.md`.
3. Create `deskops/services/atoms.py`.
4. Move the atom create/edit/split/merge/retarget/delete methods out of `deskops/operations.py` into that service.
5. Move `_rewrite_inbound_atom_references` (with the F0 tokenized fix) alongside them.
6. Convert the moved methods to use doc_io transactions.
7. Reduce the corresponding `deskops/operations.py` methods to delegating wrappers.
8. Wrap merge and split in a `DocTransaction` so rewritten referrers roll back (D7).
9. Add a merge failure-injection test to `tests/test_atoms_merge.py`.
10. Run: `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`.
11. Run: `pytest tests`.
12. Confirm done-when: atom code in service, merge rollback restores referrers, suite passes.
13. Make the task's atomic commit.

AMBIGUITIES:
1. `files:` lists only 3 paths, but validation names 4 different test files (`tests/test_atoms_cli.py`, `test_atoms_split.py`, `test_atoms_create_from_source.py` not in `files:`). Are those existing, and should they be edited?
2. "the atom methods" is never enumerated; exact method names/signatures to move are unspecified.
3. Location of `_rewrite_inbound_atom_references` is unstated (assumed `operations.py`, not written).
4. "the F0 tokenized fix" is undefined in this doc — no description, no source, no diff.
5. "D7" is referenced but not defined here; no decision text in the task.
6. "doc_io transactions" / `DocTransaction` import path, API, and nesting semantics are not given.
7. Whether create/edit/delete/retarget also need transaction wrapping, or only merge/split, is unstated.
8. Whether merge and split share one transaction or get separate ones is unstated.
9. "operations.py keeps only wrappers" — no requirement stated on preserving signatures, deprecation markers, or package `__init__`/export changes.
10. "unchanged behavior" has no definition (CLI output, error messages, ordering, exit codes).
11. Failure-injection test: which failure to inject, injection mechanism, and assertions are unspecified.
12. Done-when mentions only merge rollback, but implementation path wraps merge *and* split; split rollback acceptance is missing.
13. Validation does not state a baseline (pre-existing failures) or whether `pytest tests` duplicating the targeted run is the intended full gate.
14. Plan file `runs/planning/deskops-rewrite-inventory.md` is referenced but not in `files:`; whether to read it is unclear.
15. Task doc is `deferred`; the procedure to verify the `depends_on` task is closed/completed is not stated.
16. No statement on whether `deskops/services/` package exists or needs an `__init__.py`.
17. Pills are listed as paths with no instruction on what to do with them.
18. "Open Ambiguities: None" contradicts unfilled placeholder sections (`_Explain why…_`, `_Describe…_`, `_State…_`, `_Outline…_`, `_List…_`, `_Name…_`), suggesting the doc is still a template.
19. No acceptance criterion states how "atom code lives in the service" is verified (e.g., no import/grep check).
20. No requirement stated for whether the wrappers must be covered by tests or whether CLI tests already cover them.
