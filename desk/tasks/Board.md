# Desk Board

ID: board-001
Scope: desk

## Purpose

Route the active desk execution set: tasks, pills, and the ritual documents that govern execution and closure.

## Tasks

- desk/tasks/task-021-operate-over-sldb-desk-tasks.md
- desk/tasks/task-022-stabilize-cli-first-use-entrypoints.md
- desk/tasks/task-023-align-first-use-docs-with-deskops.md
- desk/tasks/task-024-make-desk-install-match-documented-structure.md
- desk/tasks/task-025-cover-cli-surfaces-with-tests.md


## Pills

- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-002-test-real-cli-surfaces.md
- desk/contexts/pill-003-capture-cli-gaps.md
- desk/contexts/pill-004-opsys-boundary.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-006-self-described-store-layout.md
- desk/contexts/pill-007-phase-gated-task-flow.md

## Rituals

- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md

## Notes

Every closed task must end in its own closing commit. Every non-trivial task must pass explicit initialization, execution, testing, and closeout gates. Any missing SLDB capability discovered during execution must become a new active desk task.

Current readiness sweep split the first-use gaps into explicit tasks: CLI entry surface correctness first, docs alignment second, scaffold contract third, and CLI regression tests after the public behavior stabilizes.

## Task Details

- Enable opsys operation over repo-local sldb desk tasks [active] - Make the opsys layer able to discover, route, and operate over repo-local `desk/tasks` surfaces in sibling repos so backlog state does not have to be duplicated across `issues`, `inbox`, and manual handoff notes.
- Stabilize CLI first-use entrypoints [active] - Make the package install and first-use CLI entry surface work predictably in a clean environment.
- Align first-use docs with deskops [planned] - Make the repo documentation describe this package's real install and usage paths instead of inherited `sldb` guidance.
- Make desk install match documented structure [planned] - Make `desk install` produce a coherent desk surface that matches the repo's documented structure and fails safely when prerequisites are missing.
- Cover CLI surfaces with tests [planned] - Add targeted tests for the real CLI surfaces so first-use regressions are caught automatically.

## Tags

- system:sldb
- workspace:desk
- topic:routing
