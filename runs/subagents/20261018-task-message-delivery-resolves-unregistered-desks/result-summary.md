# Task: message delivery resolves unregistered desks

## What changed

### `deskops/identity.py`
- `EcosystemIdentity.what_repository_am_i_in()` gained keyword-only `allow_unregistered=False` and `default_to_directory_name=False`.
- `allow_unregistered`: when the repo's config identity is not listed at all by the local registry, return the config identity instead of raising `Repository id ... not found in registry`. Used by `message ack` and by sender resolution.
- `default_to_directory_name`: when the desk has no `project_identity`, resolve from the registry root match if present, otherwise the repo directory name. Used by target resolution for `send`/`ack`.
- Existing strict behavior is unchanged for callers that do not pass the new flags (`tests/test_repo_identity.py::test_a_registry_that_lacks_the_repo_still_fails` still passes).
- A registry entry for the same id at a different root still raises the unregistered-root/disagreement error even with the fallbacks.

### `deskops/cli/commands/message.py`
- `MessageCLI._resolve_target`: resolves target identity with `allow_unregistered=True` and `default_to_directory_name=True`; falls back directly to `desk/config.json` or the directory name when the target has no usable store; prints a stderr warning when `desk/config.json` has no `project_identity`.
- `MessageCLI._target_ecosystem` (new): anchors `EcosystemIdentity` at the target repo's own local store, never the sender's.
- `MessageCLI._sender_ecosystem` (new): builds `EcosystemIdentity` from the sender's cwd boundary/store, ignoring `args.store` (which is the target's store when `--root` is used).
- `MessageCLI._sender_project`: rewritten to resolve from the sender's own config/registry. `--from` is accepted when it matches the sender config identity or any id in the sender's registry; if the sender has neither config nor registry, the explicit id is honored; otherwise a clear `SLDBStoreError` is raised.
- `MessageCLI._config_identity` (new): reads `desk/config.json` identity with `unknown-project` normalized to `None`.
- Imports: `DeskConfig`, `UNKNOWN_PROJECT_IDENTITY`, `find_context_root`.

### `tests/test_message_delivery.py` (new)
- `test_send_to_target_without_project_identity_uses_directory_name`
- `test_send_resolves_sender_from_sender_repo_not_target_registry` (covers with and without `--from`)
- `test_ack_falls_back_to_config_when_registry_lacks_itself`

## Validation (all run with the mandated PYTHONPATH)

Task Validation commands, executed with the required prefix:

```bash
PYTHONPATH=/tmp/rw/wt/msgdeliver python -m pytest tests/test_message_delivery.py -q
# 3 passed in 51.11s

PYTHONPATH=/tmp/rw/wt/msgdeliver python -m pytest tests -q
# 463 passed, 3 skipped in 861.52s (0:14:21)  (exit 0)
```

Additional regression run after the final edit:

```bash
PYTHONPATH=/tmp/rw/wt/msgdeliver python -m pytest tests/test_message_delivery.py tests/test_repo_identity.py tests/test_registry_robustness.py -q
# 14 passed in 33.99s
```

Earlier affected-suite run:

```bash
PYTHONPATH=/tmp/rw/wt/msgdeliver python -m pytest tests/test_message_cli.py tests/test_repo_identity.py tests/test_registry_robustness.py -q
# 20 passed in 58.86s

PYTHONPATH=/tmp/rw/wt/msgdeliver python -m pytest tests/test_cli.py -q
# 92 passed in 176.65s
```

## Tests against unfixed code

Extracted HEAD (`git archive HEAD`) to `/tmp/msgdeliver-unfixed`, copied the new test file there, and ran:

```bash
cd /tmp/msgdeliver-unfixed
PYTHONPATH=/tmp/msgdeliver-unfixed python -m pytest tests/test_message_delivery.py -q
# 3 failed in 49.13s
```

Failures on unfixed code:
- `test_send_to_target_without_project_identity_uses_directory_name`: `SLDBStoreError: Desk config project_identity is not established (found 'unknown-project').`
- `test_send_resolves_sender_from_sender_repo_not_target_registry`: sender resolution used the target registry (`Unable to resolve sender identity` without `--from`; `Repository id 'sender-repo' not found in registry ... (found: target-repo)` with `--from`).
- `test_ack_falls_back_to_config_when_registry_lacks_itself`: `Repository id 'graph-repo' not found in registry ... (found: graph_ui).`

Manual sandbox reproduction was also run in `/tmp/msgcase` and `/tmp/msgcase2`; all three cases returned exit 0 after the fix and produced the expected `target_project`/`sender_project`/`acknowledged_by`.

## Ambiguities / task issues

- The task document cites no line numbers, so there was nothing to re-verify; the cited code locations (`message.py`, `identity.py`) were correct.
- Implementation Path step 1 says "a target whose registry lists only itself, with and without `--from`". The underlying defect for that case is sender resolution, not target resolution: the sender was looked up in the target's registry. Implemented and tested it as the sender-resolution case.
- `--from` is described as "checked against the sender's registry or config". Interpretation used: match the sender's config identity or any id in the sender's registry; if the sender has neither, accept the explicit id; otherwise raise a descriptive error.
- No sldb bug was found.

## Not done by instruction

No commit, no `git add`, and no desk-mutating deskops command was run in this worktree.
