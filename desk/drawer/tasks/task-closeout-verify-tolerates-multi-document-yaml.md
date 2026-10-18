---
id: task-closeout-verify-tolerates-multi-document-yaml
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/operations.py
- tests/test_closeout.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- source:graph_ui
- topic:closeout
---

# `closeout verify` does not abort on a multi-document YAML outside desk/

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18 (desk/inbox/20261018-003127-unclear-closeout-verify-revienta-con-un-yaml-multi-documento-del-repo.md). In /home/jp/proyectos/SLDB_1/UIs/graph_ui, `deskops closeout verify --root . --task task-graph-ui-instalable-pyproject-con-dependencias-reales-y-sin-hacks-de-sys-path` ends with `Unexpected: expected a single document in the stream ... name: uml-clases ... but found another document`. The file is docs/representacion/propuesta-vocabulario-visual.assets/uml-clases.vocabulario.yaml, a legitimate YAML with several `---` documents that is not a desk document. Because verify aborts, the task never gets `closeout_evidence_verified` and stays at ritual-closeout; the advance gate reads the same evidence, so closing is blocked too.

## Goal

_Describe the concrete result this task must produce._

`closeout verify` and the closeout gate of `advance` complete on a repo that contains a multi-document YAML anywhere, and judge evidence exactly as before for every other file.

## Scope

_State what is in scope and what is out of scope._

In scope: the YAML/frontmatter read that raises (find it by reproducing: the traceback with `--debug` or by calling `DeskopsOperations(root).verify_task_closeout(id)` in Python), and one regression test. Out of scope: what counts as evidence.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce in a sandbox (lifecycle_desk fixture): add `docs/x.vocabulario.yaml` holding two documents (`name: a\n---\nname: b\n`), create a task whose `files`/`references` make verify scan the repo, run `deskops closeout verify --root . --task <id>`; it must fail today the same way.
2. Fix the read: a file that is not a single YAML document is not evidence of anything; read it with `yaml.safe_load_all` (or catch `yaml.YAMLError`) and skip it instead of raising. Do not swallow errors for desk documents that must parse.
3. Regression test in tests/test_closeout.py from step 1: verify exits per its normal evidence rules (not `Unexpected:`).

## Validation

_List the checks required before this task can close._

- pytest tests/test_closeout.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The regression test fails before the fix and passes after; `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` with the `lifecycle_desk` fixture (tests/conftest.py) or `_make_repo`/`_cli` from tests/test_lifecycle_end_to_end.py, and drive the real CLI. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
