RESTATEMENT:
1. Open `deskops/cli/commands/doctor.py`; locate the `if desk_dir.exists():` block, the `unreadable_docs` assignment inside it, and the findings section that reads `unreadable_docs`.
2. Verify the claimed bug: `unreadable_docs` is block-scoped, read after the block; lines 78/80 hold the `tracked_mds` assignment and its shadow.
3. Move `unreadable_docs: list[str] = []` to before the `if desk_dir.exists():` block, and keep or adjust the in-block assignment so it is still populated on the desk-present path.
4. Delete the dead `tracked_mds = set(inspection.tracked_surface_docs)` line that line 80 shadows.
5. Scan the findings section for any other variable read outside the block; initialize each on all paths.
6. Reproduce on an empty root: `python -m deskops doctor --root /tmp/empty`; confirm no `UnboundLocalError` / `Unexpected:`.
7. Add one regression test in `tests/test_doctor_unmodeled_surfaces.py`: create empty tmp dir, run `python -m deskops doctor --root <tmp>` via subprocess, assert returncode in (0, 1), assert the missing-desk-structure finding text appears, assert `Unexpected:` absent.
8. Run `pytest tests/test_doctor_unmodeled_surfaces.py`, then `pytest`.
9. Make one atomic commit for the closed task.

AMBIGUITIES:
1. `status: deferred`; the doc gives no promotion evidence, so it is unclear whether this task is cleared to execute.
2. `--root /tmp/empty` in the repro versus "root without `desk/`": unclear whether the root must be strictly empty (no `.sldb` store) or merely desk-less; doctor behavior may differ.
3. Exit-code acceptance is `0 or 1`; the exact expected code for a desk-less non-repair run is unspecified.
4. Exact missing-desk-structure finding text/string to assert against is not given.
5. Test invocation (`python -m deskops` subprocess) vs any repo test convention (CliRunner/`main.py` harness) is unspecified.
6. Line numbers 78/80 are asserted, not verified; drift or mismatch is undetectable from the doc alone.
7. "all finding variables exist on every code path" names only `unreadable_docs`; which other variables (if any) are block-scoped is unstated.
8. Whether the `--repair` scaffold path must remain working / be tested is implied by Resolved Decisions but not in the Validation list.
9. Whether `tests/test_doctor_unmodeled_surfaces.py` currently exists is not stated.
