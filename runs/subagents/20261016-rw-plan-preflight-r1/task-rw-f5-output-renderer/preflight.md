RESTATEMENT:
1. Read `deskops/cli/render.py`, `deskops/cli/main.py`, `deskops/cli/registry.py`, plus pill `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md` and `runs/planning/deskops-rewrite-inventory.md` (phase F5).
2. Confirm `depends_on: task-rw-f5-root-resolution-and-sandbox-guard` and the owner decision are resolved; if not, stop — task is `blocked`.
3. Define the error envelope schema (field names, required fields) in `deskops/cli/render.py`.
4. Add a single render entry point in `render.py` handling `--format text|json|yaml`; route text/json/yaml and error output through it.
5. Port each command in `deskops/cli/main.py` and its `registry.py` binding to call the renderer instead of formatting inline, preserving current JSON shape unless the decision permits the envelope.
6. Add golden tests for each JSON-producing command (text and yaml cases too), and envelope tests for the `--format json` error path.
7. Run `pytest`.
8. Run `deskops list tasks --root . --format json` and compare output against golden/decision.
9. Confirm every command prints through the renderer and error envelopes appear for json errors.

AMBIGUITIES:
1. Task `status: blocked` and `depends_on` unresolved — no instruction says whether to execute or halt.
2. Owner decision on JSON shape change is open — cannot know whether to keep today's shapes or emit a single envelope; "Done When" depends on it.
3. Envelope schema is unspecified (field names, nesting, error codes, success vs error discrimination).
4. "Every command" is unbounded — no list of commands in scope; `registry.py` and `main.py` contents not provided.
5. Unclear whether `--format` flag already exists, is global or per-command.
6. YAML output: no YAML dependency/library decision given; unclear if PyYAML is available.
7. No acceptance criteria for text format (exact formatting/padding) or yaml.
8. Unknown external consumers — no inventory to judge breakage.
9. Validation command `deskops list tasks` may not exist as-is; expected output not stated.
10. Golden tests: no file paths, no fixture source, no update mechanism given.
11. Pill content not included — contract requirements unknown.
12. `runs/planning/deskops-rewrite-inventory.md` not provided; phase F5 details unknown.
13. Error envelope scope: unclear whether non-JSON formats also render errors specially, or only `--format json`.
14. Exit codes for errors unspecified.
15. No file list for tests; `deskops/cli/render.py` may be new or existing — unclear.
16. Relationship to dependency task's changes (root resolution/sandbox guard) unknown.
