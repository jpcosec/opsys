RESTATEMENT:
1. Open `deskops/graph/extract_coverage.py`; locate `EXCLUDED_PATH_PARTS` (~line 27) and `_is_excluded` (~line 895). Add `"tools"` and `".tmp"` to `EXCLUDED_PATH_PARTS`. Leave any-path-part matching logic unchanged.
2. Open `deskops/graph/extract_sources.py`; locate `EXCLUDED_DIRS` (lines 15-26). Add `"tools"` and `".tmp"`. Confirm `.venv` remains present/unaffected.
3. In `tests/test_graph_extract_coverage.py`, add one test: construct a temp root with an atom under `tools/x/desk/atoms/` (plus whatever control layout the extractor needs), run the coverage extractor, assert no resulting node/path is under `tools/`.
4. In `tests/test_graph_extract_sources.py`, add one test: construct a temp root with a `.py` file under `tools/x/`, run the sources extractor, assert no `source_file:` node is produced.
5. Run `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py`.
6. Run `python -m deskops graph build --root .`.
7. Inspect the produced snapshot; for each node read `semantics.path` and `identity.node_id` (strip any `<kind>:` prefix) per `deskops/graph/snapshot.py:201-214`; verify count of entries starting with `tools/` or `.tmp/` is 0.
8. Run `pytest tests`; confirm green.
9. Stop; do not commit. Supervisor performs promotion/closeout commits.

AMBIGUITIES:
1. `status: deferred` contradicts the Implementation Path and Resolved Decisions describing dispatch/execution now.
2. `tests/test_graph_extract_sources.py` is listed in `files` but its existence is not stated; unknown whether to create it or edit an existing file. Same for whether `tests/test_graph_extract_coverage.py` exists.
3. Matching semantics of `EXCLUDED_DIRS` in `extract_sources.py` are unspecified (exact dir name vs path part vs substring/prefix), so whether `".tmp"` vs `"tmp"` is correct is unclear.
4. Whether `"tools"` is currently absent from either set, or already present in one, is not stated.
5. Test harness conventions are unspecified: how test roots/fixtures are built and how extractors are invoked.
6. `deskops graph build --root .` runs against the real repo; it is unspecified which store/snapshot path is written, whether that write mutates tracked files, and whether generated artifacts must be reverted or committed (executor commit policy aside).
7. The snapshot file path to inspect in step 3/7 is unnamed; "the snapshot" is not pinned to a concrete artifact location.
8. Baseline reproduction (count before fix) is described in Rationale but not required by Done When; unclear whether a pre-fix failing run must be recorded.
9. Goal wording says "path under `tools/` or `.tmp/`" while the check wording restricts to `semantics.path`/`identity.node_id` prefixes; any node whose path lives only in another field would not be covered.
10. Whether the `tools`/`.tmp` exclusions apply regardless of root depth (e.g. nested `a/tools/b`) for `extract_sources.py` is unspecified, given the any-path-part rule is stated only for coverage.
11. No acceptance criteria on node kinds other than atoms and source files (e.g. other extractors that may also place nodes under `tools/`).
12. Sandboxing intent in project guidance (write mutations to `.tmp/deskops-cli-test`) conflicts with the task's instruction to run `--root .` on the real repo.
