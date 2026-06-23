---
id: feature-workflow-execution-engine
status: draft
created: 2026-06-22
tags:
- topic:workflow-engine
- topic:automation
- topic:hooks
- topic:state-machine
- topic:proposal
- topic:decision-boundary
---

# Machine-Executable Workflow Engine

> **Boundary contract.** Throughout this document, every operation is tagged with one of:
>
> | Tag | Meaning |
> |---|---|
> | `[E]` | **Engine** — deterministic, no LLM. Pure Python, git/file/test commands, predicate evaluation, state-machine traversal, document read/write, hook target execution. |
> | `[A]` | **Agent** — semantic, LLM-driven. Code authoring, judgment, triage, interpretation, narrative writing. |
> | `[E→A]` | **Dispatch** — engine produces a typed report and hands it to an agent. The engine never decides; the agent does. |
> | `[A→E]` | **Trigger** — agent invokes an engine command. The agent decides; the engine executes. |
> | `[E|E]` | **Engine-internal** — sub-step of a single engine operation, not a boundary crossing. |
> | `[H]` | **Human operator** — explicit intervention. Only via `deskops` override commands or `attention/` review. |
>
> **Default rule:** if an operation could be done deterministically, it MUST be `[E]`. Agents are reserved for work that genuinely requires semantic judgment. The boundary is enforced by the fact that engine code cannot import LLM clients, and agent prompts cannot mutate state directly (only via `deskops` commands or hook events).

## Decision Boundary — Operation Index

| # | Operation | Tag | Where it lives | Failure mode |
|---|---|---|---|---|
| 1 | Read SLDB document | `[E]` | `deskops/storage/sldb.py` | IO error → halt |
| 2 | Resolve atom/pill references | `[E]` | `deskops/engine/context.py` | Missing ref → build fails |
| 3 | Check file existence on disk | `[E]` | `deskops/engine/predicates/file.py` | Missing → predicate fail |
| 4 | Check git working tree state | `[E]` | `deskops/engine/predicates/git.py` | Dirty → predicate fail |
| 5 | Run `pytest` on a bounded path | `[E]` | `deskops/engine/predicates/test.py` | Non-zero exit → predicate fail |
| 6 | Evaluate a registered predicate | `[E]` | `deskops/engine/condition.py` | Unregistered → fail-safe false |
| 7 | Traverse routine graph (`next`, `can_advance`, `state`) | `[E]` | `deskops/engine/routine.py` | No valid edge → returns None |
| 8 | Dispatch a hook event | `[E]` | `deskops/engine/hook.py` | Target crash → diagnostic |
| 9 | Execute a hook target (git commit, retire, run tests) | `[E]` | `deskops/engine/hook.py` + `predicates/` | Crash → halt sequence, write `attention/` |
| 10 | Build EvalContext / ContextBundle | `[E]` | `deskops/engine/context.py` | Build fail → write `attention/` |
| 11 | Validate execution gates (atomization, pill coverage, staleness) | `[E]` | `deskops/engine/executor.py` | Gate fail → block + `attention/` |
| 12 | Auto-closeout pipeline (test → commit → retire) | `[E]` | `deskops/engine/closeout.py` | Step fail → halt, resume later |
| 13 | Render a checklist verdict | `[E]` | `deskops/engine/condition.py` | Unknown → `verdict=unknown`, not block |
| 14 | Write a Markdown document (task, pill, atom, primitive) | `[E]` | `deskops/storage/sldb.py` | IO error → halt |
| 15 | Apply an operator (set field, append, delete doc) | `[E]` | `deskops/engine/operators.py` | Validation fail → reject |
| 16 | Run `deskops <command>` | `[E]` | `deskops/cli/*` | Non-zero exit → propagate |
| 17 | Triage ambiguous inbox/drawer items | `[A]` | `SupervisorAgent` (semantic) | No triage → item stays in `attention/` |
| 18 | Choose which ready task to activate | `[A]` | `SupervisorAgent` (semantic) | No choice → supervisor stalls |
| 19 | Reconcile pills against a diff (which pills apply?) | `[A]` | `ExecutorAgent` (semantic) | No reconcile → closeout halts |
| 20 | Author implementation code | `[A]` | `ExecutorAgent` (semantic) | LLM error → task returns to active |
| 21 | Write evidence narratives | `[A]` | `ExecutorAgent` (semantic) | Missing → `checklist-item.reason` stays empty |
| 22 | Decide drawer → active promotion | `[A]` | `SupervisorAgent` (semantic) | No decision → drawer task stays parked |
| 23 | Interpret soft signals (warnings, not blockers) | `[A]` | `SupervisorAgent` (semantic) | No interpretation → warning stays in `attention/` |
| 24 | Read supervisor startup report and decide action | `[E→A]` | `SupervisorAgent` consumes `[E]` report | No consumer → report archived in `attention/` |
| 25 | Receive a sealed ContextBundle and execute the task | `[A→E]` | `ExecutorAgent` calls `deskops` commands | Agent attempts direct file write → blocked by convention |
| 26 | Receive a gate-failure report and decide resolution | `[E→A]` | `SupervisorAgent` consumes `[E]` report | No consumer → task remains blocked |
| 27 | Receive a closeout-failure report and decide recovery | `[E→A]` | `SupervisorAgent` or `[H]` | No consumer → task stuck in "completing" state |
| 28 | Manual override (`deskops closeout run`, `deskops hook fire`) | `[H]` → `[E]` | Operator invokes CLI | Override is logged but not blocked |
| 29 | Review `attention/` items and resolve | `[H]` | Operator reads + acts | Item stays open |
| 30 | Register a new predicate at import time | `[A]` (or `[H]` for one-off) | Project code, not deskops core | Unregistered predicate → fail-safe false |

**Key invariant:** rows 1–16 never call an LLM. Rows 17–23 never mutate state without going through rows 1–16. The only ways state changes are (a) an `[E]` operation, (b) an `[A]` operation that goes through rows 1–16, or (c) an `[H]` operation through an explicit `deskops` command.

---

## Why — Problem & Motivation

