# Implementation Plan

## Goal
Give each project desk one explicit local config contract (identity + version expectations + testing/sandbox policy) that is actually consumed by desk resolution, testing sandbox, and legacy/version handling — not just declared.

## Key finding before planning
Much of the surface is **already implemented**. Do not re-build it:
- `deskops/config.py` already defines `DeskConfig`, `VersionExpectations` (`desk_format`, `model_version`), and `SandboxPolicy` (`enabled`, `sandbox_root`), plus a `config.json` + `config.local.json` merge loader.
- `deskops/workspace.py::_config_template` already scaffolds `desk/config.json` on `deskops init`.
- `deskops/cli/main.py::_apply_test_root_override` already consumes `config.sandbox` for the testing sandbox root (with `DESKOPS_TEST_ROOT` env taking precedence).
- `.gitignore:9` already ignores `desk/config.local.json`.
- `tests/test_config.py` already covers defaults, JSON load, and local override.

What is declared but **inert** (fields exist, nothing reads them):
- `project_identity` — never consumed. `deskops/cli/commands/inbox.py::_resolve_repo_desk` still routes by registry `name`/`id` scan, not by canonical identity (violates `pill-canonical-desk-identity-enables-horizontal-routing`).
- `versions.desk_format` / `versions.model_version` — never validated or detected anywhere. No legacy-format detection or migration path (violates `pill-legacy-desk-formats-need-explicit-adaptation`).

The remaining real work is wiring these two contracts into behavior. This is where the task is underspecified — see Ambiguities.

## Tasks
1. **Confirm scope with task owner** (blocking): decide whether this task is only to formalize/round out the already-present config (docs + tests) or to make `project_identity` and `versions` drive behavior. See Ambiguities. Do not start code until resolved.
2. **Harden config loader merge** (low-risk, in-scope regardless):
   - File: `deskops/config.py`
   - Changes: replace the hand-rolled shallow merge in `DeskConfig.load` with a single deterministic deep-merge of `config.json` then `config.local.json`; keep silent-on-malformed behavior but consider surfacing parse errors via a return flag or log rather than swallowing with bare `except Exception: pass`.
   - Acceptance: existing `tests/test_config.py` still passes; add a test for nested `versions` override from local config.
3. **Consume `project_identity` for cross-desk routing** (only if Task 1 confirms):
   - File: `deskops/cli/commands/inbox.py` (`_resolve_repo_desk`), possibly `deskops/cli/commands/repo.py`.
   - Changes: resolve current-repo canonical identity from `DeskConfig.project_identity`; fail clearly on duplicate/ambiguous registry matches instead of first-hit.
   - Acceptance: routing test that a config-declared identity resolves the sibling desk and that ambiguous matches error explicitly.
4. **Consume/validate `versions` + legacy detection** (only if Task 1 confirms):
   - File: new helper in `deskops/config.py` or `deskops/workspace.py`; surfaced via `deskops/cli/commands/doctor.py`.
   - Changes: read `versions.desk_format`; when a desk lacks `config.json` or declares an older format, report a legacy/mismatch finding (preservation-first, no silent rewrite). Wire into `DoctorCLI.run` findings.
   - Acceptance: `doctor` test where a legacy desk (no `config.json`) reports an explicit version/legacy finding rather than "healthy".
5. **Document the contract**:
   - File: capture the rule as atom(s) under `desk/atoms/` first, then reflect in `README.md` / `docs/` (per AGENTS.md docs-are-materializations rule). Document precedence: explicit CLI flag > `DESKOPS_TEST_ROOT` env > `config.local.json` > `config.json` > defaults.
   - Acceptance: atom exists and doc references it; precedence matches `main.py` behavior.
6. **Validate**: run `pytest`; run `python -m deskops doctor` against a scratch desk and a legacy-shaped desk in a sandbox (`.tmp/deskops-cli-test`), per AGENTS.md CLI-mutation-sandbox rule.

## Files to Modify
- `deskops/config.py` - deterministic merge, optional version helper.
- `deskops/cli/commands/inbox.py` - identity-based cross-desk routing (conditional on Task 1).
- `deskops/cli/commands/repo.py` - identity consumption if routing centralizes (conditional).
- `deskops/cli/commands/doctor.py` - version/legacy findings (conditional on Task 1).
- `tests/test_config.py` - nested-override and version tests.
- `README.md` / relevant `docs/` - contract + precedence documentation.

