# Implementation Plan

## Goal
Give each desk one canonical project identity and make repo self-discovery ("who am I?") and sibling desk discovery ("where is that repo's desk?") resolve deterministically, failing loudly on duplicate id/root instead of first-match guessing.

## Context Read
- Task: `desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md`
- Pills: `desk/contexts/pill-canonical-desk-identity-enables-horizontal-routing.md`, `desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md`
- Code surfaces already present:
  - `deskops/config.py` — `DeskConfig.project_identity` (default `"unknown-project"`), version + sandbox policy; loads `desk/config.json` + `desk/config.local.json`.
  - `deskops/cli/commands/inbox.py` — `_resolve_repo_desk()` (sibling lookup) and `_sender_project()` (self inference). Both iterate `RepositoryDoc` payloads and **return on first match**, no duplicate detection.
  - `deskops/cli/commands/repo.py` — `RepoCLI.register()` writes `desk/registry/repo-<id>.md` and tracks it; guards against duplicate file/tracked name only within the current store.
  - `deskops/models/repository.py` — `RepositoryDoc` (`name`, `id`, `path`, `status`, `tags`).
  - `deskops/operations.py` — `_registered_repositories()` loads `registry/repo-*.md`.
  - `deskops/cli/parser.py` — `_add_repo_commands()` only exposes `repo register`.
  - `deskops/workspace.py` — `_config_template()` seeds `project_identity` = target dir name on `init`.

## Tasks

1. **Define the canonical identity contract**
   - File: `deskops/config.py`
   - Changes: Document/normalize that `DeskConfig.project_identity` is the single canonical identity string, and that it must correspond 1:1 with the `RepositoryDoc.id` used in the ecosystem registry. Add a helper (e.g. `DeskConfig.canonical_identity`) and reject/flag the sentinel `"unknown-project"` as "not established".
   - Acceptance: unit test in `tests/test_config.py` asserting identity accessor + unset detection.

2. **Add deterministic self-discovery ("who am I?")**
   - File: `deskops/cli/commands/repo.py` (new subcommand handler, e.g. `repo whoami`/`repo identity`) + `deskops/cli/parser.py` (`_add_repo_commands`).
   - Changes: Resolve current desk `project_identity`, cross-check against registered `RepositoryDoc` entries whose resolved `path` contains the current root (reuse the `_sender_project` matching logic). Fail explicitly if the config identity and the registry-derived identity disagree, or if more than one registry entry maps to the current root.
   - Acceptance: `deskops repo whoami --store <fixture>` prints canonical id; conflicting fixtures return non-zero with a clear error.

3. **Make sibling desk resolution fail on ambiguity**
   - File: `deskops/cli/commands/inbox.py` (`_resolve_repo_desk`, `_sender_project`).
   - Changes: Replace first-match loops with collect-all-matches. If >1 `RepositoryDoc` matches the requested name/id (or >1 registry entry maps to the sender root), raise `SLDBStoreError` with an explicit duplicate message instead of returning the first hit. Keep the "not found" branch.
   - Acceptance: new tests asserting duplicate-id and duplicate-root fixtures raise/return error; single-match still resolves.

4. **Enforce canonical uniqueness at registration**
   - File: `deskops/cli/commands/repo.py` (`register`).
   - Changes: Before writing, scan existing `RepositoryDoc` entries and reject registration when the `id` OR the resolved `path` (root) already maps to another registered repo, so duplicate identities cannot enter the registry in the first place.
   - Acceptance: test registering a colliding id/path returns non-zero and writes nothing.

5. **Route both identity contract halves into one shared resolver (de-dup logic)**
   - File: `deskops/operations.py` (extend `_registered_repositories`) or a small new helper module (e.g. `deskops/identity.py`).
   - Changes: Centralize "load registry → match by id → match by root → detect duplicates" so `inbox.py`, `repo.py`, and the whoami command all consume one contract (pill: "every cross-desk lookup consume that contract"). Avoid three divergent copies of the matching rule.
   - Acceptance: callers in tasks 2–4 import the shared resolver; `pytest` green.

6. **Validation + docs sync**
   - Files: `tests/test_config.py`, new test module (e.g. `tests/test_repo_identity.py`), and any doc/atom that states the identity rule (`desk/atoms/...`, then a `docs/` materialization if a rule is added).
   - Changes: Add tests for identity resolution, duplicate detection, and whoami. Run `pytest` and `python -m deskops repo --help`.
   - Acceptance: `pytest` passes; CLI help lists new subcommand.

