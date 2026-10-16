RESTATEMENT:
1. Verify the three dependencies are complete: task-rw-f6-bootstrap-registers-all-models, task-rw-f6-graph-on-sldb-edge-index, task-rw-f6-model-contract-snapshot.
2. Read the two bound pills: desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md and desk/contexts/pill-006-self-described-store-layout.md.
3. Baseline: for every file in desk/tasks/*.md and desk/drawer/tasks/*.md except Board.md, plus every task file in the golden fixture desk used by tests/test_composition.py:66, save `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))`.
4. Read task-rw-f6-migrate-tracking-stores to obtain its store-discovery rule; scan the discovered stores for TaskDoc files with top-level frontmatter keys not in `TaskDoc.model_fields` (null values count); write them to runs/planning/taskdoc-unknown-keys.md.
5. Edit deskops/models/task.py: `extra: ignore`; delete the `frontmatter` field, the `_merge_frontmatter` validator, and the `render_payload` override; declare each frontmatter field with its own template marker (as PillDoc does); keep `from_drawer` as a plain field outside `__references__`; change the docstring to say documents are kept byte-identical, not that the contract hash is stable.
6. Edit tests/test_graph_declared_edges.py:131 to expect no frontmatter `from_drawer` edge (edge loss from removing `from_drawer` from `__references__`, deskops/graph/extract_edges.py:181-190). Leave `PROVENANCE_FIELDS` in deskops/graph/extract_edges.py unchanged (lines 340-346).
7. Run `pytest tests/test_model_contract_snapshot.py`; copy the printed TaskDoc hash into tests/fixtures/model_contract_hashes.json.
8. Re-render the step-3 set and byte-compare against the step-3 baseline; every file not listed in step 4 must be byte-identical.
9. Run: `pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py`; `deskops graph missing --root .`; `pytest tests`.
10. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. Status is `blocked` and Scope says "Blocked on the owner deciding that F6 enters this cycle"; no signal in the doc that the block is lifted.
2. Dependency outputs needed as inputs (store-discovery rule from task-rw-f6-migrate-tracking-stores, snapshot fixture from F1, edge index from F4) are not included.
3. "each frontmatter field" is not enumerated; the current TaskDoc model is not given.
4. "as PillDoc does" — PillDoc's implementation is not shown.
5. `_merge_frontmatter` and `render_payload` are referenced but not shown.
6. Which docstring is meant (rationale names `_omit_unset_from_drawer`) and whether that function survives the refactor is unstated.
7. Golden fixture desk path and which of its files count as "task files" are unstated (only a test line reference).
8. Where the step-1 renders are stored and how the byte comparison is performed are unstated.
9. Pass criteria for `deskops graph missing --root .` are unstated.
10. Required format/content of runs/planning/taskdoc-unknown-keys.md is unstated.
11. `files:` omits files touched per Implementation Path (tests/test_composition.py, tests/test_model_contract_snapshot.py, deskops/graph/extract_edges.py); whether editing them beyond the listed line is allowed is unclear.
12. No acceptance criteria for the unknown-keys file (Done When covers only byte-identical rendering).
13. Paths are relative; repo root is assumed to be the cwd.
14. Interaction/ordering between this task and task-rw-f6-migrate-tracking-stores for the discovery-rule pre-scan is unspecified.
