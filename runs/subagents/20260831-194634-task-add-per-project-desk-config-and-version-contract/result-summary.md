# Result summary

- run_id: 20260831-194634-task-add-per-project-desk-config-and-version-contract
- child session path: unavailable-in-api-context
- session_sha256: 4cf3049e4ef4144debce6c7fe6759f9f77b98f17828920593f4da207b543ac5e

## Scope completed

Implemented the requested config-contract delta only:

- hardened `DeskConfig.load` to deep-merge `desk/config.json` then `desk/config.local.json`
- preserved missing-file tolerance while surfacing malformed JSON through warnings plus `load_warnings`/`has_load_warnings`
- centralized the current `desk_format` constant and reused it from config loading and desk scaffolding
- documented authoritative precedence in code comments, a new atom, and `README.md`
- added tests for nested `versions` override and malformed JSON warning behavior

## Validation

- `pytest tests/test_config.py -q` ✅
- `pytest -q` ✅

## Touched files

- `deskops/constants.py`
- `deskops/config.py`
- `deskops/workspace.py`
- `deskops/cli/main.py`
- `desk/atoms/workflow-model/atom-desk-test-root-precedence-is-explicit.md`
- `README.md`
- `tests/test_config.py`
