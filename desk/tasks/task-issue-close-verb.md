---
id: task-issue-close-verb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/issues.py
- deskops/cli/commands/issue.py
- deskops/cli/registry.py
- tests/test_issue_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops issue close` closes an issue with its reason and keeps the file as the trace

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18 the coordinator asked every agent to bring its desk to zero through the deskops CLI only, without editing desk/ by hand. Issues have no verb. sldb-04 has three resolved issues in sldb/desk/issues/ it cannot close: their format is `ID:`/`Status:` lines with no frontmatter, and `edit`, `drawer remove` and `message ack` do not take them. deskops itself has 24 open issues in desk/drawer/issues/ using a `## Status` section. `drawer remove` deletes the entry, which loses the trace.

## Goal

_Describe the concrete result this task must produce._

`deskops issue close <selector> --reason <text> [--ref <commit-or-path> ...] --root <repo>` finds the issue under desk/issues/ or desk/drawer/issues/, sets its status to closed, appends a resolution with the date, reason and refs, keeps the file, refreshes its store record if it is tracked, and prints the path. `deskops issue list --root <repo> [--status open|closed|all]` lists issues with id, status and title.

## Scope

_State what is in scope and what is out of scope._

In scope: a new `issue` command family (close, list) registered like the other commands (deskops/cli/registry.py and a module under deskops/cli/commands/), a small service (deskops/services/issues.py) that handles the three status formats seen in practice: a YAML frontmatter `status:` key, a `## Status` section whose body is the status word, and a `Status: <word>` line near the top. The resolution is appended as a `## Resolution` section, with lines `Closed: <YYYY-MM-DD>`, `Reason: <text>` and `Refs: <comma list>`. Selector resolution goes through deskops/desk_paths.py. An issue with no recognizable status raises a typed DomainError naming the file. Out of scope: creating issues, and moving or deleting files.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. deskops/services/issues.py: find_issue(root, selector), issue_status(text), close_issue(path, reason, refs, today), list_issues(root, status). 2. deskops/cli/commands/issue.py plus a registry entry; follow how drawer.py is wired and how errors and render are used. 3. If the file is tracked in .sldb (sldb.api doc_status), re-track it after the write through deskops/doc_io.py, as other commands do. 4. Tests in tests/test_issue_cli.py: one fixture per format (frontmatter, `## Status` section, `Status:` line), close then list; refusal on an already-closed issue (exit 1, unless --force); unknown selector exits 1; the file still exists and the text above the resolution is unchanged. 5. Help text with an example; add the command to the CLI help golden if tests/test_output_goldens.py or tests/fixtures/golden requires it, and run the golden test.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_issue_cli.py tests/test_output_goldens.py tests/test_cli_contract.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

All three formats close and list correctly in tests, goldens are updated deliberately if needed, and `pytest tests` is green.
