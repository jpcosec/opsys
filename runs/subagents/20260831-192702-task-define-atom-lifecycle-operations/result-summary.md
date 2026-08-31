# Result summary

- run_id: 20260831-192702-task-define-atom-lifecycle-operations
- session: unavailable-in-api-executor-context
- session_sha256: unavailable-in-api-executor-context
- task: task-define-atom-lifecycle-operations

## Scope completed

Implemented only the reduced scope fixed in `## Resolved Decisions`:

- added `deskops atoms validate [<id>|--all]`
- added `deskops atoms delete <id> [--force]`
- kept default inbound-reference behavior as BLOCK
- verified SLDB untrack support exists (`sldb docs untrack` and `sldb.cli.commands.doc.DocCLI.untrack`)
- created deferred drawer tasks for split, merge, and create-from-source instead of implementing them

## Touched surfaces

- `deskops/cli/parser.py`
- `deskops/cli/commands/atoms.py`
- `deskops/operations.py`
- `tests/test_atoms_cli.py`
- `desk/drawer/tasks/task-split-atoms-with-provenance-safe-rerouting.md`
- `desk/drawer/tasks/task-merge-atoms-with-reference-reconciliation.md`
- `desk/drawer/tasks/task-create-atoms-from-pill-graph-and-diagram-sources.md`

## Validation

See `validation.log`.

- `pytest tests/test_atoms_cli.py -q` ✅
- `pytest` ✅ (149 passed)

## Notes for supervisor

- `atoms validate` checks AtomDoc/model validity, single 5WH1+ via `AtomDoc`, tag namespaces via `validate_atom_tag_namespaces`, provenance resolvability, and `atom-<slug>` id convention.
- `atoms delete` scans inbound `atom:<id>` references across `desk/`, refuses deletion unless `--force`, deletes the atom file, and untracks it from `.sldb` when the atom is tracked.
- Reference files are not rewritten in either blocked or forced delete paths.
- `deskops graph missing --root .` already had unrelated pre-existing missing-reference findings during recovery; this task did not change board routing or repair them.
