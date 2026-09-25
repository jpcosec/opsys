---
id: task-doctor-proposes-missing-model-registration
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files:
- deskops/cli/commands/doctor.py
- deskops/cli/commands/desk.py
- deskops/bootstrap.py
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:health
- topic:cli
---

# Doctor proposes fixes for missing model registration

## Rationale

Observed in a downstream deskops project: `deskops add task` failed because `RoutineDoc` was not registered in that project's local `.sldb` (store created before `RoutineDoc` existed in `MODEL_REFS`). Tasks could not become active and stayed in the drawer. `deskops doctor` had been reporting drift there for a while but never named the unregistered-model gap or proposed the repair.

The detection already exists in `deskops desk update` (dry run reports `Unregistered models: ...`; `--apply` calls `bootstrap.init_local_store`, registers missing models, tracks/untracks docs, and refreshes indexes). Doctor checks desk structure, tracking, readability, and invalid docs, but never compares `MODEL_REFS` against the store's registered models, so it cannot propose this fix.

## Goal

`deskops doctor` detects models in `MODEL_REFS` that are not registered in the local store and reports them as a finding with a concrete proposal, pointing at the existing repair path (`deskops desk update --apply`) instead of duplicating registration logic, per the doctor/store-boundary pill.

## Resolved Decisions

- Reuse `SLDBBootstrap._registered_model_names` and `MODEL_REFS`; do not re-implement store inspection inside doctor.
- Proposals must name runnable commands (real CLI surfaces prove operator contracts).
- Default doctor mode stays read-only: it reports the finding and proposes `deskops desk update --apply` as the repair path.
- `doctor --repair` performs the repair by calling the same `SLDBBootstrap.init_local_store` code path `deskops desk update --apply` uses (additive, idempotent, non-destructive); it does not register through new doctor-local logic.
- Run the unregistered-models check only when the local store index loads successfully; if the index cannot be read, skip the finding because the existing store-check-crash finding already covers the unknown state.
- Unregistered models are only checked when `.sldb` exists, matching the guard used by `deskops desk update`.

## Open Ambiguities

None. The two former ambiguities are resolved in Resolved Decisions.