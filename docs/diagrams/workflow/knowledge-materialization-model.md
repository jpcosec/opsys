# Knowledge Materialization Model

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

This diagram shows the generic project model where atoms distill internal knowledge and docs, specs, and diagrams materialize that knowledge for different uses.

```mermaid
flowchart TB
    raw["Raw signals\nconversations, bugs, tasks, commits, incidents"]
    atoms["Atoms\ninternal distilled knowledge"]

    subgraph Materializations["Materializations"]
        docs["Main docs\nhuman-facing narrative"]
        specs["Specs\ncontracts and constraints"]
        diagrams["Diagrams\nvisual projections"]
    end

    subgraph Execution["Execution surfaces"]
        code["Code\nexecutable materialization"]
        tests["Tests\nverification materialization"]
        ops["Operations\nprocess and runtime behavior"]
    end

    feedback["Feedback and drift\nissues, failures, review, changed reality"]

    raw -->|distill stable reusable claims| atoms
    atoms -->|explain for humans| docs
    atoms -->|formalize as contracts| specs
    atoms -->|project relationships| diagrams

    docs --> code
    specs --> code
    diagrams --> code
    specs --> tests
    docs --> ops

    code --> feedback
    tests --> feedback
    ops --> feedback
    feedback -->|atom wrong or materialization stale?| atoms
    feedback -->|update stale projection| docs
    feedback -->|update stale contract| specs
    feedback -->|update stale view| diagrams
```

## Rules

- Atoms are internal distilled knowledge, not public-facing docs.
- Main docs, specs, and diagrams are materializations of selected atoms.
- Code implements or violates the relevant atoms and specs.
- Tests verify selected atoms, specs, and behaviors.
- Feedback decides whether an atom changed or a materialization drifted.
