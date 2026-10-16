RESTATEMENT:
1. Create fixture desk `tests/fixtures/golden_desk/` containing a `desk/` doc tree with 2 tasks, 2 atoms, 1 pill, 1 drawer task in valid deskops/sldb formats.
2. Create `tests/conftest.py` (does not exist yet) containing only the `--update-golden` pytest option registration.
3. Create `tests/test_output_goldens.py` with helpers copied from `_make_repo` / `_cli` in `tests/test_lifecycle_end_to_end.py`: copy fixture into `tmp_path`, `git init`, seed commit, run `python -m deskops desk install <root>`, then drive the CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
4. In that throwaway repo run, in order: `graph build`, `graph reflect`, `closeout commit --run-dir <dir>` (one task, `--task <id>`), `closeout commit --no-run --task <id> --reason <fixed>`.
5. Capture outputs: `.sldb/runtime/graphs/deskops.kg.json`, `.sldb/runtime/graphs/deskops.nx.json`, `.sldb/runtime/self_reflection_findings.json`, `runs/subagents/index.jsonl`, and the trailers (`Task-Id`, `Run-Dir`, `Run-Id`, `Session-Sha256`, or `Closeout-Mode`/`Closeout-Reason`) of both closeout commits.
6. Normalize captured text: timestamps → `<ts>`, absolute paths (incl. `tmp_path`) → `<root>`, commit hashes → `<sha>`.
7. Walk every command path reachable from `deskops --help` recursively, run each `<path> --help`, and record text under `tests/fixtures/golden/help/<command path joined by _>.txt`.
8. Write goldens: `tests/fixtures/golden/graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (list of `{route, trailers}`), and the `help/` tree.
9. Implement the test to compare normalized captured output against goldens, and, when `--update-golden` is passed, rewrite the goldens instead.
10. Run `pytest tests/test_output_goldens.py`, then `pytest tests`.
11. Manually rename one key in the snapshot writer, confirm the golden test fails, then revert.

AMBIGUITIES:
1. Step 1 needs `desk/` docs, but Resolved Decisions says the test runs `deskops desk install <root>` to scaffold `desk/`; unclear whether `golden_desk/` holds `desk/` content, non-desk files (e.g., git config, models), or both, and how install interacts with pre-existing fixture content.
2. Implementation Path step 2 omits the seed commit that Resolved Decisions and closeout requirements imply; unclear when the seed commit is made, its content, and its message.
3. Unclear which of the 2 fixture tasks each closeout route targets, and what task state/status the closeout gates require.
4. `--run-dir <dir>` source is unspecified: how the run dir and `runs/subagents/index.jsonl` entry are produced (by what command), and whether the run must exist before `closeout commit`.
5. `closeout commit --no-run` needs a `--reason`; step 2 does not give it, and the reason becomes a compared trailer, so its exact fixed value is unknown.
6. `graph reflect` invocation arguments are unspecified.
7. Normalization detection rules are undefined: timestamp format(s), which paths count as absolute/root, hash length (short vs full), and other volatile values (versions, hostnames, Python version, run ids, durations, `Session-Sha256`).
8. Unclear whether comparison is byte-wise after normalization or structural (JSON parsed); affects key-order/indent/sort_keys expectations, and whether set-derived ordering must be canonicalized.
9. `help/<command path joined by _>` naming is undefined for the top-level `deskops --help` (no path) and for any name collisions.
10. "Every command path reachable from `deskops --help`" — recursion depth, whether leaf group commands without subcommands are included, and handling of aliases/duplicates is unspecified.
11. Done When's "fail when a key is renamed in the snapshot writer" names no file or key, and the check is manual only (no automated sensitivity assertion).
12. Dependency tasks (`task-rw-f0-*`, `task-doctor-crashes-on-deskless-roots`) have no stated completion status; whether they are done before execution is unknown.
13. Golden serialization details (JSON indent, trailing newline, `index.jsonl` line ordering/format) are unspecified.
14. Unclear whether `--update-golden` must write into the real repo working tree and whether that write is allowed for the executor given the no-commit rule.
