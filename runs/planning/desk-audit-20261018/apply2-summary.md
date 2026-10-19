# apply2 summary

Applied all 37 intended changes with `deskops desk replace` from `/tmp/rw/audit/apply2.sh`.
No files were retired; all listed files were edited.
Script ran cleanly from a clean `desk/` worktree (`EXIT:0`).

## Per-file changes

### atoms
- `desk/atoms/tag-namespaces.yaml` — removed `multi_example`, `testex`, `testns`, `valid_underscore` blocks; kept `domain`, `layer`, `pattern`, `system`, `topic`.

### roles and features
- `desk/roles/deskops-supervisor.md` — replaced the kimi-k3 model sentence with `anthropic/claude-opus-4-8` plus the `openai-codex/gpt-5.4` fallback.
- `desk/drawer/features/feature-agent-role-models.md` — replaced the RoleDoc paragraph with the historical-imports wording.
- `desk/drawer/features/feature-runtime-and-launcher.md` — status now `Implemented and committed on main.`; line 142 now points at `task-adhoc-subagent-launcher-tmux-multi-cli.md` retargeted onto Herdr.

### drawer indexes and notes
- `desk/drawer/README.md` — changed "decomposed into routines and hooks" to "implemented as CLI operations"; added `issues/`, `use-cases/`, `stress-tests/` bullets.
- `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` — line 29 path now `feature-runtime-and-launcher.md`.
- `desk/drawer/questions/README.md` — removed the `Files` bullets; ritual/routine/hook -> ritual; retitled to "Task Lifecycle Semantics" and asked about the sldb ritual graph; replaced KGDB mappings with sldb graph references; removed the `routines` node and its three edges.
- `desk/drawer/questions/question-herdr-runtime-open-decisions.md` — replaced the feature path; "Blocked Surface" section is now "Resolved" with the deduplicated-registry wording.
- `desk/drawer/rituals/knowledge-distillation-pass.md` — KGDB query state -> sldb graph state; "KGDB Tools Used" -> "Graph checks" with `.sldb/runtime/graphs/deskops.kg.json` and graph CLI checks; "Routine Steps" -> "Steps"; promotion sentence simplified; removed `system:kgdb`.
- `desk/drawer/tasks/Board.md` — 28 -> 29 issue files; removed retired `workflow-execution-engine.md` and `feature-materialization-pipeline.md` bullets and the operator-manual pill; six -> four feature docs; added the release task; marked the promoted list historical; replaced the KGDB inbox block with the merge note; removed the paper_IEEE attention list; added the 2026-10-19 audit line.

### stress-tests
- `desk/drawer/stress-tests/README.md` — replaced the open-backlog bullets with the single closed-backlog bullet.
- `desk/drawer/stress-tests/st-01-fresh-start-orientation.md` — `graph neighbors atom:atom-deskops`.
- `desk/drawer/stress-tests/st-02-inbox-capture.md` — steps 1-4 now `message send`, `message list`, `message read`, `message ack`.
- `desk/drawer/stress-tests/st-03-graph-traceability.md` — prefixes all three atom ids with `atom:`.
- `desk/drawer/stress-tests/st-05-task-lifecycle.md` — script now `list tasks`, `show task`, `next task`, `advance task`, `closeout verify`, `closeout commit`; phase-skipping rows replaced with transition-validity rows.
- `desk/drawer/stress-tests/st-07-drift-check.md` — script now `drift check --root .` and `drift check --out <dir>`; removed scope/ack rows and steps.
- `desk/drawer/stress-tests/st-08-closeout-ritual.md` — now `closeout verify` then `closeout commit --no-run`; removed phase/verbose rows.
- `desk/drawer/stress-tests/st-09-self-reflection.md` — kept `graph build` + `graph reflect`; removed `--verbose`/`--kind` steps and rows.
- `desk/drawer/stress-tests/st-11-atom-scaffold-validate.md` — all `atoms new` uses became `add atom --title ... --five-wh-one-plus what --answer ...`.
- `desk/drawer/stress-tests/st-12-desk-health-recovery.md` — `status` -> `doctor --root .`, `status --fix` -> `doctor --repair`, `--guide` step/row removed.
- `desk/drawer/stress-tests/st-13-multi-repo-context.md` — script now register, `repo whoami`, `repo list`, `repo remove`; switch-context rows removed.
- `desk/drawer/stress-tests/st-14-atom-lifecycle-split-merge.md` — `--at` -> `--into`; deprecate -> `atoms delete`; removed `--include-deprecated` step.
- `desk/drawer/stress-tests/st-15-ci-integration.md` — script now pytest, `graph missing`, `drift check`, `closeout verify`; dropped `--ci` flags and row.

