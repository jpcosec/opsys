RESTATEMENT:
1. Read task context: `desk/tasks/task-rw-f0-payload-from-drawer-resolves.md`, bound pills `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and `desk/contexts/pill-cli-gaps-become-tracked-work.md`, and `deskops/cli/commands/operations.py`.
2. Locate `resolve_drawer_source` and `attach_drawer_source` (`deskops/cli/commands/operations.py:21-27`) and confirm their inputs/outputs.
3. In `OperationsCLI.run`, determine the selector: use `args.from_drawer` if present, else `payload.get("from_drawer")`.
4. If a selector is present, run the same `resolve_drawer_source` + `attach_drawer_source` step used by the `--from-drawer` flag path so the stored value is the repo-relative drawer path.
5. Ensure an unknown or ambiguous selector exits 1 without creating a task.
6. Create `tests/test_add_task_from_drawer.py`.
7. Test A: invoke add-task with a YAML payload containing a stem `from_drawer` selector; assert stored value equals the resolved repo-relative drawer path.
8. Test B: invoke add-task with a JSON payload containing an unknown selector; assert exit 1 and assert no task artifact was created.
9. Run `pytest tests/test_add_task_from_drawer.py`.
10. Run `pytest`.

AMBIGUITIES:
1. `status: deferred` — whether this task is meant to be executed now or only preflighted.
2. Precedence when both `args.from_drawer` and payload `from_drawer` are set and differ (error vs args-wins?) is unstated.
3. Definition of "ambiguous selector" and the failure/error message text are unspecified.
4. Whether the code fix belongs only in `OperationsCLI.run` or must also touch `deskops/specs/compiler.py:64` (mentioned, but Scope says only handler + test).
5. Exact CLI flags for the YAML and JSON payload inputs are not named.
6. Which drawer task/stem the YAML test selector resolves to, and fixture setup, are unspecified.
7. Test desk root (sandbox vs repo `desk/`) is unspecified.
8. How "no task created" is asserted (which path/artifact) is unspecified.
9. "Stored path" inspection method (which file/field) is unspecified.
10. Test invocation style (subprocess vs in-process runner) is unspecified.
11. `resolve_drawer_source`/`attach_drawer_source` signatures and return values are not given.
12. The done condition "both input paths store the same resolved path" implies a flag-vs-payload equivalence test, but no such test is listed in Implementation Path.
13. Whether other `add` subcommands beyond `add task` must be covered is unstated.
14. Whether `args.from_drawer` is the actual argparse attribute name is not verified in the doc.
