---
id: task-goldens-hold-across-sldb-extraction-and-python-versions
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
- tests/test_output_goldens.py
- tests/test_doc_readability.py
- tests/fixtures/golden/output/list_pills.json
- tests/fixtures/golden/output/list_rituals.json
- tests/fixtures/golden/output/show_pill.json
- tests/fixtures/golden/output/show_pill.text
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# The golden and readability tests hold across sldb's extraction fix and Python 3.12

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18 sldb 9dcabd9a stopped literal template paragraphs from matching any paragraph by position. Hand-written documents now extract their real text. The deskops output goldens (list_pills, show_pill, list_rituals) had recorded the old, buggy empty fields, and tests/test_doc_readability.py asserted that `what` was unreadable. spec2viz-49's integrated run on Python 3.12.3 also failed test_help_goldens: argparse wraps the usage block and spells short options differently on 3.12 than on 3.13.

## Goal

_Describe the concrete result this task must produce._

`pytest tests` is green on Python 3.12 and 3.13 against sldb main. The goldens record the real extracted values, the readability test asserts the detector's contract rather than one sldb behavior, and the help goldens compare usage text and option spelling independently of the Python version.

## Scope

_State what is in scope and what is out of scope._

In scope: tests/fixtures/golden/output (re-recorded with --update-golden), tests/test_output_goldens.py (help comparison normalizes the usage block and 3.12 short-option spelling), tests/test_doc_readability.py. Out of scope: the CI Python version.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Re-record the output goldens and review that the diff only fills fields that were empty. 2. In _check_golden, for help/ goldens, compare after collapsing the usage block and rewriting `-x METAVAR, --long METAVAR` to `-x, --long METAVAR`. 3. Make the readability test assert that every reported field extracts empty and at least one does.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_output_goldens.py tests/test_doc_readability.py -q
- /tmp/rw/venv312/bin/python -m pytest tests/test_output_goldens.py -q -k help_goldens
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The help golden test passes on 3.12 and 3.13, and `pytest tests` is green.
