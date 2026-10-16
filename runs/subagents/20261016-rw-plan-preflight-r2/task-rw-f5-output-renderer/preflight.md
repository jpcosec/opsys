RESTATEMENT:

1. Read `README.md`, `docs/faq.md`, `desk/tasks/Board.md`, the board-routed pills, and `desk/rituals/execution.md` (per `AGENTS.md`), then load the `use-deskops` skill.
2. Read `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md` to extract the output-contract constraints.
3. Confirm `task-rw-f5-root-resolution-and-sandbox-guard` is closed; this task is `blocked` and `depends_on` it.
4. Read `deskops/cli/main.py` and `deskops/cli/registry.py` to enumerate every command handler, its current output formatting, and its current JSON shape.
5. Create `deskops/cli/render.py` exposing a single entrypoint (e.g. `render(data, fmt)` and `render_error(exc, exit_code, fmt)`).
6. Implement `text` output (current human formatting), `json` output (`json.dumps`), and `yaml` output.
7. Implement the error envelope: with `--format json`, print `{"ok": false, "error": {"code": <exit code>, "type": "<error class>", "message": "..."}}` and exit with that exit code.
8. For `--format yaml` and `--format text` error behavior, mirror existing/pre-decision behavior (unspecified — see AMBIGUITIES).
9. Change handlers in `main.py`/`registry.py` to return data instead of printing; route all printing through `render.py`.
10. Apply the success-shape decision (A: today's per-command shape, or B: `{"ok": true, "data": ...}`) to every JSON success path.
11. Add golden tests under `tests/` for each JSON-capable command, comparing stdout against committed goldens.
12. Run `pytest`.
13. Run `deskops list tasks --root . --format json` and compare to its golden.
14. Do not commit; leave the diff for the supervisor.

AMBIGUITIES:

1. Success-shape decision is unresolved (A vs B); Scope says the task is "Blocked on the owner decision about success shapes," but Implementation Path step 1 says the renderer/error envelope is "in scope either way" — is the whole task blocked or only step 2?
2. No list of "JSON-capable commands"; which commands must be ported and which have goldens is unspecified.
3. YAML library not specified (PyYAML? stdlib?); no dependency declaration in scope.
4. Exit-code mapping is unspecified: how `<error class>` maps to `<exit code>`.
5. `"type": "<error class>"` — Python class name vs stable slug is unspecified.
6. Error handling for `--format text` and `--format yaml` is not defined.
7. Errors raised before/during argument parsing (argparse failures) and whether they use the JSON envelope are unspecified.
8. Where command implementations live (registry vs main vs per-command modules) is not stated; the `list tasks` command file is not in `files`.
9. Golden-test location, naming, and update mechanism are unspecified.
10. Determinism requirements for YAML/JSON key ordering in goldens are unspecified.
11. Whether `--format` is global or per-command is unspecified.
12. "Every command" includes `faq`/`--help`/diagnostic commands? unspecified.
