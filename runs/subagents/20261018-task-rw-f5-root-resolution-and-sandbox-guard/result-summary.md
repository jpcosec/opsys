# task-rw-f5-root-resolution-and-sandbox-guard

## Changed

- `deskops/identity.py`
  - Added `find_context_root(start=None)`: walks up cwd and returns the nearest directory containing `desk/` or `.git` (cwd when none matches).
  - Added boundary-aware `find_local_store(start=None)`: returns only `<boundary>/.sldb` when it is a real store; never an ancestor store.
  - `resolve_store_context()` now uses those helpers, so a nested sandbox cannot fall through to the outer repo store.
- `deskops/cli/registry.py`
  - Added `resolve_context(args) -> (desk_root, store)`: `--root` sets the root, `--store` sets the store, both given must agree on `<root>/.sldb` (else `UsageError` naming both), store-only derives the root from the store, neither uses the boundary walk.
  - Changed `ROOT_ARG_MESSAGE` default from `.` to `None` so the `--store` branch is reachable.
- `deskops/cli/main.py`
  - Added `_root_option_given(argv)` to distinguish an explicit `--root` (including `--root .`) from the default.
  - `CLI.run()` now computes the explicit-root flag, applies the sandbox override based on `command.mutates`, then calls `resolve_context` and writes the resolved root/store back onto args.
  - Rewrote `_apply_test_root_override(args, *, mutates, root_explicit)`: registry-driven, explicit-root-aware, same action (rewrites the root, never refuses), marker `_deskops_root_override`.
- `deskops/cli/commands/message.py`
  - Uses the boundary-aware `deskops.identity.find_local_store`.
- `deskops/cli/commands/repo.py`
  - Same import change (not in the task's file list, but required so `repo` commands obey the same boundary invariant).
- Tests
  - `tests/test_repo_identity.py`: nested-sandbox tests (no outer store; own store used); adjusted `repo whoami` fixture so root and store agree.
  - `tests/test_message_cli.py`: `message list --store <s>` test with no `--root`; adjusted old root+external-store calls to `<root>/.sldb`.
  - `tests/test_cli.py`: explicit `--root .` bypasses `DESKOPS_TEST_ROOT`.
  - `tests/test_command_registry.py`: exact set of every `mutates=True` command.

## Validation

- `PYTHONPATH=/tmp/rw/wt/rootres python -m pytest tests/test_message_cli.py tests/test_repo_identity.py -q`
  - `16 passed in 25.59s` (exit 0)
- `PYTHONPATH=/tmp/rw/wt/rootres python -m pytest tests -q`
  - `415 passed, 3 skipped in 349.74s` (exit 0)
- `PYTHONPATH=/tmp/rw/wt/rootres python -m deskops --help`
  - exit 0
- `tests/test_output_goldens.py::test_help_goldens`
  - `1 passed` (help output unchanged)

## Against unfixed code

Built `/tmp/unfixed` from `git archive HEAD`, copied the new test files, ran:

`PYTHONPATH=/tmp/unfixed python -m pytest tests/test_repo_identity.py::test_nested_sandbox_never_reads_the_outer_repository_store tests/test_repo_identity.py::test_nested_sandbox_uses_its_own_store_when_it_has_one tests/test_message_cli.py::test_message_list_uses_store_when_no_root_is_given tests/test_cli.py::test_explicit_root_dot_bypasses_the_sandbox_override tests/test_command_registry.py::test_mutating_commands_are_declared_explicitly -q`

Result: `3 failed, 2 passed`.
- Failed on unfixed: nested-sandbox-no-outer-store, `message list --store`, explicit `--root .` guard bypass.
- Passed on unfixed: nested-sandbox-own-store (old walk finds the nearest store first), mutating-command set (the existing registry already marked the expected set).

## Notes / ambiguities

- Existing tests paired `--root <repo>` with an ecosystem `--store` outside that root (e.g. `tmp_path/.sldb` while root was `tmp_path/target-repo`). That conflicts with the task's unconditional rule, so those fixtures/calls were changed to `<root>/.sldb`.
- `deskops/cli/commands/repo.py` was not listed but had the same `sldb.store.resolver.find_local_store` import; changed it so the boundary rule covers every command.
- `identity.resolve_store_context` shares the same helpers rather than importing `registry.resolve_context` (avoids a CLI->data-layer dependency).
- No sldb bug observed. No sldb files touched.
- Nothing committed or staged; no desk/ mutations performed.
