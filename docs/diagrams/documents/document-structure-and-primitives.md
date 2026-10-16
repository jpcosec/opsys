# Document Structure and the Lifecycle Graph

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

The desk has both structured and less structured documents.

Structured documents are backed by `sldb`. Less structured documents can exist where precision is not yet useful, such as future features, loose issues, or notes in drawers.

```mermaid
flowchart TB
    subgraph Documents["Document kinds"]
        structured["Structured docs\nsldb-backed\nfield-defined"]
        loose["Less structured docs\nfeatures / issues / notes\nallowed to be looser"]
    end

    subgraph Fields["Structured field design"]
        fields["Fields\nsmall semantic units"]
        compose["Composition\nother docs select fields"]
        nodrift["No unnecessary copied prose\nless drift"]
    end

    subgraph Graph["The sldb graph adds action"]
        states["States\nrituals: execution, testing, closeout"]
        transition["Transition\nRelationDoc between rituals\ntyped by a RelationTypeDoc verb"]
        condition["Condition\nsldb --where predicate on the task"]
        effect["Effect\nstatus the transition sets\n(spec/workflows/task_lifecycle.yaml)"]
    end

    subgraph Example["Example"]
        board["Board\nindexes tasks"]
        task["Task\ncurrent_node = a ritual"]
    end

    structured --> fields
    fields --> compose
    compose --> nodrift
    loose -->|can later be structured| structured

    structured -->|tracked in the store, nodes of| states
    states --> transition
    transition -->|guarded by| condition
    transition -->|declares| effect

    board -->|routes| task
    task -->|sits in| states
    condition -->|reads| task
    effect -->|updates| task

    classDef docs fill:#e7f2ff,stroke:#2a6099,color:#111;
    classDef fields fill:#e9f8ee,stroke:#2f7a44,color:#111;
    classDef action fill:#ffe8ee,stroke:#9e3152,color:#111;
    classDef example fill:#fff3d9,stroke:#a66a00,color:#111;
    class structured,loose docs;
    class fields,compose,nodrift fields;
    class states,transition,condition,effect action;
    class board,task example;
```

## Rules

- If something is already written, reference it instead of copying it.
- Copying already-written content creates drift.
- Structured docs should expose model fields that are small enough to query and edit safely through SLDB.
- A document composed from another structured document should use SLDB composition/query surfaces rather than duplicate prose or create separate field-instance docs.
- Less structured docs are acceptable for future/deferred/unclear work, but can later be converted into structured docs when the workflow needs precision.
- The sldb graph is what gives action to `sldb` data: rituals are states, RelationDocs are transitions, and their `--where` conditions are the gates.
- A board indexes tasks; each task sits in one ritual of the lifecycle graph and moves when a transition's condition holds.
