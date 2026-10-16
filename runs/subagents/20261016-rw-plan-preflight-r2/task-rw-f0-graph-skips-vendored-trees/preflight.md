RESTATEMENT:
1. Open `deskops/graph/extract_coverage.py`; add `"tools"` and `".tmp"` to `EXCLUDED_PATH_PARTS` (~line 27); confirm `_is_excluded` (~line 895) still matches any path part, unchanged.
2. Open `deskops/graph/extract_sources.py`; add `"tools"` and `".tmp"` to `EXCLUDED_DIRS` (lines 15-26); leave walker logic unchanged.
3. Add one test to `tests/test_graph_extract_coverage.py`: fixture atom under `tools/x/desk/atoms/` yields no node.
4. Add one test to `tests/test_graph_extract_sources.py`: `.py` under `tools/x/` yields no `source_file:` node.
5. Run `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py`.
6. Run `python -m deskops graph build --root .`, then the `python -c "import json; ..."` check over `.sldb/runtime/graphs/deskops.kg.json`; expect `0`.
7. Run `pytest`.
8. Do not commit; leave whole-repo diff for supervisor closeout.

AMBIGUITIES:
1. Task `status: deferred` — no statement whether execution should start now.
2. Goal/`Done When` require zero nodes under both `tools/` and `.tmp/`, but the Validation snippet only counts `tools/`; no `.tmp/` check given.
3. The snippet does substring matching on `json.dumps(node)`, not the node's path field; unknown which field holds the path, and substring match would also trip on text like `"tools/"` inside a title/atom body.
4. Exclusion entries are matched as any path part, so `"tools"` will also drop non-root directories named `tools` (e.g. `desk/tools/`); unknown if that is intended versus root-only `tools/`.
5. Whether excluded parts are compared exactly (no leading/trailing slash), so `".tmp"` vs `".tmp/"` spelling matters; unknown required literal form.
6. Existing content/kinds of `EXCLUDED_PATH_PARTS` and `EXCLUDED_DIRS` not shown; unknown whether they are sets, lists, or tuples, or already contain dot-prefixed entries.
7. Fixture mechanics for the two tests unspecified: no helper names, no construction path for a fake atom or source file, no assertion API for nodes.
8. `.venv/` exclusion is asserted to stay but no regression check is specified.
9. Snapshot path `.sldb/runtime/graphs/deskops.kg.json` assumed to be the output of `graph build --root .`; no confirmation of graph name or file location.
10. Unknown whether other walkers/extractors (beyond the two named files) also emit nodes with paths under `tools/`/`.tmp/`; goal is snapshot-wide, implementation touches two files only.
11. Rebuild writes into `.sldb/runtime/`, which may be a tracked artifact; the no-commit decision leaves it unclear whether the rebuilt snapshot may be left modified.
