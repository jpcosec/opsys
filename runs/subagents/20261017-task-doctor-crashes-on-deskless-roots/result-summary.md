# Result: task-doctor-crashes-on-deskless-roots

## Changes

- `deskops/cli/commands/doctor.py`
  - `DoctorCLI.run`: moved `unreadable_docs: list[str] = []` next to the other finding accumulators, before `if desk_dir.exists():`.
  - `DoctorCLI.run`: removed the dead `tracked_mds = set(inspection.tracked_surface_docs)` assignment that was immediately shadowed by `tracked_mds: set[Path] = set()`.
  - Removed the now-redundant `unreadable_docs` initialization inside the `if desk_dir.exists():` block.
- `tests/test_doctor_unmodeled_surfaces.py`
  - Added `test_doctor_reports_missing_desk_without_crashing_on_deskless_root`: runs `python -m deskops doctor --root <empty tmp dir>`, asserts exit 1, `Missing desk structure: desk/` in stdout, and no `Unexpected:` in stdout/stderr.

## Validation

- `PYTHONPATH=/tmp/rw/wt/doctor python -m pytest tests/test_doctor_unmodeled_surfaces.py -q`
  - `4 passed`
- `PYTHONPATH=/tmp/rw/wt/doctor python -m pytest tests -q`
  - `336 passed, 3 skipped`
- Manual: `PYTHONPATH=/tmp/rw/wt/doctor python -m deskops doctor --root /tmp/empty-doctor-test`
  - stdout: `Doctor Findings:\n- Missing desk structure: desk/`; exit code 1; no crash text.

## Test against unfixed code

Before the fix, the new test failed:

```
assert 'Missing desk structure: desk/' in ''
E assert 'Missing desk structure: desk/' in ''
...
stderr="Unexpected: cannot access local variable 'unreadable_docs' where it is not associated with a value\n"
```

The standalone unfixed command reproduced the same `Unexpected: cannot access local variable 'unreadable_docs' ...` message with exit code 1.

## Notes / ambiguities

- Cited line numbers matched the real code: dead `tracked_mds` assignment at line 78, shadowing assignment at line 80.
- The full suite initially failed one unrelated test, `tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path`, because the fresh worktree lacks the gitignored `.pi/` directory. Copying the existing `.pi/` skill tree from the main checkout into the worktree (ignored, not tracked) made the suite green. No source or desk files were changed by this.
- No sldb bug encountered. The desk-less path never invokes SLDB store checks.
