RESTATEMENT:

1. Locate inputs I don't have: `runs/planning/deskops-rewrite-inventory.md` (D7), `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md`, `desk/contexts/pill-012-create-operations-transactional-rollback.md`, and the output of `task-rw-f3-tasks-service`.
2. Read `deskops/operations.py` to inventory all atom functions (create, edit, split, merge, retarget, delete) plus `_find_inbound_atom_references` / `_rewrite_inbound_atom_references`.
3. Read the existing `deskops/services/` modules (esp. the tasks service from the dependency) to copy the `XService(root)` constructor pattern, imports, and how `doc_io` is called.
4. Read the `DocTransaction` implementation (location/API) in `doc_io` to learn the context-manager and tracking/commit-rollback seams.
5. Create `deskops/services/atoms.py` with `class AtomsService(root)` owning atom create, edit, split, merge, retarget, delete; move `_find_inbound_atom_references` and `_rewrite_inbound_atom_references`; route every write through `doc_io`.
6. Rewrite the corresponding functions in `deskops/operations.py` as thin delegation wrappers to `AtomsService`.
7. Wrap the full `merge_atom` body in one `DocTransaction`.
8. Wrap the full `split_atom` body in one `DocTransaction`.
9. In `tests/test_atoms_merge.py`, add a failure-injection test that makes the doc_io track step raise after the referrer rewrite; assert every touched file's bytes equal originals and `sldb stores check` is unchanged.
10. In `tests/test_atoms_split.py`, add the analogous failure-injection test raising after the first new atom is written.
11. Run `pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py`.
12. Run `pytest tests`.
13. Verify `grep -n 'def merge_atom' deskops/services/atoms.py` matches and `operations.py` only delegates.

AMBIGUITIES:

1. I only received the task document; `operations.py`, `doc_io`/`DocTransaction`, `deskops/services/`, the pills, inventory D7, and the `task-rw-f3-tasks-service` output are not provided, so every concrete API name and signature must be guessed from the repo.
2. The `doc_io` "track step" is unnamed — no module, method, or exception name given for the raise point.
3. `DocTransaction` import path, constructor signature, and commit/rollback semantics are unspecified.
4. "after the referrer rewrite (merge)" is ambiguous when merge rewrites multiple referrers — which rewrite the raise should follow is unstated.
5. "after the first new atom is written (split)" — which write counts as the "first new atom" (ordering) is unstated.
6. "every touched file's bytes equal the originals" — how touched files are enumerated (transaction-tracked paths vs a fixed list) is unstated.
7. "`sldb stores check` is unchanged" — the baseline snapshot and comparison method are unspecified.
8. Whether the moved reference helpers become `AtomsService` methods or stay module-level functions is unspecified.
9. "operations.py keeps only wrappers" — whether public function names/signatures/return values must stay identical is unspecified.
10. `AtomsService(root)` "owns atom create, edit, split, merge, retarget and delete", but the listed tests cover only create/merge/split/cli; retarget and delete have no named acceptance test.
11. Done When's `grep -n 'def merge_atom'` only requires a match; it does not state there must be no second definition elsewhere.
12. Open Ambiguities says "None" and the task text does not contradict that.
