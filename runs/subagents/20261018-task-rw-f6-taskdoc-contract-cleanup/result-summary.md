# task-rw-f6-taskdoc-contract-cleanup — executor summary

## Changes

### deskops/models/task.py
- `TaskDoc.model_config` is now `{"extra": "ignore"}`.
- Removed the `frontmatter: dict | None` field, `_merge_frontmatter`, and the `render_payload` override.
- Replaced the `⸢rev,dict•frontmatter⸥` template block with one marker per frontmatter field, in the previous byte order: `id` (rev), `status`/`summary` (optrev), `tags` (rev,list), `current_node`/`history`/`references`/`depends_on`/`pills`/`files`/`task_type`/`inherits_from`/`inherit_acceptance_context`/`atoms`/`from_drawer` (optrev / optrev,list).
- `current_node`, `pills`, `atoms` moved from `__containment__` to `__references__` with `__reference_models__` (`RitualDoc`, `PillDoc`, `AtomDoc`); no `__containment__` remains.
- `from_drawer` removed from `__references__` and `__reference_models__`; it remains a plain field.
- Kept `_omit_unset_from_drawer`; rewrote its docstring to say it keeps *rendered documents* byte-identical, not the contract hash (the field schema is hashed).
- Added module constant `_ABSENT_FRONTMATTER_DEFAULTS` and a `model_validator(mode="before")` `_apply_absent_frontmatter_defaults` that drops `None` values for the migrated optrev frontmatter fields. sldb extracts an absent marker as `None`; without this, defaults would be replaced by `None` and both extraction and byte-identical rendering would break. This is the only mechanism replacing the removed merge validator.

### tests/fixtures/model_contract_hashes.json
- TaskDoc hash updated from `14895c9f...20bd` to `2fe27e8d653b2f100f3e4cf8bcbf21f38aa3ef2e126a6074e00aafe78358bf9b`.

### tests/test_graph_declared_edges.py
- Updated module docstring to the new declarations.
- Renamed the containment test to `test_declared_references_become_edges_with_the_field_as_role`.
- `test_from_drawer_is_provenance_not_a_declared_reference` now asserts that no `from_drawer` declared edge exists.

### tests/test_composition.py
- Removed stale `routine` and `checklists` keys from `test_task_doc_keeps_machine_metadata_in_frontmatter`; they are no longer fields and `extra: ignore` deliberately drops them. Required to keep `pytest tests` green.

### runs/planning/taskdoc-unknown-keys.md
- New read-only pre-scan result: 46 stores, 447 TaskDoc files scanned, 306 files with unknown top-level keys (`routine`, `checklists`, and legacy keys such as `created`, `domain`, `priority`, `subtasks`, `resolver_role`), plus 17 tracked entries whose files are missing. Other repos were only read.

### .sldb
- `sldb stores update --store .sldb` updated `.sldb/core/models/TaskDoc.yaml` (model/contract hashes) and `.sldb/core/store_index.yaml` (`store_hash`). No document shard content changed.
- TaskDoc document edge shards now contain only `references` edges; no `contains` and no `from_drawer` declared edges.

## Byte-identical render check

Saved `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` before editing to `/tmp/rw/f0/out/taskdoc/renders-before/` and re-rendered after to `renders-after/` for:

- 5 `desk/tasks/*.md` (Board.md excluded)
- 7 `desk/drawer/tasks/*.md` (Board.md excluded)
- 3 task files in `tests/fixtures/golden_desk/`

Result: 15/15 identical. None of these files was in the unknown-key list.

## Validation commands and final results

- `PYTHONPATH=/tmp/rw/wt/taskdoc python -m pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py -q`
  - `8 passed in 0.62s`
- `PYTHONPATH=/tmp/rw/wt/taskdoc sldb stores update --store .sldb`
  - first run: `Updated store at /tmp/rw/wt/taskdoc/.sldb`; `Semantic index: 224 processed...`
  - second run: `0 processed, 0 missing` (idempotent)
- `PYTHONPATH=/tmp/rw/wt/taskdoc sldb edges check --store .sldb`
  - `Edges OK`, exit 0. No contains-cardinality error from TaskDoc fields.
- `PYTHONPATH=/tmp/rw/wt/taskdoc python -m deskops graph missing --root .`
  - exit 1; final line `6 missing, 108 informational`
  - The 6 missing targets are pre-existing non-TaskDoc-reference findings from active tasks/issues (`source_file:deskops/services/closure.py`, `source_file:deskops/cli/render.py`, `test_file:tests/fixtures/model_contract_hashes.json`, and issue source-file references). The TaskDoc change added no missing target and removed the `from_drawer` provenance scan behavior unchanged (`PROVENANCE_FIELDS` untouched).
- `PYTHONPATH=/tmp/rw/wt/taskdoc python -m pytest tests -q`
  - `417 passed, 3 skipped in 416.59s (0:06:56)`, exit 0.

## Commands run against unfixed code

None. The first full `pytest tests` was run after the model change; it reported `1 failed, 416 passed, 3 skipped`, the failure being the stale `routine`/`checklists` expectation in `tests/test_composition.py`, fixed above.

## Task text issues / ambiguities

- Cited line numbers were stale: `deskops/graph/extract_edges.py:181-190` and `tests/test_graph_declared_edges.py:131` no longer point at those blocks after F2–F5; located by grep.
- The task says to drop the validator but does not say how absent optrev markers should keep the old field defaults. sldb's extractor emits `None` for an absent marker (verified directly), so explicit per-field markers plus unchanged field types require the added `_apply_absent_frontmatter_defaults` validator. Without it, extraction fails validation for drawer/golden files missing optional keys and re-rendering is not byte-identical.
- `tests/test_composition.py` was not in the task's `files` list but is asserted by the task's `pytest tests` gate; it still expected the removed `routine` and `checklists` keys under `extra: allow`.

## sldb observations

No sldb bug found. Behavior noted (not a defect): an absent `rev` or `optrev` marker extracts as `None` rather than being omitted. Relevant sldb files: `src/sldb/core/data_extractor.py` and `src/sldb/core/contracts/marker.py`. Reproduce with any model whose template declares a marker and whose document omits that key.
