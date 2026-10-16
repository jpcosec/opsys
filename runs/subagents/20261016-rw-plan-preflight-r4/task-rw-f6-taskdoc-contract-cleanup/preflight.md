RESTATEMENT:
1. Confirm deps closed: task-rw-f6-bootstrap-registers-all-models, task-rw-f4-graph-on-sldb-edge-index, task-rw-f1-model-contract-snapshot; read pills `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and `desk/contexts/pill-006-self-described-store-layout.md`.
2. Capture baseline: for each text in `desk/tasks/*.md` and `desk/drawer/tasks/*.md` (exclude `Board.md`) plus every task file in the golden fixture desk at `tests/test_composition.py:66`, run `render_model_markdown(TaskDoc, extract_model_data(TaskDoc, text))` and store the outputs for later comparison.
3. Discover the tracking stores via task-rw-f6-migrate-tracking-stores' discovery rule; for each TaskDoc file, find top-level frontmatter keys not in `TaskDoc.model_fields` (count null values as keys); write the list to `runs/planning/taskdoc-unknown-keys.md`.
4. Edit `deskops/models/task.py`: set `extra: ignore`; delete the `frontmatter` field, `_merge_frontmatter` validator, and `render_payload` override; declare each frontmatter field with its own template marker (match PillDoc's pattern); move `from_drawer` out of `__references__` to a plain field; rewrite the `_omit_unset_from_drawer` docstring to claim byte-identical documents, not contract-hash stability.
5. Update `tests/test_graph_declared_edges.py:131` to expect no `from_drawer` frontmatter edge.
6. Run `pytest tests/test_model_contract_snapshot.py`, copy the printed TaskDoc hash into `tests/fixtures/model_contract_hashes.json`.
7. Re-render all step-2 files; assert byte-identical for every file not listed in `runs/planning/taskdoc-unknown-keys.md`.
8. Run `pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py`, `deskops graph missing --root .`, then `pytest tests`.
9. Leave commit to supervisor per Resolved Decisions.

AMBIGUITIES:
1. Status is `blocked` and Open Ambiguities says the owner has not decided whether F6 enters this cycle — precondition unresolved.
2. Where to persist the step-1 baseline renders (path, format, lifecycle) is unspecified.
3. The golden fixture desk path used by `tests/test_composition.py:66` is not given; I must locate it by reading the test.
4. task-rw-f6-migrate-tracking-stores' discovery rule is not defined in this document; I cannot know which stores to scan.
5. Format/content of `runs/planning/taskdoc-unknown-keys.md` is unspecified (per-file grouping? key list? ordering?).
6. "declares each frontmatter field with its own template marker (as PillDoc does)" — the exact marker syntax and per-field marker names are not given; must be inferred from PillDoc.
7. Whether `render_payload` has other callers or public API consumers is not stated; removal risk unknown.
8. Pill reference forms are inconsistent (`desk/contexts/pill-legacy-...md` vs bare `pill-006-...`); resolution path for `pill-006` not stated.
9. `_omit_unset_from_drawer` location (presumably in `deskops/models/task.py`) is not confirmed in this doc.
10. "exclude `Board.md`" — whether other Board.md-like files elsewhere in those trees are in or out is unclear.
11. Byte-identical comparison does not state encoding, line-ending, or trailing-newline normalization rules.
12. The Done When byte-identical condition is not tied to a Validation command; how compliance is proven/evidenced is unspecified.
13. The contract-hash fixture update assumes a TaskDoc keyed entry; key/entry format for `tests/fixtures/model_contract_hashes.json` is not described.
14. Whether the new `from_drawer` plain field affects the contract snapshot hash beyond what step 6 copies is left implicit.
15. Scope mentions `PROVENANCE_FIELDS` "stays"; no explicit confirmation that no other edge/line-scanner behavior needs updating.
