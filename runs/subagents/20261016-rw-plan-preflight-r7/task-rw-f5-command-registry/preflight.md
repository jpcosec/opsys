RESTATEMENT:
1. Confirm prerequisites exist: tests/test_cli_contract.py, tests/fixtures/golden/help/ contents, tests/test_output_goldens.py; if missing, stop.
2. Read deskops/cli/parser.py fully; inventory every command path, its help text, args, defaults, mutually exclusive groups (parser.py:161, 185, 1094), epilog, and which `--format` variant it uses (`_add_output_format_argument` at 906-912 vs the inbox/message/faq text|json|yaml set).
3. Read deskops/cli/main.py to see how the parser is built, how the Namespace is dispatched, and where handler classes are instantiated.
4. Create deskops/cli/registry.py with frozen dataclasses `Arg(flags, kwargs, group=None)` and `Command(path, help, args, handler, mutates, epilog=None)`; define shared arg groups once (`--root`, selectors, both `--format` variants).
5. Convert the data-generated command loops (parser.py:782, 847, 950, 1024) into factory functions returning `Command`s, including model-generated args.
6. Port commands group by group into registry entries; after each group run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py` and confirm help goldens unchanged.
7. Rewrite parser.py as a registry walker: single `add_parser` call site, args built from `Arg` tuples, groups applied via `add_mutually_exclusive_group`, help/epilog preserved byte-identically.
8. Update main.py to resolve `handler` dotted `module:Class` paths and dispatch, preserving current exit codes.
9. Delete all per-command builder functions from parser.py.
10. Add tests/test_command_registry.py asserting registry command-path set == set of command-path files under tests/fixtures/golden/help/.
11. Run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`, `python -m deskops --help`, `deskops faq`, then `pytest tests`.
12. Do not edit tests/test_cli*.py, tests/test_output_goldens.py, tests/conftest.py, tests/fixtures/golden/; do not run `--update-golden`; do not rename commands or flags. Do not commit.

AMBIGUITIES:
1. No handler invocation contract: whether handlers receive `argparse.Namespace`, kwargs, or argv; constructor signatures and shared state are unspecified.
2. `mutates: bool` semantics and consumers are unspecified; only declaration is required.
3. `group` semantics unspecified: whether grouped args are mutually exclusive (as parser.py:161/185/1094 suggests) or merely clustered.
4. Registry path → golden help filename mapping convention unspecified (e.g., nested `graph build` vs top-level), so the equality test's normalization is a guess.
5. Byte-identical help requires unspecified argparse settings: `prog`, `formatter_class`, `description`, `epilog`, `usage`, `metavar`, `dest`, argument order and registration order.
6. Dependencies (task-rw-f3, f4, f1-cli-contract, f1-output-goldens) have no completion evidence; if goldens/contract tests are absent or differ, the task cannot be validated.
7. Task is `status: deferred` while framed as executable; no statement that prerequisites are closed.
8. Exact split of which commands use `text|json` vs `text|json|yaml` is not enumerated; must be inferred from parser.py.
9. Scope of main.py changes is undefined ("update main.py" implied by files list only).
10. Validation list omits pytest tests/test_command_registry.py, though Done When requires it; unclear whether it must run in the Validation gate.
11. No stated acceptance criteria for exit-code parity beyond "as pinned by F1 contract tests"; no list of those pins.
12. Factory function naming/location for data-generated commands is unspecified.
13. Whether hidden/alias commands count toward the registry-equality set is unspecified.
14. Whether global/top-level args and `--help` itself must live in the registry is unspecified.
