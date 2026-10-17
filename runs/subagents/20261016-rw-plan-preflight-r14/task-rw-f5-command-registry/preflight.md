## RESTATEMENT

1. Confirm dependencies are closed and usable: `task-rw-f1-cli-contract-tests` (`tests/test_cli_contract.py`), `task-rw-f1-output-golden-files` (`tests/fixtures/golden/help/`), `task-rw-f3-atoms-service`, `task-rw-f4-single-snapshot-reader`. If any is missing/unclosed, stop.
2. Read `deskops/cli/parser.py` end to end; inventory every `add_parser` call and record per command: `path` tuple (top-level + subcommand + nested), `help`, `epilog`, per-arg flags/kwargs/type/default/choices, mutually exclusive group membership and whether the group is required (per parser.py:161, 185 required; 988 optional), output-format variant, current handler class, and whether the command writes state.
3. Inventory the shared args currently redefined per command: `--root`, selectors, `_add_output_format_argument` (parser.py:839-845, `text|json`), and the separate `text|json|yaml` variant used by inbox, message, faq (plus any runtime workers that add format args).
4. Inventory the data-driven loops at parser.py:715, 780, 874, 918 (including model-generated args) and identify the data source of each so each becomes a factory function.
5. Create `deskops/cli/registry.py` with frozen dataclasses:
   - `Arg(flags: tuple[str, ...], kwargs: dict, group: str | None = None, group_required: bool = False)`
   - `Command(path: tuple[str, ...], help: str, args: tuple[Arg, ...], handler: str, mutates: bool, epilog: str | None = None)`
6. Define the shared `Arg` instances/helpers once in `registry.py` (root, selectors, `text|json` format group, `text|json|yaml` format group) and reference them from commands.
7. Declare every command exactly once in the registry, in the same order the old parser added parsers, preserving insertion order so `--help` output stays byte-identical.
8. Convert each data-driven loop (parser.py:715, 780, 874, 918, model-generated args) into a factory function returning `tuple[Command, ...]`.
9. Port command groups in batches; after each batch run the F1 contract tests and the `help/` goldens:
   - `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`
10. Rewrite `deskops/cli/parser.py` so it walks the registry and calls `add_parser` only from the walker; reuse `Arg.group`/`group_required` to build mutually exclusive groups via `add_mutually_exclusive_group(required=...)`.
11. Update `deskops/cli/main.py` to build the parser from the registry and dispatch by resolving `handler` (`module:Class`) via `importlib` and invoking it, preserving current dispatch semantics and exit codes.
12. Delete all per-command builder functions from `parser.py`; leave only the registry walker and top-level parser construction.
13. Add `tests/test_command_registry.py`: build the registry, derive the set of command paths, derive the set from the filenames under `tests/fixtures/golden/help/`, assert set equality (drops and extras both fail).
14. Verify no forbidden file changed: `tests/test_cli*.py`, `tests/test_output_goldens.py`, `tests/conftest.py`, `tests/fixtures/golden/**`; do not run `--update-golden`.
15. Run validation: `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`; `python -m deskops --help`; `deskops faq`; `pytest tests`.
16. Report diff to supervisor; supervisor commits (executor does not), closeout requires `pytest tests` green.

## AMBIGUITIES

1. `deskops/cli/main.py` is listed in `files` and "dispatch" is in scope, but no statement of what must change there (parser construction, handler resolution, exit-code plumbing) or how handlers are currently dispatched.
2. `handler: str` is given as `module:Class`, but the full mapping of command → handler path is not provided; whether every command is class-backed or some are functions is unstated, so the resolution scheme (instantiate vs. call, lifecycle, shared state) is a guess.
3. Where handler classes live: `deskops.cli.commands.runtime` is only an example. Whether `deskops/cli/commands/` exists or must be created is not stated, and it is not in `files`.
4. Registry-equality test rule is underspecified: no defined mapping from `tests/fixtures/golden/help/` filenames to `Command.path` tuples (separator, nesting for subcommand groups, whether argument-bearing names are included).
5. Unknown whether `help/` goldens cover only top-level commands or also each subcommand group; "byte-identical" cannot be verified without that enumerated set.
6. `mutates: bool` has no derivation rule for commands whose mutation status is debatable (`graph build`, `closeout commit`, `stores check`).
7. No rule for `epilog`: which commands have one and where the text comes from is unstated.
8. `text|json` format group is described as living at parser.py:839-845 "and runtime workers" — the specific workers and where they attach format args are not identified.
9. For commands other than inbox/message/faq, keeping the `text|json` variant is only implied; a command that currently has no format arg is not covered by the rule.
10. Factory function names/locations and whether factories live in `registry.py` or per-command modules are unspecified, which affects import-cycle strategy.
11. Ordering constraint: registry declaration order must match old `add_parser` order for byte-identical help, but this is only implied, not stated.
12. `tests/test_cli.py` is named in Validation; if it does not exist (F1 created `tests/test_cli_contract.py`), the pytest invocation errors, and no guidance is given.
13. Dependencies (`task-rw-f3-atoms-service`, `task-rw-f4-single-snapshot-reader`) are listed but their status and interfaces are not given; no way to tell if the refactor surface is stable.
14. Task header says `status: deferred` while Resolved Decisions describe supervisor promotion before dispatch — no signal whether this execution run is authorized.
15. Done When does not state that `--format` variant assignment per command is part of acceptance, nor which goldens prove it.
