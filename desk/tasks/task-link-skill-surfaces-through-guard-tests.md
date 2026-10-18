---
id: task-link-skill-surfaces-through-guard-tests
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
- deskops/constants.py
- deskops/operations.py
- desk/materializations/materialization-skill-drift-guards.md
- tests/test_closeout_skill_links.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Link skill surfaces through atom-linked drift guard tests

## Rationale

_Explain why this task exists or the business driver behind it._

Skill Markdown files cannot be graph nodes: `extract_doc_nodes` does not scan skill trees and
`extract_source_file_nodes` only creates `.py` nodes. As a result, every skill-touching task fails
`missing_changed_file_link` even when a tracked guard test reads the skill. The gate must not be
weakened to accept an arbitrary test.

## Goal

_Describe the concrete result this task must produce._

Accept a changed skill file as linked only when a tracked test that reads that skill tree is itself
linked to an atom or materialization, and emit evidence naming both the guard test and the skill
path.

## Scope

_State what is in scope and what is out of scope._

In scope: skill-tree constants, closeout link evidence, one materialization contract, and tests.
Out of scope: adding skill Markdown as graph nodes, weakening the atom/materialization requirement,
and changing the follow-up-reference fallback.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add `SKILL_TREE_PREFIXES = (".pi/skills/", ".agents/skills/", ".opencode/skills/")` to
   `deskops/constants.py`.
2. In `deskops/operations.py`, add `_skill_guard_test_evidence(relative_path, graph_context)`.
   Return `[]` unless the path starts with one of those prefixes.
3. Build the set of atom-linked test nodes from `graph_context["edges"]`:
   `edge.source` starts with `test_file:` and targets `atom:`, or `edge.target` is the test node
   and `edge.source` is a valid `materialization:` (not in `invalid_materializations`).
4. A candidate guard test qualifies only if its source text contains the skill tree prefix (or the
   exact relative path) and the token `SKILL.md`. Read candidate files under `tests/` only.
5. Return `guard-test:<test_path> -> <relative_path>` for each qualifying test.
6. In `_closeout_link_gate`, extend `file_evidence` with this helper before the follow-up fallback.
   Keep the existing fallback and all other gate behavior unchanged.
7. Create `desk/materializations/materialization-skill-drift-guards.md` as a
   `MaterializationContractDoc` with id `materialization-skill-drift-guards`, source atoms
   `atom-git-ignored-skill-trees-need-tracked-drift-guards` and
   `atom-tasks-enable-zero-context-subagents`, `target_kind: test_file`,
   `target_identity: tests/test_skill_cli_drift.py`, and validation
   `python -m pytest tests/test_skill_cli_drift.py -q`.
8. Add `tests/test_closeout_skill_links.py`:
   - a repo with an atom, the materialization contract, and `tests/test_skill_cli_drift.py`
     containing `.pi/skills` and `SKILL.md` verifies a task whose changed file is
     `.pi/skills/use-deskops/SKILL.md`;
   - the same repo without the materialization/atom link still reports
     `missing_changed_file_link`;
   - a changed Python module under deskops/ does not use this evidence path.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_closeout_skill_links.py -q
- python -m pytest tests/test_closeout.py tests/test_skill_cli_drift.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

An atom-linked guard test covers a changed skill file with explicit evidence; an unlinked or
non-matching test does not; non-skill changed files keep the existing gate behavior.
