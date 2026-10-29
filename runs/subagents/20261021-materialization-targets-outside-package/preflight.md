# Preflight: task-declared-materialization-targets-resolve-outside-the-indexed-package

Source read: `desk/tasks/task-declared-materialization-targets-resolve-outside-the-indexed-package.md` (only file read).

## What I would implement

1. `deskops/graph/extract_sources.py`
   - Add `_declared_materialization_target_paths(root)`: glob `desk/materializations/**/*.md`, parse the leading `---` block with `yaml.safe_load`, and skip unreadable or malformed files without raising.
   - Collect `target_identity` values that are plain repo-relative paths with no `kind:` prefix.
   - Keep a path only if:
     - the file exists and is a file;
     - it is not excluded by `EXCLUDED_DIRS`, `EXCLUDED_PATH_PREFIXES` or the suffix rules;
     - no existing path rule (`_is_source_path`, tests, spec, config) already classifies it;
     - it is not a doc-node path (`docs/**/*.md`, `README.md`, other `extract_docs.py` surfaces).
   - Build a node for each kept path:
     - kind `source_file`, file_kind `source`;
     - id `source_file:<path>`;
     - provenance `{path, source_kind: "declared_materialization_target", extractor: EXTRACTOR_NAME}`.
   - Merge these nodes into `extract_source_file_nodes`, deduplicated against path-rule nodes and sorted by id.
   - Nonexistent targets get no node, so `missing_declared_target` is still reported for them.
2. `deskops/graph/extract_edges.py` `_missing_target_id`: no change unless tests require one.
3. `deskops/operations.py` `_track_created_artifact`: also track `artifact.materialization`, alongside atom and pill, when a `.sldb` store exists.
4. No changes to `closeout_gates.build_closeout_graph_context` or the graph snapshot; both already call `extract_source_file_nodes`.
5. Atom: create it with `deskops add atom --root . --title "Declared materialization targets are graph nodes" --five-wh-one-plus how --answer "..." --tags system:deskops topic:materialization topic:closeout topic:graph`, then reference it from the task.

## What I would test (no mocks)

- New `tests/test_materialization_targets_outside_package.py`:
  - Build a real git repo, run `deskops init`, then `python -m deskops add atom`, then `add materialization --target-identity` for `src/vsm/organs/links.py` and `.github/workflows/pulse.yml`.
  - Assert both files are graph nodes.
  - Assert `python -m deskops graph missing --root <repo>` exits 0.
  - Assert a materialization targeting a nonexistent path is still reported as `missing_declared_target`.
  - Assert `python -m deskops closeout verify --root --task` for a task whose `files` are those two paths has no `missing_changed_file_link`.
    - Reuse the `_make_repo`, `_git` and `_write_task` patterns from `tests/test_closeout.py` and `tests/test_closeout_atomless.py`.
  - Assert the created materialization appears under `MaterializationContractDoc` in `.sldb/store.yaml`, or in `sldb stores check --store .sldb --format json`.
- Extend `tests/test_graph_extract_sources.py`:
  - a unit test for the declared-target node;
  - a unit test that doc paths are not duplicated.
- Validation:
  - `pytest tests/test_materialization_targets_outside_package.py tests/test_graph_extract_sources.py`
  - `pytest`
  - `deskops graph missing --root .`
  - manual reproduction in a `.tmp/` sandbox

## Ambiguities

1. **Medium – atom path.** `files` lists `desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md` (flat), but `deskops add atom` may write to a subfolder or use a different slug. "Move nothing" conflicts if the paths differ, and closeout file links may then break.
2. **Medium – where to reference the atom.** `atoms: []` and `references:` both exist; the task does not say which field gets the new atom.
3. **Medium – suffix exclusions.**
   - The task says existing suffix exclusions still apply but does not list them.
   - If `.yml` or `.github/` is excluded, the target `.github/workflows/pulse.yml` can never become a node, which contradicts the Goal ("whatever the file's directory or suffix").
4. **Medium – what counts as a doc node.**
   - "Other extract_docs.py surfaces" is undefined.
   - Should I import the doc-path predicate from `extract_docs.py` or duplicate it? Duplicating risks drift.
5. **Medium – `target_identity` format.**
   - Scalar or list? The task does not say whether one materialization can declare several targets.
   - The exact `kind:` prefix syntax is not given. Does a path containing `:` count as prefixed?
6. **Medium – path normalization.** Behavior is unspecified for:
   - `./x`, absolute paths, `..` escaping the repo;
   - symlinks, directories as targets;
   - Windows separators, trailing whitespace.
7. **Low – how to detect "already classified".** Dedup by node id or by path? A config-file rule node may have a different id or kind than `source_file:<path>`.
8. **Low – `extract_edges.py`.** It is not in `files:`; if tests show it needs a change, the file list must be extended.
9. **Medium – store-tracking failure.**
   - The behavior when `.sldb` exists but tracking fails is unspecified: warn, or fail and roll back per pill-012?
   - "When one exists": is existence detected by the `.sldb/` dir or by `store.yaml`?
10. **Medium – closeout test setup.**
    - Unspecified whether the target files must be committed, staged, or only changed in the working tree.
    - Which commit range `closeout verify` compares against.
11. **Low – `sldb` CLI in tests.** Availability on PATH is unknown; checking `.sldb/store.yaml` directly avoids the dependency, but the expected YAML shape is unspecified.
12. **Low – CLI flag spelling.** `--five-wh-one-plus how` and the space-separated `--tags` values are not verified; I did not read the CLI.
13. **Low – "no new findings" baseline.** No baseline is recorded for `deskops graph missing --root .` on this repo; it is unknown whether it currently exits 0.
14. **Low – sandbox reproduction.** The "Done When" `.tmp/` reproduction is manual; its expected steps or script are not specified.
15. **Low – task metadata.**
    - `status: draft` with `current_node: ritual-execution` and an empty `summary`.
    - Unclear whether the task is promoted and ready for implementation.
16. **Low – recursive glob noise.** `desk/materializations/**/*.md` may include README or index files without frontmatter; they are skipped silently, but that is not confirmed.
