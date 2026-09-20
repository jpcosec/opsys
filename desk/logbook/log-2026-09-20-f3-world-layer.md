# F3: the world layer (relations, derived status, bootstrap)

Date: 2026-09-20
Scope: deskops central workflow harness
Triggered By: deskops rebuilt on pron (task-deskops-rebuilt-on-pron-total-refactor-fireproof-test)

## Summary

Closed F3 of `docs/implementation-plan.md` in the `deskops-pron` worktree: the
23 relation types, the derived conditions, the derived status, and an
in-process `deskops init`. No subprocess is spawned anymore.

## Central Changes

- `deskops/derived_conditions.py` (new): the four spec predicates as
  projections over tracked documents, plus the task slice they are computed on.
- `deskops/derived_status.py` (new): the status ladder over those conditions and
  `tasks_in_status` ("which tasks are in planning?"), read from the store.
- `deskops/bootstrap.py` (rewritten in process): store creation, model
  registration from the spec's `worlds[]`, the 23 relation types, and the
  derived-graph refresh; idempotent.
- `deskops/world.py`: `ensure_store_root` seam for a repo without `.sldb`.
- `deskops/models/plan.py`, `deskops/models/plan_target.py`: `targets`,
  `iterations` and `contract` declared as fields, because a `__containment__`
  over a field that does not exist is dropped on write.
- `spec/world/deskops-world.yaml`: the ladder is declared cumulative (the
  literal reading of `execution` made every later rung unreachable).

## Evidence

- `pytest -q` -> 250 passed / 9 failed (the 9 pre-date F3; table in the plan).
- `pytest -q tests/test_derived_conditions.py tests/test_derived_status.py
  tests/test_bootstrap_world.py` -> 26 passed.
- `python -m deskops --help` -> usage printed.
- `World.refresh()` after `bootstrap_world(<tmp>)` -> no error; second bootstrap
  adds nothing.
- `pron say "which tasks are in planning?"` -> `I don't have "in"`; the
  operational projection has no vocabulary for a derived status yet. Recorded in
  `desk/pron-gap-log.md` and moved to F4 T4.2.

## Commits

- `eef7e47` F3 T3.1: graph model, 23 relation types + `init_relations`
- `fefa147` F3 T3.3: derived conditions
- `d014d9e` F3 T3.2: derived status ladder
- `79c6bc4` F3 T3.4: `deskops init` in process through pron
