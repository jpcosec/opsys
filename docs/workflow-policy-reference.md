---
atoms:
- id: atom-cheap-zero-context-reviews-test-the-brief-recursively
  role: documents
- id: atom-docs-are-human-facing-atom-materializations
  role: documents
- id: atom-phase-gates-prevent-agent-skipping
  role: documents
- id: atom-code-changes-close-with-tests-and-commit
  role: documents
- id: atom-available-tasks-are-board-routed-work
  role: documents
- id: atom-drawers-feed-tasks-through-promotion
  role: documents
- id: atom-pills-carry-transitional-task-knowledge
  role: documents
- id: atom-pills-are-reusable-across-tasks
  role: documents
- id: atom-pills-end-as-atoms-docs-or-deletion
  role: documents
- id: atom-phases-are-dependency-layers-of-tasks
  role: documents
- id: atom-phase-closeout-reconciles-pills-and-next-work
  role: documents
- id: atom-tasks-enable-zero-context-subagents
  role: documents
- id: atom-task-board-phases
  role: documents
- id: atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly
  role: documents
---
# Workflow Policy Reference

Source atoms are declared in the YAML frontmatter.

This reference summarizes the current workflow policy used by `deskops`.

> **No task is complete without the closeout evidence it declared at creation and its own closing commit. No phase is complete without integration validation and pill reconciliation.**

## Quick Links

- [Task Management](../desk/tasks/Board.md) - Active tasks
- [Pills Reference](../desk/contexts/pills.md) - Context pill format
- [Deferred Work](../desk/drawer/README.md) - Waiting items
- [Context Review Ritual](../desk/rituals/context-review.md) - Cheap recursive brief comprehension
- [Phase Ritual](../desk/rituals/phase.md) - Dependency-layer execution and closeout

---

## Core Model

### Tasks

A task is the atomic workflow unit.

- One coherent deliverable.
- May depend on other tasks.
- Executes in a fresh subagent context.
- Declares how it activates and how it closes by choosing a task type (`deskops add task --task-type`); the type's activation rule names the review receipts it needs, the type's closeout rule names the evidence receipts it closes with, and the task closes only when `deskops closeout verify` has written them accepted and intact, with its own atomic closing commit. `--evidence` only adds kinds to the type's floor, never removes one the type requires.

#### Task types

A task type is a model: a `TaskDoc` subclass registered in the store. `model <= <Tipo>` names the type's family (including its subtypes); a subtype inherits the gates of its ancestors and can only add, never remove.

| Type | Extends | Activation receipts | Closeout evidence |
|---|---|---|---|
| `task.code` | `TaskDoc` | `preflight` + `bundle` | `tests` + `commit` + `atom\|materialization` |
| `task.docs` | `TaskDoc` | `preflight` | `commit` + `document` |
| `task.debug` | `TaskDoc` | `preflight` + `reproduction` | `tests` + `commit` + `atom\|materialization` |
| `task.refactor` | `task.code` | `preflight` + `bundle` + `goldens` | `task.code` + `goldens` |
| `task.decision` | `TaskDoc` | `owner` | `commit` + `document` |
| `task.aggregate` | `TaskDoc` | none (its dependencies closed; `children` is not a field yet) | `commit` (no `children` clause until `TaskAggregateDoc` has a children field) |
| `task.external` | `TaskDoc` | `preflight` | `external` (URL) |

`atom|materialization` is one gate with two alternatives. `commit` means a commit reachable from `HEAD`. The closeout column is data, `deskops/data/rules/closeout-evidence.yaml` (task type -> kinds): `deskops closeout verify` reads it to choose the producers it runs and `deskops add task` reads it as the floor `--evidence` adds to; a desk subtype reads its nearest factory ancestor's entry. A desk adds its own subtypes in `desk/models/*.py`; `deskops desk update --apply` registers them and migrates legacy `task_type` strings (`code`/`implementation`/`test` → `task.code`; `docs`/`spec`/`design` → `task.docs`; `external` → `task.external`; empty → `task.code`).

#### Activation rules

