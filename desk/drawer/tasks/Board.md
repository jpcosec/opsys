# Drawer Board

This board routes deferred work only.

## Remaining

- `tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md` — waiting for the coordinated deploy of the whole suite; no tag until then.

## Retired

The covered use-cases, stress-tests (the CI gap closed by task-test-ci-knowledge-integrity-flow, which added scripts/ci-knowledge-check.sh and tests/test_ci_integration.py), findings archive, answered questions, drawer rituals, attention review, and obsolete feature outlines were retired on 2026-10-19. The runtime-and-launcher feature and the tmux launcher task were retired the same day by the coordinator's decision: `deskops runtime supervise` plus the external harness (Herdr) cover what the tmux launcher would have done. Each retirement commit names the test or replacement that covers it, and git history is the durable record.

## Rule

Promote work from `desk/drawer/` into the active surfaces of `desk/` before implementation starts.
