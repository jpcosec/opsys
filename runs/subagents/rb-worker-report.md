# rb-worker: `deskops closeout resolved-by`

Task: `desk/tasks/task-closeout-resolved-by-cerrar-una-tarea-cuyo-trabajo-ya-entró-por-pr.md`.
Branch `wt/closeout-resolved-by`, base `24c8a824`. Brief: `~/proyectos/SLDB_1/coord2-ccconfig/rb-worker-brief.md`.
Logs: `~/proyectos/SLDB_1/coord2-ccconfig/rb/`.

## What changed

- `deskops/services/closure.py`: new method `ClosureService.close_resolved_by`, placed after `close_superseded` and following its pattern. Only added lines.
  1. It validates the reason, the refs and the tests, and then the task.
  2. It writes `status: resolved` and appends `resolved-by` to history with `doc_access.write_doc`.
  3. It calls `_close(route="resolved-by", run_gates=False, explicit_paths=True, ...)` with the trailers and `index_entry.mode = "resolved-by"`.
  4. If the close fails, it restores the file, exactly as supersede does.
- `deskops/cli/commands/closeout.py`: dispatches `resolved-by` to `_resolved_by`, passing `--paths` and `--message`. The class docstring and the usage line now include the subcommand.
- `deskops/cli/registry.py`: adds the command `closeout resolved-by`.
  - `--ref` and `--test` are repeatable and required; `--reason` is required.
  - `-m/--message` and `--paths` work the same way as in `closeout commit`.
  - The epilog follows the pattern of supersede.
- `tests/test_closeout_resolved_by.py` (new).
- Help goldens: `deskops_closeout.txt` and `deskops_closeout_resolved-by.txt` (new).
- `docs/operator-manual.md`:
  - a new subsection «Close a task whose work already entered the history»;
  - the paragraph that lists the ways to close now includes resolved-by;
  - a new row in the command table.
- `CHANGELOG.md`: new entry under `## [Unreleased]` / `### Added`.

## Acceptance

Commits: `0589ad49` (feature) and `4cd91183` (`test_command_registry`). Each pytest file ran on its own, behind the anchored `pgrep` guard, with `TMPDIR=/dev/shm` and `MemoryMax=2G`. The logs are in `coord2-ccconfig/rb/`.

1. **r6 coverage, nothing written on failure.** `tests/test_closeout_resolved_by.py`: **19 passed** (`test_closeout_resolved_by.log`).
   - **Success** (`test_resolved_by_closes_with_an_ancestor_commit_and_an_accepted_test`):
     - `status: resolved` and `- resolved-by` appear in the task as `_close` sees it (spy on `_close`).
     - The trailers are Task-Id, `Closeout-Mode: resolved-by`, Closeout-Reason, Closeout-Ref and Closeout-Test.
     - The task leaves the Board; `index_entry.mode` is `resolved-by`.
     - There is one closing commit (`HEAD~1` = HEAD before), it touches Board, the task and `index.jsonl`, and `git status` is clean.
   - **PR URL as an extra ref:** accepted; trailers in order `[commit, URL]` (`..._accepts_a_pr_url_as_an_additional_ref`).
   - **Test declared in `files` plus several tests:** one `Closeout-Test` per test (`..._accepts_a_test_declared_in_the_task_files_and_several_tests`).
   - **`--paths` and `--message` (b2):** they reach the closing commit (`..._passes_paths_and_message_to_the_closing_commit`).
   - **Failures with exit 1** (`test_resolved_by_refuses_and_writes_nothing`, 8 cases):
     - commit-less: only a URL;
     - ref that is a path (not a commit or URL);
     - ref `not-a-ref`;
     - unknown commit `000…0`;
     - missing test;
     - `.py` outside `tests/` and not in `files`;
     - one of two tests missing (d1);
     - blank reason.

     In each one, `_snapshot` is unchanged: the sha256 over `desk/` (paths and bytes), `git status --porcelain --untracked-files=all` and HEAD. `runs/` is not created.
   - **Missing flag with exit 2** (`..._requires_reason_ref_and_test_flags`, 3 cases): no `--reason`, no `--ref`, no `--test`. The snapshot is unchanged.
   - **Service called directly** (`..._service_refuses_missing_evidence_and_writes_nothing`, 3 cases): `refs=None`, `tests=None`, a blank test. The snapshot is unchanged.
   - **Unknown task:** exit 1, snapshot unchanged.
2. **Goldens.**
   - Generated with `pytest tests/test_output_goldens.py -k test_help_goldens --update-golden` (`update_help_goldens.log`, 1 passed).
   - `git status` afterwards shows only `M deskops_closeout.txt` and `?? deskops_closeout_resolved-by.txt`.
   - The new golden is the `--help` output of the subcommand, 34 lines (in the commit).
   - Diff of `deskops_closeout.txt`:

