RESTATEMENT

1. Read `deskops/cli/registry.py`, `deskops/identity.py` (`find_local_store` :36, `resolve_store_context`), `deskops/cli/main.py` (`_apply_test_root_override` :184-216), `deskops/cli/commands/message.py` (:171-181) to see current resolution, guard, and dispatch wiring.
2. Add `resolve_context(args) -> (desk_root, store)` in `deskops/cli/registry.py`: `--root` → desk_root; `--store` → store; if both given and store != `<root>/.sldb`, raise a usage error naming both; otherwise fall back to cwd.
3. Rework the upward search so it stops at the first ancestor containing `desk/` or `.git`; if none exists up to filesystem root, set desk_root = cwd and let store-needing commands raise the existing "No local store found" error.
4. Insert `mutates=True` in the registry entries for: bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, deprecated inbox alias.
5. Read the handlers for atoms crossroad/proto/type and runtime workers/supervise; add `mutates=True` if they write files, store, or git.
6. Move the guard so it reads the `mutates=True` flag, runs for those commands only, and only when `--root` was not passed explicitly; keep its current redirect action (repoint to `DESKOPS_TEST_ROOT`/configured sandbox root, no refusal).
7. Call `resolve_context` from every command's dispatch path so all commands use one resolver.
8. Edit `deskops/cli/commands/message.py` to stop defaulting `--root` to `.` so the `--store` branch (:171-181) is reachable.
9. Add tests: (a) nested sandbox inside a repo never reads the outer registry, (b) `message list --store <s>` uses that store, (c) a test enumerating every `mutates=True` command so additions are deliberate.
10. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py`, then `pytest tests`.

AMBIGUITIES

1. `--store` given without `--root`: the task only defines behavior when both are given; the resulting desk_root is unspecified.
2. Whether `--store` given explicitly should also suppress the sandbox guard (guard text conditions only on `--root`).
3. Where the guard lives after resolution (main.py vs registry.py) and how it learns the dispatchee's `mutates` flag before dispatch.
4. Ordering: whether the guard runs before or as part of `resolve_context`, and how "explicit `--root`" is detected (argparse default vs `None` sentinel) while preserving existing CLI behavior.
5. `mutates=True` is per-command, but `doctor --repair` and `closeout commit` are flag/subcommand-conditional (e.g., `doctor` without `--repair` is read-only); whether `mutates` is per-command, per-subcommand, or per-flag is unspecified.
6. The exact fix for `message.py` is not stated (drop the `.` default vs change branch order); only the test outcome is given.
7. "a test lists every `mutates=True` command" — the mechanism (exact-set assertion that fails on additions vs snapshot listing) and file location are unspecified.
8. Test file names for the nested-sandbox test and the mutating-command-list test are not given.
9. Whether `tests/test_repo_identity.py` and `tests/test_message_cli.py` already exist, or must be created.
10. Whether the deprecated inbox alias still exists in the registry to be marked.
11. The "Read ... and mark them too if they write files" step is a judgment call, so the final mutating-command set is not verifiable against a fixed list.
12. Whether `--store` paths require validation (exists / is a store) is unspecified.
13. `find_local_store` (:36) is cited as the culprit but the task does not state whether it is modified, wrapped, or bypassed by `resolve_context`.
