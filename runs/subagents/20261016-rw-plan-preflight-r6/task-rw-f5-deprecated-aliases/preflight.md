RESTATEMENT:
1. Confirm `depends_on` are closed and that `deskops/cli/registry.py` already contains the `Command` dataclass and `deskops/cli/main.py` the dispatcher (created by task-rw-f5-command-registry) plus the output renderer.
2. Obtain and record the owner decision (warned alias vs removal) for each of `inbox`, `status`, `atoms list`, `atoms show`.
3. In `deskops/cli/registry.py`: add field `deprecated_for: tuple[str, ...] | None = None` to `Command`; set it to the canonical path (e.g. `("message",)`) for each surviving alias; delete the registry entry for each removed name.
4. In `deskops/cli/main.py`: in dispatch, before any command output, if `deprecated_for` is set print ``Deprecated: use `deskops <canonical>` `` to stderr, then execute the canonical command with the same args.
5. In `deskops/cli/parser.py`: keep aliases listed in `--help` with their deprecation note (current behavior, parser.py:500-505); for removed names rely on argparse `invalid choice`, exit 2.
6. Keep `MessageCLI._run_legacy` flag translation (`--list/--show/--ack`) for `inbox` at `deskops/cli/commands/message.py:32,57`.
7. In `tests/test_cli.py` and `tests/test_message_cli.py`: run alias and canonical with equivalent args in the same test, assert the stderr deprecation line and byte-identical stdout; for each removed name assert exit 2 / `invalid choice`; update the alias-listing assertions at `tests/test_cli.py:42` and `tests/test_message_cli.py:35`.
8. Rewrite recommending mentions to canonical names in `docs/faq.md`, `README.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, `desk/atoms/`, `desk/contexts/`; keep deprecation notes for surviving aliases; do not touch `desk/drawer/`.
9. Run `pytest tests`, `pytest`, `deskops faq`, and `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`; confirm every remaining hit is a deprecation note.
10. Do not commit; hand the diff to the supervisor for closeout via `deskops closeout commit`.

AMBIGUITIES:
1. Owner decision per duplicate is unresolved (task `status: blocked`); without it, steps 3, 7, and 8 branch differently and execution cannot start.
2. Canonical mappings are only implied by the Rationale (`inbox`→`message`, `status`→`doctor`, `atoms list`→`list atoms`, `atoms show`→`show atom`); no authoritative mapping table is given, and multi-token canonicals make the warning text format ambiguous.
3. Interaction of the warning with invalid alias args is unspecified: "before any output" vs argparse failing on the alias's own flags (warning printed or not? exit code?).
4. Whether the surviving alias's `--help` deprecation note comes from `deprecated_for` or existing static help text is unspecified.
5. For removed names, no statement on whether any prior `--help` entry must be deleted explicitly or whether argparse rejection alone suffices.
6. "Recommending" vs "deprecation note" is not defined; grep-hit classification is a judgment call with no stated rule.
7. Whether `deskops status` / `deskops inbox` are invoked internally by other deskops code (and thus need internal updates) is not stated.
8. Whether the warning applies to the `inbox` legacy flag path (`_run_legacy`) after translation is not stated.
9. Acceptance criteria for the `README.md` and SKILL.md edits are qualitative ("updated"), with no specified wording or count.
10. Whether tests must assert exact warning text/spacing/quoting is not specified beyond the backticked example.
11. Not stated whether `depends_on` tasks are actually closed or whether their artifacts already exist, so step 1 cannot be verified from this document.
