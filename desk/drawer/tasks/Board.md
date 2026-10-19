# Drawer Board

This board routes deferred work only.

## Remaining

- `features/feature-runtime-and-launcher.md` — OWNER decision: keep a Herdr-backed `deskops launch` or retire it in favor of `deskops runtime supervise` plus an external harness.
- `tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md` — OWNER, same launch decision.
- `tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md` — OWNER, blocked by the no-deploy rule.
- `stress-tests/st-15-ci-integration.md` and `use-cases/uc-15-deskops-as-a-ci-step.md` — GAP: the CI knowledge-integrity flow is pending a task; tests cover the individual commands, while `.github/workflows/tests.yml` runs only pytest.

## Retired

The covered use-cases, stress-tests (except the CI gap), findings archive, answered questions, drawer rituals, attention review, and obsolete feature outlines were retired on 2026-10-19. Each retirement commit names the test or replacement that covers it, and git history is the durable record.

## Rule

Promote work from `desk/drawer/` into the active surfaces of `desk/` before implementation starts.
