## Review

### 1. Executive summary
- Correct: `desk/tasks/Board.md` frontmatter and its generated `## Task Details` section are internally aligned. The routed task list in `desk/tasks/Board.md:7-21` omits `task-enrich-templates-with-instructional-text`, and the generated summaries in `desk/tasks/Board.md:76-89` omit it too.
- Blocker: `deskops list tasks` is not board-routed for the local repo. It inventories every `desk/tasks/task-*.md` file via a directory glob in `deskops/operations.py:338-350`, so any leftover task file appears even when `desk/tasks/Board.md` no longer routes it.
- Blocker: `task-enrich-templates-with-instructional-text` still appears as `active | complete` because its task file still exists and still says `status: active` plus `current_node: complete` (`desk/tasks/task-enrich-templates-with-instructional-text.md:5,41`). The resolving commit `6389323` did not perform closeout cleanup; it updated the task doc and kept all runtime artifacts.
- Note: The repo currently has multiple effective truth surfaces: board frontmatter for routing, task file presence/frontmatter for local CLI visibility, manual board notes for prose status, and git history for evidence only. That split is the root of the stale-state confusion.

### 2. Evidence-backed explanation of the stale-state mechanism
- Blocker: The local task listing path is file-based, not board-based. `deskops/operations.py:338-350` loops over `desk/tasks/task-*.md` and loads each task file. It never checks whether the task is referenced by `desk/tasks/Board.md`.
- Correct: Cross-repo routed task listing already uses board routing. `deskops/operations.py:352-382` reads each sibling repo's `desk/tasks/Board.md` and lists only referenced tasks. So the same CLI surface mixes two different contracts: local = filesystem inventory, sibling repos = board routes.
- Correct: Current repo evidence shows exactly one mismatch. A direct comparison found `board_count 14`, `file_count 15`, `only_in_files ['task-enrich-templates-with-instructional-text']`, `only_in_board []`.
- Blocker: `python -m deskops list tasks` currently prints `task-enrich-templates-with-instructional-text | active | complete`, matching the stale file on disk, even though `desk/tasks/Board.md:7-21` does not route it.
- Blocker: The stale task remains visible because its file is still present under `desk/tasks/` and still carries active state in frontmatter (`desk/tasks/task-enrich-templates-with-instructional-text.md:1-52`). `deskops list tasks` treats that as enough to list it.
- Note: `deskops next` without a selector is board-routed (`deskops/operations.py:1196-1205`) and errors when multiple board tasks are routed. But `deskops next <task-id>` bypasses board routing and resolves any matching task file directly (`deskops/operations.py:1196-1199`). That means orphan task files are still operationally addressable if explicitly named.

### 3. Why `task-enrich-templates-with-instructional-text` still shows `active | complete`
- Blocker: The task file itself still encodes the stale state: `status: active` and `current_node: complete` in `desk/tasks/task-enrich-templates-with-instructional-text.md:5,41`.
- Blocker: The resolving commit exists, but it was not a closeout commit. `git show 6389323` shows a feature commit titled `feat(models): enrich templates with instructional fixed text`; it modified the task doc and created the routine/checklist/condition/edge artifacts, but did not delete the task, did not delete the routine, and did not touch `desk/tasks/Board.md`.
- Blocker: Current closeout automation only runs when both `status == "closed"` and `current_node == "complete"` (`deskops/operations.py:455-483`, especially `:477-479`). This stale task never meets that contract because it remains `active`.
- Blocker: This task's routine is a legacy outlier. `desk/routines/routine-task-enrich-templates-with-instructional-text.md:4-14` contains only checklist nodes and edges to `complete`; it has no close operator. By contrast, the current default task lifecycle includes a close operator that sets `status` to `closed` and then transitions to `complete` (`deskops/operations.py:798-870`). A repo scan found this is the only current `routine-task-*` file missing the close operator shape.
- Note: Runtime behavior also explains how a legacy routine can reach `complete` without changing status. In `deskops/runtime/primitives.py:174-176`, entering a terminal node or `complete` sets `current_node = "complete"` but preserves the existing `status`. So `active | complete` is mechanically possible for older task bundles.
- Note: The closeout ritual explicitly says the closed-task end state is: task gone from `desk/tasks`, board no longer routes it, and a dedicated closing commit exists (`desk/rituals/closeout.md:42-47,67-70`). `task-enrich-templates-with-instructional-text` satisfies none of those cleanup conditions.

