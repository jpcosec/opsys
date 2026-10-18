# Result: task-init-repairs-a-broken-owner-link

## Changes

- `deskops/bootstrap.py`
  - `SLDBBootstrap._ensure_owner_link`: reads the `deskops` link through `sldb.api.store_links` (`{name, path, resolved, status}`).
    - Healthy link pointing at the owner store: unchanged (`False`).
    - Healthy link pointing at another real store: keeps the existing warning and returns `None` (no replace).
    - Broken link (`status` `missing`/`not-a-store`) and sldb exposes `replace`: calls `doc_io.link_store_alias(..., replace=True)`, prints `Replaced broken 'deskops' link ...`, returns `True`.
    - Broken link but old sldb without `replace`: keeps the old warning and skips.
  - `SLDBBootstrap._link_store_supports_replace`: feature detection via `inspect.signature(sldb.api.link_store).parameters` (no version check).
- `deskops/doc_io.py`
  - `link_store_alias(root, other_store, name, *, replace=False)` now forwards `replace` to `sldb.api.link_store`.
- `tests/test_doctor_model_registration.py`
  - `test_init_repairs_a_broken_deskops_link`: init a repo, re-point its `deskops` link at a directory that is then deleted (`missing`), re-run `deskops init`, assert the link resolves to the owner store and `python -m sldb stores check --quiet` exits 0.
  - `test_init_leaves_a_healthy_deskops_link_to_another_store`: init two repos, re-point the first's `deskops` link at the second real store, re-run init, assert the warning is printed and the link target is unchanged.
  - Helpers `_store_index`, `_deskops_link`, `_point_deskops_link_at`, `_sldb_stores_check`.

## Validation (all commands prefixed with `PYTHONPATH=/tmp/rw/wt/ownerlink`)

- `python -m pytest tests/test_doctor_model_registration.py`
  - `8 passed in 74.46s`
- `python -m pytest tests`
  - `462 passed, 3 skipped in 840.75s (0:14:00)` (exit 0)
- `python -m pytest tests -q`
  - `462 passed, 3 skipped in 935.64s (0:15:35)` (exit 0)

## Test against unfixed code

- With `deskops/bootstrap.py` and `deskops/doc_io.py` restored from `HEAD`:
  `python -m pytest tests/test_doctor_model_registration.py -k 'repairs_a_broken or leaves_a_healthy'`
  - `1 failed, 1 passed, 6 deselected in 25.44s`
  - `test_init_repairs_a_broken_deskops_link` failed at `assert "Replaced broken 'deskops' link" in out` (old code only warned and skipped).
  - `test_init_leaves_a_healthy_deskops_link_to_another_store` passed, as expected (behavior unchanged for healthy links).

## Task notes / ambiguities

- No line numbers were cited in the task; the cited files matched.
- Dependency floor left at `structuredLanguageDB>=0.1.12` as instructed. sldb main still reports 0.1.12 in its `pyproject.toml`.
- The task refers to sldb commit `691f1ae`; the editable checkout `/home/jp/proyectos/SLDB_1/sldb` is at `c7e47254`, which already contains `link_store(replace=)`, `unlink_store`, `store_links`/`broken_links`. No sldb bug found.
- Non-importable sldb fallback in `_ensure_owner_link` (CLI path) was left as-is: it cannot inspect link status without richer CLI output parsing. In practice `deskops bootstrap`/`init` install sldb before reaching this path.
- Scope note: the repair branch uses `link_store(replace=True)`, which internally drops the broken link entry; `unlink_store` is not called directly (it would refuse while models still inherit from the link name).
