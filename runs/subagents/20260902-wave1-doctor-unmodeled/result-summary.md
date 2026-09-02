# Result summary

- run_id: 20260902-wave1-doctor-unmodeled
- child_session_path: unavailable-from-api-context
- session_sha256: 73eef8f05626043f7628b6138a477bf6b3bcd24c54e942c763776cd531f9ca40

## Scope implemented

Adjusted doctor untracked-surface detection so it ignores desk markdown that is intentionally not SLDB-modeled, while keeping modeled-but-untracked documents as findings.

## Files touched

- `deskops/workspace.py`
- `deskops/cli/commands/doctor.py`
- `tests/test_doctor_unmodeled_surfaces.py`

## What changed

- Added workspace helpers to classify desk markdown as SLDB-modeled vs intentionally unmodeled by top-level desk family.
- Treated only known modeled desk families as candidates for the doctor untracked check.
- Excluded intentionally unmodeled surfaces such as `desk/drawer/**`, `desk/inbox/**`, `desk/issues/**`, top-level desk notes like `desk/METHODOLOGY.md`, and other non-modeled top-level families such as `desk/features/**` and `desk/logbook/**`.
- Kept doctor output backward-compatible with `Untracked desk documents: ...` while adding explicit text that these are broken tracking/state findings for SLDB-modeled surfaces and listing ignored-by-design surface classes.
- Added dedicated tests covering classification, ignored unmodeled surfaces, and mixed modeled/unmodeled reporting.

## Validation

- Targeted: `pytest tests/test_doctor_unmodeled_surfaces.py -q` -> `3 passed`
- Full: `pytest -q` -> `178 passed`

## Doctor counts

- Before logic (same workspace, pre-fix computation): `before_untracked_count=411`
- After logic (current computation): `after_untracked_count=239`
- Fresh CLI run after change recorded in `doctor-after.txt`.

## Notes

- Working tree intentionally left uncommitted.
- No staged files were created by this task.
