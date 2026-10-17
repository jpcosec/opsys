RESTATEMENT:
1. Verify prerequisites: confirm `task-rw-f3-atoms-service`, `task-rw-f4-single-snapshot-reader`, `task-rw-f1-cli-contract-tests`, `task-rw-f1-output-golden-files` are closed, and that `tests/test_cli_contract.py`, `tests/test_output_goldens.py`, and `tests/fixtures/golden/help/` exist.
2. Read `deskops/cli/parser.py` (~1,100 lines) and inventory every command path: name, help text, epilog, args, defaults, `required`, destination, mutually exclusive groups (parser.py:161, 185, 1094), and format variant (parser.py:906-912).
3. Inventory the data-driven command loops at parser.py:782, 847, 950, 1024, including model-generated args, and note their source data.
4. List the files under `tests/fixtures/golden/help/` to derive the mapping from golden file path to command path tuple.
5. Check bound pills `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md` and `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` for `when`/`where`/`how_not` constraints.
6. Create `deskops/cli/registry.py` with frozen dataclasses `Arg(flags, kwargs, group)` and `Command(path, help, args, handler, mutates, epilog)`.
7. Convert the four data-driven loops into factory functions returning `Command` objects (in `registry.py`).
8. Declare every command in the registry, with two shared format arg groups: `text|json` (runtime workers etc.) and `text|json|yaml` (inbox, message, faq), each command keeping its current variant.
9. Port commands group by group; after each group run `pytest tests/test_cli_contract.py` and the `tests/fixtures/golden/help/` comparison so help text and exit codes stay pinned.
10. Rewrite `parser.py` to a walker over the registry that is the only place calling `add_parser`; delete all per-command builder functions.
11. Update `deskops/cli/main.py` to resolve `handler` dotted `module:Class` paths and dispatch, mapping handler return to the pinned exit codes.
12. Add `tests/test_command_registry.py` asserting the registry command-path set equals the command-path set derived from `tests/fixtures/golden/help/`.
13. Run `pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py`, `python -m deskops --help`, `deskops faq`, then `pytest tests`.
14. Confirm Done When: `registry.py` exists, `parser.py` has no per-command builders, registry-equality test passes, contract/golden tests pass with files unmodified.
15. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. No instruction on verifying prerequisite task status or what to do if they are not yet done; the task is `status: deferred`.
2. `handler` is described as a dotted `module:Class` path, but no dispatch contract is given: constructor arguments, instance reuse, method name (`run`? `__call__`?), and how the returned value maps to exit codes.
3. No `deskops/cli/commands/` directory or its classes appear in `files`; unclear whether handler modules already exist or must be created, and if created, whether that is in scope.
4. `Command` has `help` and `epilog` but no `description`/`usage`; unclear where the root parser's and subparsers' descriptions come from.
5. Whether the root command (`deskops` itself, empty path) is a registry entry, which affects the path-equality test against the golden help directory.
6. Mapping from golden help filenames to command path tuples is unspecified (flat vs nested, separator, trailing extensions).
7. Which commands use `text|json` vs `text|json|yaml` is only partly enumerated ("runtime workers", "inbox, message, faq"); the full list must be inferred from parser.py.
8. Default value, choices ordering, and whether `--format` is passed as `default=`/`choices=` in `kwargs` is unspecified; byte-identical help depends on it.
9. Whether `_add_output_format_argument` (parser.py:906-912) is deleted, moved into the registry, or kept as a helper; `parser.py` "only walks the registry" implies removal, but it is not stated.
10. `Arg.group` semantics: whether the mutual-exclusion group is `required=True` and how the group is keyed/scoped (per-command vs per-parser) is not stated.
11. `mutates: bool` consumers are not specified; no guard, logging, or gate is described that reads it.
12. What changes in `deskops/cli/main.py` are expected beyond dispatch; the file is listed but no requirement is given.
13. Line references (161, 185, 782, 847, 950, 1024, 1094, 906-912) are revision-specific and no commit/branch is pinned, so they may not match the working tree.
14. Exit-code pinning is required, but no mechanism, mapping table, or contract detail is provided.
15. No instruction on where factory functions live or their naming convention.
16. `runs/planning/deskops-rewrite-inventory.md` is cited but is not in `files`; unclear whether it is readable or authoritative.
17. "Do not edit tests/test_cli*.py" does not cover other test files, so adding `tests/test_command_registry.py` is the only stated test addition; no criteria for its failure messages.
18. Done When does not require `pytest tests` green, while Resolved Decisions does; no rule for what to do if only one is unsatisfied.
