# Task Accumulation, Initialization, and Resolution

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

This diagram focuses only on how tasks enter the active work system, become executable by a clean subagent, and disappear after resolution.

```mermaid
flowchart TB
    subgraph Sources["Task accumulation sources"]
        external["External project need\nrequirement / question / bug"]
        inbox["Inbox\ninter-project message"]
        issue["Issue\ndrawers/issues\nloose problem detection"]
        feature["Feature\ndrawers\ndeferred future work"]
        atom["Atom\ndurable structured knowledge\nmay be referenced by task"]
        direct["Direct task capture\nknown active work"]
    end

    subgraph Accumulation["Accumulation into active task space"]
        candidate["Task candidate\nnot necessarily active yet"]
        taskdoc["TaskDoc\nserializable work unit"]
        taskboard["Tasks Board\nindex + routing heap/stack"]
    end

    subgraph Planning["Board-wide planning"]
        atomize_board["Atomize whole board\nsmall coherent tasks"]
        dependencies["Resolve dependencies\nfiles / surfaces / ordering"]
        phases["Build board-local phases\nparallel tasks that do not touch each other"]
    end

    subgraph Initialization["Per-task initialization"]
        scope["Fix task scope\nfiles / dependencies / references"]
        validation["Fix task validation\ndone_when / touched-surface tests"]
        rituals["Bind relevant rituals\nexecution / testing / closeout"]
        pills["Bind or create context pills\nno clean-agent improvisation"]
        ready["Initialized task\nready for clean subagent"]
    end

    subgraph Execution["Execution by clean subagent"]
        subagent["Clean subagent\nreceives task + pills + rituals"]
        ambiguity["Step 1: ambiguity review\nif unclear, return task"]
        change["Code / tests / docs change"]
        unit["Automatic routine\nunit test touched surface only\nafter each task"]
        update["Update task state\nstatus / current node / history"]
    end

    subgraph PhaseValidation["Phase validation"]
        e2e["Automatic routine\nrun full e2e after phase\nall parallel tasks integrated"]
    end

    subgraph Resolution["Resolution and cleanup"]
        closeout["Closeout ritual\nconfirm validation + cleanup"]
        hook["Automatic hook\nclose/test/commit\nopen trigger/order design"]
        ingest["Ingest used pills\ninto atoms and/or docs"]
        delete_pills["Delete obsolete pills\ntransient context removed"]
        unroute["Remove task from board\nand active task set"]
        commit["Closing git commit\nsource of durable history"]
        branching["Open design area\nbranching + commit naming"]
    end

    external --> inbox
    inbox --> candidate
    issue --> candidate
    feature --> candidate
    candidate -->|references when work touches durable knowledge| atom
    direct --> candidate

    candidate --> taskdoc
    taskdoc --> taskboard
    taskboard --> atomize_board

    atomize_board --> dependencies
    dependencies --> phases
    phases -->|for each task in phase| scope
    scope --> validation
    validation --> rituals
    rituals --> pills
    pills --> ready

    ready --> subagent
    subagent --> ambiguity
    ambiguity -->|unclear| scope
    ambiguity -->|clear| change
    change --> unit
    unit --> update
    update --> e2e

    e2e -->|fails or reveals gap| dependencies
    e2e -->|passes| closeout
    closeout --> hook
    hook --> ingest
    ingest --> delete_pills
    delete_pills --> unroute
    unroute --> commit
    commit --> branching
```

## Notes

- Accumulation is not the same as initialization: a task can exist as a candidate before it is safe to execute.
- Atomization happens over the whole board, not only one task. Dependencies and touched surfaces are used to build phases inside the tasks board; `phase` is not a standalone document.
- Initialization turns each task in a phase into a small, bounded, serializable unit with scope, validation, rituals, and context pills.
- The first action of every clean subagent is ambiguity review. If implementation is ambiguous, the subagent returns the task instead of improvising.
- After each task, only the touched surface should be unit tested.
- After each phase, the full e2e suite should run because parallel changes are now integrated.
- Unit tests, e2e tests, board cleanup checks, and commit-if-green behavior are automatic routines/hooks, not LLM tasks.
- Ambiguity review, implementation, failure triage, and pill ingestion decisions are LLM/subagent tasks.
- Resolution does not merely mark a task as done. It must clean context, ingest transient pills into durable knowledge/docs, remove active routing, and leave the durable record in git.
- The close/test/commit hook is required, but its exact trigger and order still need workflow design: per-task, per-phase, or both.
- Branching and commit naming are still an open workflow design area.
