RESTATEMENT:
1. Read `runs/planning/deskops-rewrite-inventory.md` (phase F5), the two pills, and current `deskops/cli/parser.py`, `deskops/cli/main.py`; inspect `tests/test_cli_contract.py`, `tests/test_output_goldens.py`, `tests/fixtures/golden/help/` to learn the pinned help text and exit codes.
2. Create `deskops/cli/registry.py` defining the registry types: a command entry carrying path, help, args, handler, and `mutates: bool`, plus shared argument group definitions (`--root`, selectors, and the two `--format` variants `text|json` and `text|json|yaml`).
3. Enumerate every existing command in `parser.py` and port them into the registry group by group, preserving per-command argument order and help text.
4. After each group, run `pytest tests/test_cli_contract.py tests/test_output_goldens.py`.
5. Rewrite `parser.py` as a walker that iterates the registry and builds the parser, leaving only the walker's own `add_parser` call.
6. Rewire `main.py` dispatch to route to registry handlers.
7. Delete the per-command builder functions from `parser.py`.
8. Add a test asserting the set of command paths from `build_parser()` equals the set declared in the registry.
9. Run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`, `python -m deskops --help`, `deskops faq`, then `pytest tests`.

AMBIGUITIES:
1. Registry type shape is unspecified: dataclass vs dict, exact field names/types, how `args` are represented (argparse specs, custom objects), and how shared arg groups are attached.
2. `mutates: bool` has no stated consumer or behavior; unclear whether `main.py` must act on it.
3. Which commands belong to the `text|json` vs `text|json|yaml` `--format` variant is not enumerated (only "inbox, message, faq" and "runtime workers" are named).
4. Handler contract is undefined: what arguments handlers receive, return values, and how exit codes are propagated to preserve the F1 pins.
5. Where the new registry-equality test file goes is unspecified, and it is unclear whether creating a new file under `tests/` is permitted given only some test paths are listed as off-limits.
6. Command-path representation for the equality test (e.g., `"graph build"` vs `["graph","build"]`) is undefined.
7. Nested subcommand groups (e.g., `graph build`) may require more than one `add_parser` call, conflicting with "the walker's own `add_parser` call is the only one left."
8. How shared args are inserted while keeping each command's argument order/position byte-identical to goldens is unspecified.
9. Scope of `main.py` changes is undefined beyond "parser and dispatch."
10. Whether dependency tasks (`task-rw-f1-*`, `task-rw-f3-atoms-service`, `task-rw-f4-single-snapshot-reader`) are complete is not stated.
11. Group definitions for "port commands group by group" are not given.
12. Whether `_add_output_format_argument` (parser.py:906-911) stays as a function or is replaced is unspecified.
13. No acceptance criterion states whether help output is verified by running the goldens test or by a separate unknown command.
