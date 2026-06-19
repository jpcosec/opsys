# Inbox, Drawers, Features, and Issues Workflow

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

This workflow covers coordination and deferred work. It is separate from active task execution.

```mermaid
flowchart TB
    subgraph External["External coordination"]
        project_a["Project A"]
        project_b["Project B desk"]
        inbox["Project B inbox\nrequirements / questions / bugs"]
    end

    subgraph Triage["Triage"]
        classify["Classify message"]
        requirement["Requirement"]
        question["Question"]
        bug["Bug / problem report"]
    end

    subgraph Holding["Deferred holding"]
        drawers["Drawers\nholding area before active work"]
        feature["Feature\nfuture work, less structured"]
        issue["Issue\ndrawers/issues\nloose problem detection"]
    end

    subgraph Promotion["Promotion paths"]
        task_candidate["Task candidate\nwhen active work is needed"]
        atom_gap["Atom/doc gap\nwhen durable knowledge is missing"]
        response["Response / clarification\nback to external project"]
    end

    project_a -->|writes to| inbox
    inbox --> classify
    classify --> requirement
    classify --> question
    classify --> bug
    requirement --> drawers
    requirement --> feature
    question --> response
    question --> atom_gap
    bug --> issue
    issue --> task_candidate
    feature --> task_candidate
    atom_gap --> task_candidate
    project_b --> inbox
```

## Rules

- Inbox is for coordination between projects.
- A project can write requirements, questions, or bugs into another project's inbox.
- Drawers hold things until they become active work.
- Features are future work and can be less structured than tasks.
- Issues live under `drawers/issues` and can be loosely structured detections of problems.
- Promotion to task happens only when work becomes active.
