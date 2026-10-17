RESTATEMENT:

1. Confirm the task is unblocked: verify `task-rw-f5-output-renderer` and `task-rw-f5-command-registry` are closed so `deskops/cli/registry.py` exists and the dispatcher in `deskops/cli/main.py` is the one this task extends.
2. Obtain the owner decision for each of the four duplicates: `inbox`, `status`, `atoms list`, `atoms show` — each is either "warned alias" or "removal".
3. Add `deprecated_for: tuple[str, ...] | None = None` to the `Command` dataclass in `deskops/cli/registry.py` (the dataclass created by task-rw-f5-command-registry).
4. In the dispatcher in `deskops/cli/main.py`, when `deprecated_for` is set, print `` Deprecated: use `deskops <canonical>` `` to stderr before any output, then execute the canonical command.
5. For aliases: keep the alias in `--help` with its deprecation note, matching parser.py:500-505 behavior asserted by tests/test_cli.py:42 and tests/test_message_cli.py:35.
6. For removals: make argparse reject the name so it fails with `invalid choice` and exit 2; update the command-set assertion at tests/test_cli.py:42.
7. Keep `inbox`'s flag grammar (`--list/--show/--ack`) and its `MessageCLI._run_legacy` translation in `deskops/cli/commands/message.py:32,57` intact.
8. In tests/test_cli.py and tests/test_message_cli.py: for each surviving alias, add one test that runs the alias and the canonical command with equivalent args and asserts the stderr deprecation line and byte-identical stdout; for each removed name, assert exit 2 with `invalid choice`.
9. Update `docs/faq.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, `README.md`, `desk/atoms/`, and `desk/contexts/`: rewrite recommending mentions to the canonical command; keep existing deprecation notes for surviving aliases.
10. Run the grep validation: `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`; confirm every remaining hit is a deprecation note, not a recommendation.
11. Run `pytest tests` and `deskops faq`.
12. Do not commit; leave the diff for the supervisor's closeout commit.

AMBIGUITIES:

1. Missing owner decision: for each of `inbox`, `status`, `atoms list`, `atoms show` it is unknown whether the outcome is a warned alias or removal. Task is `status: blocked` and this is the stated blocker.
2. Task is blocked and depends on two open tasks (`task-rw-f5-output-renderer`, `task-rw-f5-command-registry`); the preflight cannot verify the `Command` dataclass or dispatcher shape exists.
3. Canonical direction is unstated for overlapping pairs: is `doctor` canonical and `status` the duplicate, or vice versa? Same for `message`/`inbox`.
4. `deprecated_for` example is `("message",)`; for `atoms list`/`atoms show` it is unclear whether the tuple is `("list", "atoms")` (subcommand-first) or `("atoms", "list")`, and how the warning string renders multi-word canonicals.
5. Exact stderr format is ambiguous: trailing newline, backticks vs quotes, and whether the canonical is printed as `deskops list atoms` or `deskops atoms list`.
6. "Before any output" is ambiguous for error paths — whether the warning prints before argparse errors on a bad alias subcommand.
7. `docs/faq.md`, `.pi/skills/use-deskops/SKILL.md`, and `.opencode/skills/use-deskops/SKILL.md` are listed as individual files, but `desk/atoms` and `desk/contexts` are directories with no named files; the specific atoms/contexts to edit are unknown.
8. It is unstated whether the two skill copies (`.pi/skills` and `.opencode/skills`) must remain byte-identical or are edited independently.
9. For a removed duplicate, it is unclear whether the underlying command implementation is deleted or only its CLI registration.
10. For a removed `inbox`, it is unstated whether the `--list/--show/--ack` grammar and `MessageCLI._run_legacy` translation are kept, redirected to `message`, or deleted.
11. The referenced pill (`desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`) content is not provided.
12. `runs/planning/deskops-rewrite-inventory.md` is referenced in the rationale but not listed in `files`; whether it needs updating is unclear.
13. "byte-identical stdout" is ambiguous for commands whose canonical subcommand ordering differs (e.g., `atoms list` vs `list atoms`) and for commands with non-deterministic output (timestamps, ordering).
14. It is unstated whether the grep must exit nonzero when only deprecation-note hits remain, or whether any hits are acceptable.
15. Acceptance is "every remaining grep hit is a deprecation note" — this is a manual judgment with no mechanical criterion.
