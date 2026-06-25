# Refactor primitives into AST-driven Task nodes

## Kind

architecture

## Status

open (blocked on sldb upstream)

## Problem

Currently, `deskops` generates a highly fragmented file structure for a single task. Creating a task spawns a `Routine`, multiple `Checklists`, `Conditions`, `Edges`, and `Operators` as separate Markdown files in `desk/primitives/` and `desk/routines/`. This destroys the "Locality of Behavior"—a human or agent cannot read a single task file and understand its complete lifecycle or execution state. Furthermore, conditions are limited to "dumb" string matching instead of real execution checks.

## Desired Outcome

Once the `sldb` core repository implements AST-driven templates, decoupled field instances, and native markdown hooks (as requested in their inbox), `deskops` must be refactored to consume this new architecture:

1. **Collapse the Primitive Directories**: Deprecate and remove `desk/primitives/` and `desk/routines/`.
2. **Refactor TaskDoc**: Update the `TaskDoc` model in `deskops/models/task.py` to embed Checklists, Conditions, and Operators as nested SLDB classes.
3. **AST-Native Markdown**: Update the task `__template__` so that checklists are represented as native Markdown task lists (`- [ ]`) and conditions/operators are represented as embedded executable hooks (e.g., `<!-- hook: pytest tests/ -->`).
4. **Rewrite the Execution Engine**: Modify `deskops/runtime/primitives.py` and `deskops operations.py` (`advance_task`) so that instead of loading external files, the engine parses the current Task's AST, evaluates the embedded hooks, mutates the local AST (checking boxes), and re-renders the single file.

## Questions

- How do we model multi-task routines or cross-task dependencies if the routine graph is collapsed into individual task files?
- What is the migration path for existing legacy workspaces that use fragmented primitives?
- How do we secure the execution of embedded Python/Bash hooks to prevent arbitrary code execution vulnerabilities during `deskops advance`?

## Related Atoms

- atom-primitives-encode-operational-rules
- atom-deskops-owns-workflow-not-document-infrastructure
