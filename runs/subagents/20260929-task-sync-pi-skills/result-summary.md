# Result summary — Executor run, task-sync-pi-skills

Run: 2026-09-29-task-sync-pi-skills
Role: fresh-context Executor (zero-context bundle: TaskDoc + 8 pills + 3 atoms + reference copy + existing removal guard)
Date: 2026-09-29

## Changes made (TaskDoc implementation path, 3 steps)

1. **`.pi/skills/use-deskops/SKILL.md`** — Replaced the stale CLI-surface line
   `deskops promote drawer-task-to-active-task <task-selector>` with the
   promotion line copied verbatim from the same block position of the
   already-fixed `.opencode/skills/use-deskops/SKILL.md`:
   `deskops add task --root . --from-drawer <drawer-selector> --title <title> --goal <goal> --scope <scope> --validation <check>`.
   Both blocks are code fences (no bullet style to adapt). The full flag form
   is documented; the bare `--from-drawer` form is not shown anywhere.

2. **`.pi/skills/deskops-task-lifecycle/SKILL.md`** — Rewrote Paso 2 step 2 in
   Spanish: author the active task from the drawer item with the full flag
   form `deskops add task --from-drawer task-<id> --title "..." --goal "..." --scope "..." --validation "..."`,
   note that `from_drawer` is recorded and the drawer file is kept for manual
   cleanup, and state (paraphrased, without the literal removed-command
   token) that direct drawer-to-active promotion was deliberately removed
   because mechanical conversion only filled fields with placeholders.
   Elided `...` placeholders kept; rest of the protocol (heading, step 1,
   Pasos 2.5–5, anti-patterns) untouched.

3. **`tests/test_skill_cli_drift.py`** (new) — Guard test that rglobs
   `SKILL.md` under `.pi/skills`, `.agents/skills`, and `.opencode/skills`
   (READMEs excluded by design; missing dirs count as empty), asserts at
   least one skill file is collected (never vacuous), asserts no skill file
   contains the removed-command token (forbidden everywhere, including
   removal mentions), and asserts `from-drawer` presence in exactly the two
   use-deskops copies (`.pi` and `.opencode`). The guard only asserts; it
   never mutates documents (pill-drift-checks-are-review-surfaces-not-mutators).

Pre-edit verifications (per preflight resolution 10): `git show --stat d35726a`
confirmed the removal commit touched only the `.opencode` skill copy, and
`tests/test_inbox_promote_cli_gaps.py::test_drawer_to_active_task_promotion_no_longer_exists`
passes unchanged.

## Validation evidence

Full outputs in `validation.log` (same directory). Summary:

| Check | Command | Result |
|---|---|---|
| Full suite | `python -m pytest` | PASS — 298 passed, including the 2 new drift-guard tests |
| Token absence | `grep -rn drawer-task-to-active-task .pi/skills .agents/skills .opencode/skills` | PASS — no hits (exit 1) |
| from-drawer documented (.pi) | `grep -c from-drawer .pi/skills/use-deskops/SKILL.md` | PASS — 1 (>= 1) |
| from-drawer documented (.opencode) | `grep -c from-drawer .opencode/skills/use-deskops/SKILL.md` | PASS — 1 (>= 1) |
| New guard test | `python -m pytest tests/test_skill_cli_drift.py tests/test_inbox_promote_cli_gaps.py -v` | PASS — 21 passed (2 new + 19 existing, incl. the removal guard) |
| Sandbox proof | `deskops desk install` + seeded drawer + `deskops add task --root .tmp/deskops-cli-test --from-drawer sandbox-loose-idea --title ... --goal ... --scope ... --validation pytest` | PASS — exit 0; bundle `task-sandbox-drawer-proof.md` authored with real field values (`from_drawer: desk/drawer/tasks/task-sandbox-loose-idea.md`, real title/goal/scope/validation); drawer file kept for manual cleanup; `deskops show task` reports `From drawer: desk/drawer/tasks/task-sandbox-loose-idea.md` |

## Scope discipline

- No CLI or `deskops/` code changes. No desk/inbox or desk/drawer/issues changes.
- No other `.pi` vs `.opencode` divergences harmonized (the two copies keep
  their pre-existing differences outside the one promotion line).
- No `git commit` (executor rule): nothing staged; the working tree carries
  the changes only. Closure goes through `deskops closeout verify` /
  `deskops closeout commit` by the supervisor.
- Sandbox residue: `.tmp/deskops-cli-test/` (gitignored, disposable) kept as
  inspectable proof; safe to delete.

## Deviations / notes

- Test-doc wording: the guard test's docstring and failure message say
  "agent-facing skills" rather than "tracked skills", because the whole
  `.pi/` tree is gitignored (`.gitignore:10`); `.agents/` and `.opencode/`
  are git-tracked. The TaskDoc/preflight language used "tracked" loosely;
  the guard reads on-disk skill surfaces regardless of git tracking, and the
  docstring records this explicitly.
- `deskops desk install <path>` requires the target directory to exist first
  (the proof created it with `mkdir -p` before installing). Minor operator
  friction, not a documented-path failure; noted for the supervisor to route
  if it should become tracked work (pill-cli-gaps-become-tracked-work).
- No blockers. All done-when conditions observable and met.