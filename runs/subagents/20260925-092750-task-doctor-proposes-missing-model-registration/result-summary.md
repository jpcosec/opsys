# Result summary — task-doctor-proposes-missing-model-registration

Role: executor
Task: task-doctor-proposes-missing-model-registration

## What was done

- `deskops/cli/commands/doctor.py` now compares `MODEL_REFS` against the local store's
  registered models (via `SLDBBootstrap._registered_model_names`, reuse not reimplementation).
- Dry run: emits finding `Unregistered models: <sorted names>. Run
  `deskops desk update --apply` ...` (proposal names a runnable command).
- `--repair`: calls the same `SLDBBootstrap.init_local_store` path `deskops desk update --apply`
  uses; success → `Registered missing models.` under Repairs applied; failure → explicit
  `Manual repair required` line so exit accounting stays honest.
- Store index unreadable → explicit note finding `Could not read the local .sldb store
  index; unregistered-model check skipped.` (broad Exception catch, matching desk update).
- No `.sldb` → check skipped entirely (store-check-crash finding covers the state).

## Guardrails honored

- pill-doctor-separates-desk-repair-from-sldb-health: doctor delegates store queries to
  SLDB/bootstrap; no new registration logic.
- pill-drift-checks-are-review-surfaces-not-mutators: read-only default; mutation only on
  explicit `--repair`.
- pill-real-cli-surfaces-prove-operator-contracts: contract proven on real CLI in
  `.tmp/deskops-cli-test` (dry run finding → --repair registers → healthy exit 0).

## Validation

- tests/test_doctor_model_registration.py: 4 passed (see validation.log).
- Full suite: 296 passed.
- Sandbox CLI proof: drifted store (RoutineDoc removed from store_index.yaml) → finding;
  --repair → registered; rerun → "Desk is healthy." exit 0.

## Handoff

Testing gate satisfied; ready for closeout.
