# Preflight comprehension gate — task-sync-pi-skills

Run: 2026-09-29-task-sync-pi-skills
Gate: zero-context TaskDoc-only restatement (agent: delegate, fresh context)
Result: PASS with findings — restatement reproduced intent; ambiguities resolved in TaskDoc before Executor dispatch.

## Subagent restatement (verbatim)

1. `.pi/skills/use-deskops/SKILL.md` — replace the stale CLI line (line 125) listing `deskops promote drawer-task-to-active-task <task-selector>` with `deskops add task --root . --from-drawer <drawer-selector> --title <title> --goal <goal> --scope <scope> --validation <check>`, mirroring the already-fixed `.opencode` copy.
2. `.pi/skills/deskops-task-lifecycle/SKILL.md` — rewrite step 2 of "Paso 2: Promoción y Commit de Preparación" to author the active task from the drawer item via `deskops add task --from-drawer task-<id> ...`; note the drawer file is kept for manual cleanup and that `promote drawer-task-to-active-task` was deliberately removed; leave the rest of the protocol intact.
3. Add `tests/test_skill_cli_drift.py` — walk every `SKILL.md` under `.pi/skills/` and `.agents/skills/`, assert none contains the string `drawer-task-to-active-task`; also assert `.pi/skills/use-deskops/SKILL.md` documents `--from-drawer`.
4. Validate: `pytest` (full suite green); `grep -rn drawer-task-to-active-task .pi .agents` → no hits; `grep -c from-drawer .pi/skills/use-deskops/SKILL.md` → ≥ 1.
5. Explicitly out of scope: sldb inbox note and spec/ packaging gap; other `.pi` vs `.opencode` divergences; historical mentions in `runs/`, `desk/inbox/`, `desk/drawer/issues/`; any CLI or `deskops/` code changes.

## Ambiguities reported and their resolution (TaskDoc updated before dispatch)

1. `.agents/skills/` existence unestablished → RESOLVED: it exists (`.agents/skills/subagent-execution/SKILL.md`); guard test walks it; missing dirs are treated as empty, and the test asserts it collected at least one skill file so it can never pass vacuously.
2. Grep-scope conflict (`.pi .agents` trees vs SKILL.md-only scan) → RESOLVED: validation and guard test share one scope: all files under `.pi/skills/`, `.agents/skills/`, and `.opencode/skills/`.
3. Replacement-line formatting unstated → RESOLVED: copy the promotion line verbatim from the CLI surface block of `.opencode/skills/use-deskops/SKILL.md` (same block position).
4. Lifecycle rewrite language / `--root` inconsistency → RESOLVED: rewrite in Spanish (doc's own language), command mirrors the old line's style without `--root`: `deskops add task --from-drawer task-<id> --title "..." --goal "..." --scope "..." --validation "..."`.
5. Placeholder elision → RESOLVED: keep elided `...` placeholders as the old doc did; no worked example.
6. Test conventions → RESOLVED: paths resolve from `Path(__file__).resolve().parents[1]`; recursive `rglob("SKILL.md")`; missing dir = empty; fail with a clear message if zero skill files collected.
7. `.opencode/skills/` excluded from guard → RESOLVED: include `.opencode/skills/` in the guard test scope; also assert both use-deskops copies (`.pi` and `.opencode`) document `--from-drawer`.
8. No commit instruction → RESOLVED: the Executor does not commit; closure goes through the closeout ritual (`deskops closeout verify` + `deskops closeout commit`) by the supervisor.
9. Line anchors may drift → RESOLVED: locate stale text by content, not line number.
10. Unverifiable references under document-only review → RESOLVED: Executor verifies `git show --stat d35726a` and the existing guard test before editing.
