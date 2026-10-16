RESTATEMENT:

1. Do not start: task is `blocked` on `task-rw-f5-root-resolution-and-sandbox-guard`, and on the owner decision about success JSON shape; wait for both and for supervisor promotion to `desk/tasks/`.
2. Read: `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`, `runs/planning/deskops-rewrite-inventory.md`, `deskops/errors.py`, `deskops/cli/main.py`, `deskops/cli/registry.py`, `deskops/cli/render.py`, `tests/test_output_goldens.py`, existing F1 goldens under `tests/fixtures/golden/`.
3. Implement in `deskops/cli/render.py`: a single renderer that takes handler-returned data plus `--format` and prints text, json, or yaml; yaml uses `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
4. Implement the error envelope: with `--format json`, on error print to stdout `{"ok": false, "error": {"code": <exit code>, "type": "<class name from deskops/errors.py>", "message": "..."}}` and exit with that code.
5. Leave argparse usage errors unwrapped: keep argparse's stderr text, exit 2, no envelope.
6. Wire `main.py`/`registry.py` so every command that accepts `--format` routes through the renderer; `--help` and streaming/progress output (e.g. `runtime supervise`) bypass it.
7. Port commands (success JSON per the resolved decision) to return data instead of self-formatting; text output stays byte-identical to today (F1 goldens).
8. Add/adjust goldens at `tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml>` for every `--format` command; refresh only via `--update-golden`.
9. Run validation: `pytest tests`; `deskops list tasks --root . --format json`; `deskops list tasks --root .`.
10. Complete only when every `--format` command prints through the renderer, its text/json/yaml outputs match goldens, and `pytest tests` is green.
11. Do not commit; hand the diff to the supervisor for the closeout commit.

AMBIGUITIES:

1. Success JSON shape (A per-command shapes vs B `{"ok": true, "data": ...}`) is unresolved; it changes every json golden and the data key, so no implementation or golden can be fixed.
2. The exact set of commands that accept `--format` is not enumerated; `registry.py` and `main.py` are listed as files but no command list is given.
3. The mapping from error class in `deskops/errors.py` to exit code is not stated here, so the envelope's `code` value is undetermined.
4. Which exceptions get wrapped into the envelope (only typed errors? unexpected exceptions?) is not specified.
5. Error behavior for `--format yaml` and `--format text` is undefined; only the json envelope is specified.
6. JSON serialization parameters (indent, separators, `sort_keys`, `ensure_ascii`) are unspecified while goldens are compared, likely byte-exact.
7. `<command path joined by _>` naming is not defined with examples (subcommand vs option inclusion), so golden filenames cannot be derived.
8. Whether text goldens are required for commands that only support json, and whether yaml goldens are required for commands that never emitted yaml, is unclear.
9. What the handler returns for text mode (a string printed verbatim vs structured data rendered) is not specified.
10. Where the renderer is invoked (per-handler call vs decorator/wrapper in `main.py` or `registry.py`) is not stated.
11. Validation steps have no expected outputs or assertions, so it is unclear what counts as passing beyond exit code and "green".
12. No test file or test case is named for the error envelope or the argparse-bypass rule; only golden comparison is named.
13. Repo guidance requires `pytest`; the task requires `pytest tests` — the intended scope is unstated.
14. Dependency completion state is not verifiable from the document alone.
