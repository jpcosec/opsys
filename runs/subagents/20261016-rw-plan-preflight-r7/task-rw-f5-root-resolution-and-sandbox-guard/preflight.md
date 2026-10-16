RESTATEMENT:

1. Read the command registry in `deskops/cli/registry.py` (and the dependency `task-rw-f5-command-registry`) to learn the command entry shape and how a `mutates` flag is declared.
2. Add `resolve_context(args) -> (desk_root, store)` in `deskops/cli/registry.py`: `--root` sets `desk_root`; `--store` sets `store`; if both are given and `store != <root>/.sldb`, raise a usage error naming both.
3. Implement the upward search inside that resolver: from cwd, walk up and stop at the first ancestor containing `desk/` or `.git`; if none exists up to the filesystem root, `desk_root` is cwd and commands needing a store fail with the existing "No local store found" error.
4. Update `find_local_store()` / `resolve_store_context` in `deskops/identity.py` (currently walking up to `~/.sldb`) so it no longer uses the outer repo registry.
5. Update `_apply_test_root_override` in `deskops/cli/main.py`: keep its current action (rewrites the root rather than refusing), gate it on `--root` not being passed explicitly, and apply it to every command whose registry entry is `mutates=True`.
6. Mark `mutates=True` for: bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, and the deprecated inbox alias.
7. Read the handlers of atoms crossroad/proto/type and runtime workers/supervise; mark `mutates=True` if they write files, the store, or git.
8. Fix `deskops/cli/commands/message.py`: remove/relax the `--root` default of `.` so the `--store` branch (lines ~171-181) is reachable.
9. Add tests: a sandbox nested inside a repo never reads the outer registry; `message list --store <s>` uses that store; a test that enumerates every `mutates=True` command.
10. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py`, then `pytest tests`.

AMBIGUITIES:

1. Relationship between the new `resolve_context` (registry.py) and the existing `resolve_store_context`/`find_local_store` (identity.py) is unspecified: replace, wrap, or keep both.
2. Exact usage-error mechanism and message: argparse error, custom exception, or exit code; "naming both" format unspecified.
3. Store path comparison for the both-given check: string equality, resolved path, or normalized path is unspecified.
4. How to detect that `--root` was "not given explicitly" (sentinel default, sentinel object, or inspecting `sys.argv`) is unspecified.
5. Registry contract from `task-rw-f5-command-registry` is not stated here: field name, decorator vs dataclass, and default value of `mutates` are guesses.
6. Priority between `DESKOPS_TEST_ROOT` and the configured sandbox root when both are set is unspecified.
7. Config file path/format carrying sandbox policy (per pill) is not given, so where the "configured sandbox root" is read from is a guess.
8. Whether the guard should also intercept explicit `--store` (not just root rewriting) is not stated.
9. Which commands "need a store" (for the `No local store found` fallback) is not enumerated.
10. The exact name of the "deprecated inbox alias" command is not given.
11. Exact CLI paths for `desk install/migrate/update` and `runtime init/stop` are assumed from the list.
12. Whether every command already accepts `--store`, or only some, is not stated; adding it globally could conflict with existing per-command options.
13. Whether `message list` already exists or must be added is unclear (only send/ack are named as mutating).
14. Tie-break rule when the nearest ancestor has `.git` but `desk/` lives in a different ancestor is not specified.
15. Which test file each new test belongs in (existing `tests/test_message_cli.py`, `tests/test_repo_identity.py`, or new files) is not stated.
16. Whether existing tests that assert the old `~/.sldb` walk behavior must be updated is not stated.
17. Acceptance criteria for "read the handlers ... and mark them too" is subjective; no observable condition distinguishes write vs non-write handlers beyond the stated heuristic.
18. `Open Ambiguities` says None and `Resolved Decisions` do not contradict the task text.
