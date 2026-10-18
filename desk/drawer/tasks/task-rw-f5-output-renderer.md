---
id: task-rw-f5-output-renderer
status: deferred
references: []
depends_on:
- task-rw-f5-root-resolution-and-sandbox-guard
pills:
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
files:
- deskops/cli/render.py
- deskops/cli/main.py
- deskops/cli/registry.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f5
- topic:cli
- topic:output
---

# One renderer for text, json and yaml output with an error envelope

## Rationale

_Explain why this task exists or the business driver behind it._

Each command formats its own output; JSON shapes differ by command and errors have no machine-readable form.

Plan: phase F5 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Handlers return data; deskops/cli/render.py prints it as text, json or yaml; with `--format json` an error prints `{"ok": false, "error": {"code": <exit code>, "type": "<class name from deskops/errors.py, e.g. DomainError>", "message": "..."}}` and exits with that code. argparse usage errors keep argparse's stderr text and exit 2 and are never wrapped, because they happen before `--format` is known.

## Scope

_State what is in scope and what is out of scope._

The renderer, the port and the error envelope land together after it. Handlers return data plus, for text mode, a formatter that produces exactly today's stdout; before porting, record today's stdout for every format each command accepts as the output goldens (step 3), so byte-identity is checked against them. yaml is `yaml.safe_dump(data, sort_keys=False, allow_unicode=True)` (PyYAML, already a dependency). The envelope prints to stdout, like the JSON it replaces. Streaming or progress output (for example `runtime supervise`) and `--help` bypass the renderer. Exit codes and class names come from deskops/errors.py (task-rw-f2-typed-errors-and-exit-codes).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Record the goldens of step 3 from the current code.
2. Implement the renderer and the error envelope, then port commands; success JSON follows the decision.
3. Goldens in tests/fixtures/golden/output/<command path joined by _>.<text|json|yaml> for every command that accepts `--format`, compared by tests/test_output_goldens.py and refreshed only with `--update-golden`.

## Validation

_List the checks required before this task can close._

- pytest tests
- deskops list tasks --root . --format json
- deskops list tasks --root .

## Done When

_Name the observable condition that makes the task complete._

Every command with `--format` prints through the renderer and, for each format that command already accepts (text|json or text|json|yaml; no command gains a format), its output matches the golden recorded before porting (under option B the json comparison is between the golden and the envelope's `data`); `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): option A. Success JSON keeps today's per-command shapes; the error envelope ships.

## Open Ambiguities

None.
