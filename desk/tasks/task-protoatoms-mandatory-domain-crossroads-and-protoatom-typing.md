---
id: task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing
current_node: checklist-task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing-execution-ready
history: []
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing-execution-ready
- checklist-task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing-testing-ready
- checklist-task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-protoatoms-are-free-atoms-captured-before-typing
- atom-domain-crossroads-are-mandatory-parents
- atom-typing-a-protoatom-keeps-a-redirect-stub
---

# Protoatoms, mandatory domain crossroads and protoatom typing

## Rationale

_Explain why this task exists or the business driver behind it._

graph_ui's mindmap becomes a tag explorer: brainstorm nodes are free atoms placed by domain:<path> tags, and every branch of the domain tree must describe itself before holding children.

## Goal

_Describe the concrete result this task must produce._

Add ProtoAtomDoc and CrossroadDoc, enforce that every domain path prefix has a written crossroad, and add an explicit operation that types a protoatom into another sldb model while keeping a redirect stub.

## Scope

_State what is in scope and what is out of scope._

deskops models, a domain_tree module, atoms CLI subcommands (crossroad, proto, type, tree), domain checks in atoms validate --all and in atom creation, tests. The graph_ui tag-explorer UI is out of scope.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/models/protoatom.py, deskops/models/crossroad.py, deskops/domain_tree.py, deskops/cli/commands/atoms.py, deskops/cli/parser.py, deskops/operations.py (_all_atom_paths filter and creation hooks), deskops/bootstrap.py, tests/test_domain_tree.py

## Validation

_List the checks required before this task can close._

- python3 -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

Crossroads and protoatoms can only be created top-down, atoms validate --all reports missing or empty crossroads, typing yields a tracked typed document plus a redirect stub, and the full deskops suite passes.
