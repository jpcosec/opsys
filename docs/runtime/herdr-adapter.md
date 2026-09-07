# DeskOps runtime: Herdr adapter

DeskOps owns the semantic execution plan. Herdr owns the live terminal
workspace. The boundary is implemented by `deskops.runtime.herdr.HerdrProvider`.

## Identity invariant

Each DeskOps desk creates exactly one Herdr workspace for that execution:

```text
desk_id (durable semantic identity)
    -> ExecutionPlan
    -> Herdr workspace (ephemeral runtime identity)
```

`workspace_id`, `tab_id`, `pane_id`, and live agent names are runtime
references. They may be persisted as recovery hints, but they are never used
as the identity of a task or desk. If Herdr disappears, DeskOps must rebuild
the workspace from the plan and the durable desk state.

## Creation order

The adapter follows Herdr's actual lifecycle:

1. `workspace create` creates the workspace, first tab, and root pane.
2. `pane split` creates the remaining panes. Each `LayoutPaneSpec.parent`
   points to an already-created semantic pane.
3. `pane run` starts ordinary processes such as Neovim, Yazi, or tests.
4. `agent start --kind pi` starts Pi in an existing shell pane.

The adapter captures every Herdr ID from the command's JSON response. It does
not predict IDs or use DeskOps IDs as pane IDs.

## Failure and recovery

Herdr command failures raise `HerdrError`. The provider is intentionally
injectable with a command runner so the plan-to-runtime contract can be tested
without a running Herdr server. A future durable `ExecutionDoc` should store
the plan first and the returned runtime references second; recovery should
verify those references and recreate missing runtime objects.

## Scope of this adapter

The adapter owns workspace, pane, process, agent prompt, focus, status, and
close operations. It does not own task completion, gates, role semantics,
SLDB documents, Git worktree policy, or terminal rendering. Those remain
DeskOps/Opsys concerns.
