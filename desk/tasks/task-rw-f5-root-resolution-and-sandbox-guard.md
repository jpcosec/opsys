---
id: task-rw-f5-root-resolution-and-sandbox-guard
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f5-command-registry
pills:
- desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md
- desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md
files:
- deskops/identity.py
- deskops/cli/main.py
- deskops/cli/commands/message.py
- deskops/cli/registry.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f5-root-resolution-and-sandbox-guard.md
---

# `--root` and the store resolve in one place, and the sandbox guard covers every mutating command

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory findings S7 and S8. `find_local_store()` (used by `resolve_store_context`, deskops/identity.py:36) walks up to `~/.sldb`, so a sandbox inside the repo uses the repo registry. The sandbox redirect `_apply_test_root_override` (deskops/cli/main.py:184-216) moves `--root .` to `DESKOPS_TEST_ROOT` or the configured sandbox root, but cannot tell an explicit `--root .` from the default, and its command list omits atoms, closeout, doctor and desk, which mutate the desk. `message` defaults `--root` to '.', so its `--store` branch (deskops/cli/commands/message.py:171-181) is unreachable.

Plan: phase F5 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

One resolver turns `--root`/`--store`/cwd into `(desk_root, store)` for every command and stops searching at the nearest ancestor that contains `desk/` or `.git`; the redirect keeps its current action (it changes the root, it does not refuse) but applies to every command the registry marks `mutates=True` and only when `--root` was not given explicitly.

## Scope

_State what is in scope and what is out of scope._

In scope: the resolver, the guard, message.py. Rules: `--root` sets desk_root; `--store` sets the store; if both are given and the store is not `<root>/.sldb`, fail with a usage error naming both. Mutating commands (known today): bootstrap, init, add, edit, bind, advance, promote, repo register, desk install/migrate/update, atoms add-namespace/reorganize/create/delete/split/merge, closeout commit, doctor --repair, graph build, graph reflect, materialize, runtime init/stop, message send/ack, and the deprecated inbox alias. Read the handlers of atoms crossroad/proto/type and runtime workers/supervise and mark them too if they write files, the store or git; a test lists every `mutates=True` command so additions are deliberate. Out of scope: the registry format.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `resolve_context(args) -> (desk_root, store)` in deskops/cli/registry.py.
2. The upward search stops at the first ancestor with `desk/` or `.git`; if none exists up to the filesystem root, desk_root is the current directory and commands that need a store fail with the existing 'No local store found' error.
3. Mark the commands above `mutates=True`; the guard reads that flag.
4. Tests: a sandbox nested inside a repo never reads the outer registry; `message list --store <s>` uses that store.

## Validation

_List the checks required before this task can close._

- pytest tests/test_message_cli.py tests/test_repo_identity.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

All new tests (nested sandbox, `message --store`, the mutating-command list) pass and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