```diff
-usage: deskops closeout [-h] {commit,supersede,retire,verify} ...
+usage: deskops closeout [-h] {commit,supersede,retire,resolved-by,verify} ...
@@
-  {commit,supersede,retire,verify}
+  {commit,supersede,retire,resolved-by,verify}
@@
     retire              Remove a task that was already resolved before the
                         ritual lifecycle.
+    resolved-by         Close a task whose work already entered the history,
+                        naming an ancestor commit and a test.
```

3. **Tests run one at a time.**

| File | Result |
|---|---|
| `tests/test_closeout.py` | 49 passed |
| `tests/test_command_registry.py` | **1 failed, 2 passed**: only `('review', 'record')`, which **fails before my change**; see d5 |
| `tests/test_cli_help_examples.py` | 11 passed |
| `tests/test_output_goldens.py` | 7 passed |
| `tests/test_cli.py` (copy `/dev/shm/deskops-rb` at `0589ad49`, b4) | 101 passed |

   - The `/dev/shm` copy was removed with `git worktree remove --force`.
   - No process of mine remains in it.

4. **Untouched files.**
   - Against the base `24c8a824`, which is the merge-base with `origin/main`: `git diff 24c8a824 -- deskops/services/closeout_gates.py deskops/operations.py deskops/services/tasks.py` → 0 lines.
   - In `closure.py`: 112 lines added, 0 removed.
   - `close_superseded`, `close_retired` and `close_with_run` are unchanged.
5. **`wc -l`.**

| File | Before (`24c8a824`) | After |
|---|---|---|
| `deskops/services/closure.py` | 1103 | 1215 |
| `deskops/cli/commands/closeout.py` | 129 | 148 |
| `deskops/cli/registry.py` | 1873 | 1916 |
| `tests/test_closeout_resolved_by.py` | 0 | 400 |
| `tests/test_command_registry.py` | — | +1 |
| `docs/operator-manual.md` | 931 | 955 |
| `CHANGELOG.md` | 164 | 165 |
| `tests/fixtures/golden/help/deskops_closeout.txt` | 18 | 20 |
| `tests/fixtures/golden/help/deskops_closeout_resolved-by.txt` | 0 | 34 |

6. **CHANGELOG and manual.**
   - CHANGELOG: one entry under `## [Unreleased]` / `### Added`.
   - `docs/operator-manual.md`:
     - the subsection «Close a task whose work already entered the history», with a non-runnable example;
     - resolved-by in the list of ways to close (§ advance);
     - a row in the command table.

No changes in `desk/` or `.sldb/`. Paths were added one by one, never `git add -A`.

## Deviations and decisions

- **d1 (r2, tests): every `--test` must resolve, not just one.**
  - r2 says «al menos un --test tiene que pasar».
  - I rejected any test that does not resolve, the same way r2 already treats refs: a `Closeout-Test` trailer that names a missing file would be false evidence.
  - Effect: `--test tests/ok.py --test tests/missing.py` fails with exit 1.
  - Reversible: removing the rejection of the extra tests is a two-line change.
- **d2 (validation order):** the order is reason → refs → non-empty tests → task exists → each test against the task's `files`. Nothing is written before every check passes.
- **d3:** CLI-level absence of `--reason`, `--ref` or `--test` is an argparse error (exit 2), as with supersede. Only a blank value or an unresolvable one reaches the service (exit 1). Both paths are covered and write nothing.
- **d4:** `origin/main` moved forward while I was working (CC32: `6afc78b0..0e72f891`), and that work touches `CHANGELOG.md`.
  - My branch was not rebased.
  - On merge, the CHANGELOG entry may need a trivial conflict resolution in `### Added`.
  - The checks in item 4 are measured against the base `24c8a824` (the merge-base).
- **d5 (`test_command_registry`, a file outside the list):**
  - I added `("closeout", "resolved-by")` to `MUTATING_COMMANDS` (one line, commit `4cd91183`).
  - It is the test's invariant for every mutating command, so the subcommand cannot pass without it.
  - The test is still red because of `("review", "record")`:
    - the registry declares it mutating but the test does not list it;
    - this was already so at `24c8a824` and at `origin/main` (`git show <c>:tests/test_command_registry.py | grep -c '("review", "record")'` → 0 in both);
    - it is a CC32 follow-up (review record), and **I did not fix it** because it is out of scope.
  - It needs a one-line task or a decision from the coordinator.
- **r4 note (CC33):** `close_resolved_by` calls `reference_points_to_commit`, `reference_points_to_url` and `reference_points_to_test` as they are, and writes no evidence receipts. When CC33 turns the fact producers into receipts, it decides whether resolved-by writes `evidence` receipts.