### Problem 1: Rituals are advisory, not enforceable

The current execution/testing/closeout rituals are human-readable Markdown documents at `desk/rituals/*.md`. An agent must:
1. Choose to read them
2. Interpret the steps correctly
3. Voluntarily follow them
4. Not skip steps

In practice, agents routinely skip cold-review gates, skip pill-binding sweeps, and jump from implementation straight to retirement without testing or committing. AGENTS.md and rituals are treated as suggestions, not gates.

### Problem 2: Checklists have no checkbox state

Checklist items are plain `- ` bullets in Markdown. There is no `checked: bool` field. The system cannot programmatically verify whether a checklist item is done. The `condition_refs` field links to ConditionDoc instances, but nothing evaluates them at runtime. A checklist cannot produce a machine-auditable pass/fail verdict.

### Problem 3: Conditions exist as data, not as evaluators

`ConditionDoc` has structured fields (`subject`, `predicate`, `expected`) but no evaluation logic. The condition "task.implementation_path is not empty" is stored as strings but never actually checked by code. Conditions are documentation about intended validation, not validation itself.

### Problem 4: Hooks have no runtime

`HookDoc` has `event`, `target`, and `condition_ref` fields, but there is no event system, no dispatcher, no subscriber registry. Hooks describe what *could* happen but never actually fire.

### Problem 5: Routines are static graphs, not state machines

A `RoutineDoc` defines an `entrypoint`, edge topology, and terminal nodes. But nothing advances the state machine. The task's `current_node` must be manually written into the history field. There is no `routine.next()` or `routine.advance()` — the agent must manually determine what step comes next.

### Problem 6: Closeout depends on agent will

The closeout ritual requires testing, evidence writing, board cleanup, and a commit boundary. But the agent chooses whether to perform each step. The paper_IEEE exercise showed that commit-boundary enforcement, test execution, and task retirement were routinely skipped until the closeout step was formalized — and even then, only when the supervisor explicitly checked.

### Problem 7: No context-bundle construction

Subagents receive a free-form prompt with whatever context the supervisor decides to include. There is no typed, machine-constructed ContextBundle that guarantees the subagent receives: the exact task, resolved atoms, bound pills, allowed file paths, expected test commands, and pre-verified gate state.

---

## What — Concrete Changes

### 1. Model Enrichment

#### ChecklistDoc — structured items with checkbox state

```python
# deskops/models/checklist.py

class ChecklistItem(BaseModel):
    text: str
    checked: bool = False
    required: bool = True
    evaluator: str | None = None  # optional condition_ref to auto-evaluate
    reason: str = ""  # why it passed or failed (populated by evaluator)

class ChecklistDoc(PrimitiveDoc):
    items: list[ChecklistItem]
    condition_refs: list[str]
    mode: str = "all"  # "all" | "any"
    # NEW:
    verdict: str = "unknown"  # "pass" | "fail" | "unknown"
    evaluated_at: str = ""
```

Template items render as:
```markdown
## Items

- [x] The task has an implementation path.  (condition: condition-task-xxx-has-implementation-path → pass)
- [ ] Validation targets are explicit.  (condition: condition-task-xxx-has-validation → fail)
```

Checkboxes reflect real boolean state in the document. Conditions can auto-evaluate them.

#### ConditionDoc — runtime evaluator

```python
# deskops/models/condition.py

class ConditionDoc(PrimitiveDoc):
    subject: str         # e.g. "task.implementation_path"
    predicate: str       # e.g. "not_empty" | "eq" | "contains" | "file_exists" | "git_clean" | "test_passes"
    expected: str        # expected value
    # NEW:
    evaluate: callable   # registered function that reads subject, applies predicate against expected
    # The evaluate function signature:
    # evaluate(context: EvalContext) -> EvalResult
```

Built-in predicates:
- `not_empty` — field is non-null and non-empty
- `eq` — field equals expected value
- `file_exists` — path exists on disk
- `git_clean` — working tree has no unstaged changes
- `test_passes` — running `pytest <path>` exits 0
- `dep_met` — all tasks in depends_on have status=closed

Each predicate maps to a registered Python function in the engine. New predicates can be registered by adding functions to the predicate registry.

#### EvalContext — what the evaluator can read

```python
@dataclass
class EvalContext:
    task: TaskDoc | None
    board: dict  # all task statuses
    desk_state: dict  # inbox, drawer, ritual status
    git_state: dict  # branch, clean/dirty, ahead/behind
    file_state: dict  # file existence, content hashes
    test_results: dict  # cached test results
```

The evaluator is never open-ended. Every predicate operates on a bounded, typed context. No LLM calls during condition evaluation.

#### RoutineDoc — state machine with next/advance

```python
# deskops/engine/routine.py  (not a doc — the engine)

class RoutineEngine:
    def __init__(self, routine: RoutineDoc, edges: list[EdgeDoc],
                 conditions: dict[str, ConditionDoc], context: EvalContext)

    def next(self) -> str | None:
        """Return the next valid node id, or None if at terminal."""
        # 1. Read current_node from the bound task (passed via context)
        # 2. Find all edges where source == current_node
        # 3. For each edge, evaluate condition_ref if present
        # 4. Return the target of the first edge whose condition passes
        # 5. If no edge condition passes, return None

    def advance(self) -> str | None:
        """Move to next node, update task.current_node, return new node id."""
        n = self.next()
        if n is None:
            return None
        # Update task.current_node = n
        # Append to task.history
        # Fire hook: event = f"routine.{routine.id}.enter.{n}"
        return n

    def can_advance(self) -> bool:
        """Check if the current node's outgoing edge condition is satisfied."""
        return self.next() is not None

    def state(self) -> dict:
        """Return full state machine snapshot: current node, possible transitions, conditions."""
```

The routine engine is a pure Python state machine. It does not need SLDB or disk I/O. It reads pre-loaded docs and returns transitions deterministically.

#### HookDoc — event system runtime

