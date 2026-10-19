---
id: task-derived-store-out-of-git
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
- .sldb/store.yaml
- .gitignore
- .github/workflows/tests.yml
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops declares its store in .sldb/store.yaml and takes .sldb/core out of git

## Rationale

_Explain why this task exists or the business driver behind it._

Owner decision of 2026-10-19, design in sldb docs/architecture/derived-store-boundary.md (inbox note 20261019-112931). What the store derives does not belong in git. deskops is step 2 of the coordinator's order because it owns the federated models: sldb, spec2viz and graph_ui link ../deskops/.sldb.

## Goal

_Describe the concrete result this task must produce._

.sldb/store.yaml declares deskops' models, predicates and include rules with no absolute paths. .sldb/core/ is git-ignored and removed from the index. In a clean clone with sldb as a sibling, `sldb stores build` and `sldb stores check` pass. CI runs `sldb stores build` before pytest and `sldb stores build --check`. spec2viz and graph_ui are told by inbox.

## Scope

_State what is in scope and what is out of scope._

In scope: .sldb/store.yaml, .gitignore, `git rm -r --cached .sldb/core`, .github/workflows/tests.yml, scripts/ci-knowledge-check.sh if it needs a build first, and any test that reads the committed store. Out of scope: other repos' stores and sldb's declare command (gaps are reported to sldb).

## Implementation Path

_Outline the expected implementation route or affected surface._

Blocked until sldb step 1 is green on origin. A local dry run on 2026-10-19 passed `declare --write` and `build --check`, but showed two declare gaps, reported to sldb: absolute paths for sldb-package models (RelationTypeDoc, RelationDoc), and include rules taken from the current index (BoardDoc glob desk/tasks/*.md, no TaskDoc rule). Then: 1. declare --write; hand-write the include rules per folder (BoardDoc desk/tasks/Board.md, TaskDoc desk/tasks/task-*.md and desk/drawer/tasks/task-*.md, AtomDoc/PillDoc/RitualDoc globs); fix the model paths per sldb's answer. 2. build --check PASS. 3. Before git rm, confirm build --check rebuilds everything currently in .sldb/core; anything that cannot be rebuilt goes to the coordinator first. 4. Ignore .sldb/core/ and git rm -r --cached .sldb/core. 5. Clean-clone proof with sldb as a sibling: build and check PASS, pytest green, then delete the clone. 6. CI: checkout sldb as a sibling, run stores build before pytest, and add a build --check step. 7. Push, then inbox spec2viz and graph_ui.

## Validation

_List the checks required before this task can close._

- sldb stores build --check --store .sldb
- python -m pytest tests -q
- bash scripts/ci-knowledge-check.sh .

## Done When

_Name the observable condition that makes the task complete._

store.yaml and .sldb/README.md are the only tracked .sldb files, a clean clone builds and checks PASS, CI is green with build --check, and spec2viz and graph_ui have been told.
