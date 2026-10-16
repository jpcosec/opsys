RESTATEMENT:
1. Confirm blocker cleared: dependency `task-rw-f5-output-renderer` closed and an owner decision exists for each of `inbox`, `status`, `atoms list`, `atoms show` (alias or removal). If not, stop.
2. Read `deskops/cli/registry.py` to learn how command names/paths are registered, resolved, and dispatched, and locate the dispatcher code that runs the resolved command.
3. For each duplicate chosen as alias: add `deprecated_for="<canonical path>"` to its registry entry (`inbox`→`message`, `status`→`doctor`, `atoms list`→`list atoms`, `atoms show`→`show atom`).
4. For each duplicate chosen for removal: delete its registry entry so argparse rejects it (`invalid choice`, exit 2).
5. In the dispatcher, when the resolved entry has `deprecated_for`, print ``Deprecated: use `deskops <canonical>` `` to stderr before any other output, then run the canonical command unchanged.
6. Add tests: for each alias, assert the exact stderr line and stdout identical to the canonical command; for each removal, assert exit code 2.
7. Update `docs/faq.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md` so no text recommends a deprecated/removed name.
8. Run `pytest`.
9. Run `deskops faq` and confirm it works.
10. Run `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills` and confirm no matches.
11. Do not commit; leave the diff for supervisor review and closeout commit.

AMBIGUITIES:
1. Open Ambiguities leaves the owner decision unresolved for all four duplicates (`inbox`, `status`, `atoms list`, `atoms show`): alias vs removal is unknown — task is `status: blocked` and cannot be executed or known done.
2. No place is specified for recording/reading the owner decision, so I cannot verify the block is lifted.
3. `deskops/cli/registry.py` is listed but the dispatcher file that must print the warning is not; I would have to guess where dispatch happens.
4. No test file path or naming convention is given.
5. Whether deprecated aliases must be hidden from `--help`/usage output is unspecified.
6. Whether a `deprecated_for` field already exists in the registry schema or must be added is not stated.
7. Exact precedence/format when the stderr warning is `Deprecated: use \`deskops <canonical>\`` — whether `<canonical>` is the full path (`atoms show` vs `show atom`) is not spelled out.
8. Whether the alias must still accept the same arguments/flags as the canonical command, and whether argument parsing errors change exit codes, is unspecified.
9. Removal scope wording ("argparse rejects the name") does not state whether a custom message is required or only argparse's default `invalid choice`.
10. The validation grep covers only `docs`, `.pi/skills`, `.opencode/skills`; other likely mentions (e.g. `README.md`, `desk/` docs/atoms, other skills) are not in scope, so "no doc recommends a deprecated name" cannot be fully verified.
11. The grep pattern requires the literal `deskops ` prefix and that exact ordering, so it misses bare `inbox`/`status` mentions and alternate orderings; passing grep is not a reliable completeness check.
12. No acceptance criteria define the "identical stdout" comparison baseline (canonical run captured when and how).
13. References list is empty and `runs/planning/deskops-rewrite-inventory.md` (cited in Rationale) is not in `files`, so I cannot confirm the phase-F5 plan details.
