# Workflow Questions

These questions capture the open manual gaps discovered while reading the repo. They are intentionally broad. No question here is considered superfluous until the workflow has a durable answer.

## Orientation

### What

- What is the minimal definition of `deskops` that every user and agent should read first?
- What is the exact boundary between `deskops`, `sldb`, `kgdb`, and `spec2viz`?
- What is a workflow surface, and which surfaces are active, deferred, durable, generated, or transient?
- What is the difference between an atom, pill, task, issue, feature, inbox note, ritual, routine, hook, gate, board, spec, doc, and diagram?
- What is the smallest set of concepts needed before a clean agent can use this repo safely?

### Why

- Why does this repo need atoms instead of only docs?
- Why does this repo need pills instead of only atoms or docs?
- Why does this repo need rituals before routines and hooks are implemented?
- Why should work be routed through a board instead of discovered from arbitrary files?
- Why should durable knowledge not stay inside tasks or pills?

### How

- How should a new user move from `README.md` to `desk/` to a first safe action?
- How should an agent decide whether to read docs, atoms, board, pills, rituals, graph, or specs first?
- How should a manual answer become part of the system instead of staying in conversation history?

## Atom Creation

### What

- What exactly qualifies as an atom candidate?
- What is not allowed to become an atom?
- What is the difference between an atom candidate, a draft atom, a curated atom, and an obsolete atom?
- What fields are required for an atom beyond `ID`, `5WH1+`, `Answer`, and tags?
- What does it mean for an atom to answer exactly one question?

### Why

- Why should atoms be grouped by domain folder instead of by explicit `domain` field?
- Why should atoms not own outgoing references to every consumer?
- Why should obsolete atoms be deleted instead of deprecated, retired, or versioned?

### Who

- Who is allowed to create atoms: human, primary agent, subagent, graph reflection routine, CLI command, or closeout hook?
- Who reviews whether an atom is durable enough?
- Who decides whether an atom should be split, merged, deleted, or rewritten?

### When

- When does a conversation produce an atom candidate?
- When does an inbox note produce an atom candidate?
- When does a task produce an atom candidate?
- When does a pill produce an atom candidate?
- When does a drift finding produce an atom candidate?
- When should atom creation be blocked because the evidence is weak?

### Where

- Where should atom candidates live before curation?
- Where should curated atoms live when more than one domain applies?
- Where should the source evidence for an atom be recorded, if atoms should not track all usage?

### How

- How is a new atom created from scratch?
- How is a new atom created from a pill during closeout?
- How is a new atom created from a graph finding?
- How is a new atom created from a diagram relation map?
- How does `deskops add atom` fit into the workflow?
- How should the system validate that an atom is small, stable, reusable, and one-question?
- How should tags be chosen and validated?

### How Not

- How do we prevent atoms from becoming copied doc prose?
- How do we prevent atoms from becoming task descriptions?
- How do we prevent atoms from becoming relation indexes?
- How do we prevent weak graph inference from creating false atoms?

## Atom Materialization Into Code, Docs, Specs, Tests, and Diagrams

### What

- What does it mean for docs to materialize atoms?
- What does it mean for specs to formalize atoms?
- What does it mean for tests to validate atoms?
- What does it mean for code to implement, respect, violate, or depend on atoms?
- What does it mean for diagrams to project atoms?

### Why

- Why should larger surfaces declare atom references instead of copying atom content?
- Why is atom-to-code not a simple composition relation?
- Why are generated diagrams projections rather than source truth?

### When

- When should adding an atom force a doc update?
- When should adding an atom force a spec update?
- When should adding an atom force a code change?
- When should adding an atom force a test update?
- When is an atom purely explanatory and not actionable?

### Where

- Where should atom references live: frontmatter, sections, sidecar indexes, graph edges, SLDB composition metadata, or all of these?
- Where should relation role metadata live?
- Where should materialization contracts live?
- Where should generated materialization manifests live?

### How

- How does a user ask, "what docs materialize this atom?"
- How does a user ask, "what code implements this atom?"
- How does a user ask, "what tests validate this atom?"
- How does a user ask, "what specs constrain this atom?"
- How does a user ask, "what diagrams project this atom?"
- How should a task use atoms to decide which files to inspect?
- How should a closeout ritual verify that changed code/docs/specs still match relevant atoms?

### How Not

- How do we avoid updating atoms when only a materialization is stale?
- How do we avoid updating code when the atom is actually stale?
- How do we avoid treating a low-confidence graph edge as proof of implementation?

## Drift and Synchronization

### What

- What counts as drift between atoms and docs?
- What counts as drift between atoms and specs?
- What counts as drift between atoms and code?
- What counts as drift between atoms and tests?
- What counts as drift between diagrams and their source?
- What is the difference between missing traceability and actual semantic drift?

### Why

