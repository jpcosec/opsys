# Inject code files and atoms into subagent task context

## Issue

While the task model supports `files`, `pills`, and `references`, the process of assembling the required context for zero-context subagents is manual and lacks explicit enforcement for atoms. A task should robustly declare not just the transient context (pills) but also the exact source files (code) to touch and the durable architectural rules (atoms) that apply.

## Core Need

Formalize how code files and atoms are injected into a subagent's task context. Update the CLI (e.g. `deskops add task` and edit commands) to easily attach these dependencies so subagents can mechanically resolve their reading set before starting the ambiguity review.

## Constraints

- Subagents must not fall back to searching the whole codebase.
- Injected contexts should validate against KGDB (no broken file or atom references).
- Should build upon existing SLDB models (`TaskDoc`'s `files`, `pills`, and `references`).

## Follow-Up Shape

- Modify `deskops add task` and models to explicitly support and validate `--file`, `--pill`, and `--atom` flags.
- Document the zero-context subagent reading routine in an atom or ritual.

## Tags

- system:deskops
- topic:agents
- topic:subagents
- topic:tasks
- topic:context
