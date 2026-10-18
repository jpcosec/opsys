# Executor result: task-docs-teach-closeout-commit-as-the-only-close

## What changed

- `docs/quickstart.md`
  - Intro now says the task closes with `deskops closeout commit`.
  - "Advance The Task" says `advance` stops at `ritual-closeout` and never closes.
  - "Close Out" rewritten: set `files`/`references`, then close with `--run-dir` or `--no-run --reason`.
  - Documents the board-routed `deskops closeout verify` gate: test evidence, a link for every changed file (atom/materialization or routed follow-up under `desk/tasks`, `desk/drawer/tasks`, `desk/drawer/issues`), and a commit reference that is `HEAD` or an ancestor.
  - States the commit reference must already exist, e.g. the task's promotion commit, because the closing commit is made by the command.
- `docs/faq.md`
  - `deskops advance task` entry now says it stops at `ritual-closeout` and the only close is `deskops closeout commit` with both routes.
  - Adds the board-routed verify gate and the earlier-commit rule.
- `deskops/data/faq.md`
  - Resynced packaged FAQ copy with `docs/faq.md` (required by `tests/test_packaging.py::test_packaged_faq_matches_the_human_copy`). This is data, not code.
- `.pi/skills/use-deskops/SKILL.md` and `.opencode/skills/use-deskops/SKILL.md`
  - CLI surface adds `closeout commit` (both routes) and `closeout verify`.
  - Key rules: `advance` stops at the closeout node; close only with `closeout commit`.
  - `.pi` is gitignored; the edit exists on disk but is not in `git status`.
- `docs/diagrams/process/current-agent-workflow-and-automation.mmd` and `.md`
  - `auto_advance` node now says it stops at `ritual-closeout` and never closes.
  - `auto_close` node now describes `deskops closeout commit`.
  - Flow edge changed from `close_gate --> auto_advance` to `close_gate --> auto_close`.
  - Section "automatic closeout side effect inside `advance_task()`" replaced with a `deskops closeout commit` section that documents the gate and refusal behavior.
  - Mermaid block in `.md` still matches `.mmd` byte-for-byte.

## Validation commands and results

- `grep -rn "advance task" docs README.md .pi/skills .opencode/skills`
  - Exit 0; only legitimate non-closing mentions remain (advance-to-closeout-node examples and command listings).
- `PYTHONPATH=/tmp/rw/wt/docsclose python -m pytest tests -q`
  - First run: `2 failed, 447 passed, 3 skipped in 703.98s (0:11:28)`
    - `test_packaging.py::test_packaged_faq_matches_the_human_copy` (caused by the `docs/faq.md` edit; fixed by syncing `deskops/data/faq.md`).
    - `test_taskdoc_read_without_overlay.py::test_read_doc_taskdoc_equals_extract_model_data` (pre-existing).
  - Second run after the data copy: `2 failed, 447 passed, 3 skipped in 688.53s (0:11:28)`
    - `tests/test_output_goldens.py::test_command_output_goldens` (pre-existing at HEAD).
    - `tests/test_taskdoc_read_without_overlay.py::test_read_doc_taskdoc_equals_extract_model_data` (pre-existing at HEAD).
- `PYTHONPATH=/tmp/rw/wt/docsclose python -m pytest tests/test_packaging.py tests/test_skill_cli_drift.py -q`
  - `7 passed in 9.68s`

## Pre-existing failures verified against unfixed HEAD

Created a detached worktree at HEAD `436919c` and ran the failing tests there:

- `PYTHONPATH=/tmp/rw/docsclose-head python -m pytest tests/test_taskdoc_read_without_overlay.py -q`
  - `1 failed in 0.46s`
  - Cause: `desk/drawer/tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md` uses `# Title` plus plain `ID:`/`Status:` lines instead of SLDB front matter. `extract_model_data(TaskDoc, ...)` raises `ValidationError` with `id` and `status` missing.
- `PYTHONPATH=/tmp/rw/docsclose-head python -m pytest tests/test_output_goldens.py::test_command_output_goldens -q`
  - `1 failed in 65.45s`
  - Cause: `tests/fixtures/golden/output/list_pills.json` has empty `what/why/when/where/how/how_not`; current sldb extracts the populated sections from `pill-golden-rule.md`.

Both are outside this docs-only task. `docs/drawer` history is explicitly out of scope, and the golden file is test data. No fix applied.

## Task issues / ambiguities

- The task refers to line numbers but cites none; only file names. Verified against current code instead.
- The task says "docs only" but `pytest tests` requires syncing the packaged `deskops/data/faq.md` copy. Synced that data file; no `deskops/` Python code changed.
- The task says `advance` stops at `ritual-closeout`. The runtime behavior matches through `TasksService.advance_task`, although `deskops/lifecycle.py` still contains generic terminal-transition support; `lifecycle.advance` would return a terminal result, and the service discards it and points at `closeout commit`. Docs describe the service/CLI behavior.
- Full suite cannot be green in this environment without unrelated desk/test-fixture changes (the two pre-existing failures above).

## Suspected sldb issue

Not recorded as an sldb bug. The `test_taskdoc_read_without_overlay` failure is an SLDB `ValidationError` triggered by a malformed desk document, not an sldb defect:

- File: `desk/drawer/tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md`
- Command: `PYTHONPATH=/tmp/rw/docsclose-head python -m pytest tests/test_taskdoc_read_without_overlay.py -q`
- Output: `pydantic_core._pydantic_core.ValidationError: 2 validation errors for TaskDoc; id Field required; status Field required`

## Supervisor note

The closeout gate required docs/diagrams/process/current-agent-workflow-and-automation.md to declare its sources, because it has a sibling .mmd. The supervisor added frontmatter with the 7 atoms the page already names as source_atoms, and the .mmd as provenance. Tests that mention diagrams: 29 passed.
