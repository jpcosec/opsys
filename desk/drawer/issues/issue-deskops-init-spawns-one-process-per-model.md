# `deskops init` spawns one Python process per model

## Kind

performance bug

## Status

resolved

## Resolution

Bootstrap now drives sldb in process (init_store, load_store_index, ModelCLI().add) with the subprocess path kept as the fallback for a bootstrap before install. Measured: `deskops init` 12.27s -> 1.28s on a fresh directory, and the six tests named here went from 9.6-12.5s each to 1-4s, taking the suite from 114s to 60s. Commit 3e863fe.

## Problem

`deskops init` takes ~8.5 s, almost all of it spent starting Python interpreters.

`BootstrapCLI.init_local_store` (`deskops/bootstrap.py:102`) calls `run_sldb` once for `stores init`, once for `models list` (`_registered_model_names`), and once per entry in `MODEL_REFS`. `run_sldb` (`deskops/bootstrap.py:132`) does:

```python
subprocess.run([sys.executable, "-m", "sldb", *args])
```

So a fresh store costs ~20 subprocesses, each paying ~0.4 s of interpreter start-up plus importing pydantic, sldb and markdown-it before doing any work.

Measured on 2026-09-10:

- Profile of `tests/test_cli.py::test_doctor_reports_invalid_documents`: 11.7 s total, of which `_init` 8.49 s; `run_sldb` called 20 times at 0.424 s each.
- `pytest --durations=20` over the full suite (273 tests, 113.9 s): six tests take 9.6–12.5 s each and every one goes through `init`. Together they are ~67 s of the 114 s. The next slowest test is 6.1 s (the end-to-end lifecycle, which shells out to the CLI on purpose) and everything else is under 2 s.

  - `test_cli.py::test_doctor_reports_untracked_documents_and_missing_structure` 12.51 s
  - `test_cli.py::test_doctor_reports_invalid_documents` 12.11 s
  - `test_doctor_unmodeled_surfaces.py::test_doctor_reports_only_untracked_sldb_modeled_surfaces` 11.24 s
  - `test_cli.py::test_add_task_tracks_generated_bundle_in_local_sldb_store` 10.99 s
  - `test_doctor_unmodeled_surfaces.py::test_doctor_ignores_intentionally_unmodeled_surfaces` 10.52 s
  - `test_cli.py::test_list_tasks_warns_on_malformed_artifact` 9.59 s

The same ~8 s is paid by every real `deskops init` in any repository.

## Desired Outcome

When sldb is importable, drive it in-process instead of through a subprocess per call — the same way `PromoteCLI._untrack_note` already calls `DocCLI().untrack(...)` directly:

- `stores init` → sldb's store-creation function
- `models list` → `load_store_index(...)` and read `.models`
- `models add` → `ModelCLI().add(SimpleNamespace(model=..., store=..., pythonpath=..., canonical=False))`

Keep the subprocess path only as a fallback for the bootstrap case where sldb is not importable yet (`_sldb_importable` already exists to tell the two apart).

## Questions

- Was the subprocess isolation deliberate (e.g. bootstrap running before sldb is installed into the environment)? If so, the fallback above preserves it.
- Each `models add` also runs `rebuild_semantic_indexes` and `cascade_hash_a` over the whole store. In-process removes interpreter start-up, but registering 18 models still rebuilds the indexes 18 times. A batch registration path in sldb (register all, rebuild once) would remove that too.

## Validation

- `pytest --durations=20` before and after; the six tests above should drop well below 2 s each.
- Wall time of `deskops init` on a fresh directory before and after.
- `sldb stores check` on the created store must still pass.
