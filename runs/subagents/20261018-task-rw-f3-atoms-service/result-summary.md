# task-rw-f3-atoms-service — execution summary

## Changes

- Added `deskops/services/atoms.py` (`AtomsService(root, operations=None)`).
  - Owns `list_atoms`, `reorganize_atoms`, `validate_atoms`, `delete_atom`, `create_atom_from_source`, `split_atom`, `merge_atom`.
  - Owns atom helpers: `_all_atom_paths`, `_build_atom_from_{pill,graph_finding,diagram}`, `_parse_graph_finding_selector`, `_compose_exact_provenance`, `_split_atom_answer_sections`, `_resolve_atom_split_assignments`, `_render_atom_split_redirect_answer`, `_detect_atom_merge_ambiguities`, `_merge_atom_{tags,answers}`, `_render_atom_merge_{appendix,redirect_answer}`, `_validate_atom_path`, `_is_valid_atom_slug`, `_provenance_is_resolvable`, `_find_inbound_atom_references`, `_rewrite_inbound_atom_references`, `_retarget_atom_documents`, `_untrack_atom_document`, `atom_folder_axis`, `_atom_doc_path`.
  - Follows the service pattern: shared storage/IO helpers delegate to `DeskopsOperations`; all writes go through `doc_io`.
- `deskops/operations.py`: atom methods reduced to delegating wrappers; added lazy `atoms` property and `_atoms` field. Kept `show_task`, `_lifecycle_gates`, `_add_closeout_facts`, `show_artifact`, `_reference_points_to_atom`, and shared `_write_doc`/`_read_doc` in operations.
- `tests/test_atoms_transactions.py`: two failure-injection tests.
  - Merge: forces `doc_io.track_document_file` to fail on the first call (after the referrer rewrite); asserts source/target/referrer bytes and `check_store` unchanged.
  - Split: forces failure on the second track call (after the first new atom is written); asserts source bytes, both would-be child files absent, and `check_store` unchanged.

## Validation (final runs, after final edits)

- `PYTHONPATH=/tmp/rw/wt/atomsvc python -m pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py -q`
  - `15 passed in 2.73s`
- `PYTHONPATH=/tmp/rw/wt/atomsvc python -m pytest tests -q`
  - `404 passed, 3 skipped in 317.35s`
- `grep -n 'def merge_atom' deskops/services/atoms.py`
  - `321:    def merge_atom(`

## Test against unfixed code

- Exported HEAD with `git archive HEAD` to `/tmp/rw/f0/atomsvc-baseline/repo`, symlinked the sibling `sldb`, copied `tests/test_atoms_transactions.py`, then ran it with `PYTHONPATH` pointing at the baseline:
  - `2 passed in 3.67s`.
- HEAD already had `DocTransaction` around merge/split (from the F2 transactional-doc-io work), so the injection tests are regression guards rather than proofs of a new rollback implementation.

## Anomalies / ambiguities

- Task line numbers are stale as expected (`merge_atom` was at 683; validation range 952-1405 etc. shifted); located code by grep/AST.
- Implementation Path says "Wrap merge_atom and split_atom each in one DocTransaction"; both already were wrapped at HEAD. The move preserved them.
- "Owns atom create, edit, ...": there is no atom-specific edit method. Generic `edit_artifact_field` remains in `operations.py`; atom editing through it now resolves `_atom_doc_path` via the service wrapper.
- Scope says the four existing test files pass unmodified, so failure-injection tests were added in a new file instead of editing `test_atoms_merge.py`/`test_atoms_split.py`.
- No sldb bugs observed; no sldb files changed.
