RESTATEMENT:
1. Read context: `desk/contexts/pill-010-graph-runtime-output-policy.md`, `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`, plus `tests/test_lifecycle_end_to_end.py` (copy `_make_repo`/`_cli` pattern) and the graph/snapshot writers.
2. Create `tests/conftest.py` with only `pytest_addoption` registering `--update-golden` (store_true) and (if needed) a fixture exposing it.
3. Create fixture desk `tests/fixtures/golden_desk/` containing 2 tasks, 2 atoms, 1 pill under `desk/contexts/`, and 1 drawer task under `desk/drawer/tasks/`, using valid SLDB markers/frontmatter.
4. Write `tests/test_output_goldens.py`:
   - Copy `golden_desk/` into `tmp_path`, `git init`, one seed commit.
   - Drive real CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=tmp)`.
   - Run `graph build`; read `.sldb/runtime/graphs/deskops.kg.json`, `.nx.json`, `self_reflection_findings.json`; run `closeout commit --run-dir` and `closeout commit --no-run`; read `runs/subagents/index.jsonl` and commit trailers.
   - Normalize: timestamps -> `<ts>`, absolute paths -> `<root>`, commit hashes -> `<sha>`.
   - Compare against `tests/fixtures/golden/`; on `--update-golden`, rewrite goldens instead.
   - Enumerate every command path reachable from `deskops --help`, run each `--help`, write `tests/fixtures/golden/help/<path joined by _>.txt`, and compare.
5. Produce initial goldens: `graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (list of `{route, trailers}`), and `help/*.txt` by running with `--update-golden`.
6. Run `pytest tests/test_output_goldens.py` and `pytest tests`.
7. Manually rename a key in the snapshot writer, rerun to confirm failure, revert.

AMBIGUITIES:
1. Resolved Decisions say CLI tests scaffold via `deskops desk install <root>`; Implementation Path says copy a prebuilt fixture desk. Which pattern applies here?
2. `tests/conftest.py` "only the `--update-golden` option" — is a fixture/helper exposing the flag also allowed, or must tests read `pytestconfig` directly?
3. Source of the `--run-dir` run: no run-creation command or fixture run directory is specified; unclear what produces a valid run dir.
4. `closeout_trailers.json` exact schema: `route` values, trailer ordering, nested `trailers` shape.
5. Exact scope of normalization: which fields count as timestamps, paths, shas; whether `.nx.json` node/edge ordering is determinized.
6. Where `self_reflection_findings.json` is produced (graph build vs closeout) and its determinism is unspecified.
7. "every command path reachable from `deskops --help`": unclear whether hidden/deprecated commands, aliases, or deeply nested subcommands are included; how "reachable" is detected.
8. `git init` + commit in `tmp_path` may fail without `user.email`/`user.name`; not specified.
9. `graph build` requires a seed commit and SLDB store; minimum required fixture fields/frontmatter for tasks/atoms/pill are not specified.
10. `--update-golden` semantics on missing goldens / partial dirs not specified (write-all vs fail).
11. Done When says rename "a key in the snapshot writer" — which key/file is not specified.
12. `files:` lists `tests/fixtures/golden/` and `tests/fixtures/golden_desk/` as files though they are directories; expected contents beyond listed goldens unspecified.
13. Task is `status: deferred` with `depends_on` tasks; whether all dependencies are complete is not stated.
14. No acceptance threshold for help enumeration stability (e.g., CLI version string in help output).