### 4. Sources of truth and where they diverge
- Correct: **Routing truth should be board frontmatter**. `desk/tasks/Board.md:7-21` is the structured routed task set, `desk/README.md:25-26` calls `desk/tasks/Board.md` the active routing board, and `desk/rituals/execution.md:45-50` requires that "The board routes the task as active."
- Correct: **Per-task workflow state belongs in the task doc frontmatter**. Fields like `status` and `current_node` are the task-local lifecycle state (`desk/tasks/task-enrich-templates-with-instructional-text.md:3-46`). This is appropriate only for tasks that are actually routed.
- Note: **Board prose notes are not authoritative state**. In `deskops/models/board.py:8-13`, `## Task Details` is generated from the `tasks` frontmatter list, but `## Notes` is a free-text `notes` field (`deskops/models/board.py:38-48,68-70`). That is why `desk/tasks/Board.md:67` still says `Make list behavior data-integrity-safe [active]` even though the routed task list and generated Task Details no longer include that task.
- Correct: **Commit history is evidence, not live task state**. The code only checks git commits as closeout evidence references (`deskops/operations.py:948-955,998-1012`). No code path derives task retirement from commit history alone.
- Blocker: Today there is not one unified machine truth for "active task" visibility. Local `list tasks` uses file presence plus task frontmatter; `next` without selector uses board frontmatter; board notes can still narrate stale status; commit history can say "Resolves task" without changing live routing state.

### 5. Recommended cleanup options ranked by safety
- Correct: **Option 1 — Data/doc cleanup only (safest immediate cleanup, but incomplete long-term)**
  - Remove the stale legacy task artifacts for `task-enrich-templates-with-instructional-text` so the workspace matches the closeout ritual:
    - `desk/tasks/task-enrich-templates-with-instructional-text.md`
    - `desk/routines/routine-task-enrich-templates-with-instructional-text.md`
    - all `desk/primitives/{checklists,conditions,edges}/...enrich-templates-with-instructional-text...md`
  - Clean the stale prose note in `desk/tasks/Board.md:67` for `Make list behavior data-integrity-safe [active]`.
  - This fixes the current stale surfaces without changing code.
  - Limitation: `deskops list tasks` will still diverge from the board again whenever another orphan task file survives.
- Blocker: **Option 2 — Data/doc cleanup plus smallest safe code contract change (recommended)**
  - Do Option 1.
  - Change `deskops list tasks` so the default local listing is board-routed, matching the board contract already used for sibling repos and `next` without selector.
  - If raw file inventory is still needed, expose it explicitly with a new flag such as `--all` or `--include-unrouted` rather than making it the default.
  - This is the smallest durable fix that gives the supervisor one clean routing truth.
- Note: **Option 3 — Broader routing enforcement (lower safety / broader scope)**
  - In addition to Option 2, enforce board membership for `next <task-id>`, `show task`, and possibly `advance task`.
  - This would remove more stale-state escape hatches, but it is a wider CLI contract change and is not necessary for the immediate hygiene fix.

### 6. If a code fix is warranted, exact functions/files likely involved
- Correct: **Smallest safe contract change**: make local `list tasks` board-routed by default.
- Note: Likely touched code files for that smallest change:
  - `deskops/operations.py`
    - `list_tasks` at `:338-350` — switch from filesystem glob to `desk/tasks/Board.md` references.
    - likely add/reuse a local board-ref resolver near `_next_task_path` / `_resolve_repo_board_task_path` at `:1196-1234`.
    - possibly reuse `_task_route_summary` at `:1236-1257` or add a local equivalent that returns hydrated `Task` objects from board refs.
  - `deskops/cli/parser.py:534-540`
    - add/rename flags if keeping a raw filesystem mode (for example `--all` or `--include-unrouted`).
  - `deskops/cli/commands/operations.py:82-88`
    - pass any new flag through if `operations.list_tasks()` grows a routed/all mode parameter.
  - `tests/test_cli.py`
    - add a regression test proving unrouted local task files do not appear in default `list tasks` output.
    - if an explicit raw inventory flag is added, add a second test proving the orphan task appears only with that flag.
- Note: If the supervisor wants to tighten all routing-sensitive commands later, additional likely touchpoints are:
  - `deskops/operations.py:430-436` (`show_task`)
  - `deskops/operations.py:1196-1205` (`_next_task_path`)
- Note: I do **not** recommend a code change that auto-deletes any `active | complete` task or infers closure from commit messages. That would be unsafe because the closeout ritual requires explicit board cleanup and a dedicated closeout commit, not heuristic retirement.

### 7. Specific supervisor next actions
- Blocker: Decide and state the contract explicitly: **recommended contract = `desk/tasks/Board.md` frontmatter is the sole routing truth for active tasks**.
- Blocker: Perform targeted closeout cleanup for the single orphan legacy task `task-enrich-templates-with-instructional-text` and remove its stale runtime artifacts.
- Blocker: Remove the stale `Make list behavior data-integrity-safe [active]` prose line from `desk/tasks/Board.md:67`; it is manual note residue, not routed state.
- Correct: If you want durable behavior alignment, implement the small CLI change so default `deskops list tasks` follows board routing.
- Note: The worktree is currently dirty with unrelated tracked and untracked changes (`runs/.../git-status.txt` and current `git status --short`). Any cleanup or closeout commit should be isolated carefully; do not let an auto-close or manual cleanup commit absorb unrelated changes.
- Note: After cleanup, rerun these inspection commands as acceptance checks:
  - `python -m deskops list tasks`
  - `python -m deskops next`
  - a board-vs-files diff check to confirm there are no `only_in_files` task docs left under `desk/tasks/`

