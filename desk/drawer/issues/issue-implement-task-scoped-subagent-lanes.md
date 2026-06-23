# Implement task-scoped subagent lanes

## Kind

feature

## Status

open

## Problem

When agents are left to run free, they tend to expand across unrelated work or drift out of the intended task boundary. There is no formalized "sandbox" or "lane" for an executor subagent to run safely, persist its traces, and be reviewed by a supervisor without mixing context with other tasks.

## Desired Outcome

Adopt task-scoped execution environments (e.g., using `tmux` sessions or isolated run directories) as an external orchestration layer. 
- Execution runs should happen in a dedicated directory (e.g., `runs/tmux-subagents/[timestamp]-[task-name]/`).
- The run should output specific traces (`task-context.md`, `result-summary.md`) to prove completion.
- The orchestration layer must remain strictly external and not leak into the project's runtime code.

## Questions

- Should `deskops` ship with native lightweight subagent runner scripts (like `scripts/launch_deskops_tmux_subagent.sh`)?
- How does `deskops` ingest the `result-summary.md` to update the board automatically?
- What are the required artifacts for a subagent trace to be considered valid for closeout?

## Follow-Up Shape

- Add subagent runner scripts or native deskops commands (`deskops subagent launch <task>`).
- Define the directory structure for `runs/` in the standard desk scaffold.
- Document the boundary ensuring `tmux`/orchestration tools do not become runtime dependencies.

## Related Atoms

- atom-tasks-enable-zero-context-subagents
- atom-cli-mutation-testing-uses-sandbox-desk-roots
