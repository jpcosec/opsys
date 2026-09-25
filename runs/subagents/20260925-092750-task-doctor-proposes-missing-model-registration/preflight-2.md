# Zero-context preflight comprehension gate — second pass

Source read (only): `desk/tasks/task-doctor-proposes-missing-model-registration.md`

## 1. Step-by-step restatement of intended work

1. Add a new check to `deskops doctor` (`deskops/cli/commands/doctor.py` — the only file edited) that compares the keys of `MODEL_REFS` against the models registered in the local store and reports any missing ones as a doctor finding.
2. Store inspection reuses `SLDBBootstrap._registered_model_names` and `MODEL_REFS`; no doctor-local store-introspection logic.
3. Finding format: a single line `Unregistered models: <names>` (names = exact sorted set difference of `MODEL_REFS` keys minus registered names; lexicographic sort). Mirrors the wording `deskops desk update` already prints on dry run.
4. Proposal text must name the runnable repair command verbatim: `deskops desk update --apply` (real CLI surface, no duplicated registration logic, per the doctor/store-boundary pill).
5. Guards for the check:
   - Skip entirely when `.sldb` does not exist (same guard `deskops desk update` uses).
   - Skip when the local store index fails to load (the existing store-check-crash finding already covers that unknown state).
   - Extra registered models not present in `MODEL_REFS` are out of scope.
6. New `doctor --repair` behavior (or repair mode of the finding): performs the repair by invoking `SLDBBootstrap.init_local_store` — the same code path `deskops desk update --apply` uses — which additively, idempotently, and non-destructively registers missing models. It does not register via new doctor-local logic. `--repair` repairs only this finding, not doctor's other findings, and mirrors doctor's existing repaired/manual-repair accounting (finding counts as repaired or as manual-repair-needed).
7. Contract participation: plain `doctor` still exits non-zero when any findings exist (including the new one); default mode remains read-only reporting.
8. Tests mirror the existing doctor test file under `tests/`, covering: (a) missing model → finding with the `deskops desk update --apply` proposal; (b) unreadable store index → check skipped; (c) `.sldb` absent → check skipped; (d) `--repair` registers missing models and is idempotent on a second run.
9. Validation: repo-standard `pytest`, plus a sandboxed CLI run of `deskops doctor` (dry run and `--repair`) against a test fixture outside this repo's real `desk/`.
10. Out of scope: edits to `desk.py` and `bootstrap.py` (reference-only, read to reuse helpers and mirror wording); extra registered models; docs/atoms capture (deferred to closeout ritual).

## 2. Ambiguities, gaps, and guesses still required

| # | Item | Severity | Note |
|---|------|----------|------|
| A1 | Insertion point/ordering of the new check among doctor's existing checks (findings output order) | minor | Cosmetic; not pinned. Any position that keeps contract behavior is acceptable. |
| A2 | Mapping of finding line + proposal onto doctor's concrete finding data structure (title/detail/proposal fields) | minor | Wording is pinned but the field mapping is inferable only by reading `doctor.py`. Bounded: file is listed under `files:`. |
| A3 | Test file name/location | minor | "Mirror the existing doctor test file in `tests/`" requires discovering the actual filename. Bounded discovery. |
| A4 | Method to construct the fixture state "store missing a model registration" for pytest and the sandbox CLI validation (monkeypatch `MODEL_REFS`, hand-edit store registry files, vs. create-then-unregister) | minor | Intent is unambiguous (registered set lacks a `MODEL_REFS` key); construction mechanism is a test detail not pinned. Slight risk the sandbox dry-run fixture is trickier than expected. |
| A5 | Sequencing of the check within `--repair` flow (check-then-repair position relative to other repair steps) | minor | Implied (report then repair via `init_local_store`) but the exact position is left to reading existing code. |
| A6 | Exit-code behavior of `doctor --repair` when this finding is repaired but other findings remain | minor | "Mirrors existing repaired/manual-repair accounting" defers to existing code; no explicit statement. Bounded by reading `doctor.py`. |
| A7 | Which API call counts as "local store index loads successfully" | minor | Discoverable from `bootstrap.py`/`desk.py` reference surfaces; not named in the doc. |
| A8 | Store path resolution for doctor (cwd `.sldb` vs. desk-root-derived) | minor | "Matching the guard used by `deskops desk update`" defers resolution to `desk.py`. Bounded. |
| A9 | Wording precedence if `desk update`'s literal message differs from the doc's quoted `Unregistered models: <names>` | minor | Pin says wording mirrors `desk update` and also gives the literal string. If code differs, implementer must pick; likely code wins ("mirrors"). |

None of these are intent-level guesses. All are bounded discovery inside the three referenced files (`doctor.py`, `desk.py`, `bootstrap.py`) plus naming details. The task's own "Open Ambiguities: None" claim holds for every substantive decision: finding format, proposal wording, set-difference definition, read-only default, `--repair` code path and scope, guards, reference-only files, CLI output contract, test targets, and validation steps are all pinned.

## Verdict

PASS for execution-without-guesswork.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "9 concrete residual items (A1–A9) with source file paths and minor severity listed in the findings table of this report; no blocker-severity items."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read desk/tasks/task-doctor-proposes-missing-model-registration.md",
      "result": "passed",
      "summary": "Single-file read per zero-context gate; no repo exploration."
    }
  ],
  "validationOutput": [
    "Comprehension gate: task doc restated with full fidelity; all substantive decisions pinned; residual items are bounded discovery, not intent-level guesses."
  ],
  "residualRisks": [
    "A4: method to construct the 'store missing a model registration' fixture state for pytest and sandbox CLI validation is unpinned (minor).",
    "A9: wording precedence if desk update's literal message differs from the doc's quoted 'Unregistered models: <names>' (minor).",
    "A2/A6/A7: finding data-structure mapping, --repair exit-code accounting with other findings, and index-load API depend on reading doctor.py/bootstrap.py/desk.py (bounded, minor)."
  ],
  "noStagedFiles": true,
  "diffSummary": "No code changes; review-findings only, written to this preflight-2 report.",
  "reviewFindings": [
    "minor: task doc — check insertion point/ordering among doctor's existing checks unpinned (A1)",
    "minor: task doc — finding line/proposal mapping onto doctor's finding data structure inferable only from doctor.py (A2)",
    "minor: task doc — pytest test filename must be discovered from tests/ (A3)",
    "minor: task doc — fixture-state construction method for 'store missing model registration' unpinned (A4)",
    "minor: task doc — check position within --repair flow implied but not pinned (A5)",
    "minor: task doc — --repair exit-code behavior with remaining other findings defers to existing accounting (A6)",
    "minor: task doc — 'store index loads successfully' API not named; discoverable from reference files (A7)",
    "minor: task doc — store path resolution defers to desk update's guard in desk.py (A8)",
    "minor: task doc — wording precedence between quoted literal and actual desk update message unspecified (A9)",
    "no blockers"
  ],
  "manualNotes": "Verdict: PASS for execution-without-guesswork. The doc's 'Open Ambiguities: None' claim holds for substantive decisions (finding format, proposal wording verbatim 'deskops desk update --apply', sorted set difference, read-only default, --repair via init_local_store, both guards, reference-only desk.py/bootstrap.py, test targets, pytest + sandboxed CLI validation). Residual items A1-A9 are minor and resolvable by reading the three files listed under files:."
}
```
