RESTATEMENT:
1. Read `deskops/identity.py` (`find_local_store`, `resolve_store_context`), `deskops/cli/registry.py`, `deskops/cli/main.py` (lines ~186-209 guard), `deskops/cli/commands/message.py` (lines ~171-181), and the mutating-command handlers named in Scope.
2. Add `resolve_context(args) -> (desk_root, store)` in `deskops/cli/registry.py`: walk up from cwd, stop at first ancestor containing `desk/` or `.git`; derive `desk_root`; derive `store` from `--store` if given else `<desk_root>/.sldb`.
3. Apply rules: `--root` sets desk_root; `--store` sets store; both given but store != `<root>/.sldb` → usage error naming both.
4. Replace/redirect `find_local_store`/`resolve_store_context` usage in `identity.py` so resolution goes through `resolve_context` and no longer walks to `~/.sldb`.
5. Update guard in `deskops/cli/main.py` to read `mutates=True` from the registry entry for the invoked command instead of the current hardcoded check; ensure it can distinguish explicit `--root .` from default.
6. Mark `mutates=True` in the registry for: bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, deprecated inbox alias; inspect atoms crossroad/proto/type and runtime workers/supervise and mark if they write files/store/git.
7. Fix `message.py`: stop defaulting `--root` to `.` so `--store` branch is reachable.
8. Add tests in `tests/test_repo_identity.py` (sandbox nested in repo never reads outer registry) and `tests/test_message_cli.py` (`message list --store <s>` uses that store); add a test listing every `mutates=True` command.
9. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py` then `pytest tests`; leave changes uncommitted for supervisor review.

AMBIGUITIES:
1. `task-rw-f5-command-registry` is a dependency; no guarantee it is complete, and its registry format is out of scope yet this task adds `mutates=True` to it.
2. `find_local_store`/`resolve_store_context`: replace, wrap, or remove not stated; `~/.sldb` handling after change unspecified.
3. Behavior when no ancestor contains `desk/` or `.git` is unspecified.
4. Precedence when the nearest ancestor has only `.git` but a parent has `desk/` (or vice versa) is unspecified.
5. `--store` relative-path base (cwd vs desk_root) unspecified.
6. Usage error for `--root`+`--store` mismatch: class, exit code, and exact message format unspecified.
7. Mechanics for distinguishing an explicit `--root .` from the default value are unspecified.
8. `mutates=True` existence/shape in the current registry unverified; whether per-subcommand (e.g. `doctor --repair`, `repo register`) or per-command is unspecified.
9. "if they write files" for atoms crossroad/proto/type and runtime workers/supervise requires handler inspection; no criteria given for deciding.
10. Deprecated inbox alias: exact command name not given.
11. Test file for the "lists every `mutates=True` command" check not named.
12. Sandbox-in-repo test fixture/setup (creating nested sandbox, asserting no outer registry read) not specified.
13. Whether the guard change must also apply to nested subcommands invoked via `python -m deskops` vs `deskops` entrypoint is unstated.
14. Done criteria ("both new tests pass") conflicts with the extra third test for `mutates=True` commands; which tests count as the two is unclear.
