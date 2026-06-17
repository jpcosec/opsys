# Improve CLI help with progressive disclosure

ID: task-improve-cli-help-progressive-disclosure
Status: active
Priority: high

## Goal

Make `deskops --help` and subcommand help understandable without reading the code.

## Scope

- Replace jargon-heavy command descriptions with user-facing intent.
- Add examples to core commands and generated artifact commands.
- Document selector formats for `show`, `advance`, `promote`, and `inbox --show`.
- Explain command order and workflow context instead of treating commands as isolated islands.
- Replace generated flag descriptions like `Title Field` with useful value expectations.

## Pills

- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`

## Source Inbox Notes

- `20260614-163534-unclear-cli-help-poco-explicativo.md`
- `20260614-163535-unclear-flag-descriptions-in-tiles.md`
- `20260614-163544-unclear-help-sin-ejemplos-de-uso.md`
- `20260614-163545-unclear-formatos-de-selector-undocumented.md`
- `20260614-163546-unclear-sin-contexto-de-flujo-en-el-cli.md`

## Done When

- A first-time user can run `--help` on the main command and core subcommands and know what to do next.
- At least one real invocation example exists for each core workflow command.
- Selector formats are documented consistently and validated by CLI tests.