```python
# deskops/engine/hook.py

class HookEngine:
    def __init__(self, hooks: list[HookDoc], conditions: dict[str, ConditionDoc])

    def fire(self, event: str, context: EvalContext) -> list[HookResult]:
        """Fire all hooks matching event whose condition passes."""
        # 1. Find all hooks where hook.event == event
        # 2. For each, evaluate condition_ref if present
        # 3. Execute hook.target (could be operator, routine, or CLI command)
        # 4. Return list of HookResult(status, hook_id, output)

    def on(self, event: str) -> list[HookDoc]:
        """Return all registered hooks for an event (inspection only)."""
```

Event namespace convention: `source.scope.action`
- `task.active.enter` — task enters active status
- `task.execution.gate` — execution gate check requested
- `task.complete.trigger` — task signals completion
- `routine.advance.pre` — before routine advances
- `routine.advance.post` — after routine advances
- `supervisor.start` — supervisor session start
- `board.phase.ready` — phase dependencies satisfied

#### Target execution (hook actions)

The `hook.target` field references one of:
- An `OperatorDoc` — atomic state mutation (set field, append to list, delete doc)
- A routine id — start/advance a routine
- A CLI command string — shell out to a bounded command
- A Python callable path — `deskops.engine.hooks.supervisor_startup`

Built-in hook targets (pre-registered):
- `check.git_state` — verify working tree cleanliness
- `check.board_consistency` — verify no orphan tasks, no stale references
- `check.dependency_satisfaction` — verify depends_on tasks are closed
- `validate.atomization` — verify task scope produces one coherent commit
- `validate.pill_coverage` — verify pills cover all touched surfaces
- `run.tests_bounded` — run only tests listed in task.files
- `run.tests_full` — run full test suite
- `git.commit_atomic` — create commit with task id in message
- `task.retire` — delete task file, remove from board, untrack from store

#### TaskDoc — lifecycle events

```python
# deskops/models/task.py

class TaskDoc(OperationalArtifactDoc):
    # Existing fields...
    event_hooks: dict[str, list[str]] = {}
    # Maps event name → list of hook ids to fire
    # Example:
    #   "on_enter_active": ["hook-check-git", "hook-validate-board"]
    #   "on_complete": ["hook-test-and-commit"]
```

This allows tasks to bind their own hooks without modifying global hook definitions. If `event_hooks` is empty, the global hook definitions for that event apply.

### 2. New Engine Layer

Directory structure:

```
deskops/
├── engine/
│   ├── __init__.py
│   ├── routine.py        # RoutineEngine — state machine
│   ├── hook.py           # HookEngine — event system
│   ├── condition.py      # ConditionEvaluator — predicate registry
│   ├── context.py        # EvalContext builder
│   ├── supervisor.py     # Supervisor startup sequence
│   ├── executor.py       # Execution gate validators
│   ├── closeout.py       # Auto-closeout pipeline
│   └── predicates/       # Built-in predicate implementations
│       ├── git.py
│       ├── file.py
│       ├── test.py
│       └── doc.py
├── cli/
│   ├── ...
│   └── engine_commands.py  # New CLI commands
```

#### Supervisor startup sequence (supervisor.py)

```
flowchart LR
    A["[A→E] CLI invocation: deskops supervisor start"] --> B["[E|E] Hook: supervisor.start fires"]
    B --> C["[E] Check git state (row 4)"]
    B --> D["[E] Load board (row 1)"]
    B --> E["[E] Scan inbox (row 1)"]
    B --> F["[E] Scan drawers (row 1)"]
    B --> G["[E] Check ritual consistency (row 11)"]
    B --> H["[E] Check active task routine state (row 7)"]
    C --> I["[E] Aggregate into EvalContext + report"]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I
    I --> J{"[E] All preconditions met?"}
    J -->|Yes| K["[E→A] Return green startup report"]
    J -->|No| L["[E] Halt + write failure report"]
    L --> M["[E] Write diagnostic to desk/drawer/attention/"]
    K --> N["[A] SupervisorAgent reads report, decides next action (row 17, 18)"]
```

Every node in this diagram is `[E]` or `[E|E]` (engine-internal). The agent appears **only** at the very end, consuming the report. The supervisor engine never starts without running these checks. The startup hook is automatic — it triggers on session init, before any agent prompt is constructed, with no `[A]` involvement.

#### Execution gate (executor.py)

```
flowchart LR
    A["[A→E] Supervisor invokes deskops routine advance"] --> B["[E|E] Hook: task.execution.gate fires"]
    B --> C["[E] Validate atomization (row 11)"]
    B --> D["[E] Validate pill coverage (row 11)"]
    B --> E["[E] Check staleness vs depends_on (row 11)"]
    C --> F{"[E] All gates pass?"}
    D --> F
    E --> F
    F -->|Yes| G["[E] Build ContextBundle (row 10)"]
    F -->|No| H["[E] Write gate failure report"]
    H --> I["[E→A] Route to attention/ for supervisor (row 26)"]
    G --> J["[E→A] Return bundle to supervisor"]
    J --> K["[A] Supervisor hands bundle to executor (row 25)"]
```

The executor subagent receives a ContextBundle with gates pre-verified. It cannot start without passing the gates. If gates fail, the task goes back to the drawer/attention for human resolution. The agent does not appear until step K, and its input is the pre-built bundle.

#### Auto-closeout pipeline (closeout.py)

```
flowchart LR
    A["[A→E] Agent invokes deskops routine advance (completion)"] --> B["[E|E] Hook: task.complete.trigger fires"]
    B --> C["[E] Hook: run.tests_bounded (rows 5, 9)"]
    C --> D{"[E] Tests pass?"}
    D -->|Yes| E["[E] Hook: git.commit_atomic (row 9)"]
    D -->|No| F["[E] Write test failure report"]
    F --> G["[E→A] Block retirement, route to attention (row 27)"]
    E --> H["[E] Hook: task.retire (row 9)"]
    H --> I["[E] Hook: board.phase.ready check (row 11)"]
    I --> J{"[E] Dependencies met?"}
    J -->|Yes| K["[E] Fire phase.ready"]
    J -->|No| L["[E] Wait for remaining tasks"]
```

