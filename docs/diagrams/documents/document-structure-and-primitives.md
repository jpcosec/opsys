# Document Structure and Primitives

The desk has both structured and less structured documents.

Structured documents are backed by `sldb`. Less structured documents can exist where precision is not yet useful, such as future features, loose issues, or notes in drawers.

```mermaid
flowchart TB
    subgraph Documents["Document kinds"]
        structured["Structured docs\nsldb-backed\nfield-defined"]
        loose["Less structured docs\nfeatures / issues / notes\nallowed to be looser"]
    end

    subgraph Fields["Structured field design"]
        fields["Model fields\nSLDB payload units"]
        compose["Composition\ntracked docs and payload fields"]
        nodrift["No unnecessary copied prose\nless drift"]
    end

    subgraph Actions["Primitives add action"]
        primitive["Primitive\naction over sldb data"]
        checklist["Checklist\nexplicit gate / completeness"]
        condition["Condition\nreads payload state"]
        operator["Operator\nmutates payload state"]
        edge["Edge\nroutes progression"]
        hook["Hook\nruns around operation"]
    end

    subgraph Example["Example"]
        board["Board\nindexes tasks"]
        indexed["Indexed task set"]
    end

    structured --> fields
    fields --> compose
    compose --> nodrift
    loose -->|can later be structured| structured

    structured --> primitive
    primitive --> checklist
    primitive --> condition
    primitive --> operator
    primitive --> edge
    primitive --> hook

    board -->|uses primitives to act on data| checklist
    checklist --> indexed
    condition --> indexed
    edge --> indexed
```

## Rules

- If something is already written, reference it instead of copying it.
- Copying already-written content creates drift.
- Structured docs should expose model fields that are small enough to query and edit safely through SLDB.
- A document composed from another structured document should use SLDB composition/query surfaces rather than duplicate prose or create separate field-instance docs.
- Less structured docs are acceptable for future/deferred/unclear work, but can later be converted into structured docs when the workflow needs precision.
- Primitives are what give action to `sldb` data.
- A board can index tasks by using primitives such as checklists, conditions, edges, or other action units.
