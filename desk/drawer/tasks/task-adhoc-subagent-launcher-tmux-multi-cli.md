---
id: task-adhoc-subagent-launcher-tmux-multi-cli
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files: []
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:launcher
---

# Ad-hoc subagent launcher (tmux + codex/agy/pi)

## Rationale

Deskops assembles task context and closes out runs, but cannot launch an agent. Launching is done by an outside harness, so context, tool limits, monitoring, and return signals are all manual. This task makes launching a first-class, disk-persisted, deskops-native surface.

Source feature: `desk/drawer/features/feature-adhoc-subagent-launcher-tmux-multi-cli.md`.

## Goal

Add `deskops launch` so an operator can start a bounded, profile-scoped subagent for one task using an external agent CLI inside tmux, with context compiled from the local desk via sldb, tool limits per role, monitoring, disk-persisted output, and deskops-mediated return signals.

## Resolved Decisions

Operator principles (authoritative) and their rulings:

1. **Context is compiled via sldb from the local desk where each run happens.**
   - The bundle builder resolves context through sldb queries against the local `.sldb` store (tracked docs, sections, fields), not by raw file reads. Roles are compiled from the tracked `RoleDoc` under `desk/roles/` for the requested profile.
   - Extract one shared `deskops/launch/context.py` used by both launch and closeout so there is a single bundle contract.

2. **Context is ad-hoc to the task and role — minimal by profile.**
   - `tester` gets the smallest bundle: role prompt + task doc + validation targets + `next` state. No full graph, no unrelated pills.
   - `executor` gets role + task + bound pills + linked atoms + linked files + board slice + `next`.
   - `supervisor` gets role + board + phase state + routing pills.
   - Bundle composition is table-driven per role, not one-size-fits-all.

3. **Task scope stays limited for trackability.**
   - One launch = one task = one run dir. No multi-task or phase fan-out in this task (deferred).
   - The launch refuses to start if the task is not in an actionable node.

4. **Everything persists to disk.**
   - Run dir `runs/subagents/<ts>-<task-id>/` gains: `console.log` (append-only stdout+stderr via tee), `launch.yaml` (agent, model, role, tmux session, pid, started_at, status, tool-profile), plus the existing evidence contract consumed by `deskops closeout commit`.
   - A `runs/subagents/launches.jsonl` index mirrors the existing `index.jsonl`.

5. **Agent gets limited tools by profile (tool-enforced).**
   - Promote the per-role tool allowlist from prose into structured `RoleDoc` fields: `tool_allowlist: list[str]`, `model_primary: str`, `model_fallback: str | None`. Migrate the three existing roles.
   - The launcher translates `tool_allowlist` into each CLI's native permission mechanism (e.g. tester = read/grep/find/ls/bash only, no edit/write). If a CLI cannot enforce a limit, launch fails loudly rather than silently over-granting.

6. **Return signals flow back through deskops (fundamental).**
   - The launched agent reports progress/blocked/done by calling deskops itself (e.g. `deskops inbox --ack`, writing `result-summary.md`, and a new lightweight `deskops launch signal <run-id> --state {progress|blocked|done} --note ...` that appends to `launch.yaml` + `console.log`).
   - `deskops launch status <run-id>` reads those persisted signals; it does not depend on the agent's own session storage.

### CLI surface

```
deskops launch <task-selector> --agent {codex|agy|pi} --role {executor|tester|supervisor} [--model ...] [--root .]
deskops launch list
deskops launch status <run-id>
deskops launch attach <run-id>
deskops launch stop <run-id>
deskops launch signal <run-id> --state {progress|blocked|done} [--note ...]
```

### Remaining pinned decisions (previously open)

- Permissions posture: default to the role `tool_allowlist` (least privilege); no blanket auto-approve. Auto-approve only within the allowlisted tools.
- tmux: hard dependency for this task; if absent, launch fails with a clear message (non-tmux backend deferred).
- Injection channel per CLI: `pi` via `--append-system-prompt <brief-file>`; `codex exec`/`agy -p` via prompt arg with the brief path referenced and bundle files under the run dir. Pin exact flags during implementation and record as an atom.
- Run/session naming: `deskops-<short-hash(task-id)>-<ts>` to respect tmux name limits; full task id stored in `launch.yaml`.
- Completion signal: run is `done` when `result-summary.md` exists AND the tmux session has exited; `blocked`/`progress` come from `launch signal`.
- Launch registry: `runs/subagents/launches.jsonl` (source of truth) reconciled against live `tmux` sessions prefixed `deskops-`.

## Scope

- IN: single-task launch; per-role minimal bundle compiled via sldb; structured RoleDoc tool/model fields + migration of 3 roles; tmux run with `console.log` + `launch.yaml` + `launches.jsonl`; list/status/attach/stop/signal; one adapter per CLI (codex/agy/pi); handoff compatible with `closeout commit`.
- OUT (defer to follow-up drawer tasks): parallel/phase fan-out, auto-closeout after run, cross-repo launches, retry/resume, resource quotas, non-tmux backends.

## Implementation Path

- `deskops/models/role.py`: add `tool_allowlist`, `model_primary`, `model_fallback`; migrate `desk/roles/*.md` frontmatter.
- `deskops/launch/context.py`: shared, role-tabled, sldb-backed bundle builder (also refactor closeout to use it).
- `deskops/launch/runner.py`: tmux session mgmt + per-CLI adapters + console.log tee.
- `deskops/cli/commands/launch.py` + `parser.py` + `main.py`: the `launch` command group.
- Tests in `tests/test_launch.py` using a sandbox desk and a fake agent CLI (no real model calls); assert bundle-per-role minimality, tool-allowlist enforcement mapping, run-dir persistence, and signal round-trip.

## Validation

- pytest
- `python -m deskops launch --help`
- launch a stub agent (fake CLI) against a sandbox task; assert `console.log`, `launch.yaml`, `launches.jsonl`, and `launch status` reflect persisted state.

## Done When

Launcher runs a bounded profile-scoped agent from a task with sldb-compiled context, enforced per-role tools, disk-persisted output, and deskops-mediated status — validated and closed with a commit.
