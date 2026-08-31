# Implementation Plan

## Goal
Define and wire a first-class "materialization contract" surface in deskops (model + spec + CLI + validation) that binds source atoms, target artifact identity/path, transformation intent, and validation checks, as the task and its two pills require.

## Context Found (read-only)
- Task: `desk/tasks/task-define-materialization-contract-slice-deskops-surface.md`. Goal: "Implement the deskops CLI and contract definition surface for materialization." Scope: source atom references, target artifact identity/path, intent model, validation checks, generated/projection metadata. Validation gate: `pytest`. KGDB relation extraction is explicitly routed to the sibling `kgdb` repo and out of scope (assumed to exist).
- Pills: `pill-materialization-contracts-declare-source-intent-and-target` (require declared source refs, stable target identity, validation that proves target still matches source) and `pill-atom-lifecycle-preserves-provenance-and-materialization-links` (lifecycle ops must preserve/reroute materialization links; keep downstream materializations queryable through stable provenance).
- Authoritative knowledge atom already exists: `desk/atoms/knowledge-model/atom-materialization-contracts-bind-source-output-validation.md` — a contract binds source atoms, output artifact kind, output path/identity, transformation intent, and validation checks. This is the spec-of-record for the model fields.
- Partial infrastructure already present:
  - `spec/fields/materializes_into.yaml` exists (`field.materializes_into`, `list[string]`, optional) but is not referenced by any artifact spec or model.
  - `deskops/graph/extract_edges.py` already parses `materialization.source_atoms` from YAML fences and emits `references` edges; `deskops/graph/self_reflection.py` already knows a `materializes` role.
  - `deskops/materializers/atoms.py` builds composed-doc payloads (`build_composed_doc_payload`, `build_architecture_doc_payload`) but records no contract metadata.
- Model/spec/CLI registration path is well established and mechanical:
  - Models under `deskops/models/`, exported in `deskops/models/__init__.py`.
  - Artifact wiring in `deskops/operations.py`: `ARTIFACT_MODELS`, `ARTIFACT_PATHS`, `ARTIFACT_SUBJECTS`.
  - Spec YAML under `spec/artifacts/*.yaml` (e.g. `atom.yaml`); field specs under `spec/fields/`.
  - CLI `add`/`edit`/`list`/`show` are auto-generated from `ARTIFACT_SUBJECTS` + Pydantic model fields in `deskops/cli/parser.py` and `deskops/operations.py` (`compile_artifact_spec` reads model fields as source of truth).
- The task's own routine (`desk/routines/routine-task-define-materialization-contract-slice-deskops-surface.md`) is the standard execution→testing→closeout gate chain; no extra workflow work required.

## Tasks
1. **Add the MaterializationContract model**
   - File: `deskops/models/materialization.py` (new)
   - Changes: Define `MaterializationContractDoc(StructuredNLDoc)` with `__semantics__`/`__template__` mirroring `deskops/models/atom.py`. Fields, per the authoritative atom: `id` (`materialization-{slug}`), `title`, `source_atoms: list[str]` (atom refs), `target_kind: str` (artifact kind, e.g. doc/spec/diagram/readme), `target_identity: str` (stable id or path), `intent: str` (transformation intent), `validation: list[str]` (checks that prove target matches source), `tags: list[AtomTag]` (reuse `AtomTag` pattern), optional `provenance: str | None`. Reuse existing patterns; do not invent new base classes.
   - Acceptance: `python -c "from deskops.models.materialization import MaterializationContractDoc"` imports; template round-trips through SLDB render/extract.
2. **Export the model**
   - File: `deskops/models/__init__.py`
   - Changes: import `MaterializationContractDoc` and add to `__all__`.
   - Acceptance: `from deskops.models import MaterializationContractDoc` works.
3. **Add the artifact spec**
   - File: `spec/artifacts/materialization.yaml` (new)
   - Changes: `id: artifact.materialization`, `type: artifact`, `data.doc.model: MaterializationContractDoc`, `id_pattern: materialization-{slug}`, default tags (e.g. `system:deskops`, `topic:materialization`), and a `fields:` list. Reuse `field.materializes_into` if it maps to `source_atoms`/`target_identity`; otherwise add new field specs under `spec/fields/` (`field.source_atoms`, `field.target_kind`, `field.target_identity`, `field.intent`, `field.validation`) consistent with existing field YAML shape.
   - Acceptance: `SpecRegistry.load(spec_root)` includes `artifact.materialization` without error.
4. **Register the artifact in operations**
   - File: `deskops/operations.py`
   - Changes: add `"artifact.materialization": MaterializationContractDoc` to `ARTIFACT_MODELS`; add `"artifact.materialization": "materializations"` to `ARTIFACT_PATHS`; add `{"subject": "materialization", "list_subject": "materializations"}` to `ARTIFACT_SUBJECTS`; import the model. Confirm `ensure_workspace()` scaffolds `desk/materializations/` (add to the mkdir list in `ensure_workspace`).
   - Acceptance: `deskops add materialization --root <sandbox> --title X ...` creates a file under `desk/materializations/`; `deskops list materializations` and `deskops show materialization <id>` work. CLI options auto-generate from model fields (verify list/multi fields get `--source-atom`, `--validation`, etc. via `model_cli_fields`).
