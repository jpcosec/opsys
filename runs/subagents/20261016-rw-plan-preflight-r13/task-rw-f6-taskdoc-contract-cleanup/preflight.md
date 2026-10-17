RESTATEMENT:

1. Confirm gating: dependencies `task-rw-f6-bootstrap-registers-all-models`, `task-rw-f4-graph-on-sldb-edge-index`, `task-rw-f1-model-contract-snapshot` closed, and owner has decided F6 enters this cycle (task is `status: blocked`). Stop otherwise.
2. Read pills `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and `desk/contexts/pill-006-self-described-store-layout.md`.
3. Open `deskops/models/task.py`; inventory TaskDoc's `extra: allow`, `frontmatter` field (`exclude=True`), `_merge_frontmatter` validator, `render_payload` override, `from_drawer` inside `__references__`, and `_omit_unset_from_drawer` docstring; open PillDoc to copy its per-field template-marker pattern.
4. Baseline: for every `desk/tasks/*.md` and `desk/drawer/tasks/*.md` except `Board.md`, and every task file in the golden fixture desk used at `tests/test_composition.py:66`, save `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` output.
5. Obtain the discovery rule from `task-rw-f6-migrate-tracking-stores`; scan those stores for TaskDoc files whose top-level frontmatter keys (including null values) are not in `TaskDoc.model_fields`; write them to `runs/planning/taskdoc-unknown-keys.md`.
6. Edit `task.py`: set `extra = "ignore"`; remove `frontmatter` field, `_merge_frontmatter`, and `render_payload`; declare each frontmatter key as its own field with its own template marker; make `from_drawer` a plain field outside `__references__`; rewrite the `_omit_unset_from_drawer` docstring to say it keeps documents byte-identical.
7. Update `tests/test_graph_declared_edges.py:131` to expect no `from_drawer` frontmatter edge.
8. Run `pytest tests/test_model_contract_snapshot.py`; copy the printed TaskDoc hash into `tests/fixtures/model_contract_hashes.json`.
9. Re-render the step-4 files and diff against baseline; every file not listed in `runs/planning/taskdoc-unknown-keys.md` must be byte-identical.
10. Run `pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py`, `deskops graph missing --root .`, and `pytest tests`.
11. Do not commit; hand the diff to the supervisor.

AMBIGUITIES:

1. Blanket blocker: task is `status: blocked` on an owner decision (Open Ambiguity) not yet recorded; no criterion for detecting that it has been made.
2. Step 5 depends on "task-rw-f6-migrate-tracking-stores' discovery rule", which is not stated in this document and cannot be derived from it.
3. "each frontmatter field" is never enumerated: the current hand-kept body-field list that feeds `render_payload` is not listed, so the target field set is unknown without reading code.
4. PillDoc's location is not given; "as PillDoc does" cannot be checked from this document.
5. Step 4 globs are top-level only; whether nested task directories under `desk/tasks/` or `desk/drawer/tasks/` exist and count is unstated.
6. Done When says "every TaskDoc not listed ... renders byte-identically" but does not say whether the golden-fixture desk task files from step 1 are in that set.
7. Format/ordering of `runs/planning/taskdoc-unknown-keys.md` is unspecified.
8. Which key(s) in `tests/fixtures/model_contract_hashes.json` hold the TaskDoc hash, and whether the file is hand-edited or regenerated, is unstated.
9. No rule for what to do if a file outside `taskdoc-unknown-keys.md` fails the byte-identical check (unknown keys discovered late).
10. Scope says `PROVENANCE_FIELDS` in `deskops/graph/extract_edges.py` stays and keeps stopping the line scanner (lines 340-346), while step 3 updates the edge test to expect no `from_drawer` edge; whether the edge disappears via `__references__` removal alone or is still produced by the scanner path is not resolved.
11. Line references (`:131`, `340-346`, `181-190`) may have drifted; no fallback instruction.
12. Removal of `from_drawer` from `__references__` and the `_omit_unset_from_drawer` rewrite do not state whether `_omit_unset_from_drawer` itself is retained, moved, or deleted.
13. No stated status of the three `depends_on` tasks, nor whether "blocked" is only the owner decision or also dependency completion.
14. Resolved Decisions gives the supervisor promotion/commit path but the document does not say the task has been promoted to `desk/tasks/`; whether to execute from `desk/drawer/tasks/` is unclear.
15. "updated deliberately" has no acceptance criterion beyond matching the printed hash.
16. Validation requires `deskops graph missing --root .` but no expected output/exit criterion is given.
