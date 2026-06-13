# Task Board Phases

`Phase` is not a standalone document. It is a board-local grouping inside the tasks board.

The tasks board owns active routing. A phase is the board's current execution batch: tasks that can run at the same time because their dependencies are satisfied and their touched surfaces do not overlap.

```mermaid
flowchart TB
    subgraph Board["Tasks Board"]
        backlog["Backlog / candidate tasks\nknown work not ready to run"]
        deps["Dependency map\nwhich tasks must precede others"]
        surfaces["Touched surfaces map\nfiles / modules / docs / specs"]
        phases["Phases\nboard-local execution batches"]

        subgraph Phase1["Phase N"]
            t1["Task A\nready"]
            t2["Task B\nready"]
            t3["Task C\nready"]
        end

        blocked["Blocked / waiting tasks\ndeps not satisfied or ambiguity unresolved"]
        done["Resolved tasks\nremoved from active board after closeout"]
    end

    subgraph Gate["Phase construction rules"]
        deps_rule["Dependencies satisfied"]
        no_touch_rule["No touched-surface overlap"]
        init_rule["Each task initialized\nscope validation pills rituals"]
        ambiguity_rule["No unresolved ambiguity"]
    end

    subgraph Execution["Phase execution"]
        agents["Clean subagents\none per task"]
        unit["Per-task unit tests\nonly touched surface"]
        e2e["Phase e2e tests\nafter all phase tasks"]
        close["Close/test/commit hook\ntrigger/order still open"]
    end

    backlog --> deps
    backlog --> surfaces
    deps --> phases
    surfaces --> phases

    deps_rule --> phases
    no_touch_rule --> phases
    init_rule --> phases
    ambiguity_rule --> phases

    phases --> Phase1
    Phase1 --> agents
    agents --> unit
    unit --> e2e
    e2e -->|passes| close
    close --> done
    e2e -->|fails| blocked

    blocked -->|clarified / dependency resolved| backlog
```

## Board Shape

The board should probably grow sections like these rather than creating `PhaseDoc`:

```markdown
## Tasks

- task-a
- task-b
- task-c

## Dependencies

- task-c depends_on task-a

## Touched Surfaces

- task-a: deskops/models/task.py, tests/test_task.py
- task-b: docs/README.md
- task-c: deskops/cli/parser.py

## Phases

### Phase 1

- task-a
- task-b

### Phase 2

- task-c
```

## Rules

- A phase is computed or recorded inside the tasks board.
- A phase contains only initialized tasks.
- Tasks in the same phase must not touch the same files, modules, specs, docs, or other meaningful surfaces.
- Each task in a phase starts with clean-subagent ambiguity review.
- If ambiguity exists, the task returns to planning and does not execute.
- Each task runs only its touched-surface unit tests after implementation.
- The full e2e suite runs after the whole phase completes.
- The close/test/commit hook is required, but its exact per-task/per-phase trigger is still unresolved.