The subagent's only `[A]` action is step A — reporting completion. Everything after that is `[E]`. The subagent never decides whether to test, commit, or retire. The hooks fire automatically on task.complete. The system handles verification, commit, and retirement.

### 3. ContextBundle — Typed Subagent Payload

```python
@dataclass
class ContextBundle:
    role: str                        # "supervisor" | "executor"
    task: TaskDoc                    # the active task document
    routine: RoutineEngine           # pre-loaded state machine
    atoms: list[AtomDoc]             # resolved atom documents
    pills: list[PillDoc]             # resolved pill documents
    files: list[str]                 # explicit paths to read/modify
    tests: list[str]                 # explicit test paths
    gate_state: dict[str, str]       # {gate_name: "pass" | "fail" | "skipped"}
    hook_plan: list[HookDoc]         # hooks that will fire during this execution
    eval_context: EvalContext        # snapshot of current state
```

The ContextBundle replaces the free-form "here is your task, do the thing" prompt. It is a typed data structure that the executor receives as fact. Every field is machine-populated.

### 4. CLI Changes

| Command | Action |
|---|---|
| `deskops supervisor start` | Run supervisor startup sequence, return board summary |
| `deskops supervisor status` | Show current supervisor state (gates, active task, hook plan) |
| `deskops routine next <task-id>` | Show next valid node for the task's routine |
| `deskops routine advance <task-id>` | Evaluate edge conditions and advance to next node |
| `deskops hook fire <event> [--task <id>]` | Manually fire a hook event (for testing) |
| `deskops hook list [--event <name>]` | List registered hooks, optionally filtered by event |
| `deskops checklist verify <checklist-id>` | Evaluate all conditions, produce verdict |
| `deskops context bundle <task-id> [--role executor]` | Build and print a ContextBundle for a task |
| `deskops closeout run <task-id>` | Execute the closeout pipeline (test → commit → retire) |

No new state is introduced. Commands read and write the same SLDB-backed documents. The engine layer is a thin runtime over existing data.

### 5. What Happens to Rituals

The ritual documents at `desk/rituals/*.md` shift purpose:

**Before:** Step-by-step instructions an agent must read.
**After:** Reference documentation for the hook system. Each ritual maps to a set of hook definitions:

```
desk/rituals/execution.md  →  defines which hooks fire for execution gates
                              (validate_atomization, check_pill_coverage, check_staleness)
                              → stored as HookDoc instances in desk/primitives/hooks/

desk/rituals/testing.md   →  defines which hooks fire for verification
                              (run_bounded_tests, check_coverage)
                              → stored as HookDoc instances

desk/rituals/closeout.md  →  defines which hooks fire for retirement
                              (run_tests, commit, retire)
                              → stored as HookDoc instances
```

The Markdown documents remain as human-readable explanations. The machine-readable behavior lives in HookDoc instances that the engine loads.

---

## Who — Actors and Their Interaction

The system has four actors with **explicit boundary crossings**. Each crossing is mediated by a typed artifact (a CLI command, a report, or a ContextBundle) so neither side can silently do the other's job.

### Engine (System) — `[E]`
- **Runs** as a stateless library; the CLI is its only public surface.
- **Validates** every gate before allowing state transitions (rows 7, 11).
- **Logs** every hook fire, every condition evaluation, every gate verdict (row 9).
- **Writes** documents only via the SLDB store (rows 1, 14, 15).
- **Never** calls an LLM, never interprets natural language, never makes a judgment call outside the registered predicate set.
- **Boundary surface:** `deskops` CLI commands; emitted events; reports written to `attention/`.

### Supervisor Agent — `[A]` (with `[E→A]` consumption)
- **Triggers `[A→E]`**: `deskops supervisor start` at session beginning (row 16).
- **Receives `[E→A]`**: the startup report (rows 2, 3, 4, 24) — git state, board state, inbox/drawer scan results, ritual consistency, active-task routine state. This is a typed payload, not free-form prose.
- **Decides `[A]`**: which ready task to activate, how to triage ambiguous items, whether to promote drawer work, how to interpret soft warnings (rows 17, 18, 22, 23).
- **Triggers `[A→E]`**: `deskops context bundle <task-id> --role executor` to produce a sealed bundle (row 10).
- **Launches `[A]`**: an executor subagent and hands it the bundle.
- **Monitors `[A→E]`**: invokes `deskops routine state <task-id>` to read state-machine progress (row 7).
- **Intervenes `[A→E]`**: when gate failures route to `attention/`, the supervisor consumes the failure report and decides the resolution path (row 26).

### Executor Agent — `[A]` (with `[A→E]` writes)
- **Receives `[E→A]`**: a sealed `ContextBundle` from the supervisor (row 25). The bundle's `gate_state` is pre-verified; the executor cannot re-open a failed gate.
- **Reads `[E→E]`**: uses `deskops` read commands (rows 1, 2) to load referenced atoms/pills.
- **Writes `[A→E]`**: all file modifications and document updates go through `deskops` commands, never direct IO (rows 14, 15, 16). This is what makes the executor's actions auditable.
- **Can**: read task + atoms + pills, modify files in scope, write evidence, report completion (row 20, 21).
- **Cannot**: skip gates (row 11), skip tests (row 5), skip commit (row 9), skip retire (row 12). Those are hook-driven, not agent-driven.
- **Does not decide**: when to stop, when to commit, when to retire (row 12 handles all of these).

### Human Operator — `[H]`
- **Reviews `[H]`**: `attention/` items when gates fail or soft signals accumulate.
- **Overrides `[H]` → `[E]`**: explicitly invokes `deskops closeout run`, `deskops hook fire`, or `deskops migrate` to force progression (row 28). Every override is logged.
- **Audits `[H]`**: checklist verdicts, hook logs, commit history (read-only via `deskops`).
- **Configures `[H]`**: registers new predicates, hooks, and event mappings in the project codebase, not in deskops core (row 30).
- **Resolves `[H]`**: items that `SupervisorAgent` or `ExecutorAgent` could not close on their own (row 29).

### Boundary discipline

The agents and the engine are kept apart by **physical means**, not just convention:

