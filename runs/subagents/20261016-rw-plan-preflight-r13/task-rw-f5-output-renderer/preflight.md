RESTATEMENT:
1. Verify `depends_on` `task-rw-f5-root-resolution-and-sandbox-guard` is closed and that `task-rw-f2-typed-errors-and-exit-codes` has landed, since `deskops/errors.py` must supply the exit codes and class names used by the envelope.
2. Obtain the owner decision on success JSON (option A vs B) before writing any success-JSON path, since the task is explicitly blocked on it.
3. Read `deskops/cli/main.py` and `deskops/cli/registry.py` to enumerate every command that accepts `--format` and which formats each accepts (`text|json` or `text|json|yaml`).
4. Run each such command in each accepted format against the current code (e.g. `deskops list tasks --root . --format json`) and capture stdout bytes into `tests/fixtures/golden/output/<command_path_joined_by_underscore>.<text|json|yaml>`.
5. Implement `deskops/cli/render.py`: a function taking handler data + a text formatter + selected format; text via the formatter, json via `json.dumps`, yaml via `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
6. Implement the error envelope in the renderer: on exception from `deskops/errors.py`, print `{"ok": false, "error": {"code": <exit code>, "type": "<class name>", "message": "..."}}` to stdout and exit with that code, when `--format json`.
7. Ensure argparse usage errors are not wrapped: they keep argparse stderr text and exit 2.
8. Change handlers in `main.py`/`registry.py` to return data plus a text formatter instead of printing; port every command that accepts `--format`; leave streaming/progress output (e.g. `runtime supervise`) and `--help` bypassing the renderer.
9. Add `tests/test_output_goldens.py` comparing live output to the goldens, with refresh allowed only via `--update-golden`.
10. Run `pytest tests`, `deskops list tasks --root . --format json`, `deskops list tasks --root .`.

AMBIGUITIES:
1. Owner decision A vs B (success JSON wrapped or not) is unresolved; the task is blocked and cannot be completed.
2. Status of `task-rw-f2-typed-errors-and-exit-codes` is unstated; whether `deskops/errors.py` already exposes the required exit codes and class names is unknown.
3. No mapping given for exit code / `type` of exceptions that are not `DomainError` (e.g. unexpected `Exception`); the example gives only `DomainError`.
4. Whether the error envelope also applies in text mode, or only `--format json`, is unspecified.
5. Whether anything is written to stderr for non-argparse errors is unspecified (only stdout is stated).
6. The list of commands accepting `--format` and their accepted formats is not in the task; it must be inferred from code.
7. Golden file naming collapses the command path with underscores; how nested subcommands map (e.g. `list tasks` → `list_tasks`) and how invocations requiring arguments are represented is unspecified.
8. Golden fixtures require concrete invocations/roots/seed data; none are specified, so golden content is undetermined.
9. Where `--update-golden` is implemented (pytest option vs CLI flag) is unspecified.
10. Role of `deskops/cli/registry.py` in the change (handler registry vs other) is not described.
11. Whether `runtime supervise` or other bypassed commands currently accept `--format` is unstated.
12. Whether the `code` field is an integer exit code and whether `type` is `type(e).__name__` for subclasses is not explicitly stated.
13. No acceptance criteria for error cases (which errors are tested, or golden coverage for errors) beyond the single envelope example.
14. Scope line "the renderer, the port and the error envelope land together after it" does not say how to sequence work while blocked; whether partial recording of goldens (step 3) is allowed now is not stated.
