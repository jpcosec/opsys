---
sldb:
  by: agent
  at: '2026-11-10T17:16:49Z'
  authority: generated
  via: update_document
id: atom-scion-coordinator-progresses-authorized-work
title: Scion coordinator progresses authorized work
five_wh_one_plus: how
tags:
- system:deskops
- topic:workflow
- topic:scion
- topic:autonomy
provenance: desk/tasks/task-scion-autonomy-coordinator-contract.md
---

# Scion coordinator progresses authorized work

## Answer

A Scion coordinator is a long-lived workflow supervisor, not a second scheduler or lifecycle engine. It recovers the configured current desk and tool sources from runtime context, checks canonical and dirty repository state, reads Board order and lifecycle/review gates, and inspects existing ownership from Scion labels, RunDoc and worktrees before selecting work. Source roots are tool import locations; implementation and test commands run from the configured desk_root, which is the task repository containing desk/. It skips tasks owned by another agent, but reconciles its own existing executor/tester lanes and completed handoffs first: a restart or successful child completion never makes the coordinator skip its own task or launch a duplicate. Only after that reconciliation does it select one dependency-ready unowned leaf; Board order is the only tie-breaker.

Reconciliation distinguishes Scion activity from phase. The native bridge can report phase=running while activity=completed; inspect activity=completed and the handoff evidence before deciding the child is still busy, using activity first and phase only as fallback. The coordinator may mutate modeled workflow state through the deskops and sldb CLIs, including routing, review disposition, run intent, advancement and closeout, but it never implements code. Ordinary factual or implementation questions are answered from task and source evidence; only unresolved owner decisions, real ownership conflicts, external credentials or permissions, and genuine human decisions are escalated. An accepted review is never rerun with unchanged input; technical retries are bounded to two attempts per unchanged input, and implementation correction plus independent retest cycles are bounded to two per task contract.

A dependency-ready authored task that still lacks preflight or bundle receipts is routine coordinator work, not a human blocker. The coordinator runs the existing cheap context-review CLI/ritual, adjudicates factual findings, and only then treats the task as reviewed-ready for dispatch; implementation waits until the execution gates pass. Dispatch identity is deterministic from the task contract: deskops-e for an executor or deskops-t for an independent tester, plus the first 12 hex characters of SHA256 over task id, NUL, the SLDB task contract digest, NUL and role. Attempt 1 uses that base name; attempt 2 appends -a2; there is no attempt 3. The child carries labels deskops.task_id, deskops.contract_sha256, deskops.role and deskops.attempt.

The coordinator writes RunDoc launch intent with outcome in_progress in the assigned run_dir before start; the summary says this is launch intent, not proof of start. Reconciliation reuses an existing matching RunDoc without rewriting it, and only a missing intent calls the runtime template to create one; a retry gets a new run_dir. A matching activity=completed child is inspected and its handoff reviewed before any correction launch; a stopped child resumes the same identity; unknown or unavailable Scion state is recorded as a blocker instead of duplicated. RunDoc attempts and evidence are immutable.

One executor runs per repository. A successful executor is followed by an independent tester with its own role identity and tester scope; a failed tester cannot support closeout, so the coordinator requests one bounded correction and a fresh test while preserving the failure evidence. After reviewing evidence the coordinator runs closeout verify, reviews the diff, and stages only the scoped implementation, evidence and review paths with deskops closeout commit --paths; it never uses git add -A. It reconciles the phase, then recovers and selects again. Only after all authorized work is closed, declared evidence verified and required phase integration/commit done does it write the final evidence summary and call sciontool status task_completed; an external blocker is persisted and signalled as blocked, while only an actual owner decision uses ask_user. Runtime context names absolute workspace, desk, source and sldb source roots plus the Scion project, emits DESKOPS_* environment variables and a workspace volume, and never carries secrets. Native Scion label values are printable ASCII of at most63characters. The helper preserves the full canonical contract hash and task id for name derivation and TaskDoc/RunDoc metadata, while the native contract label is its63-hex prefix. Short printable-ASCII task-id labels stay literal; longer or non-ASCII ids use a stable bounded hash descriptor. Copy helper labels exactly instead of reconstructing invalid64-hex labels.
