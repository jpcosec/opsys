RESTATEMENT:

1. Read `deskops/bootstrap.py` and locate `MODEL_REFS` (reported at lines 14–32) plus `ensure_sldb_available`.
2. Read `deskops/models/` (the `__all__` export list) to see which model classes exist and in what form they can be referenced.
3. Replace the literal 17-entry `MODEL_REFS` with a value derived from `deskops.models.__all__` (map each exported name to whatever model-ref shape `MODEL_REFS` currently uses).
4. Edit `ensure_sldb_available` so the `pip install -e ../sldb` path only runs when invoked by `deskops bootstrap`; `list`, `show`, and `add` no longer trigger installs.
5. Create/update `tests/test_doctor_model_registration.py` to run a fresh init in `tmp_path` and assert the registered model set equals the repo store's model set.
6. Run `pytest tests/test_doctor_model_registration.py`, then `pytest tests`.

AMBIGUITIES:

1. `MODEL_REFS` literal format is unknown (strings, tuples, dataclass instances) — cannot state how to derive it from `__all__`.
2. Whether `deskops.models.__all__` exists and whether every entry is a registerable model ref (vs. base/helper/abstract names) is unknown.
3. `__all__` may export names that cannot be registered; no rule for filtering, ordering, or de-duplication.
4. "same model set as the repo store" has no defined comparison basis: names, refs, or count, and no stated store path (`.sldb`?).
5. The 17 and 21 counts are asserted but unverifiable from this document.
6. Contradiction: Goal says "read commands never pip-install," but Implementation Path says restrict installs to `deskops bootstrap` — this also disables installs for `add` (a mutating, non-read command). Which commands keep install ability is unclear.
7. No stated behavior for what read commands should output when sldb is missing (error? message? exit code?).
8. "fresh init" vs `deskops bootstrap` are used interchangeably; the exact command and required args/flags are unspecified.
9. Whether `tests/test_doctor_model_registration.py` already exists or must be authored is not stated.
10. Test must not perform a real `pip install`; how installs are stubbed/isolated is unspecified.
11. Dependency `task-rw-f5-command-registry` state is unknown; whether its outputs are prerequisites is not described.
12. Referenced pills (`pill-006`, `pill-doctor-*`) and plan file `runs/planning/deskops-rewrite-inventory.md` are not provided, so their constraints cannot be applied.
13. Rationale/Goal/Scope/Implementation Path/Validation/Done When are template placeholders with `_..._` text left in, so intent beyond the three concrete bullets is unconfirmed.
14. No acceptance criterion specifying that removing `MODEL_REFS` literal does not break other importers of `MODEL_REFS`.
