# Handoff: 2026-09-10 session — uncommitted work and open items

## Kind

handoff

## Status

resolved

open — nothing below is committed

## Resolution

Every item is closed: the uncommitted work is committed (store layout, Herdr runtime, the CLI fixes, the registry dedup), the extractor regression lives in sldb with its own tests, `deskops init` is fast, the registry no longer blocks inbox writes, the mindmap regression is fixed by reading declared containment and references as edges (47a5816), the two open inbox notes are closed, decision 3 is decided and its task was deleted with the pron worktree, and the untracked documents are tracked. The one finding left is the sldb-side reference to tests/test_section_body_extraction.py, reported to sldb's inbox.

## Problem

A long session changed deskops and sldb (and the setup repo) without committing, then moved focus away from deskops. This records what exists only in working trees and what is still open, so the work can be picked up without re-deriving it.

## Done, uncommitted

deskops (`git status` shows ~45 changed/new files):

- Herdr supervised runtime: `deskops runtime supervise`, `RuntimeProfileDoc` (`desk/runtimes/`), `RunDoc` (registered, nothing writes it yet), `RoleDoc` typed frontmatter, `ROLE_AGENT_SPECS` removed. Details: `desk/drawer/features/feature-herdr-supervised-execution-runtime.md`.
- Inbox note 20260827-160657: `deskops inbox --root`; `promote inbox-to-drawer-task` untracks the note before deleting it.
- Inbox note 20260827-164846: `advance task --to complete` also sets `status: closed`.
- `promote drawer-task-to-active-task` removed. It filled every required task field with generic placeholders. A drawer item now becomes a task only through `deskops add task`.
- `deskops add task --from-drawer <selector>`: stores the origin in an optional `TaskDoc.from_drawer` field, serialized only when set. Verified before/after across 109 tracked tasks in 13 stores machine-wide: zero hash changes, so no store needs migrating. It lives in its own field because `edit task <id> references` replaces the whole list.
- `cli/main.py`: `--root` validation no longer crashes when an optional `--root` is `None`.
- Suite: 273 passed, 0 failed.

sldb (4 files + 2 test files):

- `models add` wrote `hash_b: ""` for a model with zero documents, so `stores check` failed until `models update` ran. Fixed in `cli/commands/model.py` (the live path) and in `cli/commands/model_add.py` (dead code, never called).
- Serious: `core/data_extractor.py::_handle_section_body` marked the next section's heading as consumed whenever a section was empty, shifting every later section up by one and silently dropping content. Fixed; regression tests in `tests/test_section_body_extraction.py` fail without the fix.
- Suite: 450 passed; the one failure (`knowledge_surface.py`, three classes in one file) predates this session.

Outside the repos:

- `~/.claude/skills/deskops-workflow/` updated to drop the removed command and document `--from-drawer`. Backup: `~/.claude/skills-backup/deskops-workflow-20260910-110933`.
- The setup repo has its own findings in `setup/desk/drawer/`.

## Open

1. **Commit** deskops and sldb. `sldb/src/sldb/models/structured_doc.py` has an unrelated pre-existing change (`__containment__` / `__references__`) that is not part of this session.
2. **Possible past damage from the extractor bug.** The fix stops new corruption; it does not repair tasks already rewritten by `deskops edit` while the bug existed. Several stores report TaskDoc `data_mutation`: vitali 10, gemini_test 8, hcp 8, Matrix 8, TraderBot 3, AntonIA 1, apoe 1, AWS_Infra 1. Unverified whether that is (a) stored hashes reflecting the old buggy extraction of tasks with empty sections, or (b) older hand edits. Check by hashing those files with the pre-fix extractor. If (a), inspect the task files for shifted sections before running `sldb models update TaskDoc`.
3. **`deskops init` slowness**: `issue-deskops-init-spawns-one-process-per-model.md`.
4. **Registry cleanup blocks inbox writes.** `desk/registry/` holds 20 repository docs; only `repo-deskops.md` is real. Nine point at this repo's root, so `deskops inbox "<message>"` aborts with `Duplicate repository root`. Reading (`--list/--show/--ack`) works.
5. **Mindmap regression from the pre-session `__references__` diff**: `TaskDoc`, `BoardDoc` and `RitualDoc` declare `__references__`/`__containment__` without `routine` and `current_node`, so graph_ui stops drawing Task→Routine and Task→current-checklist edges (it only falls back to the legacy global field list for models that declare nothing).
6. **Inbox notes still open**: 20260827-165024 (`PillDoc` has no template marker for `status`, `summary`, `routine`, `current_node`, `history` — `edit pill ... status` reports success and persists nothing) and 20260907-125920 (terminal node `complete` deletes the task bundle before any atomic commit). The latter note's own frontmatter contains unresolved `⸢rev•acknowledged_by⸥` markers: the renderer leaves a marker literal when a `rev` field is `None`.
7. **Decision 3** in `question-herdr-runtime-open-decisions.md` (retarget `task-adhoc-subagent-launcher-tmux-multi-cli` onto Herdr) is decided but not implemented.
8. `deskops doctor` lists ~200 untracked documents, almost all `*-test` / `*-stress` leftovers.
