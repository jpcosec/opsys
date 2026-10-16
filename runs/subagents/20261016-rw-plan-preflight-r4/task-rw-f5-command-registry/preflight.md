RESTATEMENT
1. Confirm preconditions: `depends_on` tasks (task-rw-f3-atoms-service, task-rw-f4-single-snapshot-reader, task-rw-f1-cli-contract-tests, task-rw-f1-output-golden-files) are closed, task promoted to `desk/tasks/` with status active, both pills read, and `deskops/cli/parser.py`, `deskops/cli/main.py`, `deskops/cli/registry.py` reviewed.
2. From `deskops/cli/parser.py`, inventory every command, subcommand path, shared argument, help string, epilog, default, choice set, required flag, and the `mutates` behavior; note the four data-driven loops (parser.py:782, 846, 950, 1024) and `_add_output_format_argument` (parser.py:906-912).
3. Create `deskops/cli/registry.py` with frozen dataclasses `Arg(flags: tuple[str, ...], kwargs: dict)` and `Command(path: tuple[str, ...], help: str, args: tuple[Arg, ...], handler: str, mutates: bool, epilog: str | None = None)`.
4. Define shared argument data once in `registry.py`: the `text|json` group, the `text|json|yaml` group (inbox, message, faq), plus `--root` and selectors; record which variant each command uses.
5. Convert the four data-driven loops into factory functions returning `Command` tuples.
6. Port commands group by group into registry declarations, preserving help text, epilogs, argument order, defaults, choices, required flags, and mutates metadata; run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py` after each group.
7. Rewrite `deskops/cli/parser.py` as a walker over the registry that calls `add_parser` once per `Command.path`, applies `Arg.flags`/`Arg.kwargs`, and attaches handler/mutates metadata; leave the walker's own `add_parser` as the only one.
8. Update `deskops/cli/main.py` to dispatch by resolving `Command.handler` to the corresponding function.
9. Delete all per-command builder functions from `parser.py`.
10. Add a test asserting `set(command paths in build_parser()) == set(command paths declared in the registry)`.
11. Validate: `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`; `python -m deskops --help`; `deskops faq`; then `pytest tests`. Do not run `--update-golden`, and do not modify anything under `tests/fixtures/golden/` or `tests/test_cli*.py`, `tests/test_output_goldens.py`, `tests/conftest.py`.
12. Stop; the supervisor reviews the diff and performs the closeout commit.

AMBIGUITIES
1. No full command/subcommand inventory is in the doc; completeness of `registry.py` depends entirely on reading `parser.py`, which is not provided.
2. "Group by group" — no definition of groups or their order.
3. `--format` variant assignment is explicit only for `inbox`, `message`, `faq`; which commands use `text|json` vs `text|json|yaml` for everything else is unstated.
4. "Runtime workers" are mentioned in Scope but not named or listed in `files`.
5. `handler: str` — naming convention and the module/dispatch table `main.py` must resolve against are unspecified.
6. `mutates: bool` — what consumes it (gating, confirmation, logging) and where that behavior currently lives is unstated.
7. Epilog: which commands have epilogs, their content, and whether they attach to parent or subparsers is unstated.
8. "Byte-identical" help requires exact reproduction of argparse's usage/formatting; whether that includes prog-name, metavar, `argparse.SUPPRESS`, and Python-version-dependent formatting is unstated.
9. Exit codes are "as pinned by the F1 contract tests," but no exit-code table is given, so I cannot know them without reading `tests/test_cli_contract.py`.
10. The required registry-equality test has no specified file/location; `tests/test_cli*.py` are off-limits for edits, so where the new test file goes is unclear.
11. Acceptance is undefined if some existing commands cannot be expressed as `Arg(flags, kwargs)` (custom `type=`, callables, mutually-exclusive groups); no fallback rule is given.
12. Doc status is `deferred` and tags say `source:drawer`, while Resolved Decisions state promotion precedes dispatch; that promotion state is not observable from the doc.
13. Line references (parser.py:782, 846, 950, 1024, 906-912) may not match the current file; no rule for drift.
14. No criterion states whether the walker must preserve argparse's exact subparser construction order for `--help` output.
