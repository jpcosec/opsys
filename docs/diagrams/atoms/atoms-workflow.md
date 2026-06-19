# Atoms Workflow

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

Atoms are not transient work items. They are the minimum structured knowledge units.

```mermaid
flowchart TB
    subgraph Source["Atom source space"]
        domain["Design domain folder\ndesk/atoms/<domain>/"]
        atom["AtomDoc\none curated raw answer"]
        question["5WH1+ field\nexactly one question"]
        what["What atom"]
        why["Why atom"]
        how["How / How-not atom"]
        when["When atom"]
        where["Where atom"]
        whom["For whom atom"]
    end

    subgraph Compositions["Durable compositions"]
        specs["Specs\ncompose atoms as contracts"]
        docs["Documentation\nREADME / concepts / guides"]
        code_contract["Code-facing contract\nreferences what implementation must respect"]
    end

    subgraph References["Operational references"]
        task["Task references atom\nwhen work touches durable knowledge"]
        pill["Pill references atom\nwhen transient context explains existing knowledge"]
        feature["Feature references atom\nwhen future work depends on concept"]
        code["Code relation\nnon-compositional\nneeds definition"]
    end

    subgraph Creation["Creation workflow"]
        trigger["Creation trigger\nmissing durable knowledge / repeated pattern / doc-spec need"]
        source_doc["Source material\nissue / feature / conversation processing"]
        create["Create AtomDoc\ncurated answer only"]
        place["Place by design domain"]
    end

    subgraph Maintenance["Knowledge maintenance"]
        drift["Drift detected\nspec/doc/code no longer matches atom"]
        update_atom["Update atom\nif durable knowledge changed"]
        update_materialization["Update materialization\nif implementation/doc/spec drifted"]
    end

    domain --> atom
    atom --> question
    question --> what
    question --> why
    question --> how
    question --> when
    question --> where
    question --> whom
    specs -->|sldb composition references atoms| atom
    docs -->|sldb composition references atoms| atom
    code_contract -->|reference / constraint relation| atom

    task --> atom
    pill --> atom
    feature --> atom
    code --> atom

    trigger --> source_doc
    source_doc --> create
    create --> place
    place --> domain

    specs --> drift
    docs --> drift
    code_contract --> drift
    drift -->|knowledge changed| update_atom
    drift -->|artifact stale| update_materialization
    update_atom --> atom
    update_materialization --> specs
    update_materialization --> docs
    update_materialization --> code_contract
```

## Rules

- Atoms live under `desk/atoms`, grouped by design domain.
- Atoms are durable knowledge, not tasks.
- Each atom answers exactly one `5WH1+` question: what, why, how, how-not, when, where, or for whom.
- Specs and documentation should reference or compose tracked atom documents through SLDB rather than copy atom prose.
- Structured documents should expose useful model fields in their SLDB payloads, but those fields remain inside the owning document model.
- Good model-field design plus explicit atom references keep composed documents small and prevent duplication-driven drift.
- Tasks, pills, and features may reference atoms.
- If a task changes code/spec/docs that touch durable knowledge, it should reference the relevant atoms.
- Drift can mean either the atom is stale or a materialization is stale; the workflow must decide which side changes.
- Drafts of would-be atoms are not atoms; they are issues, features, notes, or conversation-processing documents until curated into `AtomDoc`.
- Atom-to-code relationships are not simple compositions. They need their own relation model because code may implement, respect, violate, or depend on an atom without being generated from it.