- `deskops/engine/` does not import any LLM client. The package's import-time dependency graph is verified by a test (`tests/test_engine_no_llm_imports.py`).
- Agent prompts are not given shell access. They are given `deskops` CLI invocations and a ContextBundle. The supervisor is the only role that may decide *which* commands to invoke; the executor never invents new commands outside the bundle's `hook_plan`.
- A failed gate cannot be bypassed by an agent. The only override is `[H]` via a logged `deskops` command.

---

## When — Lifecycle Phases Where Automation Activates

Every row below is tagged. The two rightmost columns together tell you *which actor* runs *what* at each lifecycle point.

| Phase | Boundary | Trigger | What runs | Outcome |
|---|---|---|---|---|
| Session start | `[A→E]` | Operator / supervisor agent invokes CLI | `deskops supervisor start` (row 16) → git check, board scan, inbox scan, drawer scan (rows 3, 4, 1) | Startup report (row 24) |
| Startup triage | `[E→A]` | Engine writes report to stdout + `attention/` | `SupervisorAgent` reads report, decides: continue, recover, or escalate (rows 17, 18) | Triage decision |
| Task activation | `[E]` | Supervisor invokes `deskops routine advance` (row 7) | `task.active.enter` event → execution gates fire (row 11) | `gate_state` populated |
| Gate failure | `[E→A]` | Gate predicate returns false | Diagnostic written to `attention/` (row 11) → `SupervisorAgent` consumes (row 26) | Task blocked, resolution path proposed |
| Gate pass | `[E]` | All gates pass | `ContextBundle` constructed (row 10) | Sealed bundle ready |
| Execution handoff | `[E→A]` | Supervisor hands bundle to executor | `ExecutorAgent` receives sealed bundle (row 25) | Agent has typed payload |
| Implementation | `[A]` | Agent writes code | Direct file IO via `deskops` write commands (rows 14, 16) | Modified files, evidence drafts |
| Completion signal | `[A→E]` | Agent invokes `deskops routine advance` to mark done | `task.complete.trigger` event fires (row 8) | Event reaches closeout pipeline |
| Closeout pipeline | `[E]` | Hook engine processes `task.complete.trigger` | test → commit → retire (rows 5, 9, 12) | Atomic closeout or halt |
| Closeout failure | `[E→A]` | Any step in the pipeline fails | Diagnostic written (row 12) → `SupervisorAgent` or `[H]` decides (row 27) | Recovery command issued |
| Phase transition | `[E]` | All tasks in phase reach `closed` | `board.phase.ready` hook fires; integration validation runs (row 11) | Next phase unlocked |
| Manual override | `[H]` → `[E]` | Operator runs `deskops closeout run` or `deskops hook fire` | Engine executes, logs override (row 28) | Forced transition with audit trail |
| Attention resolution | `[H]` | Operator reads `attention/` items | Operator invokes `deskops` commands to resolve (row 29) | Item closed, audit logged |

**Key observation:** the column pattern alternates `[E]` and `[A]` in pairs. Engine runs deterministic work, dispatches to agent for semantic work, engine runs deterministic work again. The agent is **never** the only thing that can advance state — every state change is engine-mediated, with the agent providing the input that drives the engine.

---

## Where — Files and Layers Affected

| Layer | Path | Change |
|---|---|---|
| Models | `deskops/models/checklist.py` | Add ChecklistItem, verdict, evaluated_at |
| Models | `deskops/models/condition.py` | Add evaluate registry, predicate_map |
| Models | `deskops/models/edge.py` | Add runtime link to condition evaluator |
| Models | `deskops/models/hook.py` | Add target_callable, event namespace |
| Models | `deskops/models/task.py` | Add event_hooks field |
| Engine | `deskops/engine/__init__.py` | New module |
| Engine | `deskops/engine/routine.py` | RoutineEngine class |
| Engine | `deskops/engine/hook.py` | HookEngine class |
| Engine | `deskops/engine/condition.py` | ConditionEvaluator + predicate registry |
| Engine | `deskops/engine/context.py` | EvalContext builder |
| Engine | `deskops/engine/supervisor.py` | Supervisor startup sequence |
| Engine | `deskops/engine/executor.py` | Execution gate validators |
| Engine | `deskops/engine/closeout.py` | Auto-closeout pipeline |
| Engine | `deskops/engine/predicates/git.py` | Git state predicates |
| Engine | `deskops/engine/predicates/file.py` | File predicates |
| Engine | `deskops/engine/predicates/test.py` | Test predicates |
| Engine | `deskops/engine/predicates/doc.py` | Document field predicates |
| CLI | `deskops/cli/engine_commands.py` | New CLI commands |
| Hooks | `desk/hooks/*.md` | HookDoc instances defining event→action mappings |
| Rituals | `desk/rituals/*.md` | Shift from step docs to reference docs for hooks |
| Board | `desk/tasks/Board.md` | Add gate_state tracking for active tasks |
| Agent role | `desk/agents/*.md` | Reference the ContextBundle type in role descriptions |

---

## How — Architecture

The architecture is organized around one rule: **the engine and the agent do not overlap**. Every principle below restates this rule in operational terms.

### Design Principles (boundary-aware)

1. **The engine is closed under `[E]`.** Every operation in `deskops/engine/` must be expressible as a pure function or a deterministic subprocess call. No LLM client may be imported. The package's import-time dependency graph is verified by a test (`tests/test_engine_no_llm_imports.py`) that fails CI on any new LLM import. This is the structural enforcement of row 1 of the boundary table.

2. **The agent is closed under `[A]`.** Agents may call any registered `deskops` command, but may not directly mutate state. Every state change is engine-mediated. This is the structural enforcement of rows 14–16 of the boundary table.

3. **Hooks never call LLMs.** Hooks are `[E]`. They run bounded commands: git operations, test runners, file checks, doc mutations. If semantic work is needed at a hook point, the hook *dispatches* (`[E→A]`) — it writes a request to `attention/` and exits; an agent then picks it up. A hook is never a long-running agent process. (This addresses Soft Spot 2 and Soft Spot 11 below.)

