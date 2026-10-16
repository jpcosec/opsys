RESTATEMENT:
1. Verify blockers: confirm owner decision that F6 enters this cycle, and confirm dependencies `task-rw-f6-bootstrap-registers-all-models` and `task-rw-f6-graph-on-sldb-edge-index` are complete.
2. Read bound pills `desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md` and `desk/contexts/pill-006-self-described-store-layout.md`.
3. Inspect `deskops/models/task.py` for TaskDoc: `extra: allow`, the `frontmatter` field with `exclude=True`, `render_payload`, the hand-kept body-field list, `from_drawer`, `__references__`, and `_omit_unset_from_drawer` docstring.
4. Edit `deskops/models/task.py` to drop `extra: allow`.
5. Remove the frontmatter hack: delete the `frontmatter` field and the `render_payload` repopulation from the hand-kept body-field list.
6. Move `from_drawer` out of `__references__` and represent it as provenance.
7. Correct the `_omit_unset_from_drawer` docstring so it no longer claims it avoided a contract-hash change.
8. Run `pytest tests`; identify failures from the model changes.
9. Update `tests/fixtures/model_contract_hashes.json` to the new F1 contract snapshot hash.
10. Inspect `deskops/graph/extract_edges.py` and remove `PROVENANCE_FIELDS` special-casing if the graph no longer needs it.
11. Run `pytest tests`.
12. Run `sldb stores check --store .sldb`.
13. Confirm the repo store passes `stores check` after migration and the suite is green.

AMBIGUITIES:
1. Task status is `blocked`; the doc says the owner must decide whether F6 enters this cycle, with no decision recorded.
2. Scope says it ships with `task-rw-f6-migrate-tracking-stores`, but that task is not in `depends_on`.
3. “F1 contract snapshot” is not explicitly identified as `tests/fixtures/model_contract_hashes.json`.
4. No procedure or command is given for regenerating or updating the contract hash.
5. The hash format, algorithm, and fixture schema are not specified.
6. Dropping `extra: allow` has no stated handling for existing or legacy unknown fields.
7. The “frontmatter hack” body-field list is not enumerated.
8. The intended replacement behavior for `render_payload` after removing the frontmatter field is unspecified.
9. The target provenance field or representation for `from_drawer` is unspecified.
10. “Docstring is accurate” has no acceptance wording.
11. “If the graph no longer needs it” gives no criterion for deciding whether `PROVENANCE_FIELDS` special-casing can be removed.
12. No expected graph edge output or graph validation is given for the `extract_edges.py` change.
13. `pytest tests` is less specific than the repo’s documented `pytest` command; full suite vs subset is unclear.
14. The `sldb stores check --store .sldb` path assumes repo-root execution and a migrated store.
15. Done When depends on migration, but migration is described as a separate task and may be out of scope.
16. No acceptance criteria state which tests must assert TaskDoc contract behavior.
17. `references: []` despite pills and files being listed; link validation expectations are unclear.
18. No compatibility requirement is given for downstream consumers after the contract hash changes.
