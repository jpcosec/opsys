RESTATEMENT:
1. Read `deskops/graph/extract_coverage.py` and `deskops/graph/extract_sources.py` to confirm `EXCLUDED_PATH_PARTS` (line ~27), `_is_excluded` (line ~895), and `EXCLUDED_DIRS` (lines 15-26).
2. Edit `deskops/graph/extract_coverage.py`: add `"tools"` and `".tmp"` to `EXCLUDED_PATH_PARTS`; leave any-path-part matching in `_is_excluded` unchanged.
3. Edit `deskops/graph/extract_sources.py`: add `"tools"` and `".tmp"` to `EXCLUDED_DIRS`; keep existing exclusion logic unchanged.
4. In `tests/test_graph_extract_coverage.py`, add a test that places an atom file under `tools/x/desk/atoms/` and asserts no node is produced.
5. In `tests/test_graph_extract_sources.py`, add a test that places a `.py` file under `tools/x/` and asserts no `source_file:` node is produced.
6. Run `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py`.
7. Rebuild: `python -m deskops graph build --root .`.
8. Inspect the emitted snapshot (`deskops/graph/snapshot.py:201-223` layout); count nodes whose `semantics.path`, `identity.node_id` (strip any `<kind>:` prefix), or any `source.provenance[*].path` starts with `tools/` or `.tmp/`; assert count == 0.
9. Run `pytest tests`.
10. Hand the diff back to the supervisor; do not commit.

AMBIGUITIES:
1. Test harness shape is unspecified: no function names, signatures, fixture helpers, or how to invoke each extractor against a temp root.
2. Unclear whether test fixtures must create a temp directory root, an SLDB store, or a minimal `desk/` tree for extractors to walk.
3. `EXCLUDED_DIRS` matching semantics (exact part vs prefix vs substring) are not stated, so I cannot know whether adding `"tools"` covers `tools/x/` and nested `a/tools/b/`.
4. `EXCLUDED_PATH_PARTS` is any-path-part matched, which may also exclude unrelated nested dirs named `tools`; whether that is intended is not stated.
5. Whether `.tmp` should be `.tmp` vs `.tmp/` vs both, and whether root-level `.tmp/` differs from `a/.tmp/`, is unspecified.
6. Whether `.venv` already exists in both exclusion sets (goal says it "stays excluded") is asserted but not verifiable from the task text.
7. `source.provenance[*].path` field name/location is asserted but not verified; if provenance lacks `path`, step 8's count script is undefined.
8. No counting command or script is provided for the step-8 zero-node check, so the check is not mechanically specified.
9. Running `python -m deskops graph build --root .` mutates the real tracked desk graph, conflicting with the AGENTS.md rule to use a sandbox desk for mutating CLI runs; no sandbox path is designated here.
10. No acceptance threshold beyond "zero nodes" and "both tests pass"; unclear whether `.tmp/` nodes must also be zero in the existing snapshot or only after rebuild.
11. Unclear whether the two new tests must cover `.tmp/` as well as `tools/`, since the goal mentions both but the test descriptions only mention `tools`.
12. Task is `status: deferred` in the drawer; the executor cannot dispatch it, and no promotion target path (`desk/tasks/<filename>`) is given.
13. Existing test files may not exist or may not use the extractor entry points the task implies; no fallback is specified.
