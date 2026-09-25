# Preflight comprehension report — task-doctor-proposes-missing-model-registration

Source read (only file read, per gate): `desk/tasks/task-doctor-proposes-missing-model-registration.md`

## 1. Step-by-step restatement of intended work

1. **Background failure mode.** In a downstream deskops project, the local `.sldb` store was created before `RoutineDoc` existed in `MODEL_REFS`. `deskops add task` then failed because `RoutineDoc` was not registered in that store; tasks could not become active and stayed in the drawer.
2. **Existing detection gap.** `deskops doctor` already reports drift in that project but never compares `MODEL_REFS` against the store's registered models, so it never names the unregistered-model gap or proposes a repair.
3. **Existing repair path (already built).** `deskops desk update` already detects this: dry run prints `Unregistered models: ...`; `--apply` calls `bootstrap.init_local_store`, which registers missing models, tracks/untracks docs, and refreshes indexes.
4. **Primary change.** Add to `deskops doctor` a check for models present in `MODEL_REFS` but not registered in the local store, reported as a finding whose proposal names the runnable repair command `deskops desk update --apply` (real CLI surface, per the doctor/store-boundary pill) rather than duplicating registration logic.
5. **Second surface.** Add `doctor --repair`, which performs the repair by calling the same `SLDBBootstrap.init_local_store` code path that `deskops desk update --apply` uses. It must be additive, idempotent, and non-destructive; no doctor-local registration logic.
6. **Guards for the new check.**
   - Run the unregistered-models check only when the local store index loads successfully; if the index cannot be read, skip the finding (the existing store-check-crash finding already covers that unknown state).
   - Only run the check when `.sldb` exists, matching the guard used by `deskops desk update`.
7. **Default mode stays read-only.** A plain `deskops doctor` run reports the finding + proposal only; it does not mutate the store.
8. **Implementation constraint.** Reuse `SLDBBootstrap._registered_model_names` and `MODEL_REFS`; do not re-implement store inspection inside doctor.
9. **Files listed in frontmatter.** `deskops/cli/commands/doctor.py`, `deskops/cli/commands/desk.py`, `deskops/bootstrap.py`. Bound pills: `pill-doctor-separates-desk-repair-from-sldb-health`, `pill-real-cli-surfaces-prove-operator-contracts`, `pill-cli-gaps-become-tracked-work`.
10. **Doc's own claim.** "Open Ambiguities: None" — the two former ambiguities were resolved into Resolved Decisions. My strict review below still finds execution gaps the doc does not pin down.

## 2. Ambiguities, gaps, and guesses required to execute (strict)

Severity: blocker = cannot proceed correctly without a decision or convention lookup; major = must guess something user-visible; minor = low-risk convention fill-in.

- **[major] Finding surface format is unspecified.** No finding code/identifier, no message wording, no severity level (error vs warning), and no position in doctor's check ordering. I would have to copy the format of existing findings in `doctor.py` by inspection — not pinned in the doc.
- **[major] Test targets not named.** No test file paths or test-case list. Expected cases I would invent: store missing a model → finding reported with proposal; index unreadable → check skipped; `.sldb` absent → check skipped; `--repair` registers missing models and is idempotent on second run; default mode does not mutate the store. None are pinned.
- **[major] Scope of `doctor --repair` is underspecified.** Does `--repair` fix only the unregistered-model finding, or act as a general repair flag for other findings? Does it re-run checks afterward and report post-repair state? Does its output mirror `desk update --apply` output? Not pinned.
- **[major] Role of `deskops/cli/commands/desk.py` and `deskops/bootstrap.py` in `files:` is unexplained.** No stated change to either (bootstrap is to be reused, presumably read-only; desk.py maybe for message alignment or shared-helper extraction). I would have to guess whether they are reference-only or must be edited — risk of unintended scope creep or of missing a required refactor.
- **[major] CLI output contract not pinned.** Whether doctor exits non-zero when findings exist, whether the new finding is counted in any summary/counts, and whether doctor has a machine-readable/JSON output mode that must also include the new finding.
- **[medium] Comparison semantics not spelled out.** Presumed exact set difference `MODEL_REFS` keys minus registered names; ordering of multiple missing models (sorted?) is unstated. Whether extra registered models not in `MODEL_REFS` should also be flagged is implied out of scope but never stated.
- **[medium] Postconditions of `--repair` not enumerated.** "Same code path as `desk update --apply`" implies index refresh and track/untrack also happen via `init_local_store`, but the doc does not say whether doctor must verify post-repair registration or report success criteria.
- **[medium] Acceptance/validation steps not given.** Beyond the repo-standard `pytest`, no explicit commands (e.g., sandbox-desk CLI run per the CLI-mutation-sandbox rule, or a manual repro). Which CLI validation is required is a guess.
- **[minor] Failure handling for `--repair` itself.** What doctor should print/return if `init_local_store` raises during repair is unspecified.
- **[minor] Identifier of the referenced "store-check-crash finding".** The doc references it by description only; its actual code/name in `doctor.py` is not given.
- **[minor] Docs/atoms updates.** Repo rules say docs materialize atoms; the task says nothing about updating README/docs/faq doctor descriptions, or whether a new atom/pill capture is required at closeout.
- **[minor] Exact proposal wording.** Must the proposal string name `deskops desk update --apply` verbatim, and should it also mention `doctor --repair` as an alternative? Not pinned.
- **[minor] Process gates.** Status transitions, commit conventions, and closeout ritual are governed by repo rituals, not restated in the task doc (acceptable, but not pinned here).

## Verdict

The task's intent and guardrails are clear enough to restate faithfully, but it is not fully self-sufficient for a zero-context executor: finding format, test targets, `--repair` scope/output contract, and the roles of `desk.py`/`bootstrap.py` all require convention lookup in the codebase or a supervisor decision before implementation.