4. **The boundary is a typed artifact, not a contract.** Every `[E→A]` crossing is a typed object: a `StartupReport`, a `GateFailureReport`, a `CloseoutFailureReport`, a `ContextBundle`. Every `[A→E]` crossing is a `deskops` CLI command. The engine never emits free-form prose; the agent never invents its own commands outside the bundle's `hook_plan`.

5. **State is in documents, not in memory.** The engine is stateless between invocations. All state is stored in SLDB-backed documents (task.current_node, checklist.verdict, etc.). If the engine crashes mid-hook, the next invocation reads current state from disk and decides whether to retry or halt. This is why `[E|E]` and `[E]` steps are interchangeable: the engine doesn't care which called it.

6. **Every `[E→A]` crossing is a committed report.** When the engine dispatches a report, the report is first written to disk (SLDB or `attention/`), then surfaced to the agent. The agent cannot lose the report, and the operator can audit it later.

7. **Every gate failure writes to attention/.** Automation never silently swallows a failure. If a condition evaluates to false, a diagnostic note is written to `desk/drawer/attention/` with the gate name, the failing condition, the current state snapshot, and a suggested resolution path. This applies to `[E]` operations only; `[A]` operations that fail surface their own errors through the agent loop.

8. **Manual override is explicit.** A human can always run `deskops closeout run` or `deskops hook fire` to force a transition. The override is `[H] → [E]` — a logged CLI command. The system does not prevent overrides; it records them. This is the only way an agent-style judgment can override an engine decision, and it is reserved for `[H]`.

### Engine-internal vs Boundary-crossing operations

A common source of design confusion is mixing `[E|E]` (sub-steps of a single engine operation) with `[E→A]` (a report that leaves the engine). The rule:

- If the result is consumed by the *next* engine step in the same flow → `[E|E]`. No disk write, no agent involvement.
- If the result is consumed by an agent to make a decision → `[E→A]`. Write to disk or stdout in a typed format.

Example: in the closeout flow, "run tests → check exit code" is `[E|E]`. "Tests failed → report to attention/" is `[E→A]`. The line between them is whether a decision is being made.

### Predicate Registry

```python
# deskops/engine/condition.py

predicate_registry: dict[str, Callable] = {}

def register_predicate(name: str, fn: Callable[[EvalContext, str], EvalResult]):
    """Register a predicate function by name."""
    predicate_registry[name] = fn

def evaluate(condition: ConditionDoc, context: EvalContext) -> EvalResult:
    """Evaluate a condition using its predicate."""
    fn = predicate_registry.get(condition.predicate)
    if fn is None:
        return EvalResult(passed=False, error=f"No predicate registered: {condition.predicate}")
    return fn(context, condition.expected)

# Built-in registrations:
register_predicate("not_empty", lambda ctx, exp: ctx.get_field(condition.subject) is not None and ctx.get_field(condition.subject) != "")
register_predicate("eq", lambda ctx, exp: str(ctx.get_field(condition.subject)) == exp)
register_predicate("file_exists", lambda ctx, exp: Path(exp).exists())
register_predicate("git_clean", lambda ctx, exp: ctx.git_state["clean"])
register_predicate("test_passes", lambda ctx, exp: run_pytest(exp))
```

### Hook Lifecycle

```
Event fired (e.g. "task.complete.trigger")
  │
  ├─ HookEngine.fire("task.complete.trigger", context)
  │   │
  │   ├─ 1. Find all HookDoc where event == "task.complete.trigger"
  │   │      or event matches by wildcard prefix (e.g. "task.complete.*")
  │   │
  │   ├─ 2. For each, evaluate condition_ref if present
  │   │      skip if condition fails
  │   │
  │   ├─ 3. Resolve hook.target:
  │   │      - "run.tests_bounded" → find function in predicate/action registry
  │   │      - "git.commit_atomic" → find function in action registry
  │   │      - "<routine-id>" → find RoutineEngine, call advance()
  │   │
  │   ├─ 4. Execute with timeout
  │   │      - Success: log, continue to next hook
  │   │      - Failure: write diagnostic, halt sequence, set task status=blocked
  │   │
  │   └─ 5. Return list of HookResult
  │
  └─ Caller reads HookResult list
      - If all passed: proceed
      - If any failed: block, route to attention
```

### ContextBundle Construction Flow

```
flowchart TB
    A[Task activation] --> B[EvalContextBuilder.build]
    B --> C[Load task doc from SLDB store]
    B --> D[Resolve references → atoms, pills]
    B --> E[Resolve files → check they exist]
    B --> F[Resolve tests → check they exist]
    B --> G[Load routine + edges + conditions]
    B --> H[Run execution gates]
    H --> I[Build gate_state dict]
    I --> J[Load hooks matching task lifecycle]
    J --> K[Assemble ContextBundle]
    K --> L{Can build?}
    L -->|Yes| M[Return to supervisor]
    L -->|No| N[Write error to attention/]
```

---

## + — Soft Spots, Risks, and Edge Cases (W5H1+ Analysis)

### Soft Spot 1: Conditions that need human judgment

**Risk:** Some conditions cannot be evaluated programmatically. Example: "The implementation follows project conventions" or "The pill coverage is appropriate."

**Mitigation option A (strict):** All conditions MUST be evaluable by a registered predicate. If a condition requires judgment, it must be broken down into sub-conditions that are evaluable. Human-judgment conditions are not allowed as blocking gates.

**Mitigation option B (hybrid):** Allow `predicate: human_review` as a special marker. These conditions produce verdict=unknown by default and block advancement until a human explicitly sets the checklist item to checked. The system writes to attention/ and waits.

**Risk:** Option B introduces a process bottleneck. Every task with human-review conditions requires an operator to touch it.

**Recommended:** Option A for gating decisions, Option B only for post-hoc audit items that do not block advancement.

### Soft Spot 2: Hook failure mid-sequence

**Risk:** A closeout sequence has three hooks: run tests → commit → retire. If commit succeeds but retire fails (SLDB store error), the system is in an inconsistent state: the code is committed, but the task is not retired from the board.

