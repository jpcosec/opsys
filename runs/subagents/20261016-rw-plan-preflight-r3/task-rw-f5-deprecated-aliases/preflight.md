RESTATEMENT:
1. Obtain the owner decision (blocked input) for each duplicate: `inbox`, `status`, `atoms list`, `atoms show` → warned alias or removal.
2. Read `deskops/cli/registry.py`, `deskops/cli/main.py`, the parser listing at `deskops/cli/parser.py:500-505`, and `MessageCLI._run_legacy` at `deskops/cli/commands/message.py:32,57`; note existing test assertions at `tests/test_cli.py:44` and `tests/test_message_cli.py:33`.
3. For each name chosen as an alias: add a registry entry with `deprecated_for="<canonical path>"` (`inbox`→`message`, `status`→`doctor`, `atoms list`→`list atoms`, `atoms show`→`show atom`, as applicable).
4. In `deskops/cli/main.py` dispatcher: when the resolved entry has `deprecated_for`, write ``Deprecated: use `deskops <canonical>` `` to stderr before any output, then run the canonical command with the same args; stdout must be byte-identical to running the canonical directly.
5. Keep the `inbox` `--list/--show/--ack` → message translation in `MessageCLI._run_legacy` unchanged.
6. For each name chosen for removal: remove it so argparse rejects it with `invalid choice` and exit 2; verify no dispatch path remains.
7. Keep aliases listed in `--help` with their deprecation note.
8. Update tests: run the alias and the canonical command with equivalent args in the same test; assert the stderr deprecation line and identical stdout. For each removed name, assert exit 2 / `invalid choice`.
9. Update `docs/faq.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, `README.md`, and any `desk/` atoms that recommend an old name; leave existing deprecation notes intact.
10. Run `pytest tests`, `deskops faq`, and `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk`; every remaining hit must be a deprecation note.
11. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. Owner decision missing: which of `inbox`, `status`, `atoms list`, `atoms show` are aliases vs removals. Task status is `blocked`; no decision is recorded.
2. Exact canonical target for ambiguous cases: `status`→`doctor`, `atoms list`→`list atoms`, `atoms show`→`show atom` are inferred from the rationale/grep, not stated as mappings.
3. Mixed decisions (some aliased, some removed) are not addressed; unclear whether the task closes with either acceptable.
4. Contradiction: "Notes that say a name is deprecated stay" vs grep hits must all be deprecation notes — the grep cannot distinguish a note from a recommendation, so pass/fail is undefined.
5. `depends_on: task-rw-f5-output-renderer` status is unknown; no evidence it is closed, so start condition is unverifiable.
6. `files:` omits `deskops/cli/parser.py`, `deskops/cli/commands/message.py`, `tests/test_cli.py`, `tests/test_message_cli.py` and `desk/` atoms, all of which the task body requires editing.
7. Warning wording differs between body (``Deprecated: use `deskops <canonical>` ``) and scope text (same backtick form); exact literal string, trailing newline, and presence of args are unspecified.
8. Whether the alias must reproduce canonical exit codes and stdin/arg passthrough byte-for-byte is not stated (only stdout is).
9. No acceptance criterion states whether removed names must also be stripped from `--help`.
10. Removal row: unclear whether `desk/` atoms referencing removed names must be rewritten or deleted.
