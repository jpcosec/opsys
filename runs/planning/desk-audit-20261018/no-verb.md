# No-verb updates (no deskops edit surface)

These files have UPDATE verdicts but no model/CLI edit verb. Intended changes are recorded, not applied.

## desk/atoms

- `desk/atoms/tag-namespaces.yaml` — remove the `multi_example`, `testex`, `testns`, and `valid_underscore` keys; keep `domain`, `layer`, `pattern`, `system`, `topic`.

## desk/roles

- `desk/roles/deskops-supervisor.md` — replace body line 36 (old `fireworks/.../kimi-k3` sentence) with `- anthropic/claude-opus-4-8 (canonical; routing and review need long context and reliable instruction-following). Fallback: openai-codex/gpt-5.4.`

## desk/drawer

- `desk/drawer/README.md` — replace "or decomposed into routines and hooks." with "or implemented as CLI operations."; add bullets for `issues/`, `use-cases/`, and `stress-tests/`.
- `desk/drawer/features/feature-agent-role-models.md` — replace the RoleDoc paragraph with: "Supervisor, executor, and tester are RoleDocs under `desk/roles/`; the router role has no RoleDoc. The imported bodies below are historical: `desk/agents/` is deleted and retirement is `deskops closeout commit`, not file deletion."
- `desk/drawer/features/feature-runtime-and-launcher.md` — replace "Implemented and merged into working tree, uncommitted." with "Implemented and committed on main."; rewrite line 142 to point at `task-adhoc-subagent-launcher-tmux-multi-cli.md` over tmux retargeted onto Herdr.
- `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` — replace the line 29 path `desk/drawer/features/feature-herdr-supervised-execution-runtime.md` with `desk/drawer/features/feature-runtime-and-launcher.md`. (Line 55's historical inbox-note mention may stay.)
- `desk/drawer/questions/README.md` — remove the `Files` bullets for `workflow-questions.md` and `workflow-question-map.md`; replace "a ritual/routine/hook" with "a ritual"; retitle "Task And Routine Semantics" to "Task Lifecycle Semantics" and ask how the sldb ritual graph evaluates transition conditions; replace KGDB mappings with sldb graph contracts; remove the `routines` node and its edges from the Mermaid diagram.
- `desk/drawer/questions/question-herdr-runtime-open-decisions.md` — replace `feature-herdr-supervised-execution-runtime.md` with `desk/drawer/features/feature-runtime-and-launcher.md`; replace "Blocked Surface" with: "Resolved: the registry was deduplicated and `deskops message send`, `list`, `read`, `ack` works; duplicate roots are rejected by `deskops/identity.py`."
- `desk/drawer/rituals/knowledge-distillation-pass.md` — replace "KGDB query state" with "sldb graph state"; replace "KGDB Tools Used" with "Graph checks" using `.sldb/runtime/graphs/deskops.kg.json`, `deskops graph build`, `missing`, `neighbors`; rename "Routine Steps" to "Steps"; replace the routines/hooks/gates promotion sentence with "promoted into an active `desk/rituals/` document."; remove the `system:kgdb` tag.
- `desk/drawer/stress-tests/README.md` — replace the `issue-empty-selector-validation-error.md` bullet with: "`desk/drawer/issues/issue-stress-test-fix-backlog.md` — closed; all Phase 0 items are fixed, including empty selectors (`d42a3e3`)."
- `desk/drawer/stress-tests/st-01-fresh-start-orientation.md` — replace both `graph neighbors atom-deskops` with `graph neighbors atom:atom-deskops`.
- `desk/drawer/stress-tests/st-02-inbox-capture.md` — rewrite steps 1-4 as `deskops message send "..."`, `deskops message list`, `deskops message read <selector>`, `deskops message ack <selector>`.
- `desk/drawer/stress-tests/st-03-graph-traceability.md` — prefix every atom id passed to `graph neighbors` with `atom:`.
- `desk/drawer/stress-tests/st-05-task-lifecycle.md` — replace the script with `deskops list tasks`, `deskops show task <id>`, `deskops next task <id>`, `deskops advance task <id>`, `deskops closeout verify --task <id>`, `deskops closeout commit --task <id> --no-run --reason ...`; replace phase-skipping rows with transition-validity rows.
- `desk/drawer/stress-tests/st-07-drift-check.md` — rewrite the script to `deskops drift check --root .` and `deskops drift check --out <dir>`; delete steps 2-6 and the scope/ack rows.
- `desk/drawer/stress-tests/st-08-closeout-ritual.md` — rewrite to `deskops closeout verify --task <id>` then `deskops closeout commit --task <id> --no-run --reason ...`; delete phase/verbose rows.
- `desk/drawer/stress-tests/st-09-self-reflection.md` — remove steps 3-4 (`--verbose`, `--kind`) and matching rows; keep `graph build` then `graph reflect`.
- `desk/drawer/stress-tests/st-11-atom-scaffold-validate.md` — replace `atoms new "..."` with `deskops add atom --title "..." --five-wh-one-plus what --answer "..."`.
- `desk/drawer/stress-tests/st-12-desk-health-recovery.md` — replace `deskops status` with `deskops doctor --root .`; replace `status --fix` with `doctor --repair`; delete `status --guide`.
- `desk/drawer/stress-tests/st-13-multi-repo-context.md` — replace steps 2-6 with `deskops repo whoami`, `deskops repo register`, `deskops repo remove <selector>`; delete switch-context rows.
- `desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md` — replace `--at` with `--into`; replace `atoms deprecate ... --reason` with `atoms delete atom-old-idea`; remove `--include-deprecated`.
- `desk/drawer/stress-tests/st-15-ci-integration.md` — rewrite to `python -m pytest tests -q`, `deskops graph missing`, `deskops drift check`, `deskops closeout verify --task <id>`; drop all `--ci` flags.
- `desk/drawer/tasks/Board.md` — change "28 files" to "29 files"; delete the KGDB routed block and say "KGDB was merged into sldb; its inbox no longer exists."; mark the promoted list as historical; delete the paper_IEEE attention list; add the release task under Deferred task backlog; add an audit line dated 2026-10-19. Also remove the retired bullets/lines: `workflow-execution-engine.md` (line 18), `feature-materialization-pipeline.md` (line 21), and `desk/contexts/pill-operator-manual-follows-stable-runnable-slices.md` (line 147).
- `desk/drawer/use-cases/README.md` — remove the UC-06 row; retitle UC-05 "Task lifecycle" with surface "list, show, next, advance, closeout"; change UC-15 surface to "CI via pytest and graph/drift checks".
- `desk/drawer/use-cases/doc-pattern-crawl4ai-analysis.md` — in section 5.1 replace "Rituals & Routines" with "Rituals (lifecycle states)" and "Primitives (conditions, operators, checklists, edges)" with "Workflow model (tasks, atoms, graph)".
- `desk/drawer/use-cases/uc-01-fresh-start-getting-oriented.md` — replace `deskops graph neighbors atom-deskops` with `deskops graph neighbors atom:atom-deskops`.
- `desk/drawer/use-cases/uc-02-spark-of-an-idea-capture-it.md` — replace step 1 with `deskops message send "..."`; step 2 with `deskops message list`; step 3 with `deskops message read <selector>`.
- `desk/drawer/use-cases/uc-03-where-does-this-atom-touch.md` — prefix both neighbor ids with `atom:`.
- `desk/drawer/use-cases/uc-05-routine-work-ticking-off-tasks.md` — replace the flow with `list tasks`, `show task`, `next task`, `advance task`, `closeout verify`, `closeout commit`; retitle "Task lifecycle — moving through rituals".
- `desk/drawer/use-cases/uc-07-the-drift-check.md` — rewrite steps 2-4 as `deskops drift check --root .` and "read the findings"; delete color and acknowledge vocabulary.
- `desk/drawer/use-cases/uc-08-closeout-wrapping-up.md` — replace step 1 with `deskops closeout verify --task <id>`; step 4 with `deskops closeout commit --task <id> --no-run --reason ...`.
- `desk/drawer/use-cases/uc-10-i-want-to-share-this-insight.md` — replace step 2 with "write or update the atom materialization doc under `docs/` (see `MaterializationContractDoc`)".
- `desk/drawer/use-cases/uc-11-ritual-new-atom-from-scratch.md` — replace step 1 with `deskops add atom --title "..." --five-wh-one-plus what --answer "..."`.
- `desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md` — replace `status` with `doctor`, `status --fix` with `doctor --repair`; delete the `--guide` step.
- `desk/drawer/use-cases/uc-13-multi-repo-ecosystem.md` — rewrite steps 2-5 as `deskops repo whoami` and `deskops repo remove <selector>`; remove active-context switching.
- `desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md` — replace `--at` with `--into`; replace "deprecate" with `deskops atoms delete`; remove the deprecated-listing step; retitle "Atom evolution — splitting, merging, deleting".
- `desk/drawer/use-cases/uc-15-deskops-as-a-ci-step.md` — replace steps 2-4 with `python -m pytest tests -q`, `deskops graph missing`, `deskops drift check`, `deskops closeout verify --task <id>`; drop CI flags.
