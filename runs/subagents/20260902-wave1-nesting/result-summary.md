# Result summary

- run_id: `20260902-wave1-nesting`
- task_id: `task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields`
- role: `deskops executor`
- session: `unavailable in API executor context`
- session_sha256: `07254281225e40c33abc53464abccc197d911f8ea99a8298f6e74a10c974927d`

## Scope executed

Implemented a scoped promotion/extraction fix so structured task headings from inbox or drawer sources are flattened into the correct active-task fields instead of being embedded inside another field body.

## Touched surfaces

- `deskops/operations.py`
- `deskops/cli/commands/promote.py`
- `tests/test_promotion_nesting.py`
- `runs/subagents/20260902-wave1-nesting/*` evidence

## What changed

1. Added task-section parsing helpers in `deskops/operations.py` to detect canonical task headings from arbitrary markdown fragments, strip task-template placeholders, and parse validation bullets safely.
2. Updated task document reads so `TaskDoc` extraction uses first-occurrence structured sections from the markdown source. This recovers nested `## Implementation Path`, `## Validation`, and `## Done When` content even when malformed task markdown already exists.
3. Updated inbox-to-drawer promotion to render authored structured sections as top-level drawer sections instead of embedding them wholesale under `## Scope`.
4. Updated drawer-to-active promotion to strip leading drawer metadata, extract canonical sections, and populate flat active-task payload fields (`why`, `goal`, `scope`, `implementation_path`, `validation`, `done_when`).
5. Added focused regression tests for inbox promotion, drawer promotion, and active-task extraction during `advance task` reads.

## Validation

See `validation.log`.

Validated by:
- `pytest tests/test_promotion_nesting.py -q` → `3 passed`
- `pytest -q` → `184 passed`

## Residual risks

- Section normalization recognizes canonical `##` task headings only. Other ad hoc heading names remain preserved as body text under the surrounding recognized section or preamble.
- Validation parsing treats bullet-prefixed lines as checklist items and ignores empty placeholder bullets; multi-line bullet continuations are preserved only as separate stripped lines if authored outside the simple bullet form.
