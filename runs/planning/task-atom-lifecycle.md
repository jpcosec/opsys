# Implementation Plan

## Goal
Define and implement atom lifecycle operations (create, validate, split, merge, delete, traceability) as CLI + operations surfaces in deskops, preserving provenance and materialization links.

## Context Read
- `desk/tasks/task-define-atom-lifecycle-operations.md` (task, broad scope, validation = pytest)
- `desk/routines/routine-task-define-atom-lifecycle-operations.md` (standard 3-gate routine, no extra guidance)
- `desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md`
- `desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`

### Current state of the code (what already exists)
- `deskops/models/atom.py` — `AtomDoc` with `id`, `title`, `five_wh_one_plus` (single 5WH1+ enum), `answer`, `tags` (namespaced), `provenance` (optional path/URL). The single-question constraint is already modeled.
- `deskops/atom_tags.py` — namespace registry + `validate_atom_tag_namespaces`; `deskops atoms add-namespace`.
- `deskops/cli/commands/atoms.py` + `deskops/cli/parser.py` (`_add_atoms_commands`) — subcommands: `add-namespace`, `list`, `show`. No split/merge/delete.
- `deskops/operations.py` — `create_artifact("artifact.atom", ...)` already creates atoms and validates tag namespaces; `_track_created_artifact` tracks atoms in the `.sldb` store. Reference detection: `_reference_points_to_atom`. No split/merge/delete operations.
- `deskops/graph/extract_docs.py` — atoms are graph nodes; references like `atom:<id>` are edges (`graph/checks.py` flags `dangling_source_atom_reference`).

## Tasks (proposed, pending scope confirmation — see Risks)
1. **Confirm scope & write execution-ready ambiguity note** (blocking, see Ambiguities).
   - File: task doc / run notes.
   - Acceptance: each of create/validate/split/merge/delete/traceability has a concrete, agreed behavior before coding.

2. **Atom validation command** `deskops atoms validate [<id>|--all]`.
   - File: `deskops/cli/parser.py` (`_add_atoms_commands`), `deskops/cli/commands/atoms.py`, logic in `deskops/operations.py` (new method, e.g. `validate_atom`).
   - Changes: enforce single 5WH1+ question (already modeled), tag namespace validity via `validate_atom_tag_namespaces`, provenance resolvability, and id/slug convention (`atom-<slug>`).
   - Acceptance: command exits non-zero on a crafted invalid atom; pytest coverage.

3. **Atom delete** `deskops atoms delete <id> [--force]`.
   - File: parser + `atoms.py` + new `operations.py` method.
   - Changes: before deletion, scan for inbound references (reuse/extend `_reference_points_to_atom` and graph extract to find `atom:<id>` refs across `desk/`); refuse unless `--force` or refs rerouted; remove file and untrack from `.sldb` store.
   - Acceptance: deleting a referenced atom is blocked by default (pill guardrail); deleting an unreferenced atom untracks it; pytest.

4. **Atom split** `deskops atoms split <id> ...` and **merge** `deskops atoms merge <ids...> --into <id>`.
   - File: parser + `atoms.py` + `operations.py`.
   - Changes: split creates N new atoms from one, merge combines N into one; both must preserve/reroute provenance and inbound references (rewrite `atom:<old>` refs to new targets). Reuse `create_artifact` for new atoms and store tracking.
   - Acceptance: after split/merge, `deskops graph missing` / reference scan shows no new dangling `atom:` references; pytest.

5. **Atom creation from sources (pills, graph findings, diagrams)** — needs scope decision.
   - File: `deskops/cli/commands/atoms.py`, `deskops/operations.py`, possibly `deskops/graph/*`, `deskops/materializers/*`.
   - Changes: helpers to seed an `AtomDoc` payload from a pill doc, a `deskops graph missing` finding, or a diagram spec, setting `provenance` to the source path.
   - Acceptance: `deskops atoms new --from-pill <path>` (or agreed flag) creates a valid atom with provenance set; pytest.

6. **Traceability / provenance validation surface.**
   - File: `deskops/graph/checks.py` and/or `deskops/cli/commands/doctor.py`.
   - Changes: report atoms whose `provenance` points to a missing file, and orphaned `atom:` references after lifecycle ops.
   - Acceptance: doctor/graph check flags a crafted broken-provenance atom; pytest.

7. **Docs + atoms materialization at closeout** (pill-2 guardrail).
   - File: relevant `docs/` page for atom CLI, plus capture durable rulings as atoms under `desk/atoms/`.
   - Acceptance: durable rules recorded as atoms before pill retirement.

