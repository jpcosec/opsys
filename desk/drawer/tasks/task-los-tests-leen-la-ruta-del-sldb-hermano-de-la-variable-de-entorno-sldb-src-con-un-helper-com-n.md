---
id: task-los-tests-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-com-n
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los tests leen la ruta del sldb hermano de la variable de entorno SLDB_SRC, con un helper común

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-los-tests-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-común.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-los-tests-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-común.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Decisión del overlord (2026-11-11, revisable), tarea chica que va de drawer directo, sin TaskDoc (regla 3). 18 archivos de tests fijan SLDB_SRC = ROOT.parent / 'sldb' / 'src' y lo anteponen a sys.path (grep: test_cli, test_atoms_merge, test_atoms_create_from_source, test_legacy_task_states, test_domain_tree, test_atom_tags, test_atoms_cli, test_atoms_split, test_model_validators, test_atom_folder_axis, test_atom_materialization, test_role_materialization, test_composition, test_materialization_contract, test_materialization_targets_outside_package, test_lifecycle_seed_drift, test_scion_runtime, test_task_lifecycle_validator). Desde un worktree del SSD eso mete el checkout principal ~/proyectos/SLDB_1/sldb, que está fuera de uso mientras corre la demo de JP y además está viejo (1d475bcd). Hecho cuando: un helper común (en tests/conftest.py o un módulo de tests) lee la ruta de la variable de entorno SLDB_SRC, con ROOT.parent / 'sldb' / 'src' como valor por defecto, solo la antepone si existe, y los 18 archivos lo usan en lugar de la línea fija; grep de 'ROOT.parent / "sldb" / "src"' vacío fuera del helper; la suite completa de a un archivo en verde con SLDB_SRC apuntando a un clon en /dev/shm y también sin la variable desde /dev/shm.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
