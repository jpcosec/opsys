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

---

## Merged item: `adopt-agent-role-segregation`

#### Kind

feature

#### Status

open

#### Problem

Currently, `AGENTS.md` often serves as a monolithic policy dump, leading to conflicting agent behaviors where an agent might try to plan, route, execute, and evaluate simultaneously. This lack of role segregation creates "free-running" implementers that drift across task boundaries and mix orchestration with execution.

In successful implementations (like the IEEE tutoring paper desk), splitting responsibilities into distinct operational personas provides much better control and prevents hallucination.

#### Desired Outcome

Refactor the agent onboarding and execution model to explicitly separate roles:
- **Router** (`AGENTS.md`): Purely directs the incoming agent to adopt a specific operational role based on context.
- **Supervisor** (`desk/roles/deskops-supervisor.md`): Handles planning, routing tasks, launching subagents, monitoring testing, syncing the board, and enforcing closeout rituals.
- **Executor** (`desk/roles/deskops-executor.md`): Operates blindly on exactly *one* bounded task at a time, writes the code/tests, persists run traces, and stops exactly at the task boundary.

#### Questions

- How do we enforce that an agent explicitly adopts a role before acting?
- Should `deskops` CLI commands be role-aware (e.g., `deskops supervisor run`)?
- How do we migrate existing monolithic `AGENTS.md` files in other repositories?

#### Follow-Up Shape

- Rewrite `AGENTS.md` to be a pure router.
- Create default `desk/roles/deskops-supervisor.md` and `desk/roles/deskops-executor.md` templates in the deskops scaffold.
- Update the operator manual to reflect role-based workflow.

#### Related Atoms

- atom-clean-agents-start-from-minimum-workflow-set
- atom-phase-gates-prevent-agent-skipping

---

## Merged item: `inject-files-and-atoms-into-subagent-task-context`

#### Issue

While the task model supports `files`, `pills`, and `references`, the process of assembling the required context for zero-context subagents is manual and lacks explicit enforcement for atoms. A task should robustly declare not just the transient context (pills) but also the exact source files (code) to touch and the durable architectural rules (atoms) that apply.

#### Core Need

Formalize how code files and atoms are injected into a subagent's task context. Update the CLI (e.g. `deskops add task` and edit commands) to easily attach these dependencies so subagents can mechanically resolve their reading set before starting the ambiguity review.

#### Constraints

- Subagents must not fall back to searching the whole codebase.
- Injected contexts should validate against KGDB (no broken file or atom references).
- Should build upon existing SLDB models (`TaskDoc`'s `files`, `pills`, and `references`).

#### Follow-Up Shape

- Modify `deskops add task` and models to explicitly support and validate `--file`, `--pill`, and `--atom` flags.
- Document the zero-context subagent reading routine in an atom or ritual.

#### Tags

- system:deskops
- topic:agents
- topic:subagents
- topic:tasks
- topic:context

---

## Merged note: `20260621-113406-note-tmux-usage-for-development-and-testing-only.md`

### Note: tmux usage for development and testing only

#### Context
A `tmux` workspace was introduced to support concurrent implementation and test execution for the ETM specialist work.

#### Intended usage
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

#### Explicit boundary
`tmux` should **not** be treated as:
- an inner ETM-specialist agent feature
- part of the Step-1 ETM runtime contract
- a required dependency of `agents/etm_specialist/*`
- a substitute for deterministic tool boundaries, schemas, or tests

The ETM specialist implementation should remain runnable and testable without `tmux`.

#### Why this matters
This preserves a clean separation between:
- **developer operations**: terminal/session orchestration
- **agent architecture**: Step-1 ETM evaluator logic, schemas, fixtures, and tests

That separation keeps the design portable, reviewable, and aligned with the existing boundary that Step-1 ETM evaluation must remain explicit and bounded.

#### Recommended practice
If `tmux` is used in this repo, it should launch or monitor commands such as:
- `pytest -q tests/agents/etm_specialist/...`
- `python3 scripts/check_adk_connectivity.py`
- `python3 scripts/adk_live_smoke.py`
- repo inspection commands like `git status` or `deskops show ...`

It should not be embedded into the ETM workflow implementation itself.
