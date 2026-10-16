RESTATEMENT:
1. Verify `task-rw-f5-output-renderer` is closed; if not, stop (task is blocked).
2. Obtain the owner decision for each duplicate pair: `inbox`→`message`, `status`→`doctor`, `atoms list`/`atoms show`→`list`/`show atoms`.
3. Read `deskops/cli/registry.py`; locate the registrations for `inbox`, `status`, `atoms list`, `atoms show`.
4. Apply the decision per command:
   - Alias: add `deprecated_for=<canonical>` to the registry entry, keep command callable.
   - Remove: delete the registry entry.
5. Update the dispatcher so that invoking an entry with `deprecated_for=` prints a deprecation warning to stderr and still runs the canonical handler.
6. Update `docs/faq.md` to drop or annotate every old name.
7. Update `.pi/skills/use-deskops/SKILL.md` and `.opencode/skills/use-deskops/SKILL.md` to the same effect.
8. Run `pytest`.
9. Run `deskops inbox --help`.
10. Run `deskops faq`.
11. Add/adjust tests covering alias warning-on-stderr and removal behavior.
12. Make the task's atomic commit.

AMBIGUITIES:
1. The owner decision itself is unresolved; can't pick alias vs removal for any pair.
2. Which name in each pair is canonical is unstated (`inbox` vs `message`, `status` vs `doctor`, `atoms list/show` vs `list/show atoms`).
3. Whether "each duplicate" is exactly these three pairs or a larger set is not defined.
4. Warning text, format, prefix, and whether it goes before/after output are unspecified.
5. Whether alias warnings should be suppressible (flag/env) is unspecified.
6. Whether a `deprecated_for=` attribute already exists in the registry schema, or must be added, is not stated.
7. Whether removal is allowed as a breaking change / needs a deprecation cycle is not stated.
8. Whether `atoms list/show` are subcommands of an `atoms` group vs top-level is not stated.
9. Whether the two skill copies must be byte-identical or may diverge is not stated.
10. Whether existing tests referencing old names must be updated or are part of acceptance is not stated.
11. Acceptance criterion "no doc recommends a deprecated name" lacks a defined check/command.
12. The task is `status: blocked`; whether execution is permitted before unblocking is unclear.
13. The referenced pill file contents are not provided, so its constraints are unknown.
14. No done-criteria for the removal path behavior (e.g., error message on invoking a removed command).
