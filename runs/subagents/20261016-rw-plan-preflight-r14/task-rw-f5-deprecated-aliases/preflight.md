RESTATEMENT:

1. Confirm dependencies are closed: `task-rw-f5-output-renderer` and `task-rw-f5-command-registry` must be done (task status is `blocked`; owner decision also missing).
2. Obtain the owner decision for each of the four duplicates: `inbox`, `status`, `atoms list`, `atoms show` → warned alias or removal.
3. Read `deskops/cli/registry.py`; add `deprecated_for: tuple[str, ...] | None = None` to the `Command` dataclass (canonical path, e.g. `("message",)`).
4. Populate `deprecated_for` on each surviving alias in the registry; for removed names, delete the `Command` entry (and its name) instead.
5. In `deskops/cli/main.py` dispatcher, when `deprecated_for` is set, print `Deprecated: use \`deskops <canonical>\`` to stderr before any output, then dispatch the canonical handler.
6. In `deskops/cli/parser.py` (~500-505), keep aliases listed in `--help` with their deprecation note for surviving aliases; ensure removed names produce argparse `invalid choice`, exit 2.
7. In `deskops/cli/commands/message.py`, keep the `inbox` flag translation (`--list/--show/--ack`) via `_run_legacy` if `inbox` survives as an alias; remove it if `inbox` is removed.
8. In `tests/test_cli.py`, update the command-set assertion (~line 42) for removed names.
9. In `tests/test_cli.py` / `tests/test_message_cli.py`, for each surviving alias: run alias and canonical with equivalent args in the same test, assert the stderr deprecation line and byte-identical stdout. For each removed name: assert exit 2 / mismatch. Update the existing alias-help assertions (~tests/test_cli.py:42, tests/test_message_cli.py:35).
10. Run `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`.
11. For surviving aliases: keep/convert hits into deprecation notes. For removed names: rewrite every hit to the canonical command.
12. Do not edit `desk/drawer/`.
13. Run `pytest tests`, `deskops faq`, and the step-10 grep; confirm remaining hits are deprecation notes only.

AMBIGUITIES:

1. Owner decision (warned alias vs removal) is missing for all four names — the task cannot be executed or judged done.
2. Dependencies `task-rw-f5-output-renderer` and `task-rw-f5-command-registry` are unverified; whether they are closed is unknown.
3. Exact stderr text ambiguity: `${canonical}` rendering for subcommand paths (`atoms list` → `deskops list atoms`), whether a trailing period/newline is included.
4. Whether the warning must precede argparse-parsed output for `inbox`'s legacy `--list/--show/--ack` flags too.
5. For removed names, whether they still appear in `--help` (scope says aliases stay listed; removal says argparse rejects with exit 2 — conflict).
6. Unknown which specific files under `desk/atoms` and `desk/contexts` (listed as directories) are in scope, or whether pills mentioning old names must be rewritten vs kept.
7. Boundary between a "recommendation" and a "mention" in docs/skills is undefined; no criterion for which hits to rewrite.
8. Whether the new deprecation warning string itself counts as a hit for the validation grep.
9. Byte-identical stdout requirement is untestable for commands with timestamps/paths/nondeterministic output; no list of which commands are exempt.
10. No stated behavior for the canonical command when a required canonical (e.g. `list atoms`) does not yet exist.
11. Whether removing `inbox` also removes the legacy flag translation and the `--list/--show/--ack` grammar, or only the command name.
12. `status` overlaps `doctor`; whether any distinct `status` behavior must be preserved on `doctor` before removal is unspecified.
13. Referenced line numbers (`parser.py:500-505`, `main.py:80`, `tests/test_cli.py:42`, `tests/test_message_cli.py:35`) may have shifted after dependency tasks; no re-verification instruction.
14. Missing acceptance criteria mapping each of the four duplicates to its expected final state.
