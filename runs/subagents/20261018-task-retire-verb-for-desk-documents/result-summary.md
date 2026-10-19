# result summary: task-retire-verb-for-desk-documents

Done by the supervisor directly.

- `deskops/services/retire.py`: `retire_document(root, path, reason, refs, force)`. Requires a file under desk/. Refuses tasks, drawer entries, atoms and registry entries, naming their dedicated verb. Requires a non-empty reason and refs that resolve (an ancestor commit or an existing path). Refuses while desk/, docs/, README.md or AGENTS.md reference the file by path or stem, unless --force. Deletes and untracks through `DocTransaction.delete`.
- `deskops/cli/commands/retire.py` and a `retire` registry entry (mutates, raw-text epilog with an example). Help goldens updated; the root-help test, the mutating-commands list and the CLI grammar test include `retire`.
- `tests/test_retire_cli.py`: a tracked pill is retired with its store record; a referenced file is refused, then allowed with --force; Board.md is refused with a pointer to closeout; an unresolvable ref is refused; a non-markdown leftover is retired.

Validation: the full suite gave 540 passed and 1 failed. The failure was the root-help test, which expected the old command list. After that one-line fix, tests/test_cli.py -k help_uses passes.
