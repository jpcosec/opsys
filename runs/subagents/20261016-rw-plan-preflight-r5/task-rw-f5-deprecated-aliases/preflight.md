RESTATEMENT:
1. Wait for/obtain the owner decision per duplicate (`inbox`, `status`, `atoms list`, `atoms show`): warned alias vs removal. Task is `status: blocked`; without the decision no per-name behavior can be implemented.
2. For surviving aliases, add `deprecated_for: tuple[str, ...] | None = None` to the `Command` dataclass in `deskops/cli/registry.py` (created by task-rw-f5-command-registry), holding the canonical command path, e.g. `("message",)`.
3. In `deskops/cli/main.py`, when the resolved command has `deprecated_for` set, print ``Deprecated: use `deskops <canonical>` `` to stderr before any other output, then dispatch the canonical command unchanged.
4. Keep alias entries listed in `--help` with their deprecation note (existing behavior, `deskops/cli/parser.py:500-505`).
5. For removed names, ensure argparse has no such choice so parse fails with `invalid choice`, exit 2.
6. Keep `MessageCLI._run_legacy` (`deskops/cli/commands/message.py:32,57`) translating `inbox`'s `--list/--show/--ack` grammar.
7. Add tests in `tests/test_cli.py` and `tests/test_message_cli.py`: for each alias, run alias and canonical in the same test with equivalent args, assert the exact stderr deprecation line and byte-identical stdout; for each removed name, assert exit 2.
8. Run `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`; for surviving aliases keep deprecation notes, for removed names rewrite every recommending mention to the canonical command. Do not edit `desk/drawer/`.
9. Update `docs/faq.md`, `README.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, plus `desk/atoms/` and `desk/contexts/` hits, staying consistent with `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`.
10. Validate: `pytest tests`, `deskops faq`, and the grep command; confirm every remaining hit is a deprecation note.
11. Do not commit; report the diff for supervisor closeout.

AMBIGUITIES:
1. Owner decision for `inbox`, `status`, `atoms list`, `atoms show` is unresolved — cannot implement any per-name behavior.
2. `depends_on` lists only `task-rw-f5-output-renderer`, but Implementation Path depends on `task-rw-f5-command-registry` creating the `Command` dataclass; missing dependency or contradiction.
3. Canonical path for multi-word commands undefined: is `atoms list` canonicalized to `list atoms` (tuple `("list","atoms")`) or singular `atom list`? Scope uses both `list atoms` and `show atom`.
4. Exact warning template unclear: trailing space after the backticked canonical name? Formatting for multi-word canonical paths?
5. Unclear whether removed names still appear in `--help` with a note, or vanish entirely; Scope's "--help" sentence only addresses aliases.
6. Required exit code/stdout for a surviving alias when the canonical command itself fails is unspecified.
7. If `inbox` is removed, whether `MessageCLI._run_legacy` and its `--list/--show/--ack` grammar remain (Scope says the translation stays) is unclear.
8. Grep list covers only four exact `deskops `-prefixed spellings; unclear whether bare prose mentions, other orderings, or plural/singular variants count as in-scope hits.
9. No criteria distinguishing "deprecation note" from "recommendation" — Done When is a judgement call.
10. Which name is canonical for each pair is never stated (e.g. is `status` canonicalizing to `doctor`?).
11. Why the task depends on `task-rw-f5-output-renderer` is unexplained.
12. If `.pi/skills/use-deskops/SKILL.md` and `.opencode/skills/use-deskops/SKILL.md` diverge, no rule says which is authoritative.
13. No stated acceptance criteria for stderr when the alias is invoked with `--help` or with invalid args.
