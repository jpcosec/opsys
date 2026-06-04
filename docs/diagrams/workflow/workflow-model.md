# Deskops Workflow Model

This is the semantic workflow model as currently understood. It intentionally avoids infrastructure details and focuses on what each artifact does in the operating system.

```mermaid
flowchart TB
    principle["Core principle\ndivide and conquer + persisted operations\nsmall units reduce LLM drift"]

    subgraph Knowledge["Knowledge base"]
        atoms["Atoms\ndesk/atoms\nminimum structured knowledge unit\nhierarchical by design domain"]
        specs["Specs\nmaterialized from atoms"]
        docs["Documentation\nmaterialized from atoms"]
    end

    subgraph Deferred["Deferred / not active yet"]
        drawers["Drawers\nholding area before active work"]
        features["Features\nfuture work\nless structured than tasks"]
        issues["Issues\ndrawers/issues\nlooser problem detections"]
    end

    subgraph Coordination["Cross-project coordination"]
        inbox["Inbox\nexternal requirements, questions, bugs\nfrom other projects"]
    end

    subgraph Active["Active work"]
        boards["Boards\nfolder indexes\nfor tasks: stack/heap routing"]
        tasks["Tasks\nserializable active work units\ntracked in git"]
    end

    subgraph Context["Execution context"]
        pills["Context pills\ntransient agent context\nreferences atoms/code/docs\nor captures patterns"]
    end

    subgraph Process["Operating process"]
        rituals["Rituals\ncurrent textual process docs\nused around task work/testing/pills"]
        routines["Routines\ntarget decomposition\nstateful ways of working"]
        hooks["Hooks\ntarget decomposition\nrun before specific operations"]
    end

    subgraph AgentWork["Clean-agent execution"]
        subagent["Clean subagent\nexecutes one small task\nwith bounded context"]
        code["Code / tests / docs changes"]
        git["Git history\nobservable changes, closure, errors"]
    end

    principle --> atoms
    principle --> rituals
    principle --> tasks

    atoms -->|materialize| specs
    atoms -->|materialize| docs
    atoms -->|referenced by| pills
    atoms -->|referenced by| features

    drawers --> features
    drawers --> issues
    features -->|promoted when active| tasks
    issues -->|promoted when actionable| tasks
    issues -->|may clarify into| atoms

    inbox -->|triage| drawers
    inbox -->|triage| tasks
    inbox -->|may reveal knowledge gap| atoms

    boards -->|index and route| tasks
    tasks -->|requires context| pills
    tasks -->|uses process| rituals
    rituals -->|should decompose into| routines
    rituals -->|should decompose into| hooks
    routines -->|govern progression of| tasks
    hooks -->|run around operations on| tasks
    hooks -->|run around operations on| pills

    tasks -->|assigned to| subagent
    pills -->|bound context for| subagent
    subagent --> code
    code --> git
    tasks -->|state/changes visible in| git

    pills -->|before deletion ingest into| atoms
    pills -->|before deletion ingest into| docs
    pills -->|then delete when unused| git
```

## Definitions

- `Atoms`: minimum structured knowledge units. They live in `desk/atoms`, ordered hierarchically by design domain. Specs and documentation should be materializations of atoms.
- `Tasks`: persistent units for active work. They are organized by boards and tracked in git so changes, completion, and error introduction are observable.
- `Context pills`: transient context for clean subagents. They must be ingested into atoms, documentation, or both before deletion.
- `Features`: less-structured future work kept in drawers until it is promoted to active work.
- `Issues`: loosely structured problem detections under `drawers/issues`.
- `Inbox`: cross-project coordination surface for requirements, questions, and bugs from external projects.
- `Boards`: indexes for folders. For `tasks`, a board acts as routing structure, stack, or heap for ordering active work.
- `Rituals`: current textual descriptions of operating process. They should eventually be decomposed into routines and hooks.
- `Routines`: target representation for stateful ways of working.
- `Hooks`: target representation for process fragments that run before or around specific operations.

## Constraints

- Avoid duplicated writing: duplicate prose opens space for language-agent error.
- Prefer small persisted units: they support divide and conquer and make git history meaningful.
- A task should be executable by a clean subagent with no room for improvisation beyond the bounded context.
- Pills are not durable knowledge. Their durable residue must be absorbed into atoms or documentation before removal.
