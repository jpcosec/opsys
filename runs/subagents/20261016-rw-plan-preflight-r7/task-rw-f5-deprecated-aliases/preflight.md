RESTATEMENT:

1. Unblock: obtain the owner decision for each of `inbox`, `status`, `atoms list`, `atoms show` (alias vs removal).
2. Confirm dependency tasks landed: `deskops/cli/registry.py` has the `Command` dataclass, and the output renderer exists.
3. Add `deprecated_for: tuple[str, ...] | None = None` to the `Command` dataclass in `deskops/cli/registry.py`.
4. In `deskops/cli/main.py`, before any output, if `deprecated_for` is set print ``Deprecated: use `deskops <canonical>` `` to stderr, then dispatch the canonical command.
5. For each duplicate decided as alias, register the deprecated name pointing at its canonical path (`inbox`→`message`, `status`→`doctor`, `atoms list`→`list atoms`, `atoms show`→`show atom`); keep it listed in `--help` per `parser.py:500-505`.
6. Preserve `inbox`'s `--list/--show/--ack` grammar and the `MessageCLI._run_legacy` translation in `deskops/cli/commands/message.py:32,57`.
7. For each duplicate decided as removal, drop the registry entry so argparse emits `invalid choice`, exit 2; update the command-set assertion at `tests/test_cli.py:42`.
8. Add tests in `tests/test_cli.py` and `tests/test_message_cli.py`: run alias + canonical with equivalent args, assert the stderr deprecation line and byte-identical stdout; for removed names assert exit 2. Also updates at `tests/test_message_cli.py:35`.
9. Rewrite recommending mentions in `docs/faq.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, `README.md`, `desk/atoms`, `desk/contexts`; for aliases keep existing deprecation notes, for removals rewrite to canonical. Do not edit `desk/drawer/`.
10. Run the validation grep, review every hit, rewrite recommending ones.
11. Run `pytest tests` and `deskops faq`.
12. Done when each duplicate matches the decision and every grep hit is a deprecation note, not a recommendation.
13. Supervisor promotes the drawer task and commits promotion; executor does not commit; supervisor makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` (or `--no-run --reason`) after `pytest tests` is green.

AMBIGUITIES:

1. Task is `status: blocked` on the owner decision; no decision is recorded for any of the four duplicates, so steps 5–9 cannot be chosen.
2. Contradiction: Scope says "Aliases stay listed in `--help` with their deprecation note (today's behavior)" while also allowing removal, where argparse rejects the name — removed names cannot remain listed in `--help`.
3. `deprecated_for` is a tuple implying possibly multiple canonical commands; no rule for when more than one applies.
4. Exact stderr wording for multi-token canonicals (e.g. `list atoms`, `show atom`) is not specified beyond the template `` `deskops <canonical>` ``.
5. No acceptance criteria for the removal case: no message, only exit 2 — unclear whether any notice is expected.
6. `desk/atoms` and `desk/contexts` are listed as files but are directories; no instruction on which documents to edit or how to find recommending mentions.
7. Unclear whether the deprecation warning prints once per invocation or per nested dispatch when an alias is invoked.
8. No defined timeout/expiry for surviving aliases (permanent vs temporary).
9. Validation grep does not cover `deskops inbox --list/--show/--ack` flag-grammar mentions or casing/alternate spellings; "every remaining grep hit is a deprecation note" gives no threshold for acceptable non-recommending hits.
10. Acceptance of "byte-identical stdout" between alias and canonical is undefined for `inbox`, whose legacy flag translation may reorder output.
