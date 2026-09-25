# Cold review — task-doctor-proposes-missing-model-registration

Scope: task bundle only (task doc, Board.md, 5 pills, doctor.py; desk.py/bootstrap.py as reference). Empirical checks ran `deskops doctor` on disposable `/tmp` fixtures only; repo untouched.

## Review

- **Correct**: The reuse decisions are sound and evidence-backed. `desk.py:137` and `desk.py:218` already call `bootstrap._registered_model_names` and `init_local_store`, so "reuse, don't reimplement" has precedent; the doctor/store-boundary pill's "call into SLDB, do not duplicate logic" is honored. Proposal naming `deskops desk update --apply` verbatim honors the real-CLI-surfaces pill. Reference-only pinning of `desk.py`/`bootstrap.py` is sufficient — both contain everything needed (wording at `desk.py:199-200`, helpers at `bootstrap.py:103` and `bootstrap.py:164`).
- **Blocker**: Task doc claims "Open Ambiguities: None", but two implementation-shaping ambiguities remain (check placement vs stated guard; repair-failure handling). See findings 1–2 below. Resolve in the task doc before implementation starts.
- **Note**: Verified pre-existing crash in the file to edit: `deskops doctor` on a root without `desk/` fails with `Unexpected: cannot access local variable 'unreadable_docs' where it is not associated with a value` (reproduced on `/tmp/coldrev-empty`). Cause: `unreadable_docs` is defined only inside `if desk_dir.exists():` (`doctor.py:112`) but read outside it (`doctor.py:147`). The pinned test target "`.sldb` absent → check skipped" will collide with this if the fixture lacks `desk/`.
- **Note**: `doctor.py:75/77` — `tracked_mds` assigned then immediately shadowed. Pre-existing dead assignment inside the function being modified; out of scope, do not drive-by-fix.

## 1. Ambiguities the task does not resolve

1. **(Blocker) Check placement contradicts the stated guard.** Resolved decision: "Unregistered models are only checked when `.sldb` exists, matching the guard used by `deskops desk update`." But `desk.py:135` guards at root level, while all of doctor's store checks (including the `sldb stores check` subprocess at `doctor.py:80`) are nested inside `if desk_dir.exists():` (`doctor.py:58`). Placing the new check at the natural spot (next to the stores-check) means a workspace with `.sldb` present but `desk/` absent silently skips the check — violating the stated guard. Root-level placement restructures the function. The task must pin placement explicitly.
2. **(Blocker) Repair-failure path is unspecified.** `SLDBBootstrap.init_local_store` returns `1` silently on failure — it swallows `RuntimeError` without printing (`bootstrap.py:111-113`, `117-119`, `127-129`). The task pins "`--repair` … mirrors doctor's existing repaired/manual-repair accounting" (`doctor.py:178` string-matches `"Manual repair required"`), but does not pin: whether a failed repair appends a "Manual repair required … `deskops desk update --apply`" line for this finding, whether the failure detail is printed, or which mode (dry-run vs `--repair`) emits the proposal line. Literal reading risk: if the proposal line is emitted unconditionally rather than only in dry-run, the accounting denominator inflates and a *successful* `--repair` still exits 1 with "Some issues could not be repaired automatically."
3. **"Repairs only this finding (not the other findings)" vs existing behavior.** Current `--repair` already auto-scaffolds missing desk structure (`doctor.py:36-39`). Read literally, the pin says remove that; plausibly it means "adds repair only for this finding, keeping existing repairs." Unresolved; affects exit-code accounting.
4. **Exception scope of "index cannot be read".** `_registered_model_names` raises `RuntimeError` on the sldb-importable path, but the fallback path can raise `json.JSONDecodeError` (`bootstrap.py:177`, not a `RuntimeError`) or `KeyError` (`entry["name"]`). The pin doesn't say what counts as "cannot be read" (catch `RuntimeError` only vs broad `except Exception` as `desk.py:136-139` does).
5. **Name ordering tension.** Finding wording "mirrors `deskops desk update`" (`desk.py:199-200` emits `MODEL_REFS` insertion order) while the pin demands a sorted set difference. Same wording, different order between the two surfaces. Trivial, but the doc asserts both.

## 2. Missing guardrails / failure modes the plan does not cover

