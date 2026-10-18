# Result summary — task-ritual-steps-are-prose

## Changed files and functions

- `deskops/models/ritual.py`
  - Removed `RitualDoc.__containment__ = {"steps": ["StepDoc"]}`.
  - Removed the `step_details` composition (`__compositions__`), because its source was StepDoc paths and prose steps are not document refs.
  - Removed the generated `## Step Details` section from `RitualDoc.__template__`.
  - Updated the `steps` field description to say prose, not document references.
- `tests/fixtures/model_contract_hashes.json`
  - `RitualDoc`: `8189f904…` -> `fd5777c6019cce9e2c3425026376c9de410e9f8c9c66fe52f88a26a8e8f398d6`.
- `tests/test_composition.py`
  - Replaced `test_ritual_doc_renders_composed_step_details` with `test_ritual_doc_round_trips_prose_steps_containing_colons`; removed the `StepDoc` import.
- `tests/test_graph_declared_edges.py`
  - Added an explicit assertion that `ritual-phase` emits no `steps` role edge.
- `tests/test_desk_sync.py`
  - Added `test_desk_update_apply_resigns_a_moved_model_contract`, covering a corrupted RitualDoc contract hash, dry-run report, `--apply` re-sign, and clean subsequent update.
- `tests/fixtures/golden/help/deskops_add_ritual.txt`
  - One line changed to the new `--steps` help text (not a `tests/fixtures/golden/output` diff).
- `deskops/cli/commands/desk.py`
  - Added `moved_model_contracts(root, entries)`.
  - `desk update` now reports moved deskops model contracts, and `--apply` runs `python -m sldb models update <Model> --store .sldb --pythonpath <deskops checkout>` before the store check.
- `desk/rituals/phase.md`
  - Re-rendered through `RitualDoc`; the two steps containing `": "` are YAML-quoted strings. The duplicate hand-written `## Steps` body section was removed.
- `desk/rituals/{execution,testing,closeout}.md`
  - Removed the now-obsolete trailing `## Step Details` section so the new template does not absorb it into `completion`.
- `desk/rituals/ritual-deployment-ritual.md`
  - Removed the duplicate `## Steps` body that would otherwise be absorbed into `completion`.
- `.sldb/`
  - `sldb models update RitualDoc`, tracked `desk/rituals/phase.md` as `RitualDoc:ritual-phase`, and `sldb stores update`.
  - New: `.sldb/core/documents/RitualDoc/ritual-phase.yaml`.

## Migration / desk update coverage

The existing `changed_models` path in `scripts/migrate_desk_stores.py` already plans `sldb models update <model>`; `desk update --apply` did not. It now does, via `moved_model_contracts`, so a store whose RitualDoc contract moved is re-signed by `deskops desk update --apply`.

## Validation commands and final lines

1. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m pytest tests/test_model_templates.py tests/test_graph_declared_edges.py tests/test_model_contract_snapshot.py -q`
   - `22 passed in 0.87s`
2. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m pytest tests/test_desk_sync.py -q`
   - `5 passed in 68.37s`
3. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m pytest tests/test_output_goldens.py -q`
   - `7 passed in 241.48s`
4. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m pytest tests -q`
   - `460 passed, 3 skipped in 996.04s`
5. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m sldb stores check --store .sldb --format json`
   - `PASS: store integrity — 228 documents in 17 models`, `moved_contracts: []`
6. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m sldb edges unresolved --store .sldb --local`
   - `0 unresolved reference(s)`
7. `PYTHONPATH=/tmp/rw/wt/ritualsteps python -m deskops desk update --root .`
   - No `Moved model contracts` line; still exits 1 only because the worktree store reports pre-existing `Copied deskops models`. `--apply` was not run against this worktree, per instruction.

## Test against the unfixed code

Baseline targeted run before edits:
`PYTHONPATH=/tmp/rw/wt/ritualsteps python -m pytest tests/test_model_templates.py tests/test_graph_declared_edges.py tests/test_model_contract_snapshot.py -q` -> `22 passed`.

Concrete old-model reproduction (loaded `git show HEAD:deskops/models/ritual.py` as a temporary module):
```
old model containment: {'steps': ['StepDoc']}
old model declared edges: 10 {'contains'}
first: contains steps 'sldb://unresolved_ref/1. Identify the ready dependency layer …'
new model edges: 0
```
So the old contract emitted 10 ritual `contains` edges for phase.md's prose steps; the new contract emits none.

## Task issues / ambiguities

- The task cites files, not line numbers; no line-number drift to resolve.
- The task said the existing changed-models path might already cover `desk update`; it did not, so `desk update` was extended.
- `desk update --root .` still reports pre-existing `Copied deskops models` for this worktree; unrelated to RitualDoc and not repaired here.
- sldb behavior observed (not fixed, since it belongs to sldb): section-boundary extraction lets the last template field absorb trailing hand-written sections. Example with the new template and the pre-cleanup `desk/rituals/execution.md`:
  ```
  PYTHONPATH=/tmp/rw/wt/ritualsteps python -c "from deskops.models import RitualDoc; from sldb.runtime.validation import extract_model_data; print(extract_model_data(RitualDoc, open('desk/rituals/execution.md').read())['completion'][-70:])"
  ```
  output tail was `… handoff gate.\n\n## Step Details\n\n_Generated from the step references above._`
  Removing the obsolete trailing sections avoided polluting `completion`.
- No `tests/fixtures/golden/output` goldens changed; only the `add ritual --help` golden changed, matching the new field description.

## Supervisor note

- The .sldb changes were regenerated in main instead of applied from the worktree: `sldb models update RitualDoc`, then `sldb doc track desk/rituals/phase.md --model RitualDoc --name ritual-phase`, then `stores update`. Result: `stores check` PASS (239 documents) and `edges unresolved --local` 0.
- The worker re-rendered desk/rituals/*.md by hand to drop the `## Step Details` sections that the old composition generated, plus a duplicate `## Steps` body. With the new contract those headings are undeclared, and deskops would refuse to rewrite the files (83c1776). These are model-generated sections, not authored text.
- This patch was in main's working tree before the commit, and since that checkout is the package federated stores import, sldb-04 saw RitualDoc's contract move early (sldb 25d1ca21 re-signed it to this same contract). From now on, model changes stay in a worktree until their commit.