- Why should drift findings be reviewable evidence before becoming tasks or atoms?
- Why should low-confidence findings never write atoms directly?

### When

- When should drift checks run: during closeout, on demand, in CI, before task execution, after phase completion, or during graph self-reflection?
- When does a drift finding become an active task?
- When does a drift finding become a drawer issue?
- When does a drift finding become only a question?

### Where

- Where should drift findings be stored?
- Where should dedupe keys and provenance be stored?
- Where should accepted/rejected drift findings be recorded?

### How

- How are atoms compared against docs/specs/code/tests?
- How does KGDB know which relations are declared versus inferred?
- How does SLDB expose enough metadata for drift checks?
- How does a drift check decide which side is stale?
- How should `violates` edges be produced and reviewed?
- How should drift checks avoid noise from generated files, test fixtures, or temporary desk artifacts?

## Atom Queries

### What

- What questions should the atom query system be able to answer?
- What is the canonical query surface: `sldb find`, `deskops graph`, KGDB traversal, `deskops atoms`, or another command?
- What is the difference between semantic search and graph traversal?

### Who

- Who are the query users: humans, primary agents, clean subagents, CI routines, closeout hooks, or self-reflection routines?

### When

- When should an agent query atoms before implementation?
- When should an agent query atoms during testing?
- When should an agent query atoms during closeout?

### Where

- Where do graph snapshots live?
- Where do query results belong when they become evidence?
- Where should query examples be documented?

### How

- How do I find all atoms related to a file?
- How do I find all files related to an atom?
- How do I find all tasks that used an atom?
- How do I find all pills that reference an atom?
- How do I find atoms without materializations?
- How do I find docs/specs/tests/code without atom links?
- How do I ask what the system thinks is missing?
- How should query results show provenance and confidence?

## Pills

### What

- What exactly qualifies as a pill?
- What is the difference between a pill and an atom?
- What is the difference between a pill and a task-local note?
- What is the difference between a pill and a ritual step?
- What is the difference between a pill and a spec constraint?

### Why

- Why do clean agents need pills if atoms and docs already exist?
- Why are pills temporary if they can contain important reasoning?
- Why should pills reference existing knowledge instead of copying it?

### Who

- Who creates pills?
- Who binds pills to tasks?
- Who audits pills after a task?
- Who decides whether a pill becomes an atom, doc update, spec update, or deletion?

### When

- When is a pill created during planning?
- When is a pill created during execution?
- When is a pill created from ambiguity review?
- When is a pill required before implementation may start?
- When is a pill stale?
- When is a pill safe to delete?

### Where

- Where should active pills live?
- Where should task-to-pill bindings live?
- Where should deleted pill history be discoverable?
- Where should pill ingestion decisions be recorded?

### How

- How does an agent choose relevant pills for a task?
- How does the board expose global pills?
- How does a task declare local pills?
- How does testing prove a pill's guardrail?
- How does closeout ingest pill residue?
- How does a routine check that no pill is deleted before ingestion?

### How Not

- How do we prevent pills from becoming permanent docs?
- How do we prevent pills from duplicating atoms/docs/specs?
- How do we prevent agents from ignoring generic-looking pills?

## Tasks, Boards, Rituals, Routines, Hooks, and Gates

### What

- What is the complete lifecycle of a task?
- What is the difference between task status and current routine node?
- What is a board-local phase?
- What is the difference between a ritual, routine, hook, gate, checklist, operator, condition, and edge?
- What is automatic and what requires LLM or human judgment?

### Why

- Why does every non-trivial task need explicit phase gates?
- Why does task closure require testing and a dedicated commit?
- Why should tasks disappear from active workspace after closure?

### When

- When is a drawer item promoted to task?
- When is a task initialized?
- When is a task ready for execution?
- When is a task ready for testing?
- When is a task ready for closeout?
- When is a task actually closed?

### Where

- Where should task candidates live?
- Where should active tasks live?
- Where should resolved task evidence live after the task file is deleted?
- Where should phase grouping live if phase is not its own document?

### How

- How does `deskops advance task` evaluate routine progress?
- How does the board compute or record phases?
- How do routines and hooks become derived from rituals?
- How does the close/test/commit hook decide whether it runs per task, per phase, or both?
- How does a clean subagent return an ambiguous task without partially executing it?

## Diagrams

### What

- What diagrams are canonical sources versus explanatory projections?
- What diagrams should exist to make the workflow manual complete?
- What is the relationship between Mermaid `.md`, `.mmd`, spec2viz YAML, and generated outputs?

### Why

- Why should workflow questions be expressed as diagrams before implementation?
- Why should diagrams declare source atoms or specs?

### When

- When does a question require a new diagram?
- When should an existing diagram be updated instead of creating a new one?
- When should a drawer diagram be promoted to `docs/diagrams/`?

### Where

