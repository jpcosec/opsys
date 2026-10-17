RESTATEMENT:
1. Open `deskops/cli/commands/doctor.py`; find the findings section that reads `unreadable_docs` and the `if desk_dir.exists():` block where it is currently initialized.
2. Move `unreadable_docs: list[str] = []` to before the `if desk_dir.exists():` block so it is bound on every path.
3. Delete the dead/shadowed `tracked_mds = set(inspection.tracked_surface_docs)` assignment (reported near line 78, shadowed near line 80); keep the surviving statement.
4. In `tests/test_doctor_unmodeled_surfaces.py`, add a regression test that: creates an empty temp dir, runs `python -m deskops doctor --root <tmpdir>`, asserts exit code 1, asserts the missing-desk-structure finding text appears in stdout, asserts no `Unexpected:` in stderr.
5. Run `pytest tests/test_doctor_unmodeled_surfaces.py`.
6. Run `pytest tests`.
7. Manually confirm `python -m deskops doctor --root /tmp/empty` prints the missing-desk-structure finding with no `Unexpected:`.

AMBIGUITIES:
1. `status: deferred` — whether the executor may start this task now or must promote it from drawer first is unstated.
2. The literal stdout substring for the "missing-desk-structure finding" is not given; the required assertion cannot be written exactly.
3. Whether `tests/test_doctor_unmodeled_surfaces.py` already exists (append) or must be created is unstated.
4. Test harness not specified: subprocess vs `CliRunner`/in-process changes how stdout/stderr are captured and whether `Unexpected:` lands on stderr.
5. Line numbers 78/80 are asserted but not shown; which `tracked_mds`-related statement is dead vs kept is unverifiable from the doc.
6. "Empty root" definition (truly empty dir vs dir lacking only `desk/`) is not specified.
7. Task acknowledges exit code 1 does not prove the fix, but provides no other concrete pass signal beyond the unspecified finding string.
8. `runs/planning/deskops-rewrite-inventory.md` (finding X1/phase F0) is referenced but its contents or authority are not provided.
9. No requirement stated for whether `--repair` scaffolding path must be re-verified or covered by the new test.
