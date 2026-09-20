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

## F4 (mismo día): capa de formas y suite verde

- `deskops/forms.py`: create/edit/read/promote + `next_gate` (la guarda de cada
  peldaño del status derivado). Decisión registrada en el spec: el archivo de
  task materializa núcleo + intent + acceptance inline.
- La CLI usa la capa en `edit task`; los movimientos de átomos
  (`atoms reorganize`, `atoms delete`) pasan por `store.untrack`/`store.track`
  en vez de escribir el índice de sldb a mano.
- Los 9 rojos que arrastraba F2/F3 se cerraron y la suite quedó **271 passed**.

## Commits

- `eef7e47` F3 T3.1: graph model, 23 relation types + `init_relations`
- `fefa147` F3 T3.3: derived conditions
- `d014d9e` F3 T3.2: derived status ladder
- `79c6bc4` F3 T3.4: `deskops init` in process through pron
- `0a324a6` docs: F1-F3 closed, baseline real y estado del gate
- `0afd5ab` F4 T4.1-T4.3: capa de formas (create/edit/read) + materialización inline
- `3b70dc7` F4 T4.3-T4.5: promote y la guarda de advance sobre la escalera derivada
- `4d2900f` F6 T6.3: los movimientos de átomos van por el seam
- `21f2edb` tests: lifecycle con PYTHONPATH; superficie de verbos del parser
- `8b9dccc` docs: F4 por capas, suite verde, qué falta de F4
