RESTATEMENT:
1. Confirm dependency `task-rw-f2-transactional-doc-io` is complete.
2. Create `deskops/services/__init__.py`.
3. Create `deskops/services/drawer.py` with `class DrawerService` constructed as `DrawerService(root: Path)`, importing `deskops.desk_paths` and `deskops.doc_io` as modules.
4. Move `DRAWER_INDEX_FILES` (~549), `resolve_drawer_source` (~551), `attach_drawer_source` (~583) from `deskops/operations.py` into `DrawerService`.
5. In `DeskopsOperations.__init__`, build the service lazily; convert the three old members into one-line wrappers delegating to it.
6. Move the non-CLI logic of `PromoteCLI` from `deskops/cli/commands/promote.py` into `DrawerService`; leave `PromoteCLI` delegating.
7. Run unmodified: `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py`, then `pytest tests`.
8. Verify Done When: `def resolve_drawer_source` in `deskops/operations.py` is a one-line wrapper; `grep -n DrawerService deskops/cli/commands/promote.py` matches.
9. Do not commit; hand diff to supervisor for closeout.

AMBIGUITIES:
1. "Non-CLI logic of `PromoteCLI`" is not enumerated; no list of which methods/helpers move vs stay.
2. Whether `DRAWER_INDEX_FILES` must remain importable from `deskops/operations.py` for existing importers, or moves entirely.
3. "Lazily" is unspecified: property, cached attribute, or factory not stated.
4. Wrapper requirements conflict slightly: Done When names only `resolve_drawer_source` as one-line, while Scope says all old methods become one-line wrappers; signature/return-parity not stated.
5. `deskops/services/__init__.py` content unspecified (empty vs re-export of `DrawerService`).
6. How, and from where, `PromoteCLI` obtains `root` and constructs/delegates to `DrawerService` is not stated.
7. The two listed pills are given with no concrete constraints to apply.
8. Dependency state of `task-rw-f2-transactional-doc-io` is not verifiable from this document; no check named for it.
9. "Unchanged behavior" has no acceptance criterion beyond the named tests; no coverage or output-parity target given.
