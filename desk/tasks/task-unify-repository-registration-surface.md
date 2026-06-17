# Unify repository registration surface

ID: task-unify-repository-registration-surface
Status: active
Priority: medium

## Goal

Remove ambiguity between `deskops add repository` and `deskops repo register`.

## Scope

- Decide which command is canonical for repository registration.
- Make both paths produce consistent IDs and behavior, or deprecate one path explicitly.
- Update CLI help, FAQ, and tests to reflect the chosen grammar.

## Pills

- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-004-opsys-boundary.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`

## Source Inbox Notes

- `20260614-163547-unclear-caminos-inconsistentes-add-repository-vs-repo-register.md`

## Related Findings

- `desk/drawer/stress-tests/FINDINGS_INDEX.md` findings M19 and related repo register issues.

## Done When

- There is one documented registration story.
- Duplicate command paths no longer surprise users or produce mismatched IDs.
