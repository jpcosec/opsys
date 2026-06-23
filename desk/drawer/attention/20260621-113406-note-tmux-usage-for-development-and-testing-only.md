# Note: tmux usage for development and testing only

## Context
A `tmux` workspace was introduced to support concurrent implementation and test execution for the ETM specialist work.

## Intended usage
Use `tmux` as an **external orchestration layer** for development and testing, including:
- parallel schema work
- deterministic tool tests
- agent/workflow wiring checks
- connection/unit/e2e/conversational test runs
- supervisor-style repo/status review
- git/diff inspection

Current related artifacts:
- `scripts/start_etm_subagents_tmux.sh`
- `specs/SPEC_TMUX_ASYNC_SUBAGENTS_ETM.md`

## Explicit boundary
`tmux` should **not** be treated as:
- an inner ETM-specialist agent feature
- part of the Step-1 ETM runtime contract
- a required dependency of `agents/etm_specialist/*`
- a substitute for deterministic tool boundaries, schemas, or tests

The ETM specialist implementation should remain runnable and testable without `tmux`.

## Why this matters
This preserves a clean separation between:
- **developer operations**: terminal/session orchestration
- **agent architecture**: Step-1 ETM evaluator logic, schemas, fixtures, and tests

That separation keeps the design portable, reviewable, and aligned with the existing boundary that Step-1 ETM evaluation must remain explicit and bounded.

## Recommended practice
If `tmux` is used in this repo, it should launch or monitor commands such as:
- `pytest -q tests/agents/etm_specialist/...`
- `python3 scripts/check_adk_connectivity.py`
- `python3 scripts/adk_live_smoke.py`
- repo inspection commands like `git status` or `deskops show ...`

It should not be embedded into the ETM workflow implementation itself.
