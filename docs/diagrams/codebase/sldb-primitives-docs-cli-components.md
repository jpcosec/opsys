# SLDB, Lifecycle, Docs, and CLI Components

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

This diagram shows how the major deskops components interact with SLDB infrastructure, document models, specs, the task lifecycle graph, materializers, and CLI commands.

```mermaid
flowchart TB
    subgraph sldb[SLDB infrastructure]
        store[".sldb store\nmodels, tracked docs, indexes"]
        models["StructuredNLDoc models\nPydantic contracts"]
        docs["Modeled Markdown docs\nextract/render/validate"]
        fields["Fields and sections\nread/write/edit/query"]
        semantic["Semantic indexes\nfind/navigation/trace"]
        edgeidx["Edge index and relations\nRelationDoc, edges_from,\nwhere_matches"]
    end

    subgraph deskops[Deskops workflow domain]
        specs["spec/ artifacts, fields, lifecycle\ncompiler vocabulary"]
        lifecycle["Lifecycle\nwrites the ritual graph,\nfires transitions"]
        materializers["Materializers\natom/task/doc projections"]
        cli["deskops CLI\ncommands from workflow nouns"]
        surfaces["desk/ surfaces\ntasks, atoms, rituals, lifecycle, inbox, drawer"]
    end

    subgraph outputs[Human and machine outputs]
        bigdocs["Big docs\ncomposed explanations"]
        diagrams["Diagrams\nspec2viz source -> projections"]
        tests["Tests and validation\nroundtrip, tags, workflow gates"]
        issues["Issues and inbox notes\nmissing capability or unclear decisions"]
    end

    specs -->|compile to| models
    specs -->|declare transitions and effects for| lifecycle
    models -->|render/extract/validate| docs
    docs -->|tracked by| store
    fields -->|operate on| docs
    semantic -->|indexes| store
    edgeidx -->|indexes relations of| store

    cli -->|invokes| lifecycle
    cli -->|creates/updates| surfaces
    cli -->|delegates modeled document work to| docs
    cli -->|delegates field operations to| fields
    lifecycle -->|reads transitions and evaluates conditions through| edgeidx
    lifecycle -->|moves tasks in| surfaces
    materializers -->|project from| surfaces
    materializers -->|write modeled docs through| docs

    surfaces -->|materialize as| bigdocs
    surfaces -->|materialize as| diagrams
    surfaces -->|validated by| tests
    issues -->|route missing infra to| sldb
    issues -->|route missing diagram infra to| diagrams
```

## Reading Rules

- SLDB owns reusable structured-document infrastructure: models, stores, docs, fields, sections, semantic indexes, and the edge index with its relations and `--where` evaluation.
- Deskops owns workflow-domain concepts: specs, the lifecycle (which transitions exist and what they set), materializers, CLI grammar, and desk surfaces.
- The CLI should be a thin operational surface over specs, the lifecycle graph, and SLDB document operations.
- Big documents should not bypass the model; they should be modeled either as shallow composed documents or as stricter typed documents when their internal structure needs machine validation.
- Missing reusable document behavior routes to SLDB; missing diagram-source behavior routes to spec2viz; missing workflow behavior stays in deskops.

## Source Atoms

- `desk/atoms/workflow-model/atom-deskops-owns-workflow-not-document-infrastructure.md`
- `desk/atoms/workflow-model/atom-sldb-is-read-write-edit-surface.md`
- `desk/atoms/workflow-model/atom-spec-fields-compile-into-model-fields.md`
- `desk/atoms/workflow-model/atom-upstream-routing-needs-convenient-command.md`
- `desk/atoms/knowledge-model/atom-main-docs-are-composed-materializations.md`
