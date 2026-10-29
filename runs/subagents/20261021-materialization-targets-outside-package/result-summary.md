# Result Summary

Run ID: 20261021-materialization-targets-outside-package
Task: task-declared-materialization-targets-resolve-outside-the-indexed-package
Session: subagent-execution

## What Changed

### deskops/graph/extract_sources.py
- Added `yaml` import
- Added `_declared_materialization_target_nodes(root, existing_paths)` helper that reads `target_identity` from `desk/materializations/**/*.md` frontmatter and creates `source_file` nodes for valid repo-relative paths to existing files
- Added `_read_target_identity(path)` helper for frontmatter parsing
- Modified `extract_source_file_nodes()` to collect `existing_paths` and merge declared target nodes
- New nodes use `source_kind: "declared_materialization_target"` in provenance
- Validation: strips `./`, rejects absolute paths, `..` segments, `:` values; requires file exists and is not excluded or already a node

### deskops/operations.py
- Modified `_track_created_artifact()` to include `"artifact.materialization"` so new materializations are tracked in `.sldb` store

### docs/knowledge-graph/desk-source-graph-vocabulary.md
- Added `declared_materialization_target` to the `source_kind` vocabulary in the provenance table

### tests/test_graph_extract_sources.py
- Added 11 new unit tests covering declared materialization target scenarios

### tests/test_materialization_targets_outside_package.py (new file)
- 4 integration tests using real CLI and git repos:
  1. Declared target outside package becomes graph node
  2. Missing file stays missing_declared_target
  3. Materializations are tracked in .sldb store
  4. closeout verify accepts materialization coverage

### desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md (new file)
- Documents the declared materialization target extraction rule

### desk/materializations/ (4 new files)
- materialization-extract-sources-declared-targets.md → deskops/graph/extract_sources.py
- materialization-materialization-targets-outside-package-tests.md → tests/test_materialization_targets_outside_package.py
- materialization-graph-extract-sources-unit-tests.md → tests/test_graph_extract_sources.py
- materialization-graph-vocabulary-source-kind-update.md → docs/knowledge-graph/desk-source-graph-vocabulary.md

### desk/tasks/task-declared-materialization-targets-resolve-outside-the-indexed-package.md
- Added new atom to references
- Updated files list with specific materialization file paths

## Validation Results

```
$ pytest tests/test_materialization_targets_outside_package.py tests/test_graph_extract_sources.py tests/test_materialization_contract.py -v
============================= 23 passed in 50.77s ==============================
```

```
$ deskops graph missing --root .
No missing graph references found.
```

Closeout verify atom_or_materialization_link gate passes. Tests and commit evidence will be added by supervisor.

## Residual Risks

- None for the implementation scope
- Backfilling tracking for existing untracked materializations is out of scope (as stated in task)
- `kind:id` targets (e.g., `source_file:src/x.py`) remain resolved by `extract_edges`, not this helper (as designed)

## Fix round 2 (supervisor-verified)

Defects found in the executor's first round (missed by the tester):
- `target_identity.lstrip("./")` stripped every leading `.` and `/`, so `./.github/workflows/pulse.yml` became `github/workflows/pulse.yml`. Now `removeprefix("./")`.
- The node path was taken from the symlink-resolved path. Now `resolve()` is used only for the outside-root containment check, and the node path is the declared normalized path.

Regression tests added in `tests/test_graph_extract_sources.py`:
- `test_declared_target_dotslash_github_workflow_yields_correct_node`
- `test_declared_target_symlink_yields_link_path_not_resolved_target`

Validation after the fix:
- `pytest tests/test_graph_extract_sources.py tests/test_materialization_targets_outside_package.py` -> 23 passed
- `python -m pytest -q` (full suite) -> 603 passed, 3 skipped
- `deskops graph missing --root .` -> no missing references (down from the 4-in baseline)
