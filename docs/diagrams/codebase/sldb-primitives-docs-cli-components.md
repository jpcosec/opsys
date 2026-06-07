# SLDB Primitives Docs CLI Components

This diagram shows how the major deskops components interact with SLDB infrastructure, document models, specs, primitives, materializers, and CLI commands.

```mermaid
flowchart TB
    subgraph sldb[SLDB infrastructure]
        store[".sldb store\nmodels, tracked docs, indexes"]
        models["StructuredNLDoc models\nPydantic contracts"]
        docs["Modeled Markdown docs\nextract/render/validate"]
        fields["Fields and sections\nread/write/edit/query"]
        semantic["Semantic indexes\nfind/navigation/trace"]
    end

    subgraph deskops[Deskops workflow domain]
        specs["spec/ artifacts and fields\ncompiler vocabulary"]
        primitives["Primitives\nstate checks, transitions, gates"]
        materializers["Materializers\natom/task/doc projections"]
        cli["deskops CLI\ncommands from workflow nouns"]
        surfaces["desk/ surfaces\ntasks, atoms, rituals, inbox, drawer"]
    end

    subgraph outputs[Human and machine outputs]
        bigdocs["Big docs\ncomposed explanations"]
        diagrams["Diagrams\nspec2viz source -> projections"]
        tests["Tests and validation\nroundtrip, tags, workflow gates"]
        issues["Issues and inbox notes\nmissing capability or unclear decisions"]
    end

    specs -->|compile to| models
    specs -->|define legal operations for| primitives
    models -->|render/extract/validate| docs
    docs -->|tracked by| store
    fields -->|operate on| docs
    semantic -->|indexes| store

    cli -->|invokes| primitives
    cli -->|creates/updates| surfaces
    cli -->|delegates modeled document work to| docs
    cli -->|delegates field operations to| fields
    primitives -->|mutate/check| surfaces
    materializers -->|project from| surfaces
    materializers -->|write modeled docs through| docs

    surfaces -->|materialize as| bigdocs
    surfaces -->|materialize as| diagrams
    surfaces -->|validated by| tests
    issues -->|route missing infra to| sldb
    issues -->|route missing diagram infra to| diagrams
```

## Reading Rules

- SLDB owns reusable structured-document infrastructure: models, stores, docs, fields, sections, and semantic indexes.
- Deskops owns workflow-domain concepts: specs, primitives, materializers, CLI grammar, and desk surfaces.
- The CLI should be a thin operational surface over specs, primitives, and SLDB document operations.
- Big documents should not bypass the model; they should be modeled either as shallow composed documents or as stricter typed documents when their internal structure needs machine validation.
- Missing reusable document behavior routes to SLDB; missing diagram-source behavior routes to spec2viz; missing workflow behavior stays in deskops.

## Source Atoms

- `desk/atoms/workflow-model/atom-deskops-owns-workflow-not-document-infrastructure.md`
- `desk/atoms/workflow-model/atom-sldb-is-read-write-edit-surface.md`
- `desk/atoms/workflow-model/atom-spec-fields-compile-into-model-fields.md`
- `desk/atoms/workflow-model/atom-upstream-routing-needs-convenient-command.md`
- `desk/atoms/knowledge-model/atom-main-docs-are-composed-materializations.md`
