# F4 — Declared graph edges come from the sldb edge index

## What changed

- `deskops/graph/extract_docs.py`
  - Drawer tasks are emitted as `task` nodes (`_iter_doc_paths`), so their id is `task:<frontmatter id>` instead of `drawer_task:<path>`.
- `deskops/graph/extract_edges.py`
  - `extract_declared_edges` now loads the project store through `_load_store_context` (skips roots without a real `.sldb`).
  - `_store_declared_edges` projects sldb schema edges (`references`/`contains`) onto deskops node ids and uses `metadata["field"]` as the role.
  - `_store_unresolved_targets` turns `EdgeIndex.unresolved_references` into `MissingGraphTarget`s, resolving against deskops nodes first so tracked-store gaps do not become false findings.
  - `_declared_fields_for_model` feeds `skip_fields` into `_frontmatter_declarations`/`_declarations_from_mapping`, so tracked documents no longer parse their declared `__references__`/`__containment__` fields locally.
  - Local extraction remains for diagram sources, section refs, YAML-fenced atom declarations, the line path scanner, non-declared model fields, and untracked documents.
  - Drawer-task paths keep the pre-fold behavior for the line path scanner (`_is_drawer_task_path`), so no new findings appear.
- `deskops/models/task.py`
  - Added `__reference_models__` for `depends_on`, `inherits_from`, `from_drawer` (TaskDoc).
- `pyproject.toml`
  - `structuredLanguageDB>=0.1.12`.
- `tests/fixtures/model_contract_hashes.json`
  - Updated TaskDoc contract hash to `14895c9f3f8dd453ee52b39724fa9d6d8eb61d24107d57066782c63027eb20bd`.
- `.sldb/core/models/TaskDoc.yaml`, `.sldb/core/store_index.yaml`
  - Refreshed by the sldb store update.
- `tests/fixtures/golden/graph_snapshot.kg.json`, `tests/fixtures/golden/graph_snapshot.nx.json`
  - Regenerated with `--update-golden`; only the drawer node moved from `drawer_task:...` to `task:task-golden-drawer`.
- `runs/planning/graph-missing-baseline.txt`
  - Pre-change baseline.
- `runs/planning/graph-id-mapping.md`
  - Old→new id rules and concrete drawer mappings.

`deskops/graph/snapshot.py`, `deskops/services/closeout_gates.py`, `deskops/graph/self_reflection.py`, `deskops/operations.py`, `deskops/cli/parser.py`, and `tests/fixtures/knowledge_graph/static_desk_source_graph.json` needed no edits: their cited line numbers are stale and they contain no `drawer_task:<path>` literals. `tests/test_graph_extract_docs.py` already asserts only unchanged id schemes.

## Validation (final)

- `PYTHONPATH=/tmp/rw/wt/edgeidx python -m pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py -q`
  - `27 passed in 1.36s`
- `PYTHONPATH=/tmp/rw/wt/edgeidx python -m deskops graph missing --root .`
  - exit 1; `6 missing, 102 informational` (108 findings, same lines as the baseline).
- Baseline comparison as `(kind, mapped source id, mapped target id)` sets:
  - baseline 23 unique tuples, current 23 unique tuples, added 0, removed 0.
  - The 108 line count differs from 23 because the same `(kind, source, target)` appears once per provenance locator.
- `PYTHONPATH=/tmp/rw/wt/edgeidx python -m pytest tests -q`
  - `404 passed, 3 skipped in 359.09s`
- `PYTHONPATH=/tmp/rw/wt/edgeidx python -m pytest tests/test_model_contract_snapshot.py -q`
  - `2 passed in 0.27s`
- `PYTHONPATH=/tmp/rw/wt/edgeidx python -m pytest tests/test_output_goldens.py -q --update-golden`
  - `6 passed in 100.58s`

## Tests run against the unfixed code

- Before edits: `PYTHONPATH=/tmp/rw/wt/edgeidx python -m pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py -q` → `27 passed in 1.42s`.
- During diagnosis, a clean `HEAD` worktree (`/tmp/rw/old-edgeidx`) ran the two tests that initially failed after the change (`test_drift_check_is_quiet_on_a_fresh_desk`, `test_deleting_the_drawer_entry_leaves_the_task_valid`) → `2 passed in 9.21s`. This exposed that linked-store unresolved refs were being mapped onto local nodes; `load_edge_index(..., include_linked=False)` fixed it.

## Ambiguities / task corrections

- The task says `graph missing` must report the same dangling set as the baseline. Raw sldb `unresolved_references` does not: it reports ritual `steps` prose, Board paths written without `.md`, and bare `depends_on` ids whose documents are untracked but present as deskops nodes. The implementation therefore keeps the existing `_looks_like_reference` filter and resolves each unresolved value against deskops node ids before reporting it.
- Linked stores must be excluded from the index read (`include_linked=False`); otherwise the deskops owner store's Board doc is mapped onto the local `board:board-001` node and produces false `unknown_path` findings in fresh desks.
- Folding drawer tasks into `task` makes the per-line path scanner apply to them. Since the baseline had no findings from drawer tasks, `_is_drawer_task_path` preserves the old scanner scope.
- Cited locations `operations.py:1304,1863`, `parser.py:323`, `self_reflection.py:164,173,450`, and `static_desk_source_graph.json` are stale or contain no old drawer ids; no change was required.

## sldb issue observed (not fixed)

File: `/home/jp/proyectos/SLDB_1/sldb/src/sldb/store/edge_index/` (shard rebuild/`stores update`).

After adding `__reference_models__` to TaskDoc and running:

```bash
PYTHONPATH=/tmp/rw/wt/edgeidx python -m sldb stores update --store .sldb --pythonpath .
```

the model index updated its contract hash, and the three TaskDoc shards were rewritten, but they did not contain the new `depends_on` unresolved-reference edges. A following `sldb edges rebuild --store .sldb --pythonpath .` reported:

```text
Edges: 0 shard(s) written, 0 reused, 0 model(s) walked
```

Only after deleting `.sldb/runtime/edges/TaskDoc/*.yaml` and rebuilding did the shards include the `depends_on` entries:

```text
Edges: 3 shard(s) written, 219 reused, 17 model(s) walked
```

The shard staleness check appears to reuse shards built before the model contract change was applied.