### use-cases
- `desk/drawer/use-cases/README.md` — removed UC-06; UC-05 is "Task lifecycle" with lifecycle surfaces; UC-15 surface now CI via pytest and graph/drift checks.
- `desk/drawer/use-cases/doc-pattern-crawl4ai-analysis.md` — section 5.1 labels updated to "Rituals (lifecycle states)" and "Workflow model (tasks, atoms, graph)".
- `desk/drawer/use-cases/uc-01-fresh-start-getting-oriented.md` — `graph neighbors atom:atom-deskops`.
- `desk/drawer/use-cases/uc-02-spark-of-an-idea-capture-it.md` — steps 1-3 now `message send`, `message list`, `message read`.
- `desk/drawer/use-cases/uc-03-where-does-this-atom-touch.md` — prefixed both atom ids with `atom:`.
- `desk/drawer/use-cases/uc-05-routine-work-ticking-off-tasks.md` — retitled "Task lifecycle — moving through rituals"; flow now list/show/next/advance/closeout verify/closeout commit.
- `desk/drawer/use-cases/uc-07-the-drift-check.md` — flow now `drift check --root .` and read-findings; removed color/acknowledge vocabulary.
- `desk/drawer/use-cases/uc-08-closeout-wrapping-up.md` — step 1 `closeout verify --task <id>`; step 4 `closeout commit --task <id> --no-run --reason ...`.
- `desk/drawer/use-cases/uc-10-i-want-to-share-this-insight.md` — step 2 now writes the materialization doc under `docs/` with `MaterializationContractDoc`.
- `desk/drawer/use-cases/uc-11-ritual-new-atom-from-scratch.md` — step 1 now `add atom --title ... --five-wh-one-plus what --answer ...`.
- `desk/drawer/use-cases/uc-12-oops-i-broke-the-desk.md` — `status` -> `doctor --root .`, `status --fix` -> `doctor --repair`.
- `desk/drawer/use-cases/uc-13-multi-repo-ecosystem.md` — steps now register/whoami/list/remove; active-context switching removed.
- `desk/drawer/use-cases/uc-14-atom-evolution-splitting-merging-deprecating.md` — retitled to deleting; `--at` -> `--into`; deprecate -> `atoms delete`; deprecated-listing step removed.
- `desk/drawer/use-cases/uc-15-deskops-as-a-ci-step.md` — steps 2-5 now pytest, `graph missing`, `drift check`, `closeout verify`; CI flags dropped.

## Not applied

None.

## Final checks

```
$ PYTHONPATH=/tmp/rw/wt/apply2 python -m sldb stores check --store /tmp/rw/wt/apply2/.sldb
PASS: store integrity — 222 documents in 17 models
(exit 0)

$ python -m deskops doctor --root /tmp/rw/wt/apply2
Desk is healthy. No issues found.
(exit 0)

$ python -m deskops graph missing --root /tmp/rw/wt/apply2
2 missing, 135 informational
(exit 1)
```

The two graph-missing entries are pre-existing and unrelated to this change:
`issue:make-deskops-easy-to-use -> desk/tasks/task-classify-cli-grammar.md` and
`issue:refactor-primitives-into-ast-driven-task-nodes -> source_file:deskops/runtime/primitives.py`.
