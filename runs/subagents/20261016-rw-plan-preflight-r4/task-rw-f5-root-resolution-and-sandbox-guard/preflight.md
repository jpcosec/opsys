RESTATEMENT:
1. Read `deskops/cli/registry.py`; add `resolve_context(args) -> (desk_root, store)`.
2. Change the shared `--root` argument in `deskops/cli/main.py` so an explicit `--root` is distinguishable from the default (default must stop being `.`).
3. Implement upward search from explicit `--root` (else cwd): stop at first ancestor containing `desk/` or `.git`; that is `desk_root`. If none up to filesystem root, `desk_root = cwd`.
4. Resolve store: `--store` wins; if both `--root` and `--store` given and store != `<root>/.sldb`, raise usage error naming both; else store = `<desk_root>/.sldb`.
5. Update `find_local_store`/`resolve_store_context` in `deskops/identity.py` to stop at `desk/`/`.git` instead of walking to `~/.sldb`.
6. Rewrite `_apply_test_root_override` in `deskops/cli/main.py`: same action (change root, not refuse), applied only to commands the registry marks `mutates=True`, and only when `--root` was not explicit.
7. Mark `mutates=True` in the registry for: bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, deprecated inbox alias.
8. Read handlers of atoms crossroad/proto/type and runtime workers/supervise; mark `mutates=True` if they write files/store/git.
9. Fix `deskops/cli/commands/message.py` so the `--store` branch (`:171-181`) is reachable (remove/fix `--root` default of `.`).
10. Add tests: nested sandbox never reads outer registry; `message list --store <s>` uses that store; test enumerating every `mutates=True` command.
11. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py`, then `pytest tests`.

AMBIGUITIES:
1. Mechanism to distinguish explicit `--root` from default is unspecified (sentinel, `argparse.SUPPRESS`, etc.).
2. Replacement default value for `--root` is not stated.
3. Required canonicalization/absolute form of `desk_root` (pill referenced, not in doc).
4. Exact store-vs-`<root>/.sldb` comparison rule (normalize, resolve symlinks, relative vs absolute) is unspecified.
5. Whether `find_local_store`/`resolve_store_context` are removed, renamed, or kept alongside `resolve_context`.
6. Whether ancestor match requires `desk/` AND `.git` or either; whether a `.git` file (worktree/submodule) counts.
7. "Stop at first ancestor with `desk/` or `.git`" vs `~/.sldb` stop rule interaction is not fully specified.
8. Which atoms crossroad/proto/type and runtime workers/supervise handlers "write files, the store or git" is left to executor judgment.
9. The Scope mutating-command list is "known today" with mixed path spellings and no canonical command names; not stated whether authoritative/complete.
10. "Out of scope: the registry format" conflicts with adding a `mutates=True` field to registry entries.
11. Source of truth / expected contents for the test that "lists every `mutates=True` command" is not given.
12. Deprecated inbox alias name and its mutation status are not given.
13. Precedence between `DESKOPS_TEST_ROOT` and an explicit `--root` is not stated.
14. Whether the guard applies only in sandbox/test mode or to any mutating command is ambiguous ("sandbox guard covers every mutating command" vs redirect action).
15. Which commands "need a store" (thus surface "No local store found") is not enumerated.
16. Whether `--store` without `--root` is allowed, and what `desk_root` becomes then.
17. Existence of `tests/test_message_cli.py` and `tests/test_repo_identity.py` is not verifiable from the doc.
