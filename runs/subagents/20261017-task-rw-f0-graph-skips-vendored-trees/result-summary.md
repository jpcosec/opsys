# result-summary: task-rw-f0-graph-skips-vendored-trees

## Changes

- `deskops/graph/extract_coverage.py`
  - `EXCLUDED_PATH_PARTS` (line 27): added `".tmp"` and `"tools"`.
  - `_is_excluded` unchanged (existing any-path-part matching).
- `deskops/graph/extract_sources.py`
  - `EXCLUDED_DIRS` (lines 15-26): added `".tmp"` and `"tools"`.
  - `_is_excluded` unchanged (existing any-path-part matching).
- `tests/test_graph_extract_coverage.py`
  - Added `test_extract_coverage_graph_skips_atoms_under_vendored_tools_and_tmp_trees`.
- `tests/test_graph_extract_sources.py`
  - Added `test_extract_source_file_nodes_skips_vendored_tools_and_tmp_trees`.

No commits, no `git add`, no desk/ mutations.

## Snapshot count (tools/ and .tmp/ hits)

Count rule: nodes whose `semantics.path`, `identity.node_id` after the `<kind>:` prefix, or any `source.provenance[*].path` is `tools`, `tools/...`, `.tmp`, or `.tmp/...`.

Setup: copied `/home/jp/proyectos/SLDB_1/deskops/tools` into the worktree, then rebuilt.

- Before fix: `PYTHONPATH=/tmp/rw/wt/graph python -m deskops graph build --root .` -> 561 nodes, **19 hits** (5 atoms from `tools/repopackage/desk/atoms/` plus 14 `config_file` nodes from `tools/repopackage/...`, including `.sldb` YAML, `pyproject.toml`, and `desk/config.json`).
- After fix: same build -> 542 nodes, **0 hits**.

## Validation commands and final lines

- `PYTHONPATH=/tmp/rw/wt/graph python -m pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py -q` -> `5 passed in 0.19s`
- `PYTHONPATH=/tmp/rw/wt/graph python -m deskops graph build --root .` -> `Graph snapshot written: /tmp/rw/wt/graph/.sldb/runtime/graphs/deskops.kg.json`
- `PYTHONPATH=/tmp/rw/wt/graph python -m pytest tests -q` -> `337 passed, 3 skipped in 182.34s (0:03:02)`

## Test against unfixed code

New tests were added before touching the extractors and run on unfixed code:

- `pytest tests/test_graph_extract_coverage.py tests/test_graph_extract_sources.py -q` -> `2 failed, 3 passed in 0.21s`
- Coverage failure: `atom:vendored` was extracted from `tools/x/desk/atoms/`.
- Sources failure: `config_file:tools/x/pyproject.toml` (and `source_file:tools/x/deskops/impl.py`) were extracted.

## Task inaccuracies / ambiguities

- The task says the bug puts "5 atoms" in the graph. True for the coverage extractor, but the full impact is 19 nodes: `extract_sources` additionally emits `config_file` (and would emit `source_file`) nodes under `tools/`.
- The task's proposed sources test ("a `.py` file under `tools/x/` produces no `source_file:` node") is not sensitive to the bug: `_is_source_path` only classifies files whose first path part is `desk` or `deskops`, so `tools/x/thing.py` produces no node even without the fix. The test uses `tools/x/deskops/impl.py` (still under `tools/x/`) plus a vendored `pyproject.toml`, which does fail pre-fix.
- `.tmp` did not exist in the worktree, so its exclusion is covered by the unit tests but not by the pre-fix snapshot count.
- Full-suite environment note: the worktree had no `.pi/` directory (gitignored by design), so `tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path` failed on the first full run (`1 failed, 336 passed, 3 skipped in 204.17s`) for a missing `.pi/skills/use-deskops/SKILL.md`, unrelated to this task. Copied `.pi/` from the main checkout into the worktree to restore the expected on-disk skill surfaces; the guard then passed and the full rerun was green.
- No sldb bug observed. Copied `tools/` was removed at the end.
