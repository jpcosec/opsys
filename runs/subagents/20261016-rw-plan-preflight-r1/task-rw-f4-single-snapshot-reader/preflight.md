RESTATEMENT

1. Read `deskops/graph/snapshot.py`, `deskops/graph/checks.py`, `deskops/graph/self_reflection.py`; locate each place snapshot JSON is opened/parsed and each distinct key accessed.
2. Confirm `depends_on: task-rw-f4-graph-on-sldb-edge-index` is closed and read the edge-index contract it defines.
3. Read pills `desk/contexts/pill-011-self-reflection-noise-control.md` and `desk/contexts/pill-010-graph-runtime-output-policy.md` for constraints on reader API and output.
4. In `snapshot.py`, add dataclasses for nodes and edges (field names matching current snapshot keys).
5. Add one typed reader in `snapshot.py` that loads and parses the snapshot JSON exactly once and returns the nodes/edges dataclasses.
6. Replace snapshot-reading logic in `checks.py` with calls to the new reader.
7. Replace snapshot-reading logic in `self_reflection.py` with calls to the new reader.
8. Delete now-dead JSON parsing/loading code in both modules; leave `snapshot.py` as the only JSON parse site.
9. Run `pytest tests/test_graph_snapshot.py tests/test_graph_checks.py tests/test_graph_self_reflection.py`.
10. Run `pytest`.
11. On green, execute execution → testing → closeout rituals; make one atomic commit for the task.

AMBIGUITIES

1. `Rationale`, `Goal`, `Scope`, `Implementation Path`, `Validation`, `Done When` all still contain the template placeholder lines, so it is unclear which text is authoritative vs example.
2. `status: deferred` — unclear whether this task is promotable now or must be promoted via drawer flow first.
3. No test/acceptance criteria for the reader's exact API: name, parameters, return shape, caching/lazy behavior unspecified.
4. Dataclass field names and required vs optional fields are not specified.
5. The differing keys used by the three modules are not listed, so "one reader" cannot be verified as lossless per module.
6. No line numbers, no function names — unknown how many parse sites exist in each file.
7. `depends_on` task status not shown; cannot confirm the edge-index contract exists or is stable.
8. "Golden tests stay green" — no golden test file paths given; unclear which goldens encode current output.
9. Whether `tests/test_graph_snapshot.py` exists or must be created is unstated.
10. Validation lists both targeted and full pytest with no required pass/fail semantics for skips or xfails.
11. Done When "Only snapshot.py parses the snapshot JSON" — unclear whether other modules (e.g., CLI, store layer) are allowed to parse.
12. Scope says snapshot format is out of scope, but the reader must match keys; no key contract is provided.
13. Error handling for malformed/missing snapshot keys is unspecified.
14. No backward-compatibility requirement stated for callers that previously got raw dicts.
15. Pills bound but not summarized; their constraints are unknown without loading them.
16. No commit message convention, branch, or PR requirement stated.
