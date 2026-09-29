# Cold review — task-sync-pi-skills

Run: 2026-09-29-task-sync-pi-skills
Reviewer: fresh-context delegate, no prior task context. Bundle: TaskDoc, 8 pills, 3 atoms, target files, .opencode reference copy, existing removal test, AGENTS.md rules.
Verdict: fix-task-doc-first (3 substantive findings + 4 minor) → all resolved before Executor dispatch.

## Findings → resolutions

1. Step 2 command under-specified (bare `--from-drawer` form invites placeholder regression) → implementation-path now requires the full flag form and forbids documenting the bare form.
2. Documented command never executed → validation now includes a `.tmp/deskops-cli-test` sandbox run of `deskops add task --from-drawer` proving the operator path (pill-real-cli-surfaces-prove-operator-contracts).
3. Guard scope narrower than validation scope → guard test now rglobs SKILL.md under `.pi/skills`, `.agents/skills`, `.opencode/skills`; README exclusion stated explicitly.
4. Atoms in `references` conflated surfaces → moved the three input atoms to the `atoms` frontmatter field; `references` reserved for closeout graduation.
5. Placeholder frontmatter → `summary` and `task_type: implementation` filled.
6. Missed pill `pill-drift-checks-are-review-surfaces-not-mutators` → bound; the guard test only asserts (review surface), never mutates.
7. Missed pill `pill-closeout-knowledge-gates-require-traceable-evidence` → bound; closure goes through `deskops closeout verify` with resolvable evidence.

Reviewer-verified facts: stale lines at .pi/skills/use-deskops/SKILL.md:125 and .pi/skills/deskops-task-lifecycle/SKILL.md:50; `add task --from-drawer`, `closeout verify`, `closeout commit` exist; drawer-kept-for-cleanup matches operations.py; .agents/skills/subagent-execution/SKILL.md exists (guard non-vacuous).
