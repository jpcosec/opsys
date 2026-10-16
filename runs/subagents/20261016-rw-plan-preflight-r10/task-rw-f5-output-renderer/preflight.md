RESTATEMENT:
1. Confirm the blocking dependency `task-rw-f5-root-resolution-and-sandbox-guard` is closed and that this task was promoted from `desk/drawer/tasks/` to `desk/tasks/` before doing anything.
2. Enumerate every command that accepts `--format` and which formats each accepts (text|json or text|json|yaml); no command gains a new format.
3. Record goldens from the current code: run each such command in each accepted format, capture stdout to `tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml>`.
4. Implement `deskops/cli/render.py`: a single renderer that takes handler-returned data and a format, prints text (via the handler-supplied formatter that reproduces today's stdout) or json, or yaml via `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
5. Implement the error envelope: on `--format json`, print to stdout `{"ok": false, "error": {"code": <exit code>, "type": "<class name from deskops/errors.py>", "message": "..."}}` and exit with that code.
6. Leave argparse usage errors untouched (argparse stderr text, exit 2, never wrapped), and route streaming/progress output (e.g. `runtime supervise`) and `--help` around the renderer.
7. Wire `deskops/cli/main.py` and `deskops/cli/registry.py` so handlers return data (plus text formatter) through the renderer instead of formatting themselves.
8. Implement success JSON in the chosen shape (A: today's per-command shape; B: `{"ok": true, "data": <shape>}`) once the owner decides.
9. Add `tests/test_output_goldens.py` comparing rendered output to the recorded goldens, with refresh only under `--update-golden`.
10. Run `pytest tests`, `deskops list tasks --root . --format json`, and `deskops list tasks --root .`.
11. Do not commit; hand the diff to the supervisor for the closeout commit.

AMBIGUITIES:
1. Success JSON shape (A vs B) is undecided; the task is `status: blocked` on it, so goldens comparison for json and the port cannot be finalized.
2. Header says `source:drawer`, but Resolved Decisions say the supervisor promotes to `desk/tasks/` before dispatch — no info on whether promotion already happened.
3. No confirmation of the dependency `task-rw-f5-root-resolution-and-sandbox-guard`'s state or path.
4. Under option B, Done When says the json comparison is between the golden and the envelope's `data`, but the golden recorded in step 1 would be today's unwrapped shape; unclear whether the golden file stores raw shape or wrapped.
5. `<command path joined by _>` is undefined for nested subcommands and argument variants.
6. The set of commands that accept `--format`, and which formats each accepts, is not listed; must be discovered.
7. Which commands stream/progress output (bypassing the renderer) is not enumerated.
8. Handler-side text formatter signature/contract ("produces exactly today's stdout") is unspecified, and behavior for handlers without one is unstated.
9. Mapping of exit code → error class name in `deskops/errors.py` is not given.
10. Location/CLI surface of the `--update-golden` flag is unspecified.
11. "no command gains a format" requires knowing the current per-command format sets, which the task does not provide.
