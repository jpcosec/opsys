# Desk audit — lane contexts

HEAD: `2ec128a`. Read-only verification against `deskops/`, `.sldb`, `tests/`, sibling checkouts, and git history.

| file | verdict | evidence | action |
|---|---|---|---|
| desk/contexts/pill-001-task-closure-commit.md | KEEP | Matches the only closure path: `deskops closeout --help` exposes commit/supersede/retire; `deskops/services/closure.py` performs the closing commit. | None. |
| desk/contexts/pill-005-subagent-execution.md | KEEP | `desk/rituals/execution.md` and `AGENTS.md` require a fresh task-scoped subagent bundle before implementation. | None. |
| desk/contexts/pill-006-self-described-store-layout.md | KEEP | Atom `atom-001` is still current; `.sldb` layout is `core/` plus ignored `runtime/` (`.gitignore` line 7). | None. |
| desk/contexts/pill-007-phase-gated-task-flow.md | KEEP | Lifecycle spec `deskops/spec/workflows/task_lifecycle.yaml` has execution→testing→closeout transitions; Board routes all four rituals. | None. |
| desk/contexts/pill-008-kgdb-sldb-boundary.md | KEEP | Verified imports `sldb.api.graph.snapshot` and `sldb.store.graph.graph_io.save_graph`; `pyproject.toml` has no kgdb dependency. | None. |
| desk/contexts/pill-009-source-file-graph-traceability.md | UPDATE | Pill tag line 7 still says `system:kgdb`; `deskops/graph/extract_sources.py` still builds source-file nodes, so only the legacy taxonomy is stale. | `deskops edit pill pill-009 tags '["system:deskops","pill-type:model","topic:source-code","topic:traceability"]'` |
| desk/contexts/pill-010-graph-runtime-output-policy.md | UPDATE | Tag line 7 says `system:kgdb`; `when` line 31 says “KGDB graph JSON”, but output is `deskops graph snapshot` (`.sldb/runtime/graphs/`). | `deskops edit pill pill-010 tags '["system:deskops","system:sldb","pill-type:guardrail","topic:runtime","topic:drift-control"]'` and `deskops edit pill pill-010 when 'Apply this pill whenever a task writes deskops graph snapshot JSON, generated indexes, query results, or self-reflection reports.'` |
| desk/contexts/pill-011-self-reflection-noise-control.md | UPDATE | `where` line 37 says “future graph/reflection commands”; `deskops graph reflect` exists today. | `deskops edit pill pill-011 where 'Applies to desk/tasks/*self-reflection*.md, deskops graph reflect, and any generated inbox or drawer output.'` |
| desk/contexts/pill-012-create-operations-transactional-rollback.md | KEEP | `deskops/doc_io.py:250` defines `DocTransaction`; `deskops/operations.py:265` wraps `create_artifact` in it. | None. |
| desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md | KEEP | `deskops atoms --help` exposes `create`, `delete`, `split`, `merge`, `validate`; atom reference guards exist in `deskops/atom_references.py`. | None. |
| desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md | KEEP | Board routes exactly the 7 pills repeated in `desk/contexts/pills.md`. | None. |
| desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md | KEEP | `deskops/cli/commands/message.py` exists; `deskops repo whoami --root .` returns `deskops`. | None. |
| desk/contexts/pill-cli-gaps-become-tracked-work.md | KEEP | Current task/issue/inbox surfaces exist; guidance still matches `AGENTS.md`. | None. |
| desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md | KEEP | `deskops closeout verify` exists and `deskops/services/closeout_gates.py` implements evidence checks. | None. |
| desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md | UPDATE | `where` line 37 says “future desk update/sync flows”; `deskops desk update` and `deskops message ack` exist now. `deskops message` is the current transport. | `deskops edit pill pill-cross-desk-inbox-needs-delivery-verification-and-follow-up where 'Applies to deskops/cli/commands/message.py, the deprecated deskops inbox alias, repo registry resolution, deskops desk update, and cross-desk acknowledgement or reply flows.'` |
| desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md | KEEP | `deskops doctor` exists and delegates store checks to `sldb stores check` (`deskops/cli/commands/doctor.py`). | None. |
| desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md | KEEP | `deskops drift check` now calls role, runtime, and `drift_check_knowledge_surfaces` checks; it only reports findings (`deskops/cli/commands/drift.py`). | None. |
| desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md | KEEP | `_add_closeout_facts` includes `pill_graduation_verified` (`deskops/operations.py`). | None. |
| desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md | KEEP | `deskops desk migrate` and `deskops/lifecycle_migration.py` implement the legacy path. | None. |
| desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md | KEEP | `Operations.list_artifacts` prints `Warning: Failed to load artifact ...` to stderr instead of skipping silently (`deskops/operations.py:395`). | None. |
| desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md | KEEP | List/show expose `--format {text,json}`; message/faq expose yaml too; golden tests cover output. | None. |
| desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md | KEEP | `MaterializationContractDoc` is registered (`.sldb/core/models/`) and has a CLI subject (`deskops materializations`). | None. |
| desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md | KEEP | `deskops/cli/parser.py` and `deskops/cli/registry.py` still own command grammar/help. | None. |
| desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md | RETIRE | Resolved: `docs/operator-manual.md` landed in closeout `978fd98`; `tests/test_operator_manual.py` executes its `bash runnable` blocks. Pill is still referenced by `desk/drawer/tasks/Board.md:147` and tracked in `.sldb/core/documents/PillDoc/`. Retiring leaves that drawer-board line dangling. | Replaced by `docs/operator-manual.md` and `tests/test_operator_manual.py`. Remove the line from `desk/drawer/tasks/Board.md`; untrack with `python -m sldb docs untrack PillDoc/pill-operator-manual-follows-stable-runnable-slices --store .sldb`. |
| desk/contexts/pill-pattern-supervisor-playbook-buenas-tareas-bundle-contexto-cero-y-frontera-de-modelos.md | KEEP | References current role names, `runs/subagents/`, the existing `deskops-task-lifecycle` skill, and `deskops closeout commit`. | None. |
| desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md | KEEP | `desk/rituals/phase.md` is routed by the Board and still defines the integration/reconciliation pass. | None. |
| desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md | KEEP | `deskops/config.py` loads `desk/config.json` plus `desk/config.local.json`; `deskops/workspace.py:236` emits the same keys. | None. |
| desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md | KEEP | Phase ritual and lifecycle spec still define dependency-layer execution. | None. |
| desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md | KEEP | `tests/test_cli.py` exists and exercises real parser paths; `deskops/cli/` is intact. | None. |
| desk/contexts/pill-zero-context-preflight-precedes-executor.md | UPDATE | `how_not` is empty; `deskops show pill ...` prints `how_not:` with no value and the file ends after the heading (line 48). | `deskops edit pill pill-zero-context-preflight-precedes-executor how_not 'Do not dispatch an Executor when the fresh-context subagent could not restate the TaskDoc without guessing, and do not let coordinator chat memory fill gaps the TaskDoc does not contain.'` |
| desk/contexts/pills.md | KEEP | Required fields match `deskops/models/pill.py`; “current board-routed pills” matches `desk/tasks/Board.md` exactly. | None. |
| desk/contexts/README.md | KEEP | Atom links exist; pill conventions still match `PillDoc`. | None. |
| desk/rituals/phase.md | KEEP | Routed by the Board; lifecycle spec still uses the phase layer. | None. |
| desk/rituals/execution.md | KEEP | Matches `AGENTS.md` and the preflight/execution pills; preflight path is current. | None. |
| desk/rituals/testing.md | KEEP | Routed by the Board; testing-to-closeout handoff is the current lifecycle edge. | None. |
| desk/rituals/closeout.md | UPDATE | Steps 9–10 (lines 22–23) tell the operator to untrack and delete the task before `deskops closeout commit`; `deskops/services/closure.py:386-496` does Board removal, untracking, and bundle deletion itself and needs the task file. Precondition “Board updates are prepared.” is also no longer required. | In `steps`, replace old steps 9–10 with: `1. Leave removal and untracking to deskops closeout commit: it removes the task from the Board, untracks it, and deletes the bundle in the closing commit. Do not delete or untrack by hand first.` In `preconditions`, remove `Board updates are prepared.` |
| desk/rituals/ritual-deployment-ritual.md | RETIRE | Placeholder legacy fixture from `a558fdf` (“Ship code”, “PR merged”, empty lists, step `1.`). It is not a lifecycle state: `deskops/spec/workflows/task_lifecycle.yaml` declares only execution/testing/closeout transitions. No file references it; only its `RitualDoc` store entry does. | Replaced by the three lifecycle rituals; delete and untrack `RitualDoc/ritual-deployment-ritual`. |
| desk/roles/deskops-executor.md | KEEP | Frontmatter and body agree: model `openai-codex/gpt-5.4`, fallback `google-gemini-cli/gemini-3.1-pro-preview`; `tests/test_role_materialization.py` and `tests/test_runtime_profiles.py` cover it. | None. |
| desk/roles/deskops-supervisor.md | UPDATE | Frontmatter lines 8–10 declare `anthropic/claude-opus-4-8` with fallback `openai-codex/gpt-5.4`, and `tests/test_role_materialization.py:25` / `tests/test_runtime_profiles.py:51` assert that. Body line 36 still says `fireworks/accounts/fireworks/models/kimi-k3`. `desk/drawer/questions/question-herdr-runtime-open-decisions.md` decision 1 explicitly requires reconciling the prose. | No `deskops edit role` subject exists. Replace body line 36 with: `- anthropic/claude-opus-4-8 (canonical; routing and review need long context and reliable instruction-following). Fallback: openai-codex/gpt-5.4.` |
| desk/roles/deskops-tester.md | KEEP | Frontmatter and body agree: `openrouter/nvidia/nemotron-3-super-120b-a12b:free`, fallback `openrouter/openai/gpt-oss-20b:free`; tool boundary matches the materializer. | None. |
| desk/steps/step-build.md | RETIRE | Obsolete fixture from `a558fdf`/`6a4d431` (“Run build”, empty Outcome). `RitualDoc` no longer declares `__containment__` for steps; since `e60cdb3` ritual steps are prose (`deskops/models/ritual.py`). No live references; `desk/drawer/stress-tests/findings-archive.md:128,468` mentions it only as a historical finding. | Replaced by prose `steps` in `deskops/models/ritual.py`; delete and untrack `StepDoc/step-build`. |
| desk/steps/step-document-the-cli.md | RETIRE | Same retired step-reference architecture (`e60cdb3`); still contains template instructional text plus “Write user docs”. Only historical stress-test archive references it. | Replaced by prose ritual steps; delete and untrack `StepDoc/step-document-the-cli`. |
| desk/runtimes/runtime-claude.md | KEEP | Matches `RuntimeProfileDoc` fields and `tests/test_runtime_profiles.py` CLAUDE_PROFILE (file delivery, repeat tools, `--resume`, `--print`). | None. |
| desk/runtimes/runtime-pi.md | KEEP | Matches PI_PROFILE in `tests/test_runtime_profiles.py` (`--tools` comma, inline prompt, `--session`). | None. |
| desk/registry/repo-deskops.md | KEEP | `deskops repo whoami --root .` returns `deskops`; path `.` resolves. | None. |
| desk/registry/repo-graph_ui.md | UPDATE | Path exists; description is still template placeholder “Repository for graph_ui.” Sibling README describes a pron/sldb store visual editor with the active mindmap frontend. | `deskops edit repository repo-graph_ui description 'Visual editor for pron and sldb stores; active mindmap frontend under frontends/mindmap.'` |
| desk/registry/repo-sldb.md | KEEP | Path exists; description matches the sibling README and current sldb role. | None. |
| desk/registry/repo-spec2viz.md | UPDATE | Path exists; description is template placeholder “Repository for spec2viz.” Sibling README describes spec-to-diagram rendering. | `deskops edit repository repo-spec2viz description 'Turns semantic YAML specs into diagrams and charts (PlantUML, Mermaid, Vega).'` |
| desk/lifecycle/execution-task_activates.md | KEEP | Matches `task_lifecycle.yaml` transition `task_activates` and is tracked as `RelationDoc/execution-task_activates`. | None. |
| desk/lifecycle/testing-task_hands_to_closeout.md | KEEP | Matches spec condition `nonempty(validation)`; tracked as `RelationDoc/testing-task_hands_to_closeout`. | None. |
| desk/lifecycle/closeout-task_completes.md | KEEP | Matches spec terminal transition and condition `status = "ready_for_testing" and has(closeout_evidence_verified)`. | None. |
| desk/lifecycle/type-task_activates.md | KEEP | Matches generated `RelationTypeDoc` (`RitualDoc` source/target, axis HOW, empty type condition). | None. |
| desk/lifecycle/type-task_completes.md | KEEP | Matches generated `RelationTypeDoc`; the transition condition lives on the `RelationDoc`, as `deskops/lifecycle.py` writes it. | None. |
| desk/lifecycle/type-task_hands_to_closeout.md | KEEP | Matches generated `RelationTypeDoc`. | None. |
| desk/faq/faq-how-to-deploy.md | RETIRE | Placeholder from `a558fdf` (“Run deploy script”). `deskops faq` reads `docs/faq.md` and packaged `deskops/data/faq.md`, never `desk/faq/`; no references outside its store entry. | Replaced by `docs/faq.md`; delete and untrack `DeskFAQDoc/faq-how-to-deploy`. |
| desk/faq/faq-how-to-test.md | RETIRE | Placeholder (“Follow the steps”); same non-consumption by `deskops faq`. | Replaced by `docs/faq.md`; delete and untrack `DeskFAQDoc/faq-how-to-test`. |
| desk/faq/faq-how-to-test-comprehensively.md | RETIRE | Placeholder (“Test every edge case”); same non-consumption by `deskops faq`. | Replaced by `docs/faq.md`; delete and untrack `DeskFAQDoc/faq-how-to-test-comprehensively`. |
| desk/logbook/log-2026-06-21-workflow-baseline-before-roles-refactor.md | KEEP | Explicitly labeled historical record; the header already marks `desk/agents/*`, ETM/ADK, and tmux as superseded. | None. |
| desk/logbook/log-2026-08-04-task-inheritance-runtime-resolution.md | KEEP | Dated historical entry; its “Files Changed” section records past paths, which is the purpose of the logbook. | None. |
| desk/logbook/README.md | KEEP | Scope rules match the current central-harness logbook purpose. | None. |
| desk/materializations/materialization-skill-drift-guard-tests.md | KEEP | Fields match `MaterializationContractDoc`; target `tests/test_skill_cli_drift.py` exists and the validation command is current. | None. |
| desk/features/feature-atom-model-kinds-and-question-facets.md | RETIRE | No `FeatureDoc` model exists; `deskops/workspace.py:_MODELED_DESK_TOP_LEVEL_DIRS` excludes `features`; feature backlog lives in `desk/drawer/features/` after `ff01abe`. No references. | Replaced by `desk/drawer/features/` (backlog surface). Remove the file; nothing to untrack. |
| desk/tasks/Board.md | UPDATE | `tasks: []` and no active tasks, but `notes` line 42 still says “Make role prompts sldb-tracked RoleDocs ... [active]”; that work closed in `e293475`/`6555c2a`. `purpose` also extracts empty. | `deskops edit board Board notes 'No active tasks routed.'` and `deskops edit board Board purpose 'Route the active execution set for deskops.'` |
| desk/config.json | KEEP | `project_identity=deskops`; `versions.desk_format=1.0.0` equals `deskops/constants.py:CURRENT_DESK_FORMAT`; sandbox keys match `deskops/workspace.py:236-246`. | None. |
| desk/models/__init__.py | RETIRE | Tracked (`git ls-files desk/models/__init__.py` non-empty). Legacy mirror of the model registry. `13b1421` deleted the old `desk/` package; `2d39249` re-added this file for sldb-ui flows. It imports removed modules (`deskops.models.checklist`, `condition`, `edge`, `operator`, `routine`); `import desk.models` raises `ModuleNotFoundError`. Only historical `runs/subagents/` evidence references it. | Replaced by `deskops/models/__init__.py` and store federation in `deskops/bootstrap.py`. Delete the file and `desk/models/__pycache__/`. |
| desk/cli/ | N/A | Directory does not exist and `git ls-files desk/cli` is empty; removed by `13b1421`. | None. |
| desk/materializers/ | N/A | Directory does not exist and is not tracked; removed by `13b1421`; live code is `deskops/materializers/`. | None. |
| desk/primitives/ | N/A | Directory does not exist and is not tracked; the retired primitive layer is handled by `deskops/lifecycle_migration.py`. | None. |
| desk/__pycache__/ | N/A | Directory does not exist and is not tracked. (`desk/models/__pycache__/` exists locally but is untracked and gitignored by `__pycache__/`.) | None. |

