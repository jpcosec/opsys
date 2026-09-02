# Preflight comprehension reformulation

TaskDoc-understood work:

1. Read `desk/rituals/execution.md` and `desk/rituals/phase.md` to determine which ritual should own the new guardrail.
2. Add the zero-context comprehension test as an explicit numbered preparation step in `desk/rituals/execution.md`, not as a broad workflow note.
3. Make the pass criteria explicit: a fresh-context subagent must restate the intended work step by step accurately enough to show it understood the task intent.
4. Make the failure criteria explicit: if the reformulation reveals any ambiguity, missing instruction, or misunderstanding, the TaskDoc must be fixed before any real Executor is dispatched.
5. Make the evidence requirement explicit: save the TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
6. Add a short reusable pill at `desk/contexts/pill-zero-context-preflight-precedes-executor.md` with minimal `What`, `Why`, `When`, `Where`, and `How` sections.
7. Do not widen scope into task docs, board routing, tests, or Python implementation files.
8. Run `pytest -q` after the document changes and record the result.
9. Write handoff evidence under `runs/subagents/20260902-wave1-ritual-preflight/`, including a result summary with the diff summary.

Ambiguities detected:

- None that block execution. The request names the target ritual (`execution.md` preparation section), the required new pill, prohibited surfaces, validation command, and evidence directory.
