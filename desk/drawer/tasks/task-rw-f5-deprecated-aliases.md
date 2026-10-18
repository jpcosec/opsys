---
id: task-rw-f5-deprecated-aliases
status: deferred
references: []
depends_on:
- task-rw-f5-output-renderer
- task-rw-f5-command-registry
pills:
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
files:
- deskops/cli/registry.py
- deskops/cli/main.py
- deskops/cli/parser.py
- deskops/cli/commands/message.py
- tests/test_cli.py
- tests/test_message_cli.py
- docs/faq.md
- .pi/skills/use-deskops/SKILL.md
- .opencode/skills/use-deskops/SKILL.md
- README.md
- desk/atoms
- desk/contexts
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f5
- topic:cli
---

# Duplicate commands become warned aliases or are removed

## Rationale

_Explain why this task exists or the business driver behind it._

`inbox` duplicates `message`, `status` overlaps `doctor` (both run DoctorCLI, deskops/cli/main.py:80), and `atoms list/show` duplicate `list atoms`/`show atom`. The canonical side is `message`, `doctor` and `list atoms`/`show atom`.

Plan: phase F5 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

The owner's choice is applied to each duplicate.

## Scope

_State what is in scope and what is out of scope._

Alias behavior: before any output, print ``Deprecated: use `deskops <canonical>` `` on stderr, then run the canonical command. Removal behavior: argparse rejects the name (`invalid choice`, exit 2). Aliases stay listed in `--help` with their deprecation note (today's behavior, parser.py:500-505, asserted by tests/test_cli.py:42 and tests/test_message_cli.py:35). `inbox` has its own flag grammar (`--list/--show/--ack`) that `MessageCLI._run_legacy` (deskops/cli/commands/message.py:32,57) translates; that translation stays. Docs, skills, README.md, desk/atoms and desk/contexts that recommend an old name are updated in the same task; for a surviving alias, notes that say it is deprecated stay; for a removed name, every mention is rewritten to the canonical command. desk/drawer/ is history (use cases, stress tests) and is not edited.

## Implementation Path

_Outline the expected implementation route or affected surface._

Aliases: add a field `deprecated_for: tuple[str, ...] | None = None` (the canonical command path, e.g. `("message",)`) to the `Command` dataclass in deskops/cli/registry.py, which task-rw-f5-command-registry creates; the dispatcher (deskops/cli/main.py) prints the warning when it is set. Tests run the alias and the canonical command with equivalent args in the same test and assert the stderr line and byte-identical stdout, or exit 2 for each removed name (and update the command-set assertion in tests/test_cli.py:42 for removed names). Review every hit of the validation grep and rewrite the recommending ones.

## Validation

_List the checks required before this task can close._

- pytest tests
- deskops faq
- grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts

## Done When

_Name the observable condition that makes the task complete._

Each duplicate behaves per the decision and every remaining grep hit is a deprecation note, not a recommendation.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): all four duplicates (`inbox`, `status`, `atoms list`, `atoms show`) stay as warned aliases; none is removed.

## Open Ambiguities

None.
