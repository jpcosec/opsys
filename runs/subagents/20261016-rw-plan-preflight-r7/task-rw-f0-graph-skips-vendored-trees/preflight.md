RESTATEMENT:
1. Open `deskops/graph/extract_coverage.py`; add `"tools"` and `".tmp"` to the `EXCLUDED_PATH_PARTS` tuple/list at ~line 27. Keep `_is_excluded` (~line 895) any-path-part matching logic unchanged.
2. Open `deskops/graph/extract_sources.py`; add `"tools"` and `".tmp"` to `EXCLUDED_DIRS` (lines 15-26), matching the existing entry format (plain dir names).
3. In `tests/test_graph_extract_coverage.py`, add a test that builds a fixture tree containing an atom under `tools/x/desk/atoms/` (using the file's existing fixture/helper style), runs the coverage extractor, and asserts the atom yields no node.
4. In `tests/test_graph_extract_sources.py`, add a test that builds a fixture tree containing a `.py` file under `tools/x/`, runs the sources extractor, and asserts no `source_file:` node is produced.
5. Run `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py`.
6. Run `python -m deskops graph build --root .`.
7. Inspect the produced snapshot: for every node, check `semantics.path`, `identity.node_id` (strip any `<kind>:` prefix first), and each `source.provenance[*].path` (node shape per `deskops/graph/snapshot.py:201-223`); assert zero values start with `tools/` or `.tmp/`.
8. Run `pytest tests`.
9. Leave changes uncommitted; supervisor reviews diff and performs closeout commit.

AMBIGUITIES:
1. Over-exclusion: adding `tools` as an any-path-part match also excludes any nested `tools` dir (e.g. `deskops/tools/`), not only the root `tools/`; task states matching stays as-is but does not confirm nested `tools` should be excluded.
2. Same question for `.tmp` and `tools` in `EXCLUDED_DIRS`: unclear whether matching is root-only or any-depth, so scope of exclusion is undefined.
3. Exact entry format/naming convention in `EXCLUDED_DIRS` (`.tmp` vs `tmp`, whether entries carry trailing slash) is not given.
4. Repro depends on untracked `tools/repopackage/` currently existing; if absent, step 7's zero-count cannot distinguish fix from absence — no stated precondition or check.
5. Fixture construction for the new tests (how to build a minimal desk/atom tree, existing helper names, temp-dir conventions) is unspecified.
6. `deskops graph build --root .` output/snapshot location is unspecified, so which file to inspect in step 7 is a guess.
7. Line references (`snapshot.py:201-223`, `_is_excluded` line 895, `EXCLUDED_DIRS` lines 15-26) may be stale; key names `semantics.path` / `source.provenance[*].path` unverified against current code.
8. Whether changing `EXCLUDED_PATH_PARTS` also alters coverage denominators/ratios (uses at line 895) beyond node emission is not addressed.
9. Pills `pill-010-graph-runtime-output-policy.md` and `pill-009-source-file-graph-traceability.md` are bound but their constraints (e.g. required provenance for exclusions, policy on skipped dirs) are not stated; compliance cannot be verified from the task text.
10. Status is `deferred` and file lives in drawer; task does not state current location or that promotion already happened, so which artifact to edit/dispatch is unclear.
11. No acceptance check covers other untracked dirs (e.g. `runs/`) that may still leak, though `runs/` is referenced as the plan location.
12. `.venv/` is asserted to "stay excluded" but the task gives no test/check confirming it remains excluded after edits.
