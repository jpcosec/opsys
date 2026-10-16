RESTATEMENT:

1. Read `deskops/cli/parser.py`, `deskops/cli/main.py`, `tests/test_cli.py`, `tests/test_cli_contract.py`, `tests/test_output_goldens.py`, and `tests/fixtures/golden/help/` to inventory every existing command: path, help text, args, handler, and exit-code behavior.
2. Create `deskops/cli/registry.py` with frozen dataclasses `Arg(flags: tuple[str, ...], kwargs: dict)` and `Command(path: tuple[str, ...], help: str, args: tuple[Arg, ...], handler: str, mutates: bool, epilog: str | None = None)`.
3. Define shared argument builders once in the registry: the `text|json` group (currently `_add_output_format_argument`, parser.py:906-912, plus runtime workers) and the `text|json|yaml` group (inbox, message, faq); assign each existing command its current variant.
4. Convert the four data-driven command loops (parser.py:782, 846, 950, 1024) into factory functions returning `Command` objects.
5. Populate the registry with one `Command` per existing CLI command, preserving each command's path, help, args, handler, mutation flag, and epilog.
6. Rewrite `parser.py` as a walker that iterates the registry and calls `add_parser` once per `Command` (only `add_parser` call remaining), wiring handlers back to the callables referenced in `main.py`.
7. Port group by group; after each group run `pytest tests/test_cli_contract.py tests/test_output_goldens.py` until green.
8. Delete all per-command builder functions from `parser.py`.
9. Add a test asserting the set of registry command paths equals the set of command paths with a file in `tests/fixtures/golden/help/`.
10. Run validation: `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`; `python -m deskops --help`; `deskops faq`; `pytest tests`.
11. Hand the diff to the supervisor; do not commit.

AMBIGUITIES:

1. `handler: str` resolution is undefined: no rule for how a string maps to a callable (import path, `main.py` attribute, lookup table), or where that resolution lives.
2. Nothing states what consumes `mutates: bool` or what behavior must branch on it.
3. Registry-equality test file location/name is unspecified, and a natural name like `tests/test_cli_registry.py` collides with the stated ban on editing `tests/test_cli*.py`.
4. No rule for how golden help filenames encode command paths (flat vs nested dirs, separator, subcommand encoding), so the equality test's mapping is a guess.
5. Unclear whether the root `deskops` parser counts as a command path in the equality test and whether a golden exists for it.
6. No inventory of commands or of the "groups" used for incremental porting; coverage can only be inferred from the goldens.
7. Membership in `text|json` vs `text|json|yaml` is only exemplified (inbox, message, faq for the latter); the rest must be reverse-engineered from the current parser.
8. "runtime workers" for the `text|json` group is undefined and not identified in the repo.
9. `Arg(flags: tuple[str, ...])` has no representation for positional arguments, and it is unstated whether any command uses positionals or whether "selectors" are positional or optional.
10. Unspecified where shared helpers (`_add_output_format_argument` and siblings) live after the refactor: `registry.py` or `parser.py`.
11. Unspecified whether the four factory functions live in `registry.py` or `parser.py`.
12. "No per-command builder functions" is ambiguous about whether shared helpers count and whether subparser/parent wrappers are permitted.
13. Epilog sources are never given; unclear whether any command has an epilog to preserve.
14. No rule for aliases or hidden commands that would have no golden file and thus fail the equality test.
15. "Byte-identical `--help`" does not pin `prog` name, argv[0], terminal width, or argparse formatting environment, which affect output.
