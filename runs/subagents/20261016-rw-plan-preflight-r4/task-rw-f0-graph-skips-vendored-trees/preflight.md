RESTATEMENT:
1. Edit `deskops/graph/extract_coverage.py`: add string literals `"tools"` and `".tmp"` to `EXCLUDED_PATH_PARTS` (~line 27); leave `_is_excluded` (~line 895) any-path-part matching unchanged.
2. Edit `deskops/graph/extract_sources.py`: add `"tools"` and `".tmp"` to `EXCLUDED_DIRS` (lines 15-26); leave matching logic unchanged.
3. In `tests/test_graph_extract_coverage.py`: add one test that builds a fixture tree containing an atom under `tools/x/desk/atoms/`, runs the coverage extractor, asserts no node is produced.
4. In `tests/test_graph_extract_sources.py`: add one test that builds a fixture tree containing a `.py` file under `tools/x/`, runs the source extractor, asserts no `source_file:` node is produced.
5. Run `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py`.
6. Run `python -m deskops graph build --root .`, then inspect the snapshot per `deskops/graph/snapshot.py:201-223` and count nodes whose `semantics.path`, `identity.node_id` (after any `<kind>:` prefix), or any `source.provenance[*].path` starts with `tools/` or `.tmp/`; assert count is 0.
7. Run `pytest tests`.
8. Do not commit; leave diff for supervisor closeout (`deskops closeout commit --task <id> ...`).

AMBIGUITIES:
1. `EXCLUDED_DIRS` matching semantics unspecified: doc states any-path-part matching "stays as it is" only for the coverage extractor; unclear whether `EXCLUDED_DIRS` matches any path part, a prefix, or a level-1 dir.
2. Snapshot output path/location not given, and it is unclear whether running `graph build --root .` dirties tracked files that belong in the diff or are generated artifacts.
3. Exact field names in the verification step (`semantics.path`, `identity.node_id`, `source.provenance[*].path`) are asserted but not verified against `snapshot.py`; the node layout may differ.
4. No exact command/script is specified for counting snapshot nodes; the counting method must be improvised.
5. Test fixture setup is unspecified: no statement of whether to use tmp dirs, existing fixtures, or a conftest, nor of the extractor entrypoint/API functions the tests must call.
6. Task header says `status: deferred` and `source:drawer`, which conflicts with the executor role implied by the Resolved Decisions (supervisor-promoted active task).
7. Acceptance criteria are behavioral only; no requirement stated to assert the `EXCLUDED_PATH_PARTS`/`EXCLUDED_DIRS` contents directly.
8. Impact on existing tests that may depend on `tools/` being included is not addressed.
