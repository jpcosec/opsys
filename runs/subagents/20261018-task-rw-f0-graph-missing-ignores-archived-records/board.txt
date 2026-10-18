---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-rw-f0-graph-missing-ignores-archived-records.md
- desk/tasks/task-rw-ci-tests-workflow-and-changelog.md
- desk/tasks/task-rw-f1-cli-contract-tests.md
- desk/tasks/task-rw-f1-output-golden-files.md
- desk/tasks/task-closeout-verify-tolerates-multi-document-yaml.md
- desk/tasks/task-message-tracks-notes-in-the-target-store-and-ack-resigns.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- `graph missing` stops failing on paths quoted in archived drawer records [draft] - `deskops graph missing --root .` exits 0 on the repo desk while a live issue with a dangling path still exits 1. With option A or C every document carrying the record marker is handled by one general rule (no per-file allowlist); with option B the three files no longer contain path-shaped references.
- CI runs pytest on every push, and the repo has a CHANGELOG [draft] - A GitHub Actions workflow runs `pytest tests` on push and pull request to main, and CHANGELOG.md records the changes since the last tag.
- Every CLI surface without a test gets one through main(argv) [draft] - Each listed subcommand has one in-process test that calls `deskops.cli.main.main([...])` inside a sandbox repo and asserts the exit code and one stable line of output.
- Golden files pin the graph snapshot, run index, closeout trailers and --help text [draft] - Tests compare those outputs, produced from a fixed fixture desk, against committed golden files with volatile values normalized.
- `closeout verify` does not abort on a multi-document YAML outside desk/ [draft] - `closeout verify` and the closeout gate of `advance` complete on a repo that contains a multi-document YAML anywhere, and judge evidence exactly as before for every other file.
- `message`/`inbox` track a note in the target repo's store, and `--ack` re-signs it [draft] - A delivered note is tracked in the store of the repo that owns the target desk (the `.sldb` next to the target `desk/`), or not tracked with a warning when that repo has no store; `--ack` updates the tracked note so `sldb stores check` passes afterwards in the target repo.