5. **Add contract validation surface**
   - File: likely `deskops/cli/commands/doctor.py` (extend) or a new `deskops/materializers/contracts.py` + a CLI subcommand
   - Changes: implement a check that, for each materialization contract, verifies (a) every `source_atoms` ref resolves to a real atom under `desk/atoms/`, and (b) `target_identity`/path resolves. Prefer extending the existing `doctor`/`graph missing` semantic checks rather than adding a wholly new command, to satisfy the pills' "validation can prove the target still matches the source" and "keep downstream materializations queryable" requirements. **Decide direction with supervisor if scope is unclear (see Ambiguities).**
   - Acceptance: a contract pointing at a missing atom or missing target is reported; a valid one passes. Covered by a new pytest.
6. **Tests**
   - File: `tests/test_materialization_contract.py` (new); optionally extend `tests/test_atom_materialization.py`
   - Changes: model round-trip test; `create_artifact`/list/show test using a `tmp_path` sandbox root (per repo rule: never mutate real `desk/`); validation-check test for resolvable vs. dangling source atoms/targets.
   - Acceptance: `pytest` passes; new tests exercise create + validate paths.

## Files to Modify
- `deskops/models/__init__.py` - export new model.
- `deskops/operations.py` - register model in `ARTIFACT_MODELS`/`ARTIFACT_PATHS`/`ARTIFACT_SUBJECTS`, import it, scaffold `desk/materializations/` in `ensure_workspace`.
- `deskops/cli/commands/doctor.py` (or graph checks) - add contract resolution/validation (pending scope decision).
- Possibly `tests/test_atom_materialization.py` - extend if reusing.

## New Files
- `deskops/models/materialization.py` - `MaterializationContractDoc` model.
- `spec/artifacts/materialization.yaml` - artifact spec.
- `spec/fields/*.yaml` - any new field specs not already covered by `field.materializes_into`.
- `deskops/materializers/contracts.py` - optional, contract validation helpers if not folded into doctor.
- `tests/test_materialization_contract.py` - tests.

## Dependencies
- Task 2 depends on 1. Task 3 depends on 1 (model name). Task 4 depends on 1–3. Task 5 depends on 4 (needs the model + storage path). Task 6 depends on 1–5.
- Field-spec reuse decision (Task 3) gates whether new `spec/fields/*.yaml` are created.

## Risks
- **Underspecified scope (primary risk).** The task says "CLI and contract definition surface" and lists five scope items but does not name: the model name, exact field set/types, the storage directory, whether "validation checks" are stored strings vs. executable, or whether a `validate`/`check` CLI command is required vs. just the definition surface. This plan infers fields from `atom-materialization-contracts-bind-source-output-validation`, but that inference should be confirmed.
- **New CLI subcommand vs. reuse.** Adding a dedicated `deskops materialization ...` command group (like `atoms`) vs. relying on the auto-generated `add/list/show` for `ARTIFACT_SUBJECTS` is a design choice. `atoms` has a bespoke group; materialization could too. Unclear which the task wants.
- **Validation semantics.** Pills demand validation that "can prove the target still matches the intended source contract" (drift detection). Full drift/staleness comparison (see `atom-drift-checks-compare-atoms-materializations-implementation`) is a much larger effort than reference-resolution checks. Risk of scope creep; recommend limiting to reference/target resolution for this slice and deferring drift comparison.
- **Field reuse ambiguity.** `spec/fields/materializes_into.yaml` exists but is orphaned; unclear whether the task expects it to be adopted/renamed or superseded. Adopting it changes field naming (`materializes_into` vs. `source_atoms`/`target_identity`).
- **Graph coupling.** `extract_edges.py` already reads `materialization.source_atoms` from YAML fences; a new top-level model with a `source_atoms` frontmatter field may not be picked up by that extractor (it scans fences and reference sections, not arbitrary frontmatter). If graph visibility of contracts is expected, extractor changes may be needed — but KGDB extraction is explicitly out of scope per the task, so treat any graph wiring as a follow-up, not part of this slice.
- **Lifecycle rerouting (pill 2).** The pill requires atom split/merge/delete to preserve/reroute materialization links. There is currently no atom lifecycle command surface visible in the CLI; implementing rerouting is likely a separate task. Confirm whether this slice must include lifecycle-link handling or only the definition/validation surface.

## Verdict
**NECESITA-ACLARACIÓN.** The mechanical model/spec/CLI wiring is well-understood and low-risk, but four decisions block a clean implementation: (1) exact field set/naming and whether to adopt the orphaned `field.materializes_into`; (2) dedicated CLI command group vs. auto-generated artifact commands; (3) depth of the validation surface (reference resolution only vs. drift/staleness comparison); (4) whether atom-lifecycle materialization-link rerouting (pill 2) is in scope for this slice or deferred. Recommend confirming these before implementation; default assumptions are stated above.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Produced a planning document only; no code or artifact files were changed. Plan is scoped to the single task and its two pills, and explicitly defers out-of-scope items (KGDB extraction, drift checks, lifecycle rerouting)."
    }
  ],
  "changedFiles": [
    "runs/planning/task-materialization-contract.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "No validation commands run; this is a read-only planning task that produced a plan document."
  ],
  "residualRisks": [
    "Task is underspecified: field set/naming, CLI shape, validation depth, and lifecycle-link scope all require clarification before clean implementation.",
    "Orphaned spec/fields/materializes_into.yaml may or may not be intended for adoption."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added one planning markdown file under runs/planning/ describing tasks, files, dependencies, risks, and a NECESITA-ACLARACIÓN verdict.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "context.md referenced in the task prompt does not exist at repo root; proceeded using the named task doc and its referenced pills as instructed. Verdict is NECESITA-ACLARACIÓN due to four unresolved design decisions surfaced in the Risks section."
}
```