## Files to Modify
- `deskops/config.py` — canonical identity accessor + unset detection.
- `deskops/cli/commands/inbox.py` — duplicate-safe sibling and sender resolution.
- `deskops/cli/commands/repo.py` — whoami handler + duplicate-guarding register.
- `deskops/cli/parser.py` — register the new `repo` subcommand.
- `deskops/operations.py` — shared registry resolver (or delegate to new module).
- `tests/test_config.py` — identity contract tests.

## New Files
- `deskops/identity.py` (optional) — single shared "resolve identity / resolve sibling / detect duplicates" contract consumed by inbox/repo/whoami.
- `tests/test_repo_identity.py` — duplicate-id, duplicate-root, whoami, and single-match tests.

## Dependencies
- Task 1 defines the contract consumed by 2–5.
- Task 5 (shared resolver) should land before or alongside 2–4 to avoid three divergent copies; pragmatically, implement 5 first, then 2/3/4 consume it.
- Task 6 depends on 1–5.

## Risks / Ambiguities

**Verdict-blocking ambiguities (must be resolved before clean implementation):**

1. **No rationale / no acceptance beyond `pytest`.** Task "Rationale" is "Not provided" and "Done When" is generic ("promoted work completed and closed"). There is no concrete observable behavior spec, so the exact CLI surface (command names, flags, output shape) is a guess.
2. **Identity contract shape is undefined.** The task says "define the minimal per-project desk identity contract" but does not specify: is `DeskConfig.project_identity` authoritative, is `RepositoryDoc.id` authoritative, or must they agree? The plan assumes 1:1 agreement — this needs confirmation.
3. **Relationship between local config and SLDB registry is unspecified.** Scope item "decide how local desk identity relates to SLDB-backed ecosystem registration" is an open design decision, not an implementation detail. Who wins on conflict (config vs registry)? What if a repo has config identity but is unregistered?
4. **Duplicate-failure surface undefined.** Should ambiguity raise (exception/non-zero exit), warn, or require a `--strict` flag? Current code silently first-matches. The pill says "fail clearly," but the exact channel (exit code, error type, message contract) is unspecified.
5. **Self-discovery command does not exist yet.** There is no `whoami`/`identity` command; the task implies one ("answer 'who am I?' reliably") but does not name it. Command name and output format are invented in this plan.
6. **Scaffolding vs migration.** The version/sandbox pill implies legacy desks may lack `project_identity`. Task does not say whether this task must add migration/upgrade handling for existing desks with `"unknown-project"`.
7. **Promoted-from path missing.** Task frontmatter references a drawer source that no longer exists (`desk/drawer/tasks/task-establish-horizontal-desk-discovery-and-identity.md` — not found), so the original intent cannot be recovered from the drawer.

**Execution risks:**
- Changing `_resolve_repo_desk`/`_sender_project` from first-match to fail-on-duplicate can break existing tests/fixtures that rely on lenient matching — audit `tests/` for inbox/repo fixtures first.
- Adding a `repo whoami` command touches `parser.py` arg wiring and `main.py` dispatch; verify the `_apply_test_root_override` allow-list (`main.py`) includes any new command if it needs root override.
- Docs/atoms rule: per `AGENTS.md`, if a durable identity rule is added it must first be captured in `desk/atoms/` before any `docs/` change — do not skip the atom.

## Verdict
**NECESITA-ACLARACIÓN**

The code surfaces are clear and the change is scoped, but the task under-specifies the core design decisions it explicitly lists as in-scope (identity contract shape, config-vs-registry authority, and the failure channel for ambiguity). These are design choices, not implementation trivia; guessing them risks building the wrong contract. Recommend resolving ambiguities 1–5 (especially 2, 3, 4) before implementation.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Produced a read-only implementation plan for the single routed task and its two pills; no code or task files were modified, scope kept to planning only."
    }
  ],
  "changedFiles": [
    "runs/planning/task-horizontal-discovery.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Read task doc, both referenced pills, and code surfaces (config.py, workspace.py, inbox.py, repo.py, repository.py, operations.py, parser.py, main.py) to ground the plan in exact files."
  ],
  "residualRisks": [
    "context.md provided in the task path did not exist (ENOENT); planning proceeded from the named task doc only.",
    "Drawer source task referenced in frontmatter no longer exists, so original intent could not be cross-checked.",
    "Core design decisions in the task are underspecified; plan verdict is NECESITA-ACLARACIÓN."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one planning markdown file with implementation plan, ambiguity list, and verdict.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "context.md at the given path was missing (ENOENT). Verdict is NECESITA-ACLARACIÓN: identity contract shape, config-vs-registry authority, and ambiguity-failure channel must be clarified before clean implementation."
}
```
