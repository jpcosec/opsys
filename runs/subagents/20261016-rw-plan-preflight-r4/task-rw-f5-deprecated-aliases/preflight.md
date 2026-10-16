RESTATEMENT:

1. Stop: task status is `blocked`; confirm depends_on `task-rw-f5-output-renderer` is closed and obtain the owner's per-duplicate decision (`inbox`, `status`, `atoms list`, `atoms show` → alias or removal) before touching files.
2. In `deskops/cli/registry.py`: locate each duplicate's registration. For each survivor add `deprecated_for="<canonical path>"`. For each removal, delete its registration so it is no longer a valid parser choice.
3. In `deskops/cli/main.py` dispatcher: for any resolved command carrying `deprecated_for`, write ``Deprecated: use `deskops <canonical>` `` to stderr before any stdout, then run the canonical handler. Removed names are absent from choices, so argparse emits `invalid choice` and exits 2.
4. Leave the alias help listing and deprecation note intact for survivors (`deskops/cli/parser.py:500-505`), matching `tests/test_cli.py:42` and `tests/test_message_cli.py:35`.
5. If `inbox` survives, keep `MessageCLI._run_legacy` flag translation (`deskops/cli/commands/message.py:32,57`) for `--list/--show/--ack`.
6. Update `tests/test_cli.py` and `tests/test_message_cli.py`: for each survivor, one test running the alias and the canonical command with equivalent args, asserting the stderr deprecation line and byte-identical stdout; for each removed name, assert exit code 2 and `invalid choice`.
7. Run the validation grep: `grep -rn 'deskops inbox\|deskops status\|deskops atoms list\|deskops atoms show' docs .pi/skills .opencode/skills README.md desk/atoms desk/contexts`; rewrite recommending hits to the canonical name; keep deprecation notes only for survivors; zero hits for removed names.
8. Edit `docs/faq.md`, `README.md`, `.pi/skills/use-deskops/SKILL.md`, `.opencode/skills/use-deskops/SKILL.md`, and any hit files under `desk/atoms`/`desk/contexts`. Do not edit `desk/drawer/`.
9. Run `pytest tests`, `pytest`, and `deskops faq`.
10. Do not commit; report diff to supervisor for closeout.

AMBIGUITIES:

1. Owner decision is unresolved for all four duplicates; no per-name value given, so no file can be edited.
2. Canonical target for `atoms list`/`atoms show` is stated as `list atoms`/`show atom` only by implication; the warning template `deskops <canonical>` is ambiguous for a two-token canonical (e.g. `deskops list atoms` vs `deskops list-atoms`).
3. `deprecated_for="<canonical path>"` format is unspecified (dotted path, string, list?).
4. `files:` omits `desk/atoms` and `desk/contexts`, which the Scope and Validation grep require editing — contradiction.
5. "Equivalent args" for `inbox` vs `message` is undefined given `inbox --list/--show/--ack` vs message's own grammar.
6. Scope says the `inbox` flag translation "stays", but removal behavior would make `_run_legacy` dead/contradictory.
7. Whether removal also drops the alias from `--help` output (and which assertion covers that) is unstated.
8. Grep patterns are prefixed with `deskops`, so bare mentions (`inbox`, `status`) in prose are not covered by "every remaining grep hit".
9. "deprecation note, not a recommendation" has no objective criterion; no acceptance test distinguishes them.
10. Removed-name test invocation (bare command, or with args) and expected stderr text beyond `invalid choice` are unspecified.
11. `.pi` and `.opencode` skill copies may be generated from one another; regeneration mechanism unknown, risking drift.
12. No check ties `deskops faq` output to the updated names, so its pass criterion is undefined.
13. Whether canonical commands must accept the aliases' removed flags after removal is unstated.
14. Whether `inbox`/`status`/`atoms` remain as namespaces while only subcommands are removed is unstated.
