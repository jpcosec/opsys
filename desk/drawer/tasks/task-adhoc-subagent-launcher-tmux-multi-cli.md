---
id: task-adhoc-subagent-launcher-tmux-multi-cli
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:launcher
current_node: ''
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Ad-hoc subagent launcher (tmux + codex/agy/pi)

## Rationale

_Explain why this task exists or the business driver behind it._

Deskops assembles task context and closes out runs, but cannot launch an agent. Launching is done by an outside harness, so context, tool limits, monitoring, and return signals are all manual. This task makes launching a first-class, disk-persisted, deskops-native surface.

Source feature: `desk/drawer/features/feature-runtime-and-launcher.md`.

## Goal

_Describe the concrete result this task must produce._

Add `deskops launch` for one task using the existing Herdr runtime (`RuntimeProfileDoc` plus RoleDoc) with sldb-compiled context, persisted output, and deskops-mediated signals.

## Scope

_State what is in scope and what is out of scope._

- IN: single-task launch; per-role minimal bundle compiled via sldb; structured RoleDoc tool/model fields + migration of 3 roles; tmux run with `console.log` + `launch.yaml` + `launches.jsonl`; list/status/attach/stop/signal; one adapter per CLI (codex/agy/pi); handoff compatible with `closeout commit`.
- OUT (defer to follow-up drawer tasks): parallel/phase fan-out, auto-closeout after run, cross-repo launches, retry/resume, resource quotas, non-tmux backends.

## Implementation Path

_Outline the expected implementation route or affected surface._

- `deskops/models/role.py`: add `tools`, `model`, `fallback_models`; migrate `desk/roles/*.md` frontmatter.
- `deskops/launch/context.py`: shared, role-tabled, sldb-backed bundle builder (also refactor closeout to use it).
- `deskops/launch/runner.py`: tmux session mgmt + per-CLI adapters + console.log tee.
- `deskops/cli/commands/launch.py` + `parser.py` + `main.py`: the `launch` command group.
- Tests in `tests/test_launch.py` using a sandbox desk and a fake agent CLI (no real model calls); assert bundle-per-role minimality, tool-allowlist enforcement mapping, run-dir persistence, and signal round-trip.

## Validation

_List the checks required before this task can close._

- pytest
- `python -m deskops launch --help`
- launch a stub agent (fake CLI) against a sandbox task; assert `console.log`, `launch.yaml`, `launches.jsonl`, and `launch status` reflect persisted state.

## Done When

_Name the observable condition that makes the task complete._

Launcher runs a bounded profile-scoped agent from a task with sldb-compiled context, enforced per-role tools, disk-persisted output, and deskops-mediated status — validated and closed with a commit.