- Where should temporary exploratory diagrams live?
- Where should durable workflow diagrams live?
- Where should diagram source metadata live?

### How

- How are diagrams integrated into SLDB, KGDB, and spec2viz?
- How does a diagram produce candidate atoms?
- How does a diagram participate in drift checks?
- How do we prevent generated diagrams from drifting from source diagrams?

## Promotion and Decision Questions

### What

- What are the promotion criteria from question to atom?
- What are the promotion criteria from question to task?
- What are the promotion criteria from question to doc/spec/diagram?
- What are the promotion criteria from question to ritual/routine/hook?

### Why

- Why should unresolved questions stay in drawer instead of active board?
- Why should promotion be explicit rather than implicit?

### When

- When is a question answered enough to close?
- When should a question remain open even after a partial answer exists?
- When should related questions be merged or split?

### Where

- Where should answer provenance be kept?
- Where should rejected answers be recorded?

### How

- How do we audit that every important question has either an answer or a destination?
- How do we stop this drawer from becoming a graveyard?
- How do we convert this question list into active tasks without losing the system-level view?

## Answered By Current Atoms

- What is the minimal definition of `deskops` that every user and agent should read first? -> `desk/atoms/atom-deskops.md`
- What is the exact boundary between `deskops`, `sldb`, `kgdb`, and `spec2viz`? -> `desk/atoms/workflow-model/atom-deskops-owns-workflow-not-document-infrastructure.md`, `desk/atoms/workflow-model/atom-kgdb-owns-relations-between-knowledge-surfaces.md`
- Why does this repo need atoms instead of only docs? -> `desk/atoms/workflow-model/atom-atoms-are-stable-documentation-core.md`
- Why does this repo need pills instead of only atoms or docs? -> `desk/atoms/workflow-model/atom-pills-index-existing-and-bound-future-context.md`, `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md`
- Why does this repo need rituals before routines and hooks are implemented? -> `desk/atoms/workflow-model/atom-rituals-precede-routines.md`
- Why should durable knowledge not stay inside tasks or pills? -> `desk/atoms/workflow-model/atom-pills-end-as-atoms-docs-or-deletion.md`, `desk/atoms/workflow-model/atom-unwritten-knowledge-belongs-in-atoms-or-materializations.md`
- How should a manual answer become part of the system instead of staying in conversation history? -> `desk/atoms/workflow-model/atom-unwritten-knowledge-belongs-in-atoms-or-materializations.md`
- What does it mean for an atom to answer exactly one question? -> `desk/atoms/workflow-model/atom-atoms-answer-one-question.md`
- Why should atoms not own outgoing references to every consumer? -> `desk/atoms/workflow-model/atom-atoms-answer-one-question.md`, `desk/atoms/workflow-model/atom-documents-point-to-atoms.md`
- What does it mean for docs to materialize atoms? -> `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- Why should larger surfaces declare atom references instead of copying atom content? -> `desk/atoms/workflow-model/atom-documents-point-to-atoms.md`
- Where should atom references live: frontmatter, sections, sidecar indexes, graph edges, SLDB composition metadata, or all of these? -> `desk/atoms/workflow-model/atom-documents-point-to-atoms.md`, `desk/atoms/workflow-model/atom-repo-artifacts-need-atom-traceability.md`, `desk/atoms/workflow-model/atom-kgdb-owns-relations-between-knowledge-surfaces.md`
- How should a closeout ritual verify that changed code/docs/specs still match relevant atoms? -> `desk/atoms/workflow-model/atom-closeout-validates-knowledge-surfaces.md`
- How do we prevent pills from duplicating atoms/docs/specs? -> `desk/atoms/workflow-model/atom-pills-reference-not-copy.md`
- What is the difference between task status and current routine node? -> `desk/atoms/workflow-model/atom-routine-based-task-execution.md`
- What is a board-local phase? -> `desk/atoms/workflow-model/atom-task-board-phases.md`
- What is automatic and what requires LLM or human judgment? -> `desk/atoms/workflow-model/atom-automatic-routines-vs-llm-tasks.md`
- Why does every non-trivial task need explicit phase gates? -> `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`
- Why does task closure require testing and a dedicated commit? -> `desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md`
- When is a task actually closed? -> `desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md`
- Where should phase grouping live if phase is not its own document? -> `desk/atoms/workflow-model/atom-task-board-phases.md`
- How does a clean subagent return an ambiguous task without partially executing it? -> `desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md`
- What diagrams are canonical sources versus explanatory projections? -> `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- Why are generated diagrams projections rather than source truth? -> `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- How does a diagram produce candidate atoms? -> `desk/atoms/workflow-model/atom-diagrams-generate-operational-models.md`
- Why should unresolved questions stay in drawer instead of active board? -> `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`
- Why should promotion be explicit rather than implicit? -> `desk/atoms/workflow-model/atom-drawers-feed-tasks-through-promotion.md`
