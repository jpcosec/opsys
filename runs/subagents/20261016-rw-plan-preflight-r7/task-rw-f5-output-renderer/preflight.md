RESTATEMENT:

1. Confirm dependency `task-rw-f5-root-resolution-and-sandbox-guard` is closed, the owner decision on success JSON (A or B) is made, and the task is unblocked; if not, stop.
2. Enumerate every command that currently accepts `--format` (search `deskops/cli/main.py` and `deskops/cli/registry.py` for the format flag/argparse wiring).
3. Run each such command against a fixed sandbox root (e.g. `.tmp/deskops-cli-test`) in text and json mode and capture stdout/stderr/exit code verbatim into `tests/fixtures/golden/output/<command_path_joined_by_underscore>.text` and `.json`.
4. Check in `deskops/errors.py` (from `task-rw-f2-typed-errors-and-exit-codes`) that exception class names and exit-code mapping exist; use them for the envelope.
5. Implement `deskops/cli/render.py`: accept handler result (data plus optional text formatter) and a format selection; print text via the formatter, json via `json.dumps` of the chosen success shape, yaml via `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
6. Implement the error envelope in `render.py`: on exception, if format is json, print `{"ok": false, "error": {"code": <exit code>, "type": "<exception class name>", "message": "<str(exc)>"}}` to stdout and exit with that code; if format is text, print existing text error and exit with the code.
7. Ensure argparse usage errors are not wrapped (exit 2, argparse stderr text), and that streaming/progress commands (`runtime supervise`) and `--help` bypass the renderer.
8. Port each `--format` command in `main.py` (and any registry wiring in `registry.py`) to return data (+ text formatter) instead of printing directly.
9. Add `tests/test_output_goldens.py` comparing each command's text/json/yaml stdout against the goldens; support `--update-golden` as the only refresh mechanism.
10. Run `pytest tests`, then manually `deskops list tasks --root . --format json` and `deskops list tasks --root .` and compare against goldens.

AMBIGUITIES:

1. Owner decision unresolved (A vs B for success JSON) — stated in task and in Open Ambiguities; the success shape cannot be implemented.
2. `status: blocked` plus `depends_on: task-rw-f5-root-resolution-and-sandbox-guard` — no statement that the dependency is closed; cannot know if preflight may proceed.
3. No list of which commands accept `--format`; "every command" is not enumerable from the task text.
4. Scope says record goldens for "today's text and json" only, but Done When requires yaml goldens; how yaml goldens are established is unstated.
5. `yaml` goldens cannot be recorded from current code (yaml output is new); no baseline for byte-identity.
6. Golden path template `<command path joined by _>` — undefined for nested subcommands and for commands whose output depends on flags/args (e.g. `--root`).
7. Handler return contract is undefined: no signature or type for "data plus, for text mode, a formatter".
8. `deskops/errors.py` (task-rw-f2) is not in `depends_on`; unclear whether it exists yet or whether class names/exit-code mapping are available.
9. `files` lists `deskops/cli/registry.py` but the Implementation Path never says what changes there.
10. `--update-golden` — owning command, flag placement, and behavior unspecified.
11. `ok: false` envelope includes `ok`, but the success envelope shape (A/B) determines whether `ok: true` exists; asymmetry stated only implicitly.
12. Detection rules for "streaming or progress output" and "`--help`" bypassing the renderer are not specified.
13. Text-mode "exactly today's stdout" — whether stderr and exit codes are also golden-compared is unstated.
14. Validation lists only `list tasks` for manual checks while Done When covers all `--format` commands; no per-command verification list.
15. Resolved Decisions say the supervisor promotes a drawer task, but the document header shows status `blocked` under active task paths with no drawer location; not contradicted, but no promotion evidence is present.

NONE
