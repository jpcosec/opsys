# LLM Tasks vs Automatic Routines

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

Some workflow actions are work for a clean LLM subagent. Others are deterministic routines or hooks that should run automatically.

```mermaid
flowchart TB
    subgraph HumanOrLLM["LLM / subagent tasks"]
        ambiguous["Ambiguity review\nrequires language judgment"]
        design["Design / implementation choice\nrequires tradeoff reasoning"]
        code_change["Code/docs/spec change\nrequires editing"]
        pill_ingest["Pill ingestion\ndecide atom/docs destination"]
        failure_triage["Failure triage\ninterpret test or e2e failure"]
    end

    subgraph Automatic["Automatic routines / hooks"]
        run_unit["Run touched-surface unit tests"]
        run_e2e["Run phase e2e tests"]
        check_pills["Check pills were ingested before deletion"]
        check_board["Check task removed from board after closeout"]
        commit_if_green["Commit if required checks pass"]
        block_if_red["Block if checks fail"]
    end

    subgraph Boundary["Boundary rule"]
        rule["If action needs semantic judgment -> LLM task\nIf action is deterministic over known inputs -> automatic routine"]
    end

    ambiguous --> rule
    design --> rule
    code_change --> rule
    pill_ingest --> rule
    failure_triage --> rule

    rule --> run_unit
    rule --> run_e2e
    rule --> check_pills
    rule --> check_board
    rule --> commit_if_green
    rule --> block_if_red

    run_unit -->|fails| failure_triage
    run_e2e -->|fails| failure_triage
    check_pills -->|fails| pill_ingest
    block_if_red --> failure_triage
```

## Rule

- LLM tasks handle semantic judgment, ambiguity, design choices, implementation, and interpretation.
- Automatic routines handle deterministic checks and operations over known inputs.
- Automatic routines may block or return work to an LLM task, but they should not invent new semantic decisions.

## Examples

- `run touched unit tests after task`: automatic routine.
- `run e2e after phase`: automatic routine.
- `commit if tests pass`: automatic routine, once commit naming and branch rules are defined.
- `decide why a test failed`: LLM task.
- `decide whether a pill should become an atom or docs`: LLM task.
- `check that a pill has an ingestion target before deletion`: automatic routine.
