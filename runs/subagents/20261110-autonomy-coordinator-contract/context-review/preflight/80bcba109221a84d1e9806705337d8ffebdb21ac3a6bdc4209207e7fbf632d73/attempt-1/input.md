FILE:desk/tasks/task-scion-autonomy-coordinator-contract.md
---
sldb:
  by: agent
  at: '2026-11-10T15:15:34Z'
  authority: generated
  via: update_document
id: task-scion-autonomy-coordinator-contract
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- e58ee061
- tests/test_scion_runtime.py
depends_on:
- task-scion-autonomy-review-status
pills: []
files:
- deskops/runtime/scion.py
- deskops/cli/registry.py
- deskops/cli/commands/runtime.py
- desk/roles/deskops-supervisor.md
- desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
- tests/test_scion_runtime.py
- tests/fixtures/golden/help
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-coordinator-contract.md
---

# Scion autonomy: consistent coordinator and tester contract

## Rationale

_Explain why this task exists or the business driver behind it._

Owner requires unattended authorized task progress; real coordinator stopped on source-policy conflicts, stale state and false review status.

## Goal

_Describe the concrete result this task must produce._

One coherent source contract makes Scion coordinator recover configured current state, progress routine authorized work, select reviewed ready unowned tasks, dispatch fresh executor/tester and reconcile closeout before continuing.

## Scope

_State what is in scope and what is out of scope._

Role source, generated Scion modes/prompts and command examples, explicit runtime context and durable atoms/docs. No replacement lifecycle engine, automatic policy decisions, pi-subagents or unrelated CC tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Source contract: correct RoleDoc via SLDB, permitting modeled workflow CLI mutations but no implementation by supervisor. Ordinary implementation questions answered from task/source evidence; escalate only unresolved owner decisions, actual ownership conflicts or external credentials/permissions. Never rerun an accepted review with unchanged input; bound technical retries and report precise blockers instead of broad diagnostic loops. Add optional --context-file JSON to existing runtime template command (and matching generator context kwarg); context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project. Emit DESKOPS_DESK_ROOT, DESKOPS_SOURCE_ROOT, DESKOPS_SLDB_SOURCE_ROOT, DESKOPS_WORKSPACE_ROOT, DESKOPS_SCION_PROJECT and PYTHONPATH plus a supported volume source=workspace_root target=workspace_root. No secrets in context. Preserve no-context behavior. Include tester mode in existing --mode choices, auto-detect tester RoleDoc, and separate tester scope/completion instructions. Coordinator recovers this configured current desk/tools, checks canonical/dirty state, board DAG/review gates and existing ownership (labels/RunDoc/worktrees), skips blocked/owned tasks, selects one reviewed ready leaf. Deterministic task+contract-derived agent names and task/role labels: write run intent BEFORE start and reconcile existing matching Scion child before any new start; duplicate-name protection stays Scion native, not a new scheduler/registry. Explicit --project, --workspace, --type, --harness-auth api-key, --non-interactive and correct subcommand --root flags in examples. Executor -> independent tester -> coordinator validates evidence -> deskops closeout -> reconcile phase -> recover/select again. Failed tester cannot close; request bounded correction and fresh test. Waiting-for-child uses Scion blocked/completion notifications (already subscribed); only real human decisions ask_user. Capture source atom before operator docs, generate from source, test YAML/modes/context and actual command examples; runtime task supplies hooks/bootstrap and unattended integration. Concrete interface choices: project is a nonempty Scion slug or UUID (not a filesystem path); mode literal is tester. Context JSON requires all five named keys; reject missing/unknown/invalid/relative/out-of-workspace paths before generation, no partial defaults; omitted --context-file preserves existing behavior. sldb_root already names its src directory. PYTHONPATH is source_root + os.pathsep + sldb_root, without inherited stale paths. Existing role model preferences never override explicit configured harness/model alias. Bound technical retries to 2 per unchanged input and implementation correction/test cycles to 2 per task contract; if still failing persist exact blocker, do not ask owner for facts already in sources. Run intent is the existing RunDoc with in_progress outcome in the assigned run_dir, explicitly intent not proof of start. Deterministic child identity: role-specific prefix deskops-e or deskops-t plus first 12 hex of SHA256(task_id + NUL + contract_sha256 + NUL + role); labels deskops.task_id, deskops.contract_sha256, deskops.role. Reconcile exact project+name+labels and RunDoc before start; conflicting ownership blocks that task only. Matching running child is observed, stopped child resumed, completed child reviewed; never launch duplicate. Independent testers use role-deskops-tester/--mode tester and a distinct role identity. Scope also includes deskops/cli/commands/runtime.py to load/pass context-file; test helpers may be added in runtime/scion.py but no replacement scheduler or lifecycle engine. Final clarifications: source_root is the repository root containing the deskops/ package. contract_sha256 is the SLDB task __contract__ digest, obtained using existing sldb.store.hashing.hash_fields_with_map(TaskDoc, markdown) then sldb.store.graph.language.contract_hash.contract_hash(TaskDoc, field_hashes); no local reimplementation or raw-file hash. Add a runtime helper for command examples that derives child name/labels from the task path and role enum executor or tester. Status/history/references changes must not alter identity; goal/scope/contract changes must. Both retry bounds mean 2 total attempts, not 2 additional retries. Among eligible unowned ready leaves use existing Board order as deterministic tie-breaker; no invented priority. Mode autodetection applies only to the explicitly selected RoleDoc: explicit --mode wins; selected name/id ending in -tester chooses tester, supervisor/coordinator chooses coordinator, otherwise executor; never search other roles to choose one. Source task unit validation can complete independently, but final unattended acceptance/phase integration requires the declared setup runtime task; dependency output commit is recorded then, not requested as owner policy. Retry identity clarification: attempt is integer 1 or 2, first uses the base child name and second appends -a2; include deskops.attempt label. RunDoc attempts and evidence are immutable: never overwrite a previous attempt, never create attempt 3. Unknown, unavailable or active Scion state is observed or recorded as a blocker rather than duplicated. Match stopped children resume the same identity; prior completed attempts are reviewed before any correction attempt. desk_root means the task repository root containing desk/, and all task --root flags use it. Preserve omitted-context environment/path and CLI compatibility while correcting faulty instructions in all modes. Template-only generation is side-effect-free apart from its output files; supplied task/agent records intent before manual launch. Unit tests use temporary task Markdown and compare canonical SLDB digests, deterministic names/labels, bad attempts, context validation before output, tester scope and full generated command flags.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_runtime.py
- affected CLI help/output goldens if tester mode adds a choice
- real unattended coordinator -> executor -> independent tester -> closeout/continue integration

## Done When

_Name the observable condition that makes the task complete._

No source/installed instruction contradiction; tester materialization correct; routine questions not blanket ask_user; dispatch checks readiness/ownership and restart identity. Focused tests pass and live integrated experiment demonstrates the loop without parent prompts.