**Mitigation:** Each hook is atomic and idempotent where possible. The engine logs each hook result before executing the next. On any hook failure, the sequence halts and writes a recovery note to attention/ listing:
- Which hooks succeeded
- Which hook failed
- What state the system is in
- Suggested recovery command (e.g., `deskops closeout run --resume`)

**Ideal (future):** Each hook sequence is wrapped in a compensating action. If retire fails after a successful commit, a compensation hook would note the discrepancy but not revert the commit (commits are immutable).

### Soft Spot 3: Git state is dirty when supervisor starts

**Risk:** The user has uncommitted changes from a previous interrupted session. The supervisor startup hook `check.git_state` returns fail. The supervisor refuses to start.

**Edge case:** The dirty state is the task's own in-progress work from a crashed session. The system should not block — it should detect the previous session and offer resume.

**Mitigation:** The git check predicate distinguishes:
- `git_clean: true` — no dirty files → normal start
- `git_clean: false` + active task has matching dirty files → session was interrupted, offer resume
- `git_clean: false` + no active task → warn, log to attention, do not block (operator may be doing something else)

### Soft Spot 4: Concurrent tasks in the same phase

**Risk:** Two active tasks both have event hooks that fire on `task.complete`. Both try to run tests and commit. The second commit will include changes from both tasks, violating the one-commit-per-task principle.

**Mitigation:** The phase model already prohibits overlapping tasks. Within a phase, tasks execute sequentially (the next phase does not start until the current phase is done). If the board allows parallel execution in the future, the hook system must be scoped to the task: `deskops closeout run` for task A should only include files from task A.

**Current rule:** Only one active task per phase. If this changes, hook scoping must be re-addressed.

### Soft Spot 5: Engine with no active hooks

**Risk:** A task has no hooks registered for its lifecycle events. The engine fires events but nothing responds. The task proceeds without automation — reverting to the current manual ritual model.

**Is this a problem?** Not necessarily. Tasks without hooks degrade gracefully to the current behavior. Hooks are opt-in at the task level. The default is manual, and tasks opt into automation by binding hooks.

**Recommendation:** Default behavior = no hooks = current manual workflow. Hooks are explicitly bound in the task's `event_hooks` field or globally via HookDoc instances.

### Soft Spot 6: Testing the engine itself

**Risk:** The engine (routine state machine, hook dispatch, condition evaluation) must be tested. But it depends on git state, file system state, and SLDB store state.

**Mitigation:** The engine is designed with dependency injection. EvalContext is built by a builder class that can be mocked in tests. Predicate functions receive a context argument, not a live file system. Tests inject fake contexts:

```python
def test_routine_advance():
    ctx = EvalContext(
        task=TaskDoc(status="active", current_node="checklist-execution-ready"),
        git_state={"clean": True},
        file_state={"deskops/models/atom.py": hash("content")},
    )
    engine = RoutineEngine(routine, edges, conditions, ctx)
    assert engine.next() == "checklist-testing-ready"
    engine.advance()
    assert ctx.task.current_node == "checklist-testing-ready"
```

### Soft Spot 7: What if a hook target crashes?

**Risk:** A hook that shells out to a CLI command (e.g., `pytest`) crashes or hangs.

**Mitigation:** Each hook execution has a configurable timeout (default 120s). Timeouts produce `HookResult(status="timeout")`. The hook engine does not retry automatically — it halts the sequence and writes a diagnostic. The operator can re-fire the hook with `deskops hook fire`.

### Soft Spot 8: Event namespace collisions

**Risk:** Two people define hooks for `task.complete` with different intents. Or a hook definition in a task's `event_hooks` field conflicts with a global hook for the same event.

**Mitigation:**
- Global hooks fire first (in order of HookDoc id), then task-specific hooks.
- If a task's `event_hooks` explicitly lists a hook id, it is added to the fire list (not replacing defaults).
- To suppress a global hook for a specific task, the task can set `event_hooks: {"task.complete": ["suppress:global.hook-id"]}`.
- This is an advanced use case. Default behavior: global hooks + task hooks compose.

### Soft Spot 9: Predicate registry becomes a god object

**Risk:** The predicate registry in `condition.py` grows unbounded as every team adds unique predicates. Predicates become coupled to specific task types or file structures.

**Mitigation:**
- Core predicates are limited to generic operations (field checks, file existence, git state, test exit codes).
- Project-specific predicates live outside deskops core, in the consuming project's codebase, and are registered at import time.
- The registry supports namespaced predicate names: `git.clean`, `file.exists`, `test.passes`, `project.custom_predicate`.

### Soft Spot 10: Migration from old to new

**Risk:** Existing rituals, checklist docs, and edge docs must be migrated to work with the engine. Old documents that lack structured items or evaluable conditions will break.

**Mitigation phases:**
1. Engine layer is additive — old documents still work, just without automation.
2. A `deskops migrate ritual <id>` command converts a Markdown ritual doc into corresponding HookDoc instances.
3. A `deskops migrate checklist <id>` command converts plain items to ChecklistItem instances and suggests condition_refs.
4. Migration is per-task, not bulk. Each task migrates when its next phase of work begins.

### Soft Spot 11: Boundary drift over time

**Risk:** This is the most operationally dangerous soft spot. As the codebase evolves, an engineer (or an agent) will be tempted to make a hook "smarter" by adding a direct LLM call inside the hook target, or to make a predicate "context-aware" by importing an agent class. Each individual change is small and well-intentioned. The cumulative effect is that the engine gradually becomes a thin wrapper around an agent, and the boundary in this spec becomes fictional.

**Symptoms to watch for:**
- A new commit imports `openai`, `anthropic`, or any `litellm`-style wrapper in `deskops/engine/`.
- A new commit makes a hook target longer than ~50 lines of pure Python.
- A new commit introduces a "context object" that contains `prompt: str` or `messages: list[dict]` fields used inside the engine.
- The number of `[E]` rows in the boundary table shrinks while the number of `[A]` rows grows, without a corresponding rewrite of an actor.
- Agent prompts start containing shell snippets that bypass `deskops` and call `git` or `pytest` directly.

