RESTATEMENT:
1. Confirm dependency `task-rw-f5-root-resolution-and-sandbox-guard` is closed; if not, stop (task is `blocked`).
2. Read `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`, `deskops/cli/main.py`, `deskops/cli/registry.py`, and `deskops/errors.py`.
3. Enumerate every command that accepts `--format` and, per command, which formats it accepts (text|json or text|json|yaml).
4. For each such command/format, run the current CLI and capture stdout (and stderr/exit where relevant) into `tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml>`.
5. Add `tests/test_output_goldens.py` that re-runs each command, byte-compares against its golden, and supports `--update-golden` to refresh.
6. Implement `deskops/cli/render.py`: `render(data, fmt, formatter)` producing text via the supplied formatter, json, and `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
7. Implement the json error envelope: `{"ok": false, "error": {"code": <exit code>, "type": "<class from deskops/errors.py>", "message": "..."}}` to stdout, exit with that code; leave argparse errors on stderr with exit 2, unwrapped; bypass renderer for streaming/progress (e.g. `runtime supervise`) and `--help`.
8. Port `main.py`/`registry.py` handlers to return data plus, for text mode, a formatter that reproduces today's stdout.
9. Run `pytest tests`, `deskops list tasks --root . --format json`, `deskops list tasks --root .`.

AMBIGUITIES:
1. Success JSON shape is undecided (option A vs B in Open Ambiguities); the port and post-port json output cannot be finalized, and the task is explicitly blocked on it.
2. Contradiction: goldens are "recorded before porting" and compared for byte-identity, but under option B the json success shape changes post-port, so the pre-port json goldens cannot match. No instruction on regenerating them.
3. No enumerated list of which commands accept `--format` or which formats each already accepts; source of truth unspecified.
4. Golden filename scheme is under-specified: whether the top-level `deskops` name is included, how nested subcommands are joined, and which argv (e.g. `--root .`, other args) is used when recording.
5. `--update-golden` is referenced but not defined: which mechanism (pytest option, env var, script) and in which file.
6. Not stated how errors reach the renderer (raised exception vs returned result) nor how exit code maps to the `<class name>` in `deskops/errors.py`.
7. Ambiguity when a domain error's exit code equals 2: how to distinguish it from unwrapped argparse errors.
8. Not stated how "streaming or progress output" and `runtime supervise` are identified or marked to bypass the renderer.
9. Text-mode error output (stream, format, exit code) is unspecified; only the json envelope is defined.
10. Whether `tests/test_output_goldens.py` exists or is created by this task is unstated; `files` lists only three `deskops/cli/` files, no test files.
11. Whether the dependency task is already complete is not stated; `status: blocked` and no dependency status given.
12. "message" content is unspecified (exception `str` vs other).
13. Envelope goes to stdout, but whether today's text errors go to stderr is not stated, so "like the JSON it replaces" is unverifiable.
