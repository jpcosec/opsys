RESTATEMENT:

1. Read `desk/contexts/pill-010-graph-runtime-output-policy.md` and `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`, plus `README.md`, `docs/faq.md`, `desk/tasks/Board.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, `desk/rituals/closeout.md`.
2. Create fixture `tests/fixtures/golden_desk/` with a desk containing exactly: 2 task docs, 2 atoms, 1 pill (in `desk/contexts/`), 1 drawer task (`desk/drawer/tasks/`).
3. Write `tests/test_output_goldens.py` with helpers that: `shutil.copytree` the fixture into `tmp_path`, `git init`, make one empty seed commit, then drive `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root, capture_output=True, text=True)`.
4. In that sandbox run, in order: `deskops graph build`, `deskops graph reflect`, `deskops closeout commit --run-dir <dir>`, `deskops closeout commit --no-run --reason <why>`.
5. Read back: `.sldb/runtime/graphs/deskops.kg.json`, `.sldb/runtime/graphs/deskops.nx.json`, `.sldb/runtime/self_reflection_findings.json`, `runs/subagents/index.jsonl`, and the trailers of the two closeout commits (parse via `git log -1 --format=%B`/`%(trailers)`).
6. Normalize: timestamps -> `<ts>`, absolute sandbox paths -> `<root>`, commit hashes -> `<sha>`; emit JSON with `sort_keys=True, indent=2` and jsonl line-per-record.
7. Enumerate every command path reachable from `deskops --help` (recursively via the argparse parser) and capture each `--help` output.
8. Write goldens: `tests/fixtures/golden/graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (list of `{route, trailers}`), `help/deskops.txt`, `help/deskops_<sub>[_<subsub>].txt`.
9. Add `pytest_addoption` for `--update-golden` (store_true) in `tests/conftest.py`; keep normalization helpers in `tests/test_output_goldens.py`.
10. Implement the comparison test asserting normalized actual == golden, and in update mode rewriting goldens instead of asserting.
11. Run `pytest tests/test_output_goldens.py` then `pytest tests`.
12. Hand-verify sensitivity: rename a key in the snapshot writer, run the golden test, confirm failure, revert the rename.

AMBIGUITIES:

1. Fixture shape undefined: is `tests/fixtures/golden_desk/` a repo root (containing `desk/`, `desk/lifecycle/`, `.sldb`) or only a `desk/` directory to be copied into an initialized root?
2. Ordering contradiction: Implementation Path says "copy it into `tmp_path`, git init" while Resolved Decisions say "run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph)". If `init` creates the desk, does the fixture copy overwrite it, precede it, or require merge? No stated order.
3. Interchange with the fixture `lifecycle_desk`: the resolved decision allows it "faster", but it is unknown whether a fixture-built store yields byte-identical graph/help outputs to `deskops init`.
4. No content spec for the 2 tasks / 2 atoms / 1 pill / 1 drawer task (ids, statuses, fields), so golden content cannot be anticipated.
5. Which `--run-dir` value to pass (path shape, whether it must pre-exist, whether it must be inside the sandbox root).
6. Which command writes `runs/subagents/index.jsonl` (presumably `closeout commit --run-dir`) and whether it is relative to the repo root or the run dir; not stated.
7. `graph reflect` is named as the writer of `self_reflection_findings.json`, but it is unstated whether `graph build` or `closeout` also rewrites it before capture.
8. Exact normalization contract: which fields count as "timestamps", which patterns count as "absolute paths", and whether every 40-hex string is a commit hash to be replaced.
9. `closeout_trailers.json` key naming for `route` values (`--run-dir` vs `--no-run`, or `run`/`no-run`) and which trailer keys appear in each route is unspecified beyond the rationale's list.
10. `--help` reachability depth and treatment of aliases/hidden/deprecated commands; help filename rule for multi-word or hyphenated command names (`deskops_<sub>[_<subsub>].txt`) is ambiguous for nesting deeper than two.
11. `--update-golden` semantics unspecified: whether it also regenerates `help/`, whether it needs a TTY/confirmation, and whether it writes on partial failures.
12. Done When's hand-check names no specific key or file ("a key is renamed in the snapshot writer"), so the mutation target is undetermined.
13. No acceptance criteria for ordering stability (node order, line order) beyond normalization.
14. All `depends_on` tasks are `status: deferred`; the preflight cannot tell whether they are actually complete.
15. Task `status` is `deferred` and no promotion has occurred, so execution preconditions are unverifiable from the document alone.
