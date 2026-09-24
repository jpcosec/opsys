# Deskops UX stress-tests

Fifteen scripted UX tests derived from the fifteen use-case narratives in
`desk/drawer/use-cases/`. They run the real CLI and record where the experience
breaks, confuses, or contradicts the user's mental model.

Read-only by design: they execute commands and observe output, they do not edit
the desk.

## Layout

- `st-01..st-15*.md` — the tests, one per use case
- `findings-archive.md` — every finding from the six rounds that ran them, verbatim
- `desk/drawer/issues/issue-stress-test-fix-backlog.md` — what is left to fix,
  with Phase 0 re-verified against the current CLI
- `desk/drawer/issues/issue-empty-selector-validation-error.md` — the one Phase 0
  item still reproducible

## Running them

Run each test against a disposable desk root, never against this repository's
`desk/`:

```bash
deskops desk install /tmp/deskops-ux --root /tmp/deskops-ux
deskops <command> --root /tmp/deskops-ux
```

Several rounds also wrote their throwaway artifacts into a real desk; those were
deleted from `desk/`. Keep mutations in a sandbox root
(`atom-cli-mutation-testing-uses-sandbox-desk-roots`).
