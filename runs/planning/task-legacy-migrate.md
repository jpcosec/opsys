# Implementation Plan

## Goal
Make deskops explicitly detect legacy/hand-rolled `desk/` layouts (distinct from empty and from modeled-current), report which modeled surfaces are missing or malformed, and offer a preservation-first migration path into the current workspace contract.

## Context Read
- Task: `desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md`
- Pills: legacy-formats-need-explicit-adaptation, doctor-separates-desk-repair-from-sldb-health, list-surfaces-must-expose-malformed-docs, project-local-config-carries-version-and-sandbox-policy, real-cli-surfaces-prove-operator-contracts
- Source surfaces: `deskops/workspace.py`, `deskops/config.py`, `deskops/cli/commands/doctor.py`, `deskops/cli/commands/desk.py`, `deskops/cli/parser.py`

## Existing state (relevant)
- `deskops/config.py` already defines `DeskConfig` with `versions.desk_format` / `model_version` and `sandbox` policy, loaded from `desk/config.json` (+ `config.local.json`).
- `deskops/workspace.py` scaffolds a fresh desk and writes `config.json` with `desk_format: "1.0.0"`.
- `deskops/cli/commands/doctor.py` already detects missing desk structure, untracked docs, and invalid docs via `sldb stores check`. It does NOT classify "legacy vs empty vs current" and has no migration path.
- `doctor` is wired in `parser.py::_add_doctor_command` with `--root` and `--repair`.

## Tasks
1. **Define workspace classification** in `deskops/workspace.py`.
   - Add a `classify_desk(root: Path)` returning one of: `absent`, `empty`, `legacy`, `current`.
   - Rules: `absent` = no `desk/`; `empty` = `desk/` with no board/task/pill docs; `current` = presence of `desk/config.json` with a recognized `desk_format` AND modeled Board/Task/pill docs that validate; `legacy` = desk has authored workflow docs (Board.md/tasks/pills) but fails current model validation OR lacks `config.json`/`desk_format`.
   - Acceptance: unit test constructs each fixture layout and asserts the returned class.

2. **Add legacy detection report** (which modeled surfaces missing/malformed).
   - File: `deskops/workspace.py` (helper) consumed by `doctor.py`.
   - Reuse the `sldb stores check --format json` invalid-doc collection already in `doctor.py`; extend to also flag "present but unmodeled" board/task/pill files and missing `config.json`/version.
   - Honor pill `list-surfaces-must-expose-malformed-docs`: malformed docs surface as findings, never silently skipped; keep `empty` distinct from `legacy`.
   - Acceptance: `deskops doctor --root <legacy-fixture>` prints a "Legacy desk detected" finding listing missing/malformed surfaces and exits non-zero.

