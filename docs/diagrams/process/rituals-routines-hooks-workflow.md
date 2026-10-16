# Rituals and the Lifecycle Graph

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

Rituals are the current textual form of operating process. They should be decomposed once the workflow is clear.

```mermaid
flowchart TB
    subgraph Current["Process form"]
        ritual["Ritual\ntextual process document"]
        execution["Execution ritual"]
        testing["Testing ritual"]
        closeout["Closeout ritual"]
    end

    subgraph Graph["Lifecycle graph (sldb)"]
        state["State\neach ritual is a graph node"]
        transition["Transition\nRelationDoc between rituals"]
        gate["Gate\n--where condition on the transition"]
        future["Automatic checks\nfuture: more rules as conditions"]
    end

    subgraph AppliedTo["Applied to"]
        board["Tasks board\nplanning and phases"]
        task["Task\nexecution and resolution"]
        pill["Pill\ncreation, use, ingestion, deletion"]
        phase["Board-local phase\ne2e and integration"]
    end

    ritual --> execution
    ritual --> testing
    ritual --> closeout
    execution --> state
    testing --> state
    closeout --> state
    state --> transition
    transition --> gate
    ritual -.->|stable obligations can become| future

    transition --> task
    gate --> task
    gate --> board
    gate --> phase
    future -.-> pill
    future -.-> phase

    classDef current fill:#ffe8ee,stroke:#9e3152,color:#111;
    classDef target fill:#e7f2ff,stroke:#2a6099,color:#111;
    classDef applied fill:#e9f8ee,stroke:#2f7a44,color:#111;
    class ritual,execution,testing,closeout current;
    class state,transition,gate,future target;
    class board,task,pill,phase applied;
```

## Rules

- Rituals currently explain how to operate tasks, pills, code, testing, and closeout.
- Rituals have drifted and should not be treated as final architecture.
- The task lifecycle already uses the rituals as states of the desk's sldb graph; transitions between them are RelationDocs.
- Gates make preconditions explicit before progress: each transition carries an sldb `--where` condition on the task.
- As ritual obligations stabilize, more of them can become transition conditions, distinguishing automatic deterministic checks from LLM/subagent work.
- Automatic checks can run tests, validate board cleanup, block deletion, and commit when they pass; today the closeout transition plus the closeout commit do this for tasks.
- LLM/subagent tasks handle ambiguity, implementation, and semantic decisions.
