---
kind: suggestion
author: opencode
created_at: 2026-06-07T00:00:00
status: open
---

# Pill Type Taxonomy

Pills are compact context capsules that let a fresh subagent execute a task without inherited chat context, whole-repo rereads, or scope drift.

Useful pill types:

- ADR Pill: captures a decision, why it was made, alternatives rejected, and what future agents must preserve.
- Pattern Pill: describes a reusable way to solve a recurring problem.
- Anti-Pattern Pill: describes a tempting wrong approach and how to recognize or avoid it.
- How-To Pill: gives step-by-step execution instructions for a recurring operation.
- How-Not-To Pill: focuses on constraints, traps, and forbidden shortcuts.
- Boundary Pill: defines ownership, which module or tool owns what, and what must not cross the boundary.
- Contract Pill: defines an interface, schema, command behavior, output shape, or validation expectation.
- Validation Pill: explains how to prove a class of tasks is done, including commands and expected outputs.
- Dispatch Pill: tells a zero-context subagent what to read, what not to read, and how to stay scoped.
- Architecture Pill: captures structural rules, dependency direction, layer constraints, or module relationships.
- Lifecycle Pill: defines how to open, advance, test, close, or delete tasks and artifacts.
- Context-Routing Pill: explains which local docs, pills, boards, or standards must be read for a task family.
- Domain Concept Pill: explains a key concept briefly enough that an agent does not need to reread long docs.
- Glossary Pill: defines overloaded terms so agents do not confuse names such as atom, task, artifact, or graph.
- Failure-Mode Pill: captures known regressions, symptoms, root causes, and what to check before claiming completion.
- Migration Pill: explains an active transition, including old surface, new surface, compatibility stance, and deletion rules.
- Tooling Pill: documents how to use a local tool or command safely.
- Test Fixture Pill: explains canonical fixtures, golden files, and what changes are intentional versus drift.

A good pill should answer:

- What context does a fresh agent need?
- When does this pill apply?
- What files or surfaces own the behavior?
- What must the agent read?
- What must the agent not do?
- How is correctness validated?
- What are the drift signals?
