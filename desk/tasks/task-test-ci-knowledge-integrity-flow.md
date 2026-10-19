---
id: task-test-ci-knowledge-integrity-flow
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- scripts/ci-knowledge-check.sh
- tests/test_ci_integration.py
- .github/workflows/tests.yml
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Test the CI knowledge-integrity flow

## Rationale

_Explain why this task exists or the business driver behind it._

Drawer use case UC-15 and stress test ST-15 promise that a PR checks knowledge integrity, not only pytest. Each command's exit code is tested on its own, but .github/workflows/tests.yml runs only pytest, and no test exercises the combined check.

## Goal

_Describe the concrete result this task must produce._

scripts/ci-knowledge-check.sh <root> runs the desk integrity checks: `deskops doctor`, `sldb stores check` and `deskops graph missing`, which gate (non-zero fails), and `deskops drift check`, which is reported and does not gate because its findings are review items. A test runs the script against sandbox desks, and the GitHub workflow runs it on the repository after pytest.

## Scope

_State what is in scope and what is out of scope._

In scope: scripts/ci-knowledge-check.sh, tests/test_ci_integration.py (isolated HOME, sandbox desk under tmp_path), and a step in .github/workflows/tests.yml. Out of scope: running pytest from the script, which would recurse under the test; changes to the checks themselves; release and tagging.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Write the script with `set -u`. It runs the three gating checks, failing on the first non-zero, then runs drift check with its output shown and its exit code ignored. 2. tests/test_ci_integration.py: a fresh `deskops init` sandbox makes the script exit 0; a doc with a dangling source_atoms reference makes it exit non-zero. 3. Add a workflow step `bash scripts/ci-knowledge-check.sh .` after pytest. 4. Run the script on this repository and check it exits 0.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_ci_integration.py -q
- bash scripts/ci-knowledge-check.sh .
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The test proves the script passes on a clean sandbox and fails on a dangling reference, the workflow runs it, the script exits 0 on this repository, and `pytest tests` is green.