1. **(Verified) Pre-existing `UnboundLocalError` on desk-less roots** (`doctor.py:112` vs `doctor.py:147`; reproduced: `python -m deskops doctor --root /tmp/empty` → exit 1, "Unexpected: cannot access local variable 'unreadable_docs'"). The new check and its `.sldb`-absent test target interact with exactly this path. Task must decide: fix in scope (doctor.py is the only file edited, so allowed) or pin all fixtures to include `desk/`.
2. **(Verified) Missing-store parity gap.** Empirically, on a desk with no `.sldb`: dry run → "SLDB store check crashed … No store_index.yaml" exit 1; `--repair` → "Some issues could not be repaired automatically." exit 1. Doctor never bootstraps a missing store, while `desk update --apply` treats a missing store as *all* models unregistered and initializes it (`desk.py:135-144`, `217-218`). The task's "matching the guard used by `deskops desk update`" matches only the registered-names *query*, not the *repair* semantics. The proposal text should not imply the two commands behave identically; the doc should acknowledge the gap.
3. **Crash-finding coverage claim is narrower than stated.** The "store-check-crash" finding fires only on `returncode != 0 and not stdout` (`doctor.py:108`). If `sldb stores check` succeeds (stdout present) but `load_store_index` fails inside doctor's process, neither the crash finding nor the unregistered finding fires — the state is silently unchecked, contradicting the skip rationale.
4. **Partial-repair failure mode.** `init_local_store` registers models in a loop; failure on model N leaves 1..N-1 registered while doctor's accounting treats the whole finding as unrepaired. The idempotency test target covers only the success path; no test target for repair-failure accounting (ties to ambiguity 2).
5. **Output interleaving unpinned.** `init_local_store` prints "Local store already exists…" / "Registering X in …" directly to stdout (`bootstrap.py:104-125`), interleaving with doctor's "Doctor Findings:" / "Repairs applied:" blocks. The doc claims the pins answer the "CLI output contract"; this is unpinned (cosmetic).
6. **Sandbox policy unnamed.** Planned validation says "sandboxed CLI runs … on a test fixture" but doesn't name the sandbox root. AGENTS.md and the sandbox-desk atom require a disposable sandbox (e.g. `.tmp/deskops-cli-test`); pin it so `--repair` provably cannot touch the repo's real `.sldb`.
7. **Test-target feasibility unverified.** "Unreadable index → check skipped" requires simulating an index-load failure; the existing `tests/` doctor fixtures were outside this review's file scope, so feasibility of that fixture was not verified. Flag before implementation.

## 3. Pills plausibly matching but not bound

Task binds 5 pills; board routes 8. Selection criteria for which board pills to re-bind are unstated, making the following omissions ambiguous-but-plausible misses:

1. **`desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md`** (not on board, not bound) — strongest miss. `when`: "designs drift checks … or review records"; `where`: "drift CLI design … any future automation that proposes follow-up tasks"; `how_not`: "**Do not collapse review, decision, and mutation into one implicit step**." `doctor --repair` collapses finding + mutation into one invocation. The task's resolved decisions (read-only default, additive idempotent repair via existing bootstrap path) effectively *satisfy* this pill, but the pill is unbound and its `how_not` is never addressed in the doc.
2. **`desk/contexts/pill-zero-context-preflight-precedes-executor.md`** (not on board, not bound) — `when`: "whenever an active desk task enters execution and before the real Executor launch"; `where`: evidence under `runs/subagents/<run-dir>/preflight.md`. Directly matches this task's entry into execution; this cold review is preflight-shaped but the task pins no preflight evidence path.
3. **`desk/contexts/pill-005-subagent-execution.md`** (board-routed, not in task frontmatter) — `when`: "whenever an active task enters execution, especially when the board contains multiple parallel-ready tasks in the same phase" (board has two tasks). The task binds exactly two of the board's eight pills (pill-001, pill-007) with no stated selection rule: either board pills are auto-inherited (then explicitly binding pill-001/pill-007 is redundant) or per-task selection is intended (then pill-005's omission is a gap). The binding policy itself is ambiguous.
4. **`desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`** (board-routed, not task-bound) — `when`: "binds implementation-heavy pills … introduces a feature rule, or closes out work that refined project knowledge". The task defers docs/atoms capture to the closeout ritual but binds no graduation gate; binding it (or stating board-level inheritance) would make the closeout obligation explicit.

