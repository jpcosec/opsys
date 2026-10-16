RESTATEMENT:

1. Confirm precondition: `task-rw-f5-root-resolution-and-sandbox-guard` is closed, and the Open Ambiguity (success JSON A vs B) is decided by the owner. Do not start while `status: blocked`.
2. Read `runs/planning/deskops-rewrite-inventory.md` (phase F5) to get the intended CLI/output surface.
3. Enumerate every command that accepts `--format` by scanning `deskops/cli/registry.py` and `deskops/cli/main.py`.
4. For each enumerated command, run it against the current (pre-port) code and record stdout: text and json into `tests/fixtures/golden/output/<command path joined by _>.text` and `.json`.
5. Create `tests/test_output_goldens.py` that re-runs each command and byte-compares stdout to the goldens, adding an `--update-golden` refresh path that rewrites the fixture files.
6. Create `deskops/cli/render.py` with a `render(data, format, text_formatter)` that dispatches: text → `text_formatter(data)` (today's stdout), json → success shape per owner decision, yaml → `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)`.
7. Add the error envelope in `render.py`: when `--format json`, print to stdout `{"ok": false, "error": {"code": <exit code int>, "type": "<ExcClass.__name__ from deskops/errors.py>", "message": "<str(exc)>"}}`, then exit with that code.
8. Wire `--format` parsing in `main.py`/`registry.py`; ensure argparse usage errors exit 2 with argparse's stderr text and are never wrapped; ensure `--help` and streaming/progress output (e.g., `runtime supervise`) bypass the renderer.
9. Port each `--format` command handler to return data (plus a text formatter) instead of formatting its own output.
10. Record/refresh `.yaml` goldens for each ported command to satisfy Done When.
11. Run validation: `pytest tests`; `deskops list tasks --root . --format json`; `deskops list tasks --root .`.

AMBIGUITIES:

1. Blocking owner decision unresolved: success json is A) today's per-command shape or B) `{"ok": true, "data": ...}`. Task is `status: blocked`; steps 6, 9, 10, 11 cannot be finalized.
2. Golden filename spec `<command path joined by _>` is underspecified: whether to include the `deskops` program name, and how subcommand groups/positional args/flags map to segments (e.g., `deskops list tasks` → `list_tasks`?).
3. DoD requires yaml goldens match, but step 3 says record "today's text and json stdout" only. No instruction for producing yaml goldens when yaml output does not exist yet (`--format yaml` support today is unstated).
4. It is unstated which format is default, the full accepted `--format` value set, and whether `--format` is global or per-command.
5. Streaming/progress bypass is specified by example only (`runtime supervise`); no enumeration of which commands count as streaming/progress or how the renderer detects bypass.
6. Error-envelope behavior for `--format text` and `--format yaml` is unspecified; only the json envelope shape is defined.
7. `--update-golden` mechanism unspecified: pytest flag, CLI subcommand, or env var, and how it is invoked.
8. `type` for exceptions not defined in `deskops/errors.py` (e.g., unexpected/unhandled exceptions) is unspecified.
9. No acceptance criteria given for commands that fail to run in the golden harness (missing root, empty state, non-deterministic content such as timestamps or absolute paths), so golden stability is unverified.
10. Whether the renderer/port/envelope land in one diff or separate commits is unstated; Resolved Decisions say the executor does not commit, so commit boundaries are the supervisor's, but the granularity is undefined.
11. `depends_on` target's actual completion state and contract (e.g., `--root` resolution behavior used by validation commands) is assumed, not verified from the task text.
12. It is unstated whether non-deterministic json/yaml key ordering must be normalized for byte-identity, given `sort_keys=False` is mandated for yaml.
13. Whether argparse usage errors must remain identical for all subcommands or only top-level parsing is not specified.
14. Whether every `--format`-accepting command must support all three formats (text/json/yaml) or only those already supported is not stated.
