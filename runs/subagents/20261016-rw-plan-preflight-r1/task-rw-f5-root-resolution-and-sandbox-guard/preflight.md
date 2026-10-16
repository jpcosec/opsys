RESTATEMENT:
1. Read `deskops/cli/registry.py`, `deskops/cli/main.py`, `deskops/identity.py`, `deskops/cli/commands/message.py`, plus the two bound pills to learn current command registration shape and existing sandbox/whitelist logic.
2. In `deskops/identity.py`: locate `find_local_store()` (line ~36) and change its upward walk so it stops at the first ancestor containing `desk/` or `.git`, instead of walking to `~/.sldb`.
3. In `deskops/cli/registry.py`: add `resolve_context(args)` returning `(desk_root, store)`, deriving both from `--root`/`--store`/cwd using the new boundary-stopping search, and exposing it uniformly to all commands.
4. In `deskops/cli/registry.py`: add a per-command "mutating" flag to every mutating command registration.
5. In `deskops/cli/main.py`: rewrite the sandbox guard (lines ~186-209) to (a) distinguish an explicit `--root .`/explicit root from the default, and (b) read the registry mutating flag instead of a hardcoded whitelist, so `atoms`, `closeout`, `doctor`, and `desk` are covered.
6. Rewire `deskops/cli/main.py` and every command to call `resolve_context(args)` as the single source of root/store, removing per-command root/store derivation.
7. In `deskops/cli/commands/message.py`: fix the `--root` default so the `--store` branch (lines ~171-181) becomes reachable, and route it through `resolve_context`.
8. Add tests: a nested sandbox under `.tmp/` asserting the repo registry is never touched; a `message --store` test asserting the store branch executes.
9. Run `pytest tests/test_message_cli.py tests/test_repo_identity.py`, then `pytest tests`.
10. Confirm done condition: sandbox under `.tmp/` never touches repo registry and `message --store` is reachable and tested.

AMBIGUITIES:
1. `depends_on: task-rw-f5-command-registry` is unresolved in this document (deferred status); it is unknown whether that dependency is closed, so registry shape may not exist yet.
2. Contents of the two bound pills are not provided; their constraints on version/sandbox policy and canonical desk identity are unknown.
3. "Repo boundary" is defined loosely as "first directory with `desk/` or `.git`" — precedence, and behavior when both exist at different depths, is unspecified.
4. Registry format/shape is not shown, so the concrete field name and default for the "mutating" flag are unknown.
5. The full list of mutating commands to mark is not enumerated; cannot verify completeness.
6. Existing whitelist contents at main.py:186-209 are not shown other than the noted omissions; unknown whether non-listed commands must remain allowed or now blocked.
7. "Stops at the repo boundary" vs the case of no `desk/` and no `.git` ancestor is unspecified (error? fall back to cwd?).
8. Whether `resolve_context` returns absolute or relative paths, and whether it validates existence of store, is unspecified.
9. Interaction between explicit `--store` and `--root` (precedence, conflict handling) is unspecified.
10. `message --root` default change is not stated (currently '.'); the intended new default is unknown.
11. Test file paths `tests/test_message_cli.py` and `tests/test_repo_identity.py` are asserted but their current existence/content is unverified.
12. No acceptance criteria for the guard's error behavior (message, exit code, exception type) when a sandbox violation is detected.
13. "sandbox under .tmp/" is not defined — how the sandbox is detected (path prefix, config flag, pill rule) is unspecified.
14. The `--root .` explicit-vs-default distinction has no stated mechanism (e.g., sentinel default vs `None`).
15. The actual normalization of `runs/planning/deskops-rewrite-inventory.md` S7/S8 is not included, so the precise inventory requirements cannot be verified.
