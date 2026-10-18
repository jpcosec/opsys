# task-guard-extension-points — result summary

## Changes

- Added `tests/test_extension_points.py` (new file only; no runtime/desk changes).
  - `test_every_artifact_model_has_a_path` — `ARTIFACT_MODELS` and `ARTIFACT_PATHS` have the same key set.
  - `test_every_artifact_except_task_has_a_subject` — `set(ARTIFACT_MODELS) - set(ARTIFACT_SUBJECTS) == {"artifact.task"}` and no extra subjects.
  - `test_model_refs_are_exported_structured_documents` — every `MODEL_REFS` name is in `deskops.models.__all__` and resolves to a `StructuredNLDoc` subclass.
  - `test_every_spec_artifact_resolves_to_an_artifact_model` — every id in `SpecRegistry.load(data_path("spec")).artifacts` is in `ARTIFACT_MODELS` (or the task-only artifact).
  - `test_every_command_handler_resolves` — every `command_registry()` handler parses as `module:attribute` and the attribute is callable.

No registry fixes were needed; all contracts already agreed. No runtime behavior changed.

Note on cited locations: `ARTIFACT_MODELS` (operations.py:59), `ARTIFACT_PATHS` (operations.py:72), `ARTIFACT_SUBJECTS` (operations.py:85), `MODEL_REFS` (bootstrap.py:23), `command_registry()` (cli/registry.py:1330) were all at the expected places.

## Validation

- `PYTHONPATH=/tmp/rw/wt/extpoints python -m pytest tests/test_extension_points.py -q`
  - `5 passed in 0.49s`
- `PYTHONPATH=/tmp/rw/wt/extpoints python -m pytest tests/test_specs.py tests/test_command_registry.py tests/test_federated_models.py -q`
  - `8 passed in 18.81s`
- `PYTHONPATH=/tmp/rw/wt/extpoints python -m pytest tests -q`
  - `465 passed, 3 skipped in 972.93s (0:16:12)`

## Unfixed-code check

Before adding the test, ran the same assertions directly in an interpreter against the current tree:
all sets matched, 10 spec artifacts resolved, and all 107 command handlers imported and were callable.
Output was empty for every mismatch list; no fix was required. No red test existed to record.

## Wrong or ambiguous in the task

- Step 2 says every `ARTIFACT_MODELS` key exists in `ARTIFACT_PATHS`; the test also asserts the reverse, since the stated goal is that the registries agree.
- Step 5 calls `artifact.task` "the task-only artifact", but it is present in `ARTIFACT_MODELS` (and has a spec). The test accepts either branch as written.
- There is a second hardcoded artifact mapping, `artifact_model_fields()` in `deskops/cli/model_introspection.py`, that the task's enumerated checks do not cover. It currently matches `ARTIFACT_MODELS` minus `artifact.task`; no mismatch found, and it was not modified.

## sldb bugs

None observed.