## Files to Modify
- `deskops/cli/parser.py` — add `validate`, `delete`, `split`, `merge`, `new --from-*` subparsers under `atoms`.
- `deskops/cli/commands/atoms.py` — dispatch new subcommands.
- `deskops/operations.py` — new lifecycle methods (validate/delete/split/merge, reference rerouting, store untrack).
- `deskops/graph/checks.py` and/or `deskops/cli/commands/doctor.py` — provenance/traceability checks.
- Test files under `tests/` mirroring the above (see Risks — test dir not yet confirmed).
- `docs/` atom CLI page + `desk/atoms/` new atoms at closeout.

## New Files
- Possibly `deskops/atom_lifecycle.py` — if lifecycle logic is large enough to warrant separation from `operations.py`.
- New test module(s) for atom lifecycle.

## Dependencies
- Task 1 (scope confirmation) blocks all others.
- Tasks 3, 4 depend on a shared reference-scan/reroute helper (build it once, e.g. in Task 3).
- Task 6 depends on 3/4 (uses the same reference model).
- Task 7 depends on all implementation tasks landing.

## Ambiguities / Unspecified decisions (BLOCKING)
1. **Scope size**: the task bundles six distinct capabilities (create-from-scratch, create-from-sources, one-question validation, tag validation, split/merge/delete, provenance/traceability) into one "coherent deliverable". AGENTS.md requires one coherent deliverable per task — this likely needs decomposition into a phase of smaller tasks. Not resolved by task or pills.
2. **"one-question validation"**: `five_wh_one_plus` is already a single enum in `AtomDoc`, so the model already enforces one question. Unclear whether this task wants (a) a runtime `validate` command re-checking it, (b) new enforcement, or (c) it is already satisfied. No spec.
3. **CLI shape**: no agreed command names/flags for split/merge/delete/create-from-source. Need naming decision (`deskops atoms split` vs `deskops atom split`; current namespace is plural `atoms`).
4. **Split/merge semantics**: how are `answer`/`five_wh_one_plus`/`tags` divided on split and combined on merge? Interactive, flag-driven, or from a payload file? Undefined.
5. **Reference rerouting policy**: on delete/merge, do we auto-rewrite inbound `atom:<id>` references across `desk/`, block, or require `--force`? Pill says "explicit handling" but not the default. Needs a ruling.
6. **Create-from-diagram / from-graph-finding**: no defined input contract. Which diagram surface (`docs/diagrams/`, spec2viz) and which finding format (`deskops graph missing` output)? Undefined.
7. **Store tracking on delete/split/merge**: `_track_created_artifact` handles create; there is no untrack path. Need confirmation that SLDB exposes an untrack/retrack API (check `sldb.store.ops`) before relying on it.
8. **Test location/harness**: `tests/` directory not confirmed in this read; validation is only "pytest". Confirm where atom tests live and existing fixtures for a sandbox desk (AGENTS.md: use disposable sandbox desk, not real `desk/`).
9. **Rationale/Done-When are generic**: the task's Rationale is "Not provided" and Done-When is the boilerplate promotion phrase — no acceptance criteria to anchor "done".

## Risks
- Building split/merge without an agreed reference-rerouting default risks violating the provenance guardrail pill or silently orphaning references.
- Reliance on an SLDB untrack API that may not exist — verify `sldb.store.ops` before Task 3/4.
- Scope is large enough that a single commit/task likely breaks the "one coherent deliverable" and phase-gating rules; recommend splitting into a phase (create/validate | delete | split/merge | from-sources | traceability).
- `AtomDoc` already covers single-question + provenance; risk of re-implementing existing behavior if scope is not clarified.

## Verdict
**NECESITA-ACLARACIÓN** — the task is materially underspecified (bundled multi-capability scope, undefined CLI shape and split/merge/delete/reroute semantics, undefined from-source input contracts, no concrete acceptance criteria). Resolve Ambiguities 1–6 (at minimum) and confirm decomposition into a phase before implementation.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Planning-only run: produced implementation plan, explicit ambiguity list, and verdict at the authoritative output path without editing source or widening scope beyond the task doc and its two referenced pills."
    }
  ],
  "changedFiles": [
    "runs/planning/task-atom-lifecycle.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "No code changed; plan derived from reading task doc, routine, two pills, deskops/models/atom.py, deskops/atom_tags.py, deskops/cli/commands/atoms.py, deskops/cli/parser.py, deskops/operations.py, deskops/graph/extract_docs.py/checks.py"
  ],
  "residualRisks": [
    "Task scope is underspecified; verdict is NECESITA-ACLARACIÓN and requires clarification before implementation.",
    "SLDB untrack API for delete/split/merge not verified.",
    "Test directory/harness location not confirmed in this read."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added planning document runs/planning/task-atom-lifecycle.md; no code changes.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "context.md referenced in the task did not exist (ENOENT); planned from the specified task doc and pills instead. Recommend decomposing this task into a phase of smaller tasks."
}
```
