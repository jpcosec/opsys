RESTATEMENT

1. Open `deskops/cli/commands/doctor.py`; locate the `if desk_dir.exists():` block and the later findings section; confirm where `unreadable_docs` is currently defined and its exact annotation.
2. Move that definition (`unreadable_docs: list[str] = []`) to above the `if desk_dir.exists():` line so it is bound on every code path.
3. Inspect the `tracked_mds` lines (~78-80); delete the dead assignment that is immediately re-assigned by `tracked_mds = set(inspection.tracked_surface_docs)`, keeping the live one.
4. Grep the same block for any other name read after the block but bound only inside it; fix only if part of the same defect class (scope says doctor.py only).
5. Add one regression test in `tests/test_doctor_unmodeled_surfaces.py`: create an empty tmp root via `tmp_path`, run `python -m deskops doctor --root <tmpdir>` as a subprocess, assert return code == 1, assert the missing-desk-structure finding text in stdout, assert `"Unexpected:"` absent from stderr.
6. Run `pytest tests/test_doctor_unmodeled_surfaces.py`.
7. Run `pytest`.
8. Run `python -m deskops doctor --root <empty tmp dir>` manually to confirm clean output (repo rule for CLI changes).
9. Commit the scoped change as the task's atomic commit.

AMBIGUITIES

1. Contradiction: Scope says drop the dead `tracked_mds` assignment at line 78 that line 80 shadows; Implementation Path step 2 says delete the "shadowed `tracked_mds = set(inspection.tracked_surface_docs)`" line. Both quotes are the same expression text, so which line to delete is undecidable without reading the file.
2. No acceptance criterion for the exact finding string/identifier for "missing-desk-structure"; the stdout assertion cannot be written precisely.
3. Exit code 1 is stated to be insufficient proof, so correctness depends entirely on that unknown string (#2).
4. Test harness convention of the existing `tests/test_doctor_unmodeled_surfaces.py` (subprocess vs `CliRunner`) is not stated; the doc implies subprocess but does not require it.
5. Whether `unreadable_docs` is currently annotated `list[str]` inside the block (affects the literal edit) is unknown.
6. Unknown whether other finding variables share the same defect; task claims only `unreadable_docs`, unverifiable from the task text.
7. Task `status: deferred` / `source:drawer`; nothing states whether promotion to the active board is required before implementation (repo rules require a promotion commit first).
8. Unknown whether an empty root lacks other artifacts `doctor` needs (e.g. `.sldb` store), which could change output or exit code.
9. `--repair` behavior on desk-less roots is listed in Resolved Decisions but has no test or acceptance criterion.
