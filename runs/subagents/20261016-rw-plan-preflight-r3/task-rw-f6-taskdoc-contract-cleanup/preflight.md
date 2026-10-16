RESTATEMENT:

0. Do not begin: task status is `blocked`.
1. Verify dependencies are complete: `task-rw-f6-bootstrap-registers-all-models`, `task-rw-f4-graph-on-sldb-edge-index`, `task-rw-f1-model-contract-snapshot`.
2. Read `deskops/models/task.py`; note `extra: allow`, the `frontmatter` field (`exclude=True`), `render_payload`'s hand-kept body-field list, `from_drawer` inside `__references__`, and the `_omit_unset_from_drawer` docstring claim.
3. Snapshot round trips: for every TaskDoc file under `desk/` and `tests/fixtures/`, compute and save `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` (same round trip as `tests/test_composition.py:66`).
4. Run the discovery from `task-rw-f6-migrate-tracking-stores` to enumerate tracked stores; scan those stores for TaskDoc keys outside the model; record the list for closeout.
5. Edit `deskops/models/task.py`: set `extra: ignore`; declare each frontmatter field with its own template marker as `PillDoc` does; move `from_drawer` to a plain field outside `__references__`; rewrite the `_omit_unset_from_drawer` docstring to say it keeps documents byte-identical, not the contract hash.
6. Update `tests/test_graph_declared_edges.py:131` to expect no `from_drawer` frontmatter edge (edge drop per `deskops/graph/extract_edges.py:181-190`).
7. Leave `PROVENANCE_FIELDS` in `deskops/graph/extract_edges.py` unchanged (lines 340-346).
8. Run `pytest tests/test_model_contract_snapshot.py`; copy the printed TaskDoc hash into `tests/fixtures/model_contract_hashes.json`.
9. Re-render every TaskDoc from step 3; compare byte-for-byte against the step 3 snapshots.
10. Validate: `pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py`; `deskops graph missing --root .`; `pytest tests`.
11. Report results and the step 4 key list to the supervisor. Do not commit.

AMBIGUITIES:

1. No rule/file list defines which files are "TaskDoc files under `desk/` and `tests/fixtures/`".
2. The `render_payload` "hand-kept body-field list" is not enumerated.
3. "each frontmatter field with its own template marker (as PillDoc does)" — PillDoc's exact pattern and target field set are not provided.
4. Whether the `frontmatter` field is removed entirely, and how `render_payload` stops repopulating it, is unspecified.
5. The `task-rw-f6-migrate-tracking-stores` "discovery" is not provided (no command, artifact path, or store list); step 2 is not executable from this doc alone.
6. Where and in what format unknown keys are "listed in the closeout" is unspecified.
7. What counts as a "TaskDoc key outside the model" (top-level vs nested, null/empty handling) is undefined.
8. Tension: step 2/goal says non-model keys would be dropped under `extra: ignore`, while Done When requires byte-identical renders for every existing TaskDoc; no rule says whether such a file fails the task.
9. Whether removing `from_drawer` from `__references__` fully removes the edge, or interacts with the line-scanner path at `extract_edges.py:340-346`, is not specified.
10. Fixture update scope: replace only the TaskDoc hash or regenerate the whole `model_contract_hashes.json`; file schema not shown.
11. Expected result of `deskops graph missing --root .` (empty output vs threshold) is not stated.
12. State of the three `depends_on` tasks is not given.
13. Module import paths for `render_model_markdown` and `extract_model_data` are not given.
14. Byte-identical comparison mechanism (tool/hash) is not specified.
15. Whether the pills or `docs/` materializations must be updated is not stated in scope.
