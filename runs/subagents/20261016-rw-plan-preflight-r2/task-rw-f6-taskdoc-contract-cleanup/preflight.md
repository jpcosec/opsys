RESTATEMENT:

1. Read `deskops/models/task.py` in full; locate `TaskDoc`, its `extra` config, the `frontmatter` field with `exclude=True`, `render_payload`, the hand-kept body-field list, `from_drawer`, and `_omit_unset_from_drawer`.
2. Read the PillDoc model (same file or a sibling model) to copy how it sets `extra: ignore` and how it declares each frontmatter field with its own template marker.
3. In `TaskDoc`: set `extra: ignore`.
4. Replace the `exclude=True` `frontmatter` dict field plus the `render_payload` hand-kept body-field list with per-field declarations using template markers, mirroring PillDoc.
5. Move `from_drawer` out of `__references__` and declare it as a plain model field.
6. Rewrite the `_omit_unset_from_drawer` docstring to say it keeps documents byte-identical (remove the false contract-hash-stability claim).
7. Run `pytest tests/test_model_contract_snapshot.py`; copy the printed TaskDoc hash into `tests/fixtures/model_contract_hashes.json`.
8. Verify every TaskDoc under `desk/` and `tests/fixtures/` still extracts and renders byte-identically (compare rendered output before/after).
9. Confirm `PROVENANCE_FIELDS` in `deskops/graph/extract_edges.py` is untouched and still suppresses the `from_drawer` line scan (lines 340-346).
10. Run `pytest tests/test_model_contract_snapshot.py tests/test_graph_declared_edges.py`.
11. Run `deskops graph missing --root .`.
12. Run `pytest tests` until green.
13. Do not commit; leave the diff for the supervisor.

AMBIGUITIES:

1. Task is `status: blocked` and depends on three tasks with unspecified completion state; nothing says the dependencies are done.
2. Open Ambiguity (owner decision on whether F6 enters this cycle) is unresolved, and Scope itself says the task is blocked on that decision — the task cannot start.
3. "declares each frontmatter field with its own template marker (as PillDoc does)" — PillDoc's implementation is not included; the exact marker syntax/mechanism is unknown from the document alone.
4. The set of TaskDoc frontmatter fields and which are body vs. frontmatter is not listed; the hand-kept body-field list contents are unknown.
5. Contradiction: switching `extra: allow` → `ignore` drops unknown keys, which conflicts with the "byte-identical" requirement for any TaskDoc carrying extra keys; no rule given for those.
6. No method specified to prove "extracts and renders byte-identically" (no script, command, or baseline artifact named).
7. "Every TaskDoc under `desk/` and `tests/fixtures/`" — no glob/dir list given (e.g., does it include `desk/drawer/`?).
8. `from_drawer` semantics/type/optionality after leaving `__references__` are unspecified; whether its serialized form changes is unknown.
9. Whether updating the fixture hash affects hashes of other models in `model_contract_hashes.json` is unspecified.
10. `render_payload` — its owning class/base and callers are not identified.
11. `runs/planning/deskops-rewrite-inventory.md` is referenced but not provided; S10 details cannot be confirmed.
12. No acceptance criterion that the docstring text is exactly what is required beyond "says it keeps documents byte-identical".
