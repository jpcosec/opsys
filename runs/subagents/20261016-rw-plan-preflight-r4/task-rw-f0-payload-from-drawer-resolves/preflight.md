RESTATEMENT:

1. Read the task doc, both pills (`pill-real-cli-surfaces-prove-operator-contracts.md`, `pill-cli-gaps-become-tracked-work.md`), and the referenced plan `runs/planning/deskops-rewrite-inventory.md` (phase F0).
2. Open `deskops/cli/commands/operations.py`; locate the add-task branch of `OperationsCLI.run` (lines ~21–27), `DeskopsOperations.resolve_drawer_source` (~551) and `attach_drawer_source` (~583).
3. Change selector acquisition: `selector = args.from_drawer or payload.get("from_drawer")`; if `args.from_drawer` is set, use it and do not inspect the payload value; treat absent/empty/`None` payload value as no drawer source.
4. Run the existing resolve/attach step on that selector; on `FileNotFoundError`/`ValueError` keep the current `Error: ...` print and `return 1` without creating a task.
5. Store the resolved repo-relative drawer path (e.g. `desk/drawer/tasks/task-rw-f0-x.md`) in the created task instead of the raw selector.
6. Create `tests/test_add_task_from_drawer.py`; import/use helpers `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`; build one throwaway repo in `tmp_path` (git init + seed commit), run `python -m deskops desk install <root>`, drive the real CLI via subprocess.
7. Test (a): one drawer entry `task-rw-f0-x.md`; create three tasks with distinct `id`s via `--from-drawer`, `--from-yaml`, and inline JSON; assert all three stored `from_drawer` values are the identical repo-relative path.
8. Test (b): JSON payload with an unknown selector; assert exit code 1 and no new file under `desk/tasks/`.
9. Test (c): two drawer entries sharing a fragment; JSON payload using that fragment; assert exit code 1 and nothing created.
10. Run `pytest tests/test_add_task_from_drawer.py`, then `pytest tests`.

AMBIGUITIES:

1. Status is `deferred`; the doc also says the supervisor promotes this drawer task and commits before dispatch — unclear whether that promotion already happened or is a precondition I must not assume.
2. Done When says "Both new tests pass" while Implementation Path lists three tests (a, b, c) — count is contradictory.
3. Test setup says "one sandbox repo with one drawer entry", but test (c) requires two drawer entries sharing a fragment — contradictory.
4. Ambiguity detection semantics are unspecified: is "ambiguous" multiple stems, substring match, fragment match, prefix match? I cannot know without `resolve_drawer_source`, which is not included.
5. Unclear whether `resolve_drawer_source` already fails on unknown/ambiguous selectors or must be extended; the doc says "run the existing resolve/attach step", so failure behavior for ambiguity is unverifiable from the doc.
6. The flag name and argument form for the "inline JSON payload" are never given (e.g. `--from-json`, `--json`, stdin) — cannot write test (b)/(c) as described.
7. Unclear whether `--from-yaml` takes a file path or inline YAML text.
8. Minimum payload fields are given only as "at least `title`"; other required/forbidden fields and status/tags defaults are unknown.
9. Exact form of the expected stored path is unverified: the example input stem `rw-f0-x` maps to `desk/drawer/tasks/task-rw-f0-x.md` with a `task-` prefix; whether the input selector is `rw-f0-x` or `task-rw-f0-x` matters for the assertions.
10. Whether the fix must also touch `deskops/specs/compiler.py:64` (named as the cause) or only `OperationsCLI.run` is unclear; the fixes may be mutually necessary.
11. The exact `Error: ...` text is unspecified; unclear whether tests must assert message content.
12. "Creates nothing"/"creates no `desk/tasks/` file" does not specify whether other side effects (drawer mutation, partial files, exit-code-only) must be asserted, nor whether the sandbox must remain clean/untracked.
13. The variable name/shape of `payload` in `OperationsCLI.run` is unverified (may be absent, non-dict, or named differently), so `payload.get("from_drawer")` is assumed.
14. No acceptance criterion covers the case where the flag and payload both carry a value beyond "flag wins"; neither behavior nor test is specified for whether the ignored payload value is validated.
15. Unclear whether a non-string `from_drawer` value (list, number, null-in-YAML) is in scope or should error.
16. Pill contents (`when`/`where`/`how_not`) are not in the doc, so binding correctness cannot be verified from the task text alone.
