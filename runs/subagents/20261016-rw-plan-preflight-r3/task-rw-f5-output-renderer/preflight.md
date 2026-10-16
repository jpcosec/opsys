RESTATEMENT:

1. Read `deskops/cli/render.py`, `deskops/cli/main.py`, `deskops/cli/registry.py`, `deskops/errors.py`, `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`, and existing CLI tests under `tests/` to learn current per-command printing and shape of the error classes.
2. Add format resolution to `main.py`/`registry.py`: a `--format` option (text/json/yaml) resolved early, stored on the parsed args, defaulting to text.
3. Implement in `deskops/cli/render.py` a single entry point, e.g. `render(data, fmt)` / `emit(...)`, that prints handler-returned data as text, json, or yaml.
4. Convert command handlers to return data instead of printing; call the renderer at the dispatch boundary in `main.py`.
5. Implement the error envelope: in `main.py`, wrap handler dispatch in try/except; on exception with resolved format json, print `{"ok": false, "error": {"code": <exit code>, "type": "<class name from deskops/errors.py>", "message": "..."}}` and exit with that code.
6. Ensure argparse usage errors are raised/printed by argparse to stderr with exit 2 and are never routed through the renderer (they occur before `--format` parsing).
7. Leave success JSON shape per the owner decision; the envelope work is done regardless.
8. Add golden tests for each JSON-capable command under `tests/`.
9. Run `pytest tests` (must be green) and `deskops list tasks --root . --format json`.

AMBIGUITIES:

1. Success JSON shape unresolved: A) today's per-command shapes, or B) `{"ok": true, "data": <today's shape>}`. Blocks "JSON outputs match the decision."
2. Scope says blocked on that decision, yet also "the error envelope is in scope either way" — no statement of whether to land the envelope alone now or wait.
3. No list of which commands are "JSON-capable" or must be ported.
4. No spec for `yaml` output: library, structure, or acceptance check.
5. No spec for `text` output: whether it must byte-match today's output or may change.
6. Format resolution rules unspecified: global vs per-command `--format`, default value, precedence, and what changes in `registry.py` (file is listed but not referenced in the Implementation Path).
7. Exit-code mapping unspecified: whether `deskops/errors.py` defines per-class codes or the code is derived otherwise.
8. Error envelope destination unspecified: stdout vs stderr.
9. Golden tests unspecified: location, naming, comparison method, and update mechanism.
10. Validation for non-JSON formats is absent from Validation and Done When.
11. Whether commands producing raw/streamed or diagnostic output (e.g. `--help`, progress) must go through the renderer.
12. Dependency `task-rw-f5-root-resolution-and-sandbox-guard` status/availability unknown; no statement of whether it must be closed before this task starts.
