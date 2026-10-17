# e2e: inbox-to-task (deepseek/deepseek-flash)

- works (harness checks): yes
- docs ok (agent got there from the docs): yes
- cost $0.0077, 58.5s, 21 tool calls, 0 failed, 5 --help, 0 source reads

## Checks

- [x] the note was deferred into the drawer
- [x] an open task about the release process exists
- [x] the local store passes sldb stores check

## Agent

Promoted the inbox note 'Document the release process' into a drawer candidate, then authored it as the open task task-document-the-release-process (validation: pytest, from_drawer recorded, routed on Board.md).

## Friction

- **minor** (missing discovery surface) .opencode/skills/use-deskops/SKILL.md § Mandatory read route: The required first-read files AGENTS.md, README.md and docs/faq.md do not exist in this repo, so the prescribed state-recovery route cannot be followed literally. — Used CLI help (deskops --help, faq, per-command --help) and the files under desk/ instead.
- **minor** (hidden state dependency) CLI output (deskops promote inbox-to-drawer-task) § promote output: Promotion printed "Warning: could not untrack 'inbox-note-document-the-release-process' from the store: Doc 'inbox-note-document-the-release-process' not found', even though the inbox note file existed; the note was never tracked in the .sldb store. — Ignored the warning; promotion still succeeded and the source file was deleted.
- **minor** (misleading help) deskops promote --help § inbox-to-drawer-task: Help says it promotes an inbox note into a drawer candidate but does not state that the source inbox note file is deleted as a side effect. — Observed actual behavior (source file deleted) and proceeded.
- **minor** (missing discovery surface) deskops list --help § subcommands: There is no CLI surface to list or inspect deferred drawer candidates (no 'list drawer(s)'/'drawer' subcommand), so drawer work can only be discovered by reading the filesystem. — Inspected desk/drawer/tasks/ directly.
- **minor** (naming mismatch) task instruction vs CLI § deskops add task output: The requested end state 'leave the task open' has no literal 'open' status; the CLI creates the task as 'draft' and the drawer file is kept for manual cleanup by design. — Left the task at non-closed status 'draft' and kept the drawer file (CLI default) rather than guessing a cleanup policy.

## Failed commands

- none

## Source reads (docs were not enough)

- none