- Fixed: none; this was a read-only review and no project/source files were edited.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Scope stayed read-only: no project/source files were edited; only inspection commands were run and findings were written to the required run artifact path."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Findings cite exact files/lines (`deskops/operations.py`, `desk/tasks/Board.md`, `desk/tasks/task-enrich-templates-with-instructional-text.md`, `desk/rituals/closeout.md`, `deskops/runtime/primitives.py`) plus command outputs (`python -m deskops list tasks`, `python -m deskops next`, git history, board-vs-files diff check)."
    }
  ],
  "changedFiles": [
    "runs/subagents/20260702-065749-board-routing-hygiene-review/result-summary.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "python -m deskops list tasks | sed -n '1,40p'",
      "result": "observed",
      "summary": "Listed 15 local task docs, including unrouted `task-enrich-templates-with-instructional-text | active | complete`."
    },
    {
      "command": "python -m deskops next task-enrich-templates-with-instructional-text",
      "result": "observed",
      "summary": "Explicit selector still resolves the orphan task file and reports `Status: active`, `Current node: complete`, `Phase: complete`."
    },
    {
      "command": "python -m deskops next",
      "result": "observed",
      "summary": "Errored with `Multiple active tasks are routed; pass a task selector`, confirming board-routed semantics for selector-free `next`."
    },
    {
      "command": "python - <<'PY' ... board vs file task diff ... PY",
      "result": "observed",
      "summary": "Found `board_count 14`, `file_count 15`, `only_in_files ['task-enrich-templates-with-instructional-text']`, `only_in_board []`."
    },
    {
      "command": "git show --stat --summary 6389323 --",
      "result": "observed",
      "summary": "Resolving commit changed task artifacts but did not delete the task or board-route cleanup surfaces."
    },
    {
      "command": "git show --unified=40 968bdb7 -- desk/tasks/Board.md ...",
      "result": "observed",
      "summary": "Confirmed prior cleanup removed task routing and generated Task Details entry for `task-make-list-behavior-data-integrity-safe`, but stale prose note remained in `## Notes`."
    },
    {
      "command": "git diff --no-ext-diff --cached --name-only",
      "result": "passed",
      "summary": "No staged files."
    },
    {
      "command": "git status --short --untracked-files=all | sed -n '1,80p'",
      "result": "observed",
      "summary": "Worktree is dirty with unrelated tracked and untracked changes; cleanup commits must be isolated carefully."
    }
  ],
  "validationOutput": [
    "`deskops/operations.py:338-350` lists all local `task-*.md` files regardless of board routing.",
    "`desk/tasks/Board.md:7-21` routes 14 tasks and excludes `task-enrich-templates-with-instructional-text`.",
    "`desk/tasks/task-enrich-templates-with-instructional-text.md:5,41` still says `status: active` and `current_node: complete`.",
    "`deskops/operations.py:477-479` only auto-cleans when `status == closed` and `current_node == complete`.",
    "`desk/routines/routine-task-enrich-templates-with-instructional-text.md:4-14` is a legacy routine missing the close operator present in current defaults (`deskops/operations.py:798-870`).",
    "`desk/tasks/Board.md:67` contains stale prose for `Make list behavior data-integrity-safe [active]`, while `desk/tasks/Board.md:76-89` no longer includes it in generated Task Details."
  ],
  "residualRisks": [
    "Even after data cleanup, default `deskops list tasks` will continue to diverge from board routing until code changes or the contract is explicitly redefined.",
    "Explicit task selectors (`next <task-id>`, and likely `show task`) can still operate on orphan task files unless board membership is enforced more broadly.",
    "Dirty worktree state increases the risk of contaminating any cleanup/closeout commit."
  ],
  "noStagedFiles": true,
  "diffSummary": "No source diff was produced by this review; findings were recorded only in the required run summary file.",
  "reviewFindings": [
    "blocker: deskops/operations.py:338-350 - local `list tasks` uses filesystem inventory instead of `desk/tasks/Board.md` routing, so stale task files appear as active tasks.",
    "blocker: desk/tasks/task-enrich-templates-with-instructional-text.md:5,41 - the task still declares `active | complete`, so it remains visible despite not being routed.",
    "blocker: deskops/operations.py:477-479 with desk/routines/routine-task-enrich-templates-with-instructional-text.md:4-14 - this legacy task cannot reach current auto-close cleanup because it never sets `status: closed`.",
    "note: desk/tasks/Board.md:67 - board `## Notes` is stale prose and should not be treated as state; generated `## Task Details` is the structured board-derived view."
  ],
  "manualNotes": "Recommended clean truth: board frontmatter controls routing; task frontmatter controls lifecycle state only for routed tasks; board prose notes are commentary; git history is evidence, not state."
}
```