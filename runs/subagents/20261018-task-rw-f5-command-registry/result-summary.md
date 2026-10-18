# task-rw-f5-command-registry — result summary

## What changed

- `deskops/cli/registry.py` (new)
  - Frozen `Arg(flags, kwargs, group, group_required)` and `Command(path, help, args, handler, mutates, epilog, description, raw_text, subcommand_dest)` dataclasses.
  - Declares all 104 command paths once, including model-generated `add`/`edit`/`list`/`show` subjects via factory helpers (`_add_subject_commands`, `_edit_subject_commands`, `_list_subject_commands`, `_show_subject_commands`).
  - Shared args defined once (`ROOT_ARG`, runtime root variant, message/inbox variants, `OUTPUT_FORMAT_ARG` text|json, `OUTPUT_FORMAT_YAML_ARG` text|json|yaml, herdr, store, repo, pythonpath, etc.).
  - `command_registry()` (cached) and `command_for_path()`.
  - Every command carries a dotted `handler` and a truthful `mutates` flag.
- `deskops/cli/parser.py` (rewritten, 1032 → 79 lines)
  - `build_parser()` creates only the root parser and walks `command_registry()`.
  - Only one `add_parser` call site remains; no per-command builder functions.
  - Handles shared/mutually-exclusive arg groups and preserves subparser dest names.
  - Sets `_deskops_command_path` on each parser for dispatch.
- `deskops/cli/main.py`
  - Removed per-command `if args.command == ...` dispatch and the `_bootstrap`, `_init`, `_graph*` methods.
  - Resolves the handler declared in the registry, preserving the previous SLDB-bootstrap gating (`_SLDB_BEFORE_DISPATCH`) and default-pythonpath behavior (`_DEFAULT_PYTHONPATH_COMMANDS`).
- `deskops/cli/commands/core.py` (new)
  - `AboutCLI`, `BootstrapCLI`, `InitCLI` (moved verbatim from `main.py`).
- `deskops/cli/commands/graph.py` (new)
  - `GraphCLI` with the graph build/neighbors/missing/reflect logic moved verbatim from `main.py`.
- `tests/test_command_registry.py` (new)
  - Asserts registry paths equal the `tests/fixtures/golden/help/` command paths.
  - Asserts unique paths and that every parent path is declared.

No files under `tests/fixtures/golden/`, `tests/test_cli*.py`, `tests/test_output_goldens.py`, or `tests/conftest.py` were modified. No `desk/` files were touched. No commits or `git add` were made.

## Validation commands and final result lines

- `PYTHONPATH=/tmp/rw/wt/registry python -m pytest tests/test_command_registry.py -q`
  - `2 passed in 0.33s`
- `PYTHONPATH=/tmp/rw/wt/registry python -m pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py -q`
  - `99 passed in 143.59s (0:02:23)`
- `PYTHONPATH=/tmp/rw/wt/registry python -m deskops --help`
  - exit `0`; line 1 `usage: deskops [-h] [--debug]`
- `PYTHONPATH=/tmp/rw/wt/registry python -m deskops faq`
  - exit `0`; printed `deskops FAQ questions:`
- `PYTHONPATH=/tmp/rw/wt/registry python -m pytest tests -q`
  - `412 passed, 3 skipped in 309.61s (0:05:09)`
- Byte-identity check: regenerated `--help` for all 104 golden command paths and diffed against a pre-change baseline; 0 files differ.

## Test run against the unfixed code

- `PYTHONPATH=/tmp/rw/wt/registry python -m pytest tests/test_command_registry.py -q`
  - Result: collection error, `ModuleNotFoundError: No module named 'deskops.cli.registry'`.

## Task inaccuracies / ambiguities

- Cited line numbers in `parser.py` were stale (file was 1032 lines). Located all code with grep, as instructed.
- The prescribed `Command` fields were insufficient for byte-identical help: `description` (repo `register`/`whoami` and generated `add` commands), `raw_text` (whether `formatter_class=RawTextHelpFormatter` is set), and `subcommand_dest` (each parent's argparse `dest`, e.g. `subject`, `atoms_command`) are also required. Added them with defaults; no behavior change.
- `Arg`'s `group`/`group_required` had to be separated from plain argparse `kwargs`; otherwise `group` leaks into `add_argument`.
- Runtime commands use `--root ... help="DeskOps repository root."`, unlike the shared `Target repository root.`; kept a separate constant to preserve the goldens.
- The task lists `deskops faq`; the worktree CLI is not installed on `PATH`, so validation used the equivalent `python -m deskops faq`.

## sldb issues

None observed.
