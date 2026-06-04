# Workflow Policy Reference

Copied from `/home/jp/proyectos/humble/backups_cotizador/dev_backup/WORKFLOW.md` on 2026-06-04 to preserve the task workflow policy that informed the current deskops graph task atomization.

> **No task is complete without testing.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items

---

## The 4-Zone Model

```text
plan/           # Initial planning. Ephemeral - deleted when U-* completes.
|               # Context pills are drafted here during planification.
desk/
  tasks/       # Active work surface. Tasks deleted when resolved.
  drawers/     # Deferred work. Ideas waiting for prioritization.
  pills/       # Context pills bound to tasks. Audited after each step.
```

**Rule:** No surface may reference below it. `desk/` may reference `plan/` (rationale), never reverse.

---

## Context Pills

### What They Are

Pre-drafted rationale that makes tasks unambiguous. Subagents should **not create** anything - context was already drafted during planification.

Each pill captures:

- **Why** this approach over alternatives
- **What** constraints/guardrails drive the decision
- **Where** in the codebase changes apply
- **How** the pattern/model informs implementation
- **Language** - terminology conventions, naming rules
- **Scope** - context vs. implementation artifact

### Dimensions

| Dimension | Values |
|---|---|
| Type | `guardrail`, `decision`, `pattern`, `model` |
| Scope | `global`, `domain`, `component` |
| Language | `en`, `es`, Python, Typescript, etc |
| Nature | `context` (rationale) or `implementation` (artifact to create) |

### Pill Lifecycle

```text
Drafted (plan/) -> Bound to task (desk/pills/) -> Audited after step ->
  -> Still needed? Keep.
  -> Redundant with code/docs? Delete.
  -> Complete. Knowledge flows to code/docs. Delete.
```

**Non-redundancy rule:** Code is truth. Docs is index. Context is reasoning (subset of subset). Context pills must not repeat what is already in code or docs.

---

## Context Audit Ritual

After each step/execution:

```text
1. CHECK  -> Is every task aspect covered by a pill?
2. AUDIT  -> Are pills still accurate or stale?
3. UPDATE -> Update stale pills or delete them.
4. BIND   -> Link new pills to tasks as needed.
```

---

## Pre-Execution Gate

Before starting any task, subagent must ask:

> **"Is there any ambiguous or unclear aspect not covered by the context machine?"**

- **If no:** Proceed with execution.
- **If yes:** Call context composer agent to create additional pills. Do not proceed until task is unambiguous.

---

## The Rituals

### 1. Initialization Ritual

Before starting any work for an entire board or phase:

```text
1. ATOMIZE   -> Break into smallest possible child tasks
2. DEDUPE    -> Merge overlapping items
3. CLEAN     -> Delete legacy content
4. AUDIT     -> Verify existing work before claiming completion:
               - Check git history for phase commit messages
               - Verify artifacts exist as specified
               - Run tests to confirm state
5. RESOLVE   -> Resolve contradictory end states
6. BIND      -> Link context pills to tasks
7. INDEX     -> Regenerate desk/tasks/Board.md
8. EXECUTE   -> Begin work with explicit boundaries
```

> **Critical:** Do not mark a task "completed" without auditing git history. Trust the code, not the task file.

### 2. Execution Ritual

When a task is **done**:

```text
1. INVALIDATE -> Check if existing tests are broken. Update/delete.
2. VERIFY    -> Add new tests where necessary.
3. TEST      -> Run tests. ALL relevant tests must pass.
4. CHANGELOG -> Update changelog.md when the repo uses one.
5. AUDIT     -> Run Context Audit Ritual (check pills, delete stale).
6. DELETE    -> Remove task file.
7. BOARD     -> Update desk/tasks/Board.md.
8. COMMIT    -> Make atomic commit.
```

### 3. Phase Completion Ritual

When all tasks in a phase are done:

```text
1. COMPILE   -> Rebuild if applicable (bundles, dist).
2. AUDIT     -> Run tests + any quality checks.
3. REGRESS   -> Fix any test failures.
4. FLOW      -> Knowledge flows: pills -> code/docs. Delete redundant pills.
5. ADVANCE   -> Move to next phase.
```

---

## The Tasks Board

**Location:** `desk/tasks/Board.md`

```text
# Tasks Board

> Single entry point for all active work. Read this before starting any task.

## Active (status=open|in_progress)
| ID | Domain | Task | Priority | Depends On | Pills |
|----|--------|------|----------|------------|-------|

## Blocked (status=blocked)
| ID | Domain | Blocker | Gate |
|----|--------|--------|------|

## Ready to Promote (from drawers/)
| ID | Domain | Item |
|----|--------|------|
```

---

## The Deferred Board

**Location:** `desk/drawer/README.md` in this repo.

```text
# Drawers - Deferred Work

> Items waiting for prioritization. Stale after 6 months.

## Deferred Items
| ID | Topic | Stale After | Last Reviewed |
|----|-------|-------------|---------------|
```

**Stale rule:** Review at 6 months -> promote, delete, or re-date. No graveyard.

---

## Commit Triggers

Commits are made **only** when the Execution Ritual completes.

| Situation | Commit? | Message |
|---|---|---|
| Phase objectives fully checked | Yes | Use phase's specified message |
| Critical bug fix mid-phase | Yes | `fix(<scope>): <description>` |
| Chores (deps, config) | Yes | `chore(<scope>): <description>` |
| Phase not done | No | Work-in-progress is not a commit |

---

## Pre-Completion Audit

Before marking a task as **completed**, verify:

```text
1. GIT HISTORY  -> Do commits match the phase commit messages?
2. ARTIFACTS   -> Do all specified outputs exist at the specified locations?
3. TESTS       -> Do all tests pass?
4. CLEAN TREE  -> Are all untracked files either gitignored or tracked?
```

If any check fails:

- **Git history mismatch** -> Either rebase to match or update task to reflect reality
- **Artifacts missing** -> Implement them
- **Tests failing** -> Fix tests first
- **Dirty tree** -> Clean up before declaring done

> **Rule:** Trust the code, not the task file. The task file describes intent; git history is truth.

---

## Commit Message Format

```text
<type>(<scope>): <description>

Types:   feat, fix, docs, refactor, chore, test, perf
Scopes:  plan, database, persistence, runtime, quotation, item, etc.
```

---

## Branch Strategy

| Branch | Purpose | Policy |
|---|---|---|
| `dev` | Active development | Commit when Execution Ritual completes |
| `master` | Production | PR required; CI must pass |
| `legacy` | Archived reference | Never commit |

---

## CI Gate

E2E tests run automatically on PRs and pushes to `master` when configured.

- PRs to master require passing CI.
- Do not merge with failing tests.

---

## What NOT to Do (Anti-Patterns)

- Proceed with ambiguous task without calling context composer.
- Create implementation artifacts instead of referencing existing pills.
- Let pills drift from code/docs (redundant or stale).
- Keep pills after plan completion (knowledge should flow to code/docs).
- Mark task complete without auditing git history.
- Commit with untracked files (gitignore or track first).
- Skip tests to "get it done".
- Force-push to hide failures.
- Keep drawer items older than 6 months without review.
- Reference surfaces below current layer.