Considered and rejected as too weak a match: pill-006 (store layout refactor — no `.sldb` file moves), pill-list-surfaces (not a list surface), pill-machine-readable-cli-output (no `--format` change), pill-project-local-config (no root/sandbox *behavior* change), pill-closeout-knowledge-gates (closeout validation unchanged), pill-ready-phases / pill-phase-closeout / pill-board-routed-pills (board/phase-level, not task-level).

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Findings with file:line citations and severity delivered in cold-review.md: 2 blockers (check placement vs guard contradiction; unspecified repair-failure path), 3 further ambiguities, 7 guardrails/failure modes (2 empirically verified on /tmp fixtures), 4 unbound-pill matches with when/where/how_not evidence."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "python -m deskops doctor --root /tmp/coldrev-empty",
      "result": "passed",
      "summary": "Reproduced pre-existing UnboundLocalError ('unreadable_docs') on desk-less root, exit 1"
    },
    {
      "command": "python -m deskops desk install /tmp/coldrev-desk && python -m deskops doctor --root /tmp/coldrev-desk [--repair]",
      "result": "passed",
      "summary": "Verified doctor --repair cannot repair missing .sldb ('Some issues could not be repaired automatically', exit 1) while desk update --apply bootstraps it"
    },
    {
      "command": "grep -n (key lines in doctor.py / desk.py / bootstrap.py)",
      "result": "passed",
      "summary": "Pinned exact line numbers for all citations"
    }
  ],
  "validationOutput": [
    "doctor on empty root: 'Unexpected: cannot access local variable unreadable_docs' exit=1",
    "doctor dry run on desk-without-.sldb: 'SLDB store check crashed ... No store_index.yaml' exit=1",
    "doctor --repair on desk-without-.sldb: 'Some issues could not be repaired automatically.' exit=1"
  ],
  "residualRisks": [
    "Existing doctor tests/fixtures in tests/ were outside the mandated review scope; feasibility of the pinned 'unreadable index -> check skipped' fixture was not verified",
    "Task doc's 'Open Ambiguities: None' claim is contradicted by findings 1-2; parent must amend the task doc before dispatching the executor"
  ],
  "noStagedFiles": true,
  "diffSummary": "Review-only task; no files changed. Repo untouched; all CLI probes ran against disposable /tmp fixtures.",
  "reviewFindings": [
    "blocker: desk/tasks/task-doctor-proposes-missing-model-registration.md - check placement contradicts stated guard (desk.py:135 root-level vs doctor.py:58/80 nested under desk-exists); pin placement before implementation",
    "blocker: desk/tasks/task-doctor-proposes-missing-model-registration.md - repair-failure path unspecified: init_local_store fails silently (bootstrap.py:111-129) and no manual-repair fallback is pinned; accounting heuristic doctor.py:178 can misreport a successful repair as unrepaired depending on proposal-line placement",
    "note: deskops/cli/commands/doctor.py:112 vs :147 - pre-existing UnboundLocalError when desk/ absent (reproduced); interacts with pinned '.sldb absent' test target",
    "note: doctor --repair cannot bootstrap a missing .sldb while desk update --apply can (verified); doc should acknowledge parity gap",
    "note: crash-finding coverage (doctor.py:108) does not cover in-process load_store_index failure when stores-check stdout is present",
    "note: exception scope for 'index cannot be read' unpinned (RuntimeError vs JSONDecodeError/KeyError at bootstrap.py:177)",
    "note: bootstrap stdout interleaving (bootstrap.py:104-125) unpinned in CLI output contract",
    "note: 'sorted' pin vs desk.py:199-200 insertion order - cosmetic divergence from the surface the wording claims to mirror",
    "note: sandbox location/policy for planned CLI validation unnamed (AGENTS.md sandbox-desk atom)",
    "note: pill-drift-checks-are-review-surfaces-not-mutators how_not ('do not collapse review, decision, and mutation') is directly implicated by doctor --repair and unbound",
    "note: pill-zero-context-preflight-precedes-executor, pill-005-subagent-execution, pill-durable-pill-knowledge-graduates-to-atoms-at-closeout plausibly match and are unbound; pill binding policy (board-inherited vs per-task) is itself ambiguous since only 2 of 8 board pills are task-bound"
  ],
  "manualNotes": "Cold review only; no code edits per task instructions. Empirical probes used disposable /tmp fixtures (/tmp/coldrev-empty, /tmp/coldrev-desk), not the repo desk. The two blockers are task-doc amendments, not code bugs. Also flagged: doctor.py:75/77 tracked_mds shadowing is pre-existing and must not be drive-by-fixed under the minimal-change pin."
}
```
