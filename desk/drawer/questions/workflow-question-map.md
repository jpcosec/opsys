# Workflow Question Map

This diagram captures the current hypothesis for what connects to what. Edges marked with question labels are places where the workflow still needs explicit answers.

Existing diagrams that partially cover this map:

- `docs/diagrams/workflow/workflow-model.md`
- `docs/diagrams/tasks/task-accumulation-initialization-resolution.md`
- `docs/diagrams/tasks/task-board-phases.md`
- `docs/diagrams/atoms/atoms-workflow.md`
- `docs/diagrams/atoms/pills-workflow.md`
- `docs/diagrams/codebase/codebase-document-relation-map.md`
- `docs/diagrams/codebase/codebase-knowledge-surfaces.md`
- `docs/diagrams/process/rituals-routines-hooks-workflow.md`
- `docs/diagrams/process/llm-tasks-vs-automatic-routines.md`
- `docs/diagrams/intake/intake-drawers-workflow.md`

```mermaid
flowchart TB
    subgraph Intake["Intake and deferred work"]
        inbox["Inbox\nexternal questions, bugs, requirements"]
        drawer["Drawer\ndeferred ideas, issues, features, questions"]
        questions["Questions drawer\nunclear workflow/model questions"]
    end

    subgraph Knowledge["Durable knowledge"]
        atoms["Atoms\none 5WH1+ answer each"]
        docs["Docs\nhuman materializations"]
        specs["Specs\ncontracts and schemas"]
        diagrams["Diagrams\nvisual projections"]
    end

    subgraph ActiveWork["Active work"]
        board["Board\nroutes active tasks, pills, rituals"]
        tasks["Tasks\nactive executable work units"]
        pills["Pills\ntransient bounded context"]
        rituals["Rituals\ntextual process"]
        routines["Routines/hooks/gates\nstructured or automatic process"]
    end

    subgraph Execution["Execution and feedback"]
        agent["Clean subagent\nsemantic judgment and edits"]
        code["Code"]
        tests["Tests"]
        git["Git history"]
        graph["Knowledge graph\nqueries and drift checks"]
    end

    inbox -->|triage?| drawer
    inbox -->|active now?| tasks
    drawer -->|promote when actionable?| tasks
    drawer -->|knowledge gap?| questions
    questions -->|answer durable?| atoms
    questions -->|answer operational?| rituals
    questions -->|answer requires work?| tasks
    questions -->|answer visual?| diagrams

    atoms -->|materialize?| docs
    atoms -->|formalize?| specs
    atoms -->|project?| diagrams
    docs -->|declare source atoms?| atoms
    specs -->|declare source atoms?| atoms
    diagrams -->|declare source atoms/specs?| atoms

    board -->|routes| tasks
    board -->|exposes| pills
    board -->|binds process| rituals
    tasks -->|requires bounded context| pills
    tasks -->|uses process| rituals
    rituals -->|decompose when stable?| routines
    routines -->|advance/check/block?| tasks
    routines -->|audit/delete?| pills

    tasks -->|assigned to| agent
    pills -->|bound context for| agent
    rituals -->|process for| agent
    agent -->|edits| code
    agent -->|edits| docs
    agent -->|edits| specs
    agent -->|adds/updates| tests
    code -->|validated by| tests
    tests -->|evidence in| git
    docs -->|committed in| git
    specs -->|committed in| git
    code -->|committed in| git

    pills -->|ingest durable residue?| atoms
    pills -->|ingest explanatory residue?| docs
    pills -->|delete when unused?| git

    graph -->|answers where does atom touch?| atoms
    graph -->|detects missing links?| questions
    graph -->|detects drift?| tasks
    graph -->|reads relations from?| docs
    graph -->|reads relations from?| specs
    graph -->|reads relations from?| code
    graph -->|reads validation from?| tests
```

## Related Atoms

Current workflow atom base represented by this question map:

- atom-atoms-are-stable-documentation-core
- atom-changes-flow-through-tasks-and-pills
- atom-clean-code-reduces-knowledge-drift
- atom-cli-should-match-spoken-workflow-language
- atom-code-changes-close-with-tests-and-commit
- atom-deskops-automates-repeated-workflow-obligations
- atom-docs-are-human-facing-atom-materializations
- atom-drawers-feed-tasks-through-promotion
- atom-every-change-needs-descriptive-commit
- atom-git-history-is-the-past
- atom-inbox-routes-external-needs-toward-work
- atom-kgdb-owns-relations-between-knowledge-surfaces
- atom-orphan-artifacts-are-knowledge-system-failures
- atom-pills-end-as-atoms-docs-or-deletion
- atom-pills-index-existing-and-bound-future-context
- atom-repo-artifacts-need-atom-traceability
- atom-tasks-enable-zero-context-subagents
- atom-unwritten-knowledge-belongs-in-atoms-or-materializations

## Diagram Questions

- Which arrows are authoritative workflow rules, and which are only current hypotheses?
- Which arrows must be represented as graph edges?
- Which arrows are SLDB composition relations, KGDB graph relations, or plain Markdown links?
- Which arrows should become automatic routines or hooks?
- Which arrows require human or LLM semantic judgment?
- Which existing diagrams are source diagrams, and which are derived explanations?
- Should this drawer map become a durable diagram under `docs/diagrams/workflow/` once resolved?