## Summary

### Counts per verdict

- KEEP: 46
- UPDATE: 10
- RETIRE: 9
- N/A (absent directory, not tracked): 4
- Total rows: 69

### Counts per folder

| folder | files | KEEP | UPDATE | RETIRE | N/A |
|---|---:|---:|---:|---:|---:|
| desk/contexts/ | 32 | 26 | 5 | 1 | 0 |
| desk/rituals/ | 5 | 3 | 1 | 1 | 0 |
| desk/roles/ | 3 | 2 | 1 | 0 | 0 |
| desk/steps/ | 2 | 0 | 0 | 2 | 0 |
| desk/runtimes/ | 2 | 2 | 0 | 0 | 0 |
| desk/registry/ | 4 | 2 | 2 | 0 | 0 |
| desk/lifecycle/ | 6 | 6 | 0 | 0 | 0 |
| desk/faq/ | 3 | 0 | 0 | 3 | 0 |
| desk/logbook/ | 3 | 3 | 0 | 0 | 0 |
| desk/materializations/ | 1 | 1 | 0 | 0 | 0 |
| desk/features/ | 1 | 0 | 0 | 1 | 0 |
| desk/tasks/Board.md | 1 | 0 | 1 | 0 | 0 |
| desk/config.json | 1 | 1 | 0 | 0 | 0 |
| leftovers (desk/models/__init__.py + 4 absent dirs) | 5 | 0 | 0 | 1 | 4 |
