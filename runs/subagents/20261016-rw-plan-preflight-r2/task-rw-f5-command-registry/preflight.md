RESTATEMENT:
1. Read `deskops/cli/parser.py`, `deskops/cli/main.py`, `deskops/cli/registry.py`, `tests/test_cli.py`, `tests/test_cli_contract.py`, `tests/test_output_goldens.py`, and goldens under `tests/fixtures/golden/help/`.
2. Define registry types in `deskops/cli/registry.py`: one declaration per command with path, help, args, handler, `mutates: bool`; define shared args once (`--root`, selectors, `--format`).
3. Port parser commands group by group into registry entries, preserving command names, flags, help, usage, error text, and exit codes.
4. After each ported group, run `pytest tests/test_cli_contract.py` and the `tests/fixtures/golden/help/` goldens.
5. Rewrite `deskops/cli/parser.py` to walk the registry and build argparse; delete per-command builder functions; keep `add_parser(` count at most 3.
6. Route dispatch through registry handlers, including the `mutates` flag; update `deskops/cli/main.py` as needed.
7. Run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`, `python -m deskops --help`, `deskops faq`, and `pytest tests`.
8. Confirm `grep -c 'add_parser(' deskops/cli/parser.py` ≤ 3 and contract/golden tests pass unmodified.
9. Do not commit; leave the diff for supervisor closeout.

AMBIGUITIES:
1. Registry schema is undefined: field names/types for args, handler signature, and `mutates` semantics are unspecified.
2. “Group by group” is undefined: no groups, boundaries, or port order are given.
3. Shared args are only partially listed; the full set and precedence are unspecified.
4. Contradiction: “parser.py only walks the registry” and deleting builder functions vs. allowing up to 3 `add_parser(` calls; the permitted calls are unspecified.
5. “Byte-identical” help/usage/error/exit codes lack a stated baseline; goldens cover help only, not error text or exit codes.
6. `deskops/cli/main.py` is in scope as a file, but the task never states what to change there or how handlers are dispatched.
7. Dependency states are unknown: whether `task-rw-f3`, `task-rw-f4`, `task-rw-f1-cli-contract-tests`, and `task-rw-f1-output-golden-files` are complete is not stated.
8. No acceptance criteria for `registry.py` beyond existence; no test proves the parser is driven by the registry.
9. `pytest tests` has no stated baseline; unrelated failures would block validation.
10. No guidance for commands needing non-declarative/special behavior or how to represent them.
11. `mutates: bool` has no stated consumer, gating, or runtime effect.
12. “Contract and golden tests pass unmodified” does not say whether test files, fixtures, or both must remain unchanged.
