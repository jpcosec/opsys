---
sldb:
  by: agent
  at: '2026-11-12T02:25:15Z'
  authority: generated
  via: create_document
id: task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper
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
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-los-tests-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-com-n.md
---

# Los tests de deskops leen la ruta del sldb hermano de la variable de entorno SLDB_SRC, con un helper común

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión del overlord (2026-11-11, revisable). 18 archivos de tests fijan el sldb hermano como la ruta relativa al repo (carpeta padre, sldb, src) y la anteponen a sys.path. Desde un worktree del SSD eso mete el checkout principal de sldb, que está fuera de uso mientras corre la demo de JP (sldb serve en el puerto 8085) y además está 115 commits atrás: los tests fallan o prueban contra un sldb viejo.

## Goal

_Describe the concrete result this task must produce._

Un solo helper común resuelve la ruta de sldb para los tests: lee la variable de entorno SLDB_SRC y, si no está definida, usa la ruta hermana de hoy; los 18 archivos lo usan y ninguno repite la línea fija.

## Scope

_State what is in scope and what is out of scope._

En alcance: los 18 archivos de tests que anteponen el sldb hermano a sys.path (se listan con un grep de la línea fija), el helper común (en conftest o en un módulo de tests, a elección del worker), CHANGELOG. Fuera: el código de deskops, y los dos tests que arman un árbol de trabajo falso con una carpeta sldb dentro (test_scion_runtime en su prueba del workspace y test_doctor_model_registration), que no usan el sldb hermano.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: ítem de drawer d120766d.

ESTADO ACTUAL: cada uno de los 18 archivos declara SLDB_SRC como la ruta hermana de sldb y la antepone a sys.path si no está. Son test_atom_folder_axis, test_atom_materialization, test_atom_tags, test_atoms_cli, test_atoms_create_from_source, test_atoms_merge, test_atoms_split, test_cli, test_composition, test_domain_tree, test_legacy_task_states, test_lifecycle_seed_drift, test_materialization_contract, test_materialization_targets_outside_package, test_model_validators, test_role_materialization, test_scion_runtime y test_task_lifecycle_validator. El proyecto no tiene tests/__init__ y pytest corre con pythonpath = [.]. conftest se carga antes que cualquier módulo de test.

CAMBIO (s1-s4):
s1: un helper común que resuelve la ruta de sldb. Con SLDB_SRC definida, esa ruta manda y debe existir: si no existe, falla rápido con un mensaje que nombra la variable y la ruta (revisable). Sin la variable, la ruta hermana de hoy, que se antepone a sys.path solo si existe.
s2: los 18 archivos pierden su bloque fijo y usan el helper (la inserción de la raíz del repo en sys.path se queda como está). Si basta con que conftest antepone la ruta una vez, los 18 archivos solo borran su bloque; si no, importan el helper. El worker elige y lo dice en el informe.
s3: orden de imports: la ruta de sldb tiene que estar en sys.path antes de que cualquiera de los 18 archivos importe sldb o deskops, igual que hoy; con un archivo suelto (python -m pytest tests/<archivo>) también.
s4: CHANGELOG y, si hay una sección de cómo correr los tests en docs, una línea sobre SLDB_SRC.

VALIDACIÓN: la suite completa de a un archivo desde una copia en /dev/shm, dos veces: (a) con SLDB_SRC apuntando al src de un clon de sldb origin/main en /dev/shm, y (b) sin la variable y con un clon de sldb como carpeta hermana de la copia (la copia de deskops en una carpeta de /dev/shm que tenga al lado una carpeta sldb). Más una corrida con SLDB_SRC apuntando a una ruta que no existe, que debe fallar con el mensaje del helper. Un grep de la línea fija sobre tests/ queda vacío fuera del helper. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Grep de la línea fija (carpeta padre, sldb, src) sobre tests/: vacío fuera del helper común
- Suite completa de a un archivo desde /dev/shm con SLDB_SRC apuntando a un clon de sldb origin/main: verde
- Suite completa de a un archivo desde /dev/shm sin la variable, con sldb como carpeta hermana: verde
- SLDB_SRC apuntando a una ruta inexistente falla con un mensaje que nombra la variable y la ruta
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

s1-s4 hechos, el grep vacío, las dos suites completas en verde y el caso de ruta inexistente probado; CHANGELOG actualizado.
