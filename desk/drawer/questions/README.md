# Questions Drawer

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-unwritten-knowledge-belongs-in-atoms-or-materializations.md`
- `desk/atoms/workflow-model/atom-atom-candidates-come-from-durable-answers.md`
- `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`

`desk/drawer/questions/` holds unresolved workflow questions that are not active tasks yet.

Use this drawer when a concept, connection, flow, diagram, or 5WH1+ answer is unclear enough that promoting it directly into an atom, task, spec, ritual, or implementation would create drift.

## Purpose

- Capture all questions discovered while reconstructing the deskops workflow manual.
- Preserve questions before they become tasks, atoms, diagrams, specs, or docs.
- Use 5WH1+ to expose missing definitions, missing flow boundaries, and missing query surfaces.
- Identify which existing diagrams already answer a question and which diagrams are missing.

## Files

- `workflow-questions.md` - open questions grouped by surface and 5WH1+.
- `workflow-question-map.md` - diagram of the currently suspected connections and unresolved edges.

## Promotion Rule

A question leaves this drawer only when it is promoted into one of these surfaces:

- an atom, when the answer is durable one-question knowledge
- a doc/spec/diagram update, when the answer explains or formalizes a larger surface
- a task, when the answer requires implementation or migration work
- a ritual/routine/hook, when the answer changes operational process
- an inbox note, when the answer depends on another repo or tool owner

Do not delete a question just because it feels obvious after discussion. Delete or archive it only after the answer is represented in a durable surface or intentionally rejected.

---

## Merged: `workflow-questions.md`

# Workflow Questions

This file now tracks only unresolved workflow questions. Questions with stable answers have been moved into atoms or mapped to existing atoms.

## Related Atoms

- atom-deskops
- atom-deskops-owns-workflow-not-document-infrastructure
- atom-workflow-surfaces-have-operational-lifetimes
- atom-workflow-vocabulary-separates-knowledge-and-work
- atom-clean-agents-start-from-minimum-workflow-set
- atom-first-safe-action-follows-read-route
- atom-agents-read-by-decision-need
- atom-work-is-board-routed-to-preserve-intent
- atom-atoms-are-stable-documentation-core
- atom-atom-candidates-come-from-durable-answers
- atom-non-durable-notes-do-not-become-atoms
- atom-documents-point-to-atoms
- atom-repo-artifacts-need-atom-traceability
- atom-orphan-artifacts-are-knowledge-system-failures
- atom-kgdb-owns-relations-between-knowledge-surfaces
- atom-drawers-feed-tasks-through-promotion
- atom-inbox-routes-external-needs-toward-work
- atom-changes-flow-through-tasks-and-pills
- atom-pills-index-existing-and-bound-future-context
- atom-code-changes-close-with-tests-and-commit

## Answered Questions Moved To Atoms

### Orientation

- What is `deskops`? -> `atom-deskops`, `atom-deskops-owns-workflow-not-document-infrastructure`
- What are active, deferred, durable, generated, and transient surfaces? -> `atom-workflow-surfaces-have-operational-lifetimes`
- What is the minimum safe concept set for a clean agent? -> `atom-clean-agents-start-from-minimum-workflow-set`
- How should a new user begin? -> `atom-first-safe-action-follows-read-route`
- How should an agent choose between board, pills, atoms, docs, specs, graph, and rituals? -> `atom-agents-read-by-decision-need`
- Why should work be board-routed? -> `atom-work-is-board-routed-to-preserve-intent`, `atom-available-tasks-are-board-routed-work`

### Knowledge Core

- Why atoms instead of only docs? -> `atom-atoms-are-stable-documentation-core`, `atom-atoms-distill-project-knowledge`
- What qualifies as an atom candidate? -> `atom-atom-candidates-come-from-durable-answers`
- What does not become an atom? -> `atom-non-durable-notes-do-not-become-atoms`
- What does it mean for an atom to answer one question? -> `atom-atoms-answer-one-question`
- How do docs/specs/diagrams relate to atoms? -> `atom-docs-are-human-facing-atom-materializations`, `atom-specs-formalize-atoms-as-contracts`, `atom-diagrams-project-knowledge-relations`
- Why do documents point to atoms instead of atoms tracking every use site? -> `atom-documents-point-to-atoms`, `atom-reverse-traceability-is-derived`

### Graph And Traceability

- How do repo artifacts connect to atoms? -> `atom-repo-artifacts-need-atom-traceability`, `atom-knowledge-graph-connects-desk-and-source-files`
- Why are orphan artifacts failures? -> `atom-orphan-artifacts-are-knowledge-system-failures`
- What owns relations? -> `atom-kgdb-owns-relations-between-knowledge-surfaces`, `atom-kgdb-should-parallel-sldb-not-compete`
- What does SLDB provide? -> `atom-sldb-is-read-write-edit-surface`, `atom-sldb-semantics-are-graph-inputs`
- What does KGDB provide? -> `atom-kgdb-is-graph-substrate-not-reasoner`, `atom-networkx-is-first-graph-runtime`

### Work Flow

- How do drawers become tasks? -> `atom-drawers-feed-tasks-through-promotion`, `atom-drawer-is-not-active-work`
- How do project-addressed messages enter the system? -> `atom-inbox-routes-external-needs-toward-work`, `atom-inbox-is-coordination-intake`
- Why tasks plus pills? -> `atom-changes-flow-through-tasks-and-pills`, `atom-tasks-enable-zero-context-subagents`
- What do pills do? -> `atom-pills-index-existing-and-bound-future-context`, `atom-pills-are-transient`, `atom-pills-reference-not-copy`, `atom-pills-end-as-atoms-docs-or-deletion`
- Why phase gates? -> `atom-phase-gates-prevent-agent-skipping`
- What closes code work? -> `atom-code-changes-close-with-tests-and-commit`, `atom-every-change-needs-descriptive-commit`
- Where does past work live? -> `atom-git-history-is-the-past`, `atom-git-is-explanatory-surface-for-changes`

### Automation And Quality

- Why strict clean code? -> `atom-clean-code-reduces-knowledge-drift`
- Why automate repeated obligations? -> `atom-deskops-automates-repeated-workflow-obligations`
- How should CLI language feel? -> `atom-cli-should-match-spoken-workflow-language`, `atom-cli-is-thin-over-primitives-and-sldb`
- What is automatic vs LLM work? -> `atom-automatic-routines-vs-llm-tasks`
- How do rituals relate to routines/hooks? -> `atom-rituals-precede-routines`, `atom-routine-based-task-execution`

## Deferred Question Groups

### Atom Authority

- Who may create atoms: human, primary agent, subagent, graph reflection routine, CLI command, or closeout hook?
- Who reviews whether an atom is durable enough?
- Who decides whether an atom should be split, merged, deleted, or rewritten?
- How should multi-domain atoms be placed when more than one domain applies?

### Atom Lifecycle Mechanics

- How is a new atom created from scratch through CLI and SLDB?
- How is a new atom created from a pill during closeout?
- How is a new atom created from a graph finding?
- How is a new atom created from a diagram relation map?
- How should the system validate that an atom is small, stable, reusable, and one-question?
- How should tag namespaces be chosen, validated, and repaired?

### Materialization Mechanics

- Where should atom references live for each artifact family: frontmatter, sections, sidecar indexes, graph edges, SLDB composition metadata, or a combination?
- Where should materialization contracts and generated materialization manifests live?
- How should a task use atoms to decide which files to inspect?
- How should closeout verify that changed code/docs/specs still match relevant atoms?

### Drift And Synchronization Mechanics

- When should drift checks run: closeout, on demand, CI, before execution, after phase completion, or graph self-reflection?
- Where should drift findings, dedupe keys, accepted decisions, rejected decisions, and provenance be stored?
- How does a drift check decide whether the atom, materialization, test, diagram, or implementation is stale?
- How should `violates` edges be produced, reviewed, and promoted?
- How should drift checks avoid noise from generated files, fixtures, and temporary desk artifacts?

### Atom Query UX

- What is the canonical user-facing query surface: `sldb find`, `deskops graph`, KGDB traversal, future `deskops atoms`, or a layered combination?
- Where do query results belong when they become evidence?
- Where should query examples be documented?
- How should query results expose provenance, confidence, declared vs inferred relations, and next actions?

### Pill Responsibility

- Who creates pills?
- Who binds pills to tasks?
- Who audits pills after a task?
- Who decides whether a pill becomes an atom, doc update, spec update, or deletion?
- Where should deleted pill history be discoverable beyond git history?

### Task And Routine Semantics

- What exact state means initialized, ready for execution, ready for testing, ready for closeout, and closed?
- How does `deskops advance task` evaluate routine progress?
- How does the board compute or record phases?
- How does the close/test/commit hook decide whether it runs per task, per phase, or both?

### Diagram Operations

- Which diagrams are canonical sources and which are explanatory projections?
- When does a question require a new diagram versus an update to an existing diagram?
- When should a drawer diagram be promoted to `docs/diagrams/`?
- How are diagrams integrated into SLDB, KGDB, and spec2viz without drift?

### Question Drawer Governance

- When is a question answered enough to close?
- When should a question remain open after a partial answer exists?
- When should related questions be merged or split?
- Where should rejected answers be recorded?
- How do we prevent this drawer from becoming a graveyard?

---

## Merged: `workflow-question-map.md`

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