3. **Add migration/adoption command surface** (preservation-first).
   - Decision needed (see Ambiguities): either extend `doctor --repair` or add a dedicated `deskops desk migrate` / `deskops migrate` subcommand.
   - If new subcommand: add parser wiring in `deskops/cli/parser.py` (mirror `_add_doctor_command`), a handler in `deskops/cli/commands/desk.py` (or new `migrate.py`), and register it in `deskops/cli/main.py` dispatch.
   - Behavior: scaffold ONLY missing modeled surfaces (reuse `scaffold_desk`'s `_write_if_missing` non-destructive pattern), write/patch `config.json` with `desk_format`, and NEVER overwrite authored Board/task/pill content. Emit a report of adopted vs preserved vs still-manual items.
   - Acceptance: running migrate on a legacy fixture leaves authored files byte-identical, adds missing config/version + missing scaffold docs, and re-classifies the desk toward `current` (or reports remaining manual steps).

4. **Wire config/version contract into classification** (`pill-project-local-config-carries-version-and-sandbox-policy`).
   - File: `deskops/config.py` + `deskops/workspace.py`.
   - Treat missing `desk_format` or an unrecognized version as a legacy marker; migration writes the current `desk_format` into tracked `config.json` (not `config.local.json`).
   - Acceptance: a desk with authored docs but no `config.json` classifies as `legacy`; after migrate it carries `desk_format`.

5. **Keep desk repair vs SLDB health separated** (`pill-doctor-separates-desk-repair-from-sldb-health`).
   - In `doctor.py`, keep desk-structure/legacy findings desk-owned; continue delegating store/infra checks to `sldb stores check` rather than reimplementing validation.
   - Acceptance: no new local reimplementation of store health; SLDB delegation path unchanged.

6. **CLI-level tests** (`pill-real-cli-surfaces-prove-operator-contracts`).
   - File: `tests/test_cli.py` (add cases) — verify through the real command path: doctor classifies legacy vs empty vs current; migrate is non-destructive; exit codes correct.
   - Acceptance: `pytest` green; at least one CLI-level assertion per new behavior (output + exit code).

## Files to Modify
- `deskops/workspace.py` — add `classify_desk` + legacy-surface report helpers; reuse non-destructive scaffold.
- `deskops/cli/commands/doctor.py` — emit legacy classification findings.
- `deskops/config.py` — treat missing/unknown `desk_format` as legacy signal; support writing version on migrate.
- `deskops/cli/parser.py` — wire migration surface (if a new subcommand is chosen).
- `deskops/cli/main.py` — dispatch new subcommand (if chosen).
- `tests/test_cli.py` — CLI-level coverage.

## New Files
- `deskops/cli/commands/migrate.py` — migration handler (ONLY if a dedicated subcommand is chosen instead of `doctor --repair`).

## Dependencies
- Task 1 (classification) blocks 2, 3, 4, 6.
- Task 3 depends on the Ambiguity A decision (command surface).
- Task 4 pairs with 1 (config is a classification input).
- Task 6 depends on 2, 3, 4 landing.

## Ambiguities / Unspecified Decisions (blocking clean implementation)
- **A. Command surface for migration is unspecified.** Task says "provide a safe adaptation path" but not whether that is `deskops doctor --repair` extension, a new `deskops migrate`, or `deskops desk migrate`. This changes parser/main wiring. Needs a decision.
- **B. Legacy definition is not pinned.** No spec of what concrete markers count as "legacy" (missing `config.json`? old `desk_format` value? unmodeled Board frontmatter? pre-model pill format?). There is currently only one `desk_format` version (`1.0.0`), so there is no known prior version to detect against. Which real legacy layouts must be supported?
- **C. No legacy fixture / examples provided.** Task lists no sample legacy desks or file paths. Tests need at least one representative legacy layout; its shape is unspecified.
- **D. Migration outcome contract undefined.** Is migrate expected to fully convert authored docs into modeled docs (content transformation), or only add missing scaffold + config while leaving authored docs for manual fixup? Preservation-first pill implies the latter, but "migration path for legacy boards, tasks, pills" hints at content adaptation. Scope boundary needs confirmation.
- **E. `desk_format` versioning policy.** Should migrate bump/stamp a version, and is there a canonical current version constant to write? `config.py` and `workspace.py` both hardcode `1.0.0` independently — a single source of truth may be needed.
- **F. Interaction with untracked/SLDB tracking.** Legacy authored docs are likely untracked in `.sldb`; does migration also register them via `sldb docs track`, or leave that as manual (current doctor behavior)? Undefined.

## Risks
- Silent overwrite of authored history is the primary guardrail risk (`pill-legacy...how_not`); migration must be strictly additive/non-destructive — verify with byte-identical assertions on authored files.
- Misclassifying `empty` as `legacy` (or vice versa) would violate the friendly-first-use expectation; needs explicit fixture tests for both.
- `doctor.py` relies on subprocess `sldb stores check` and already has fragile branches for crash/JSON-parse; extending it risks regressions in the existing exit-code logic — cover with tests.
- Without decisions A–D, implementation would require improvisation; per repo working rules, resolve ambiguity before implementation.

## Verdict
**NECESITA-ACLARACIÓN** — the goal and guardrails are clear, but the command surface (A), the concrete legacy definition/markers (B), a representative fixture (C), and the migration outcome contract (D) are unspecified and would force guessing. Recommend resolving A–D (and confirming E, F) before execution.