## New Files
- `desk/atoms/.../atom-project-local-config-carries-version-and-sandbox-policy.md` - durable rule capture backing the pill.
- Possibly `tests/test_doctor_version.py` - legacy/version detection coverage (or extend existing doctor tests).

## Dependencies
- Task 1 gates Tasks 3, 4, and parts of 5. Tasks 2 and the sandbox/precedence doc slice can proceed independently.
- Task 6 depends on all preceding code tasks.

## Risks
- **Scope already largely satisfied**: the biggest risk is redoing existing work or over-widening. Config model, scaffold, sandbox consumption, gitignore, and tests already exist. Confirm the true delta before coding.
- **Silent-except in loader**: current `except Exception: pass` hides malformed config; changing this could alter behavior other code relies on (`main.py` calls `DeskConfig.load` unconditionally). Verify no caller expects silent failure.
- **Identity routing is a behavior change**: switching `inbox.py` from registry-name scan to `project_identity` may break existing inbox targeting flows and tests. Needs explicit validation of `test_cli.py`/inbox tests.
- **Legacy detection ambiguity**: no defined legacy markers or migration command exists; "detect and adapt" is unspecified (see Ambiguities). Building detection without agreed markers risks false positives on hand-written desks.
- **Precedence contract undocumented**: `DESKOPS_TEST_ROOT` currently overrides config sandbox in `main.py`; the intended precedence order is not stated in the task and must be confirmed to avoid regressions.

## Ambiguities / decisions that block clean implementation
1. **Is the config already "done"?** The task-declared surfaces (tracked config, local override, version fields, sandbox policy) are already present in `config.py`, `workspace.py`, `main.py`, `.gitignore`, and `tests/test_config.py`. Unclear whether this task is (a) already substantially complete and only needs docs/tests/round-out, or (b) intended to wire the inert `project_identity`/`versions` fields into real behavior. This is the primary blocker.
2. **Must `project_identity` actually drive routing now?** The canonical-identity pill implies yes, but the task Goal/Scope only says "declare" identity. Decide whether routing rework (inbox/repo) is in-scope or a separate task.
3. **Legacy format contract undefined**: no defined legacy markers, no target `desk_format` versioning scheme, and no migrate/doctor command spec. The migration/adaptation pill cannot be satisfied without deciding what a legacy marker is and whether adaptation is detect-only (doctor finding) vs. an actual migrate command.
4. **Config file format**: implementation uses JSON (`config.json`). Task text does not mandate a format; confirm JSON is acceptable vs. YAML/TOML used elsewhere in desk (`tag-namespaces.yaml` is YAML).
5. **Override precedence order** (CLI flag vs `DESKOPS_TEST_ROOT` vs `config.local.json` vs `config.json`) is implied but never explicitly specified in the task; needs an authoritative decision to document and test.
6. **Model version semantics**: what does `model_version` gate? No consumer or validation rule is defined for it.

## Verdict
**NECESITA-ACLARACIÓN** — Core config infrastructure already exists; the task does not specify whether the remaining work is wiring the inert identity/version fields into behavior (routing, legacy detection, migration) or merely rounding out docs/tests. Ambiguities 1–3 must be resolved before clean implementation.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Planning-only run: read the task doc and its three referenced pills plus the existing config surfaces (config.py, workspace.py, main.py, inbox.py, doctor.py, .gitignore, tests/test_config.py) and produced a scoped plan without editing implementation files."
    }
  ],
  "changedFiles": [
    "runs/planning/task-per-project-config.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "No validation commands run; this is a read-only planning task. Findings written to the authoritative output path."
  ],
  "residualRisks": [
    "Task appears largely already implemented; primary risk is redundant or scope-widening work if delta is not confirmed.",
    "Legacy-format detection and identity-routing rework are underspecified and may constitute separate tasks."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added planning document at runs/planning/task-per-project-config.md; no code changed.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "context.md at repo root did not exist (ENOENT); proceeded from the named task file and its referenced pills. DeskConfig/VersionExpectations/SandboxPolicy, config.json scaffold, sandbox consumption in main.py, gitignore for config.local.json, and test_config.py already exist. project_identity and versions.* are declared but consumed nowhere."
}
```
