---
id: task-document-the-atom-model-and-the-tag-namespace-workflow
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-document-the-atom-model-and-the-tag-namespace-workflow
current_node: checklist-task-document-the-atom-model-and-the-tag-namespace-workflow-testing-ready
history:
- operator-task-document-the-atom-model-and-the-tag-namespace-workflow-activate
references:
- docs/atoms.md
- a0afaea
- desk/atoms/atom-atom-folder-axis-is-one-configurable-tag-namespace.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-document-the-atom-model-and-the-tag-namespace-workflow-execution-ready
- checklist-task-document-the-atom-model-and-the-tag-namespace-workflow-testing-ready
- checklist-task-document-the-atom-model-and-the-tag-namespace-workflow-closeout-ready
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Document the atom model and the tag namespace workflow

## Rationale

_Explain why this task exists or the business driver behind it._

desk/drawer/issues/issue-document-atom-model-and-namespace-workflow.md: AtomDoc and tag namespaces are implemented, but nothing explains how to use them, so an agent has to read the model source to learn the rules.

## Goal

_Describe the concrete result this task must produce._

A durable doc, materializing the atoms that already carry these rules, that explains creating an atom, choosing the 5WH1+ question, how namespaces select the atom's folder, and how to add a namespace when existing ones do not cover the knowledge.

## Scope

_State what is in scope and what is out of scope._

docs/ plus the pointers to it from README and the desks ops skill. Reuses the existing atoms; does not invent new rules.

## Implementation Path

_Outline the expected implementation route or affected surface._

Read desk/atoms/atom-*.md, desk/atoms/tag-namespaces.yaml, deskops/models/atom.py, deskops/atom_tags.py and the atoms CLI. Write docs/atoms.md following the materialization convention already used by docs/sldb-templates.md (header listing the atoms it materializes). Add it to the docs index in README.md and to the skill route if the skill lists docs.

## Validation

_List the checks required before this task can close._

- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

docs/atoms.md exists, names the atoms it materializes, and every command it shows runs as written.