**Mitigations (must apply all four):**
1. **Test as a tripwire.** `tests/test_engine_no_llm_imports.py` runs in CI and fails on any LLM client import in `deskops/engine/`. This is the cheapest and strongest defense.
2. **Audit script.** `deskops audit boundary` walks the dependency graph of every hook target and predicate, and reports the largest non-engine imports. Run it monthly.
3. **PR review rule.** Any PR that touches `deskops/engine/` requires an explicit statement in the PR description of which boundary table rows it changes. Reviewer verifies the table is updated in the same PR.
4. **Boundary table as a living document.** The Decision Boundary table in this spec is not aspirational — it is the contract. When the implementation diverges from the table, the table (and this spec) must be updated in the same commit.

**Recommended:** Treat Soft Spot 11 as a *category*, not a single risk. Every other soft spot in this section can be solved in code; boundary drift is solved by process discipline.

---

## Implementation Order

### Phase 0: Foundation (no behavioral changes)
1. Add `ChecklistItem` model with checked/required fields (backward-compatible with plain strings)
2. Create `deskops/engine/` package structure
3. Implement `ConditionEvaluator` with predicate registry
4. Implement core predicates (not_empty, eq, file_exists)

### Phase 1: Read-only engine (inspection, no mutation)
5. Implement `RoutineEngine` with `.next()` and `.state()` (read-only, no advance)
6. Implement `EvalContextBuilder`
7. Add `deskops routine next <task-id>` CLI command
8. Add `deskops checklist verify <checklist-id>` CLI command

### Phase 2: Supervisor automation
9. Implement supervisor startup sequence
10. Implement `ContextBundle` builder
11. Add `deskops supervisor start` CLI command
12. Add `deskops context bundle <task-id>` CLI command

### Phase 3: Hook system
13. Implement `HookEngine` with event dispatch
14. Implement core hook targets (git check, test runner, commit, retire)
15. Add `deskops hook list` and `deskops hook fire` CLI commands
16. Create initial hook definitions in `desk/hooks/`
17. Update rituals to reference hooks instead of step lists

### Phase 4: Execution gates
18. Implement execution gate validators (atomization, pill coverage, staleness)
19. Wire gate failure → attention/ writing
20. Bind hooks to lifecycle events in task model

### Phase 5: Auto-closeout
21. Implement closeout pipeline (test → commit → retire)
22. Add `deskops closeout run <task-id>` CLI command
23. Wire `task.complete.trigger` → closeout pipeline
24. Bind hooks to the current active task's routine

### Phase 6: Migration tools
25. Implement `deskops migrate ritual <id>` 
26. Implement `deskops migrate checklist <id>`
27. Migrate existing task routines to use hooks

---

## Appendix A: Comparison with Current Behavior

| Aspect | Current (rituals) | Future (boundary-aware engine) | Boundary |
|---|---|---|---|
| Cold-review subagent | Agent must remember to do it | Engine dispatches a fresh-context subagent with sealed bundle on `task.active.enter` | `[E→A]` |
| Pill coverage check | Agent must read pills and compare | Gate predicate validates pill binding against file list | `[E]` |
| Staleness check | Manual | Condition checks `depends_on` task statuses before activation | `[E]` |
| Test execution | Agent decides when to run | Hook target runs bounded pytest on `task.complete.trigger`; blocks on fail | `[E]` |
| Commit boundary | Agent must remember to commit | Hook target commits atomically after tests pass | `[E]` |
| Task retirement | Agent deletes file manually | Hook target retires from board and untracks from store | `[E]` |
| Phase transition | Manual board update | Hook checks all tasks closed, fires `phase.ready` | `[E]` |
| Subagent context | Free-form prompt | Typed `ContextBundle` with pre-verified `gate_state` | `[E→A]` |
| Triage of ambiguous items | Operator judgment | SupervisorAgent consumes typed startup report | `[A]` |
| Inbox review | Operator reads by hand | Engine scans, produces a typed list; agent triages | `[E→A]` |
| Drawer → active promotion | Operator decides | SupervisorAgent decides from typed report | `[A]` |

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **Engine (`[E]`)** | The deterministic subsystem in `deskops/engine/`. Pure Python, no LLM, no judgment. Its only public surface is the `deskops` CLI. |
| **Agent (`[A]`)** | An LLM-driven role (SupervisorAgent, ExecutorAgent) that consumes engine reports and produces semantic work. Never mutates state directly; always goes through `deskops` commands. |
| **Human operator (`[H]`)** | The user. Invokes `deskops` override commands and resolves `attention/` items. |
| **Boundary crossing (`[E→A]` / `[A→E]`)** | A handoff between engine and agent. Always a typed artifact (report, CLI command, ContextBundle). |
| **Trigger** | A verb reserved for `[E→A]` dispatch: "the engine *triggers* a subagent," "the engine *triggers* a report to attention/." |
| **Dispatch** | A verb reserved for `[A→E]` invocation: "the agent *dispatches* `deskops closeout run`," "the agent *dispatches* the bundle." Note: the spec uses *dispatch* in the engine→agent direction in the lifecycle table for the same operation; the Glossary normalizes to *trigger* (E→A) and *dispatch* (A→E). Earlier sections of this spec follow the same convention. |
| **Gate** | A condition that must pass before a state transition. If it fails, the transition is blocked. |
| **Hook** | An automated action triggered by an event. Composed of event + condition + target. Always `[E]`. |
| **Predicate** | A registered function that evaluates a condition against an `EvalContext`. Always `[E]`. |
| **Event** | A named string that signals a lifecycle occurrence (e.g. `task.complete.trigger`). |
| **RoutineEngine** | A state machine that reads a `RoutineDoc` + `EdgeDoc`s + `ConditionDoc`s and returns transitions. |
| **ContextBundle** | A typed data structure carrying everything an executor subagent needs to perform a task. |
| **EvalContext** | A snapshot of the system state at the time of evaluation. Used by predicates. |
| **Gates-passed** | A `ContextBundle` whose `gate_state` dict has no `"fail"` entries. |
| **Boundary drift** | The gradual erosion of the engine/agent separation as features are added. Soft Spot 11. |
