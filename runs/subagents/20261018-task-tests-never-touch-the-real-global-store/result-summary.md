# Result summary: task-tests-never-touch-the-real-global-store

## Changes

- `tests/conftest.py`
  - Added autouse function-scoped fixture `_isolated_home(tmp_path, monkeypatch)`.
    - Creates `<tmp_path>/home`, writes a `.gitconfig` with `user.name` / `user.email`.
    - Sets `HOME` via `monkeypatch.setenv`, so in-process and inherited subprocess environments resolve `Path.home()` to the fake home.
  - No changes to `deskops/bootstrap.py`: global-store resolution (`Path.home() / ".sldb"`, lines 87 and 91) already honors `HOME`, and changing runtime global-store location is out of scope.
- `tests/test_global_store_isolation.py` (new)
  - `test_home_is_isolated_from_the_real_home`: asserts `Path.home()` is not the real home and has the fake `.gitconfig`.
  - `test_deskops_init_does_not_touch_the_real_global_store`: hashes `pwd.getpwuid(os.getuid()).pw_dir/.sldb/core/store_index.yaml`, runs `python -m deskops init` in a sandbox subprocess with the inherited env, asserts the real-store hash is unchanged and that the fake home received the global store index.

## Validation

Commands and final result lines:

```bash
sha256sum /home/jp/.sldb/core/store_index.yaml   # before/after each run
PYTHONPATH=/tmp/rw/wt/homeiso python -m pytest tests/test_global_store_isolation.py -q
# 2 passed in 4.44s

PYTHONPATH=/tmp/rw/wt/homeiso python -m pytest tests/test_cli.py tests/test_doctor_model_registration.py tests/test_doc_readability.py tests/test_federated_models.py tests/test_desk_sync.py -q
# 102 passed in 146.81s (0:02:26)

PYTHONPATH=/tmp/rw/wt/homeiso python -m pytest tests -q
# 414 passed, 3 skipped in 424.83s (0:07:04)
```

Real store hash before and after every run (including the full suite):

```
1cda861d167533c4f7123892ac33a2d93b3a022beac27167a50a65f74006bc4b  /home/jp/.sldb/core/store_index.yaml
```

## Run against unfixed code

- Did not run the test suite against unfixed code: tests spawn `deskops init` without HOME isolation and would mutate the real `~/.sldb`, which the task prohibits.
- Did run `env HOME=<tmp>/home PYTHONPATH=/tmp/rw/wt/homeiso python -m deskops init <tmp>/repo` against unfixed code; result `rc=0`, with `~/.sldb` created under the fake HOME. This confirms `Path.home()` follows `HOME`, which is the basis of the fixture.

## Notes / ambiguities

- Task metadata lists `deskops/bootstrap.py` under `files`, but no edit was needed there; the fixture covers both global-store reads (`ensure_global_store_and_models`).
- The task's cited line numbers were accurate: `deskops/bootstrap.py:87,91` (`Path.home()`), `tests/test_doctor_model_registration.py:86` (only pre-existing HOME isolation).
- Suite time rose from the stated ~3 min to ~7 min because the prescribed per-test fake HOME makes each real `deskops init` test build a fresh fake global store (~4.5 s each).
- No sldb defect found. `deskops init` under a fake HOME writes the expected artifacts under that home (`.sldb/`, `sldb/relation_types/`, `.cache/sldb`).
- No desk/ files or deskops state commands were run; no commit or git add was performed.
