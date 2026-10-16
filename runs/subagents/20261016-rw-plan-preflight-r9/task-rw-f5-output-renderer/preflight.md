RESTATEMENT:
1. Verify prerequisite: dependency `task-rw-f5-root-resolution-and-sandbox-guard` closed and the owner decision on success JSON shape is recorded; without the decision the port cannot finish.
2. Enumerate from `deskops/cli/registry.py` / `main.py` every command accepting `--format` and which formats each accepts (text|json or text|json|yaml), without adding formats.
3. Capture today's stdout for each such command in each format it accepts and write to `tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml>`.
4. Add `tests/test_output_goldens.py` comparing live output to goldens, with refresh only via `--update-golden`.
5. Implement `deskops/cli/render.py`: `render(data, fmt, text_formatter=None)`; text → `text_formatter(data)`; json → `json.dumps`; yaml → `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`. Print to stdout.
6. Implement error envelope for `--format json`: print `{"ok": false, "error": {"code": <exit code>, "type": "<exception class name from deskops/errors.py>", "message": "..."}}` to stdout, exit with that code.
7. Leave argparse usage errors unwrapped: keep argparse stderr text, exit 2.
8. Refactor handlers (`main.py`, `registry.py`) to return data plus a text formatter instead of printing; route through the renderer. Streaming/progress (e.g. `runtime supervise`) and `--help` bypass the renderer.
9. Apply the owner's success-JSON decision (A: today's per-command shapes; B: `{"ok": true, "data": <today's shape>}`) across ports.
10. Run `pytest tests`; run `deskops list tasks --root . --format json`; run `deskops list tasks --root .`.

AMBIGUITIES:
1. Success JSON shape undecided (A vs B); task is `blocked` on it, so step 9 and the JSON goldens cannot be finalized.
2. Contradiction: goldens must be byte-identical to pre-port output, but under decision B the JSON output changes, so pre-port JSON goldens cannot hold.
3. Task states it is blocked and depends on a task whose completion is not verifiable from the document.
4. No list of commands that accept `--format` or which formats each accepts; must be inferred from code.
5. Envelope contents underspecified: source of `message`, and whether `code` is the numeric exit code, are not defined.
6. Error behavior for text and yaml formats is unspecified; only `--format json` is described.
7. Whether non-argparse pre-render errors (config load, root resolution) get the envelope is unspecified.
8. `--update-golden` mechanism (pytest option, env var) is not defined.
9. Behavior for `data` not serializable by `yaml.safe_dump`/JSON is unspecified.
10. Done When says "every command with `--format`" but Validation only exercises `list tasks`; per-command coverage criteria are missing.
11. What "handler returns data" means for the registry refactor (signature, registration) is unspecified.
12. Envelope is said to print "like the JSON it replaces" to stdout, but no criterion defines text/yaml channel or exit behavior on error.
13. "step 3" cross-reference in Scope is ambiguous (points to Implementation Path item 1 vs item 3).
