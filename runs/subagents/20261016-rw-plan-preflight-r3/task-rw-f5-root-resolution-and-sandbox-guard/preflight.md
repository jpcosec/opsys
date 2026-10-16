RESTATEMENT:

1. Read routing docs per AGENTS.md (`README.md`, `docs/faq.md`, `desk/tasks/Board.md`, rulerouted pills, rituals) and load `use-deskops`.
2. Inspect current code: `deskops/identity.py` (`find_local_store`, `resolve_store_context`), `deskops/cli/main.py:186-209` (sandbox rule), `deskops/cli/commands/message.py:171-181` (`--store` branch, `--root` default `'.'`), `deskops/cli/registry.py` (command registry and any mutates flag).
3. Add `resolve_context(args) -> (desk_root, store)` in `deskops/cli/registry.py`:
   - `--root` given → desk_root = that path.
   - `--store` given → store = that path.
   - neither → walk up from cwd, stopping at first ancestor containing `desk/` or `.git`; that is desk_root.
   - no ancestor found → desk_root = cwd.
4. If both `--root` and `--store` given and store != `<root>/.sldb`, raise a usage error mentioning both.
5. Commands needing a store with no resolvable store → existing `No local store found` error.
6. Rewire `resolve_store_context` and its callers (`main.py`, `message.py`) to use `resolve_context`; remove `--root` default `'.'` in `message` so its `--store` branch is reachable.
7. In `deskops/cli/registry.py`, mark `mutates=True`: bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, deprecated inbox alias.
8. Read handlers of atoms crossroad/proto/type and runtime workers/supervise; mark `mutates=True` if handler writes files/store/git.
9. Update guard in `deskops/cli/main.py` to read the `mutates` flag and cover every mutating command, distinguishing explicit `--root .` from default.
10. Add tests: nested sandbox inside repo never reads outer registry; `message list --store <s>` uses that store; test enumerating all `mutates=True` commands.
11. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py`, then `pytest tests`.

AMBIGUITIES:

1. Contradiction: Scope/Path say the resolver lives in `registry.py`, but `deskops/identity.py` is listed as a task file with `find_local_store` at :36 — unclear whether `find_local_store` is replaced, kept as a wrapper, or edited.
2. Contradiction: "Out of scope: the registry format" vs. instruction to add a `mutates=True` marker — unclear if the flag already exists, must be added, or is forbidden.
3. Guard behavior is undefined: does it refuse the command, require explicit `--root`, prompt, or merely log? Only "cannot tell an explicit `--root .` from the default" is stated.
4. No specified error message text, exception type, or exit code for the `--root`/`--store` conflict beyond "usage error naming both".
5. No specified base for resolving a relative `--store` (cwd vs desk_root).
6. `.git` detection: directory vs `.git` file (worktrees) not specified; precedence when `desk/` and `.git` sit at different ancestor levels not stated.
7. "Commands that need a store" is not enumerated; unclear which commands fail vs. run without a store.
8. `mutates` granularity unclear: whole command vs. per-subcommand (e.g., `doctor --repair` only, `message send/ack` but not `list`, individual atoms subcommands).
9. "Read the handlers of atoms crossroad/proto/type and runtime workers/supervise" — file paths/command names not given; behavior if they do not exist is unspecified; "writes files" criterion (read-only flags, caches, temp files) is undefined.
10. Dependency `task-rw-f5-command-registry` is `status: deferred`; whether `registry.py` or the `mutates` flag exists at execution time is unknown.
11. Test file locations/existence: `tests/test_message_cli.py` and `tests/test_repo_identity.py` are assumed; the name/location of the "mutating-command list" test is unspecified.
12. Acceptance of "nested sandbox never reads the outer registry" has no concrete assertion specified (which registry, `~/.sldb` vs repo registry, expected vs forbidden calls).
13. Exact CLI command tokens ("desk install/migrate/update", "deprecated inbox alias") are not mapped to registry identifiers.
14. Whether `resolve_context` replaces `resolve_store_context` in the public API or wraps it, and whether other callers exist, is not stated.
15. Done When requires all three new tests plus `pytest tests`; no criteria for guard error text or exit status.
