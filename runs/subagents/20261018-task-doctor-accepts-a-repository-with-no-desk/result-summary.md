# Task: task-doctor-accepts-a-repository-with-no-desk

## Changes

- `deskops/cli/commands/doctor.py` — `DoctorCLI.run`
  - Replaced the `absent` branch that appended `desk/` to `missing_desk_files`.
  - When `inspect_desk(root).classification == "absent"` and `desk/config.json` does not exist: print
    `No desk at <root>: this repository has no desk/ (run deskops init to create one).` and return `0`.
  - Early return happens before findings, repair scaffolding, and store checks, so `--repair` is a no-op there (prints the same message).
  - Partial desks still go through the existing missing-structure/legacy logic and exit `1`.
  - Doctor help text in `deskops/cli/registry.py` does not describe the absent case, so it was left unchanged.

- `tests/test_cli.py`
  - Added `test_doctor_accepts_a_repository_with_no_desk` (exit 0, exact message, no findings/repair hint, no `desk/` created).
  - Added `test_doctor_repair_does_not_scaffold_a_repository_with_no_desk` (exit 0, no `Scaffolded missing desk/ structure.`, no `desk/` created).
  - Added `test_doctor_still_reports_a_partial_desk` (desk with `Board.md` + config but no drawer/phase → exit 1).

- `tests/test_doctor_unmodeled_surfaces.py`
  - Updated the F0 deskless-root regression test (`8121c5e` intent preserved: no crash, stderr clean) to expect exit `0` and the new "No desk at ... this repository has no desk/" output instead of "Missing desk structure: desk/". Renamed to `test_doctor_accepts_deskless_root_without_crashing`.

## Validation

- `PYTHONPATH=/tmp/rw/wt/nodesk python -m pytest tests/test_cli.py tests/test_doctor_model_registration.py -q -k doctor`
  - `16 passed, 93 deselected in 69.16s (0:01:09)`
- `PYTHONPATH=/tmp/rw/wt/nodesk python -m pytest tests -q`
  - `544 passed, 3 skipped in 727.03s (0:12:07)`
- Manual CLI (temporary empty dir):
  - `doctor --root <dir>` → `No desk at /tmp/tmp.vKo6HwaU8w: this repository has no desk/ (run deskops init to create one).`, exit 0
  - `doctor --root <dir> --repair` → same line, exit 0, directory still empty (no `desk/`)

## Test against unfixed code

- Temporarily restored `HEAD:deskops/cli/commands/doctor.py`, then ran:
  `PYTHONPATH=/tmp/rw/wt/nodesk python -m pytest tests/test_cli.py tests/test_doctor_unmodeled_surfaces.py -q -k "accepts_a_repository_with_no_desk or deskless_root"`
  - `2 failed, 103 deselected in 1.10s`
  - Both failures show `assert 1 == 0`; output was `Doctor Findings:\n- Missing desk structure: desk/` with exit 1.
- Fixed file restored immediately after (`git diff` confirms only intended changes).

## Notes / ambiguities

- Task wording "config without desk/" describes an impossible state: `desk/config.json` lives inside `desk/`, and `inspect_desk` classifies a root as `absent` only when the `desk` directory does not exist. The guard is implemented literally but the config check is unreachable for `absent`.
- An existing `desk/` directory containing only a `config.json` (no Board/task/context docs) is classified `empty` by `inspect_desk`; doctor reports it healthy (exit 0, "Desk is healthy."). That is pre-existing behavior and was left untouched, as the task scoped changes to the `absent` branch.
- Full suite runtime was ~12 minutes here, not ~3 minutes.
- No sldb bug encountered.