The activation gate of a type is not Python: it is a `RuleDoc` (sldb GO06/GO08) the desk carries under `desk/lifecycle/rule-activation-<type>.md`, a managed seed of the deskops package (`deskops/data/rules/`, declared in `deskops/data/desk_declaration.yaml` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply`; a desk's copy that differs is rewritten and a second run changes nothing). Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-execution"` and has the subject `model <= <TypeDoc>`, so a desk subtype (`desk/models/*.py`) inherits it without code and a desk can add its own `RuleDoc` with a narrower subject to add a clause. A receipt counts when a `ReviewDoc` of that `kind` has the task as `subject`, `verdict: accepted` and `anchor_state: intact` (sldb pins `subject` with the task's contract hash when the receipt is saved and recomputes the state on every read: editing `goal`, `scope`, `files`, `validation`, `done_when`, `title` or `implementation_path` leaves it `changed`).

| Rule | Subject | Condition | Message |
|---|---|---|---|
| `rule-activation-task-code` | `model <= TaskCodeDoc` | `any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") and any(^subject: … kind = "bundle") and all(depends_on: status = "closed")` | Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-docs` | `model <= TaskDocsDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.docs se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-debug` | `model <= TaskDebugDoc` | `any(^subject: … kind = "preflight") and any(^subject: … kind = "reproduction") and all(depends_on: status = "closed")` | Una tarea task.debug se activa con recibos preflight y reproduction aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: … kind = "goldens")` (the `task.code` rule already applies to the family) | Una tarea task.refactor se activa, además de lo que pide task.code, con un recibo goldens aceptado e intacto. |
| `rule-activation-task-decision` | `model <= TaskDecisionDoc` | `any(^subject: … kind = "owner") and all(depends_on: status = "closed")` | Una tarea task.decision se activa con un recibo owner aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-aggregate` | `model <= TaskAggregateDoc` | `all(depends_on: status = "closed")` | Una tarea task.aggregate se activa con sus dependencias cerradas. |
| `rule-activation-task-external` | `model <= TaskExternalDoc` | `any(^subject: … kind = "preflight") and all(depends_on: status = "closed")` | Una tarea task.external se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |

`…` abbreviates `anchor_state = "intact" and verdict = "accepted" and`. A dependency that closed no longer exists as a task document, so `all(depends_on: …)` omits it. `deskops review` writes `preflight`, `bundle` and `node` receipts; `reproduction`, `goldens` and `owner` have no command yet.

`deskops advance` passes the task to sldb as the `document` of its `on_transition` rules: when an `error` finding holds the edge back, the message lists each finding (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: {...}) (witness: ...)`) instead of the edge's condition; a gate held back only by its own condition (`ritual-testing`, `ritual-closeout`) keeps the message `Gate <node> is not complete (...)`. `deskops show task` prints the same findings under each lifecycle gate (`blocked by:`; `findings` in `--format json`) and `deskops next` under `Blocked by:`. A blocked task is not a status: it stays `draft` at `ritual-execution` with the blocked edge visible in `show` and `next`.

#### Closeout rules

The closeout gate of a type is a `RuleDoc` too (CC33b): `desk/lifecycle/rule-closeout-<type>.md`, a managed seed of `deskops/data/rules/` declared and tracked like the activation rules. Every rule is `on_transition`, `severity: error`, applies `where current_node = "ritual-closeout"` (the source of `task_completes`, whose own condition is only `status = "ready_for_testing"`) and has the subject `model <= <TypeDoc>`. It asks, per kind of the table, for an evidence receipt `deskops closeout verify` writes (CC33a): `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")`, with `atom|materialization` as an `or` of the two.

| Rule | Subject | Clauses (receipts accepted and intact) |
|---|---|---|
| `rule-closeout-task-code` | `model <= TaskCodeDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-docs` | `model <= TaskDocsDoc` | `commit`, `document` |
| `rule-closeout-task-debug` | `model <= TaskDebugDoc` | `tests`, `commit`, `atom` or `materialization` |
| `rule-closeout-task-refactor` | `model <= TaskRefactorDoc` | `any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted")` (the receipt of `deskops review record --kind goldens`; the `task.code` rule already applies to the family) |
| `rule-closeout-task-decision` | `model <= TaskDecisionDoc` | `commit`, `document` |
| `rule-closeout-task-aggregate` | `model <= TaskAggregateDoc` | `commit` |
| `rule-closeout-task-external` | `model <= TaskExternalDoc` | `external` |

The closing order is fixed: `deskops closeout verify` runs the producers and writes the receipts (`accepted` or `rejected`); `deskops closeout commit` writes none and evaluates the rule on the task read at `ritual-closeout`. When an error finding holds it back the commit is not made and the output lists each finding (`- error: [rules/rule-closeout-<type>] ...`) and says to run `deskops closeout verify --task <id>`; editing a contract field after verify leaves the receipts `changed`, so the rule blocks again until verify writes new ones. `deskops show task` and `deskops next` show the same findings on the `task_completes` gate. The board view runs verify read-only.

When the atom|materialization gate passes without a linking document (a desk without local atoms, coverage only by a routed follow-up, or a skill guard test), verify writes an accepted `atom` receipt whose `value` is `exempt: <why the gate passed>`, so the rule needs no special case. `--evidence` (the task's `closeout_evidence`) only adds kinds (DA5): an added kind is verified and gets its receipt, and when it fails verify reports it as the alert `added_closeout_evidence_not_verified` without blocking; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`.

Two rules over the task's own fields are `on_write` alerts, `subject: model <= TaskDoc`: `rule-closeout-alert-implicit-code` (`has(task_type) or nonempty(closeout_evidence)`: a task that predates types is gated as code) and `rule-closeout-alert-pill-graduation` (`not nonempty(pills) or any(references: model <= AtomDoc)`: a task that binds pills references the atom they graduate to). The other field checks stay in verify because the rule language has no quantifier over the elements of a list value: the closeout evidence vocabulary (`deskops add task --evidence` refuses an unknown kind), `python_changes_without_declared_tests` and the http(s) shape of an `external` reference.

### Task lifecycle graph

A task moves through the desk's lifecycle graph, which lives in the desk's sldb store: every state is a tracked ritual (`RitualDoc:ritual-execution`, `ritual-testing`, `ritual-closeout`) and every transition is a `RelationDoc` under `desk/lifecycle/`, typed by a `RelationTypeDoc` named by the verb (`task_activates`, `task_hands_to_closeout`, `task_completes`). Each `RelationDoc` declares the whole transition: its `condition` (an sldb `--where` predicate over the task, such as `nonempty(validation)`) and its effects in `attributes`, following sldb's transition convention (GO09): `sets` names the task fields the transition writes (`status: active`, `ready_for_testing`, `closed`) and `terminal: true` marks the transition that closes the task (`task_completes`).

`deskops advance task` asks sldb which edges leaving the task's current node hold (`sldb.api.edges_holding`, with the task as `document` so its activation rule runs), takes that edge, applies its effects with `sldb.api.apply_effects` (validated against the task type's model), sets `current_node: complete` when the edge is terminal and appends the relation type to the task's `history`. One edge leaves each ritual, so nothing depends on the order sldb returns edges in. A blocked task stays where it is with the gate named. The terminal transition is never persisted by `advance`: the only closing entry point is `deskops closeout commit`. `deskops next` reads only the states of `deskops/spec/workflows/task_lifecycle.yaml` (ritual, next actions, `advance_when`); `deskops next --diagram` draws the desk's graph.

The six lifecycle documents and the seven activation rules are managed seeds of the deskops package (`deskops/data/desk_declaration.yaml`, templates in `deskops/data/lifecycle/` and `deskops/data/rules/`). `deskops init` and `deskops desk update --apply` write them, track them (with the three lifecycle rituals by their ids) and rewrite a desk's copy that differs from the package's: `desk update` lists it under `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote <path>`, and a second run changes nothing. Every other scaffold only creates what is missing. Changing a transition's effect means changing the `RelationDoc` through sldb; no YAML of deskops has to change, and the next `desk update --apply` restores the package's version.

#### Lifecycle consistency (CC37)

A task's `status`, `current_node`, `history` and `task_type` are checked together by a validator of the `TaskDoc` model (`deskops/models/task_lifecycle.py`). sldb applies it on every write: `deskops` itself, `sldb fields update`, `sldb docs update`, `sldb serve` `/save` and transactions. So a write that leaves a task inconsistent is refused with the validator's message, whatever path it takes. A task is consistent in one of these states:

- **Entry:** `current_node` is the entry node, `history` is empty and `status` is `draft`.
- **After transitions:** the last `history` item is the transition that leads to `current_node`, and `status` is what that transition `sets` (`active`, then `ready_for_testing`). The table comes from the package's `RelationDoc`s, not from the desk's store.
- **Closed by closeout:** `superseded` after `superseded`, `resolved` after `resolved-by`, and `closed` after `task_completes`. `closed` is never persisted by `advance`; `closeout commit` removes the task.
- **Outside the lifecycle**, with no `current_node` and empty history: `draft`, a drawer task's `deferred`, and the pre-lifecycle statuses that `closeout retire` removes (`resolved`, `closed`, `done`, `complete`).

`task_type` matches the document's model: each typed model accepts only its own type, and the generic `TaskDoc` accepts an empty or unregistered type. `deskops desk update --apply` does not write an inconsistent task. It reports the task with the reason sldb gives. Only `deskops advance` and `deskops closeout` change a task's lifecycle fields; `deskops edit task` refuses them (GC06).

### Phases

Tasks form an execution dependency graph.

A **phase** is one horizontal dependency layer in that graph:

- task prerequisites are already satisfied
- tasks are ready at the same time
- planned operational changes do not overlap
- tasks may run in parallel when the environment supports it

A phase has execution meaning, not business meaning. It is the workflow unit above individual tasks and below the whole board.

### Boards

The board is the routing surface for active work.

- It names the active tasks.
- It routes board-wide pills and rituals.
- Its current ready dependency layer is the current phase.

---

## Cheap Context Review and Fresh Subagents

Before promoting or executing a draft, plan, package or leaf, run the [context-review ritual](../desk/rituals/context-review.md). It tests the quality of the written question with a cheap reviewer: faithful reformulation, explicit ambiguities and a detailed dry-run of proposed readings, changes, validation and dependencies. The reviewer names intended commands without executing them or editing sources.

Supply the exact versioned brief and only necessary explicit references. Use a new ephemeral process for every attempt, without chat history, earlier reviews, oral fixes, persistent memory, automatic context/skills or tools. Record the chosen cheap provider/model/profile and reason; an expert cannot rescue a failed cheap comprehension gate. The ritual specifies the verified Pi isolation profile and per-node evidence layout.

The coordinator compares understanding with intent, corrects the written brief and recursively decomposes large nodes into children and explicit edges. Review root, packages, every leaf and dependency interfaces before selecting ready leaves. A root-only review does not cover descendants. Unresolved ambiguity blocks execution. Changed input or a changed dependency contract invalidates affected reviews; retries use a new process. Technical transport/quota failures are recorded separately from ambiguity.

Before Executor dispatch, preserve two distinct cheap roles: TaskDoc-only preflight (also saved in `runs/subagents/<run-dir>/preflight.md`) and cold-bundle coverage. The explicit execution bundle contains task, board-routed instructions/rituals, bound pills, linked atoms/files and validation targets. Neither review executes implementation. Expert council review, Executor work, independent Tester validation and human product approval remain separate gates; a word such as APTO or structural PASS grants none of them.

Evidence lives at `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`: exact input bytes/hash, model/profile/selection, command/isolation, reformulation/ambiguities/dry-run, coordinator comparison and required edits. These are process records, not runtime enforcement or a new lifecycle state. Each active task then executes in its own fresh context, and an independent Tester validates implementation. The coordinator integrates outputs and enforces task/phase closeout. Do not carry unrelated tasks through one long-lived context.

---

## Pill Lifecycle

Pills are temporary execution aids, but they are not task-specific instances. Correction: pills are not 1:1 with tasks.

```text
Draft or refresh reusable pills -> bind pills to tasks opportunistically -> execute tasks ->
close tasks -> reconcile pills at phase closeout ->
keep / delete / merge / graduate to atoms -> prepare next phase pills
```

At phase closeout, classify touched pills explicitly:

- **still active** - keep for the next phase
- **stale** - delete or retire
- **redundant** - merge or remove duplicates
- **durable** - promote the stabilized residue into atoms first
- **materialization-worthy** - land resulting changes in code, specs, or docs as needed

Do not let durable knowledge remain pill-only once it stabilizes. Do not create a new pill just because a new task exists; create or update a pill only when there is a reusable atomic truth worth rebinding.

---

## Ritual Stack

### 1. Phase Ritual

Before starting a ready dependency layer:

```text
0. REVIEW   -> Review root/packages/leaves and edges cheaply; correct briefs and decompose.
1. IDENTIFY -> Select reviewed ready non-overlapping leaves.
2. BUNDLE   -> Confirm each task has its fresh context bundle.
3. EXECUTE  -> Run the execution ritual per task.
4. CLOSE    -> Require each task to close with its declared evidence and a task commit.
5. VALIDATE -> Run phase-level integration or end-to-end checks.
6. REGRESS  -> Fix interaction regressions.
7. RECONCILE-> Audit pills; delete, merge, or graduate them.
8. SURFACE  -> Capture newly discovered tasks and next-phase pills.
9. COMMIT   -> Make the phase-closing commit.
```

### 2. Task Execution Ritual

For each task in the phase:

```text
1. INIT   -> Confirm task scope, files, pills, validation, and declared closeout evidence.
2. REVIEW -> Accept cheap TaskDoc-only preflight, then separate cheap cold-bundle coverage.
3. BIND   -> Bind every relevant pill.
4. IMPLEMENT -> Make only task-scoped changes.
5. HANDOFF   -> Open an explicit testing handoff.
```

### 3. Task Testing Ritual

```text
1. CHECK  -> Confirm the intended contract and pill guardrails.
2. UPDATE -> Fix stale tests or add missing ones.
3. RUN    -> Execute the smallest relevant scope first.
4. EXPAND -> Run broader checks when shared behavior changed.
5. HANDOFF-> Open an explicit closeout handoff.
```

### 4. Task Closeout Ritual

```text
1. VERIFY -> Run `deskops closeout verify`: it checks the type's evidence (declared X;
             found Y) and writes the evidence receipts the closeout rule reads.
2. CLEAN  -> Remove stale task-local context when appropriate.
3. DELETE -> Remove the resolved task from active routing.
4. COMMIT -> Close with `deskops closeout commit`: it evaluates the type's closeout rule
             on those receipts and writes none; `closeout supersede` when the
             subject no longer exists, `closeout retire` for a pre-lifecycle resolution.
5. WAIT   -> If this was the last task in the phase, do not start the next phase until phase closeout passes.
```

---

## Commit Rules

### Task commit

Every closed task gets its own atomic commit, made by `deskops closeout commit`, `closeout supersede`, or `closeout retire`. The evidence it must show is its type's (plus any kind `--evidence` added at creation), as receipts `deskops closeout verify` wrote and the type's closeout rule accepts.

### Phase commit

When all tasks in a phase are closed, make one separate descriptive phase commit for:

- integration fixes
- pill reconciliation
- captured next work
- board/phase bookkeeping

Do not hide unfinished task work inside a phase commit.

---

## Anti-Patterns

- Starting implementation before identifying the ready phase.
- Treating semantic milestones as phases when tasks still depend on each other.
- Running multiple unrelated tasks through one stale context.
- Closing tasks without the evidence they declared or without a dedicated task commit.
- Starting the next phase after isolated green task tests without integration validation.
- Carrying stale or overlapping pills forward because each task passed independently.
- Leaving durable rules only in pills instead of promoting them into atoms.
- Skipping newly discovered task capture at phase closeout.
