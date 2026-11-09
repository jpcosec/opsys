---
id: task-closeout-el-gate-de-tests-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_closeout_test_paths.py
- pytest tests/test_closeout_gates.py
- 1a7107dc2791fe8c685c38b002814a8e5d8aa8b0
- desk/atoms/atom-el-gate-de-tests-del-closeout-acepta-py-bajo-cualquier-tests-del-repo-o-declarados-en-files.md
depends_on: []
pills: []
files:
- deskops/services/closeout_gates.py
- tests/test_closeout_test_paths.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-closeout-commit-reference-points-to-test-solo-acepta-root-tests-py.md
---

# closeout: el gate de tests acepta .py bajo cualquier tests/ del repo o declarados en files

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de deskops que viene de AntonIA (Chatbot_Infra), encargado por el overlord el 2026-11-09. El gate de tests del closeout (deskops/services/closeout_gates.py:149, reference_points_to_test) solo acepta archivos .py bajo <root>/tests/. Chatbot_Infra tiene sus pruebas en ops/tests, runtime/*/tests y paquetes/*/tests, así que sus tareas de código quedan trabadas en ritual-closeout aunque citen sus tests. Fuentes: este drawer (inbox desk/inbox/20261026-123537-unclear-closeout-commit-reference-points-to-test-solo-acepta-root-tests-py.md) y la nota sin trackear desk/inbox/20261104-222852-suggestion-closeout-las-pruebas-en-paquete-tests-no-cuentan-como-evidencia.md del main compartido de deskops, que se lee pero no se toca.

## Goal

_Describe the concrete result this task must produce._

reference_points_to_test acepta como evidencia de tests un archivo .py existente dentro del repo que esté bajo cualquier directorio tests/ (<root>/tests/** o */tests/**), o cuya ruta esté declarada en files del TaskDoc. Sigue rechazando las rutas absolutas, las que salen del root con .., los archivos inexistentes y las cadenas que solo parecen evidencia. Hay tests del rechazo y de la aceptación.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/closeout_gates.py (reference_points_to_test, _test_path_candidates y la llamada en closeout_reference_evidence, solo para pasarle files), un archivo de test nuevo tests/test_closeout_test_paths.py y una entrada en CHANGELOG.md (## [Unreleased]). Fuera: tests/test_closeout_gates.py (lo toca CC35a), reference_points_to_document (su exclusión de <root>/tests no cambia), las otras clases de evidencia, el resto de closeout_gates.py, desk/ y .sldb/, y las notas de inbox.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (origin/main 5e25164c): deskops/services/closeout_gates.py (278 líneas). closeout_reference_evidence (:89) recorre payload["references"] y, para cada una, reference_points_to_test (:149) decide si es evidencia de tests. Hoy acepta solo un .py existente bajo <root>/tests/, con sufijo ::nodo opcional y la forma «pytest <ruta>» (_test_path_candidates, :210). Rechaza rutas absolutas y las que escapan de tests/ con ... Los tests existentes del gate viven en tests/test_closeout_gates.py.

PRECISIONES (coordinador del plan, 2026-11-09):
p1 (evidencia nueva): una referencia es evidencia de tests cuando, tras quitar ::nodo y la forma pytest, nombra un archivo .py existente, relativo al root, que resuelto queda dentro del root, y además cumple (a) o (b). (a) Alguno de sus directorios, relativo al root, se llama exactamente «tests» (tests/x.py, runtime/foo/tests/test_x.py, ops/tests/sub/test_y.py). (b) Su ruta, normalizada, está en files del TaskDoc (payload["files"]). La evidencia sigue saliendo de references: files solo amplía qué ubicaciones cuentan, no es evidencia por sí mismo.
p2 (rechazos que se mantienen o se agregan): rutas absolutas; rutas que tras resolver salen del root (incluye .. y symlinks hacia fuera); archivos inexistentes; sufijo distinto de .py; cadenas que solo parecen evidencia («tests pass», «see tests/», «tests/», «pytest», «tests/nope.py», un directorio tests/ sin archivo). También se rechaza todo .py dentro de un directorio que empieza con «.» (.venv, .git, .sldb) o que se llama site-packages o node_modules, aunque tenga un tests/ en la ruta: el código de terceros no es evidencia.
p3 (sin recorrer el disco): la comprobación es por referencia (resolve + is_file). No hay rglob, os.walk ni lectura de pyproject; las testpaths de pytest quedan fuera (alternativa de la nota de Chatbot_Infra, no elegida).
p4 (archivo de test propio): los tests nuevos van en tests/test_closeout_test_paths.py. tests/test_closeout_gates.py no se toca porque CC35a lo modifica. El archivo nuevo cubre cada caso de p1 (a, b, root/tests, ::nodo, forma pytest) y cada rechazo de p2, construyendo CloseoutGatesService sobre un tmp_path con los archivos necesarios. No usa un desk real ni deskops init, salvo un test de extremo a extremo opcional sobre una copia en /dev/shm.
p5 (comportamiento existente): las referencias que hoy cuentan siguen contando. tests/test_closeout_gates.py y test_cli pasan sin cambiar expectativas; test_output_goldens y test_cli_help_examples, sin --update-golden.
p6 (cambio mínimo): no se toca otra función de closeout_gates.py. El docstring de reference_points_to_test se reescribe con la regla nueva. CHANGELOG: una entrada en ## [Unreleased] / ### Changed.
p7 (fuera): las notas de inbox no se tocan; el ack o la respuesta a Chatbot_Infra los hace el coordinador al integrar.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-09):
b1 (de qué TaskDoc salen los files): del TaskDoc que el closeout evalúa, el mismo payload de closeout_reference_evidence (:89), que ya lee payload["files"] para la evidencia de documentos. No es este TaskDoc.
b2 (sin test de extremo a extremo): no hay test de extremo a extremo. Todos los tests son unitarios sobre CloseoutGatesService en un tmp_path, y se borra la frase «salvo un test de extremo a extremo opcional» de p4.
b3 (qué corre desde /dev/shm): test_cli, test_output_goldens y test_cli_help_examples corren desde una copia de solo lectura del worktree en /dev/shm: git -C <worktree> worktree add --detach /dev/shm/deskops-ctp HEAD, pytest ahí con PYTHONPATH=/dev/shm/deskops-ctp y, al terminar, git -C <worktree> worktree remove --force /dev/shm/deskops-ctp. tests/test_closeout_test_paths.py y tests/test_closeout_gates.py pueden correr en el worktree.
b4 (sufijo): se compara exacto con «.py», como hoy (resolved.suffix != ".py"). «.PY» y «.Py» no cuentan, y un test lo fija.
b5 (cadenas que solo parecen evidencia): la regla es la de p1. Todo lo que no nombre un .py existente que cumpla p1 tras quitar ::nodo y la forma pytest no es evidencia. Los ejemplos de p2 son los casos que el test fija; no hace falta un listado exhaustivo.

## Validation

_List the checks required before this task can close._

- tests/test_closeout_test_paths.py nuevo: aceptación (root/tests, */tests/**, files, ::nodo, forma pytest) y rechazo (absoluta, .., inexistente, no .py, .venv/site-packages/node_modules, cadenas que solo parecen evidencia)
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests/test_closeout_test_paths.py, tests/test_closeout_gates.py, tests/test_cli.py, tests/test_output_goldens.py y tests/test_cli_help_examples.py (sin --update-golden); los que leen mucho el desk, desde una copia en /dev/shm
- grep: sin rglob ni os.walk nuevos en closeout_gates.py
- wc -l antes y después
- CHANGELOG
- Resultado (coordinador de proyecto, squash 1a7107dc): test_closeout_test_paths 31 y test_closeout_gates 7 verdes de a uno; test_cli 101, output_goldens 7 y help_examples 11 verdes en la rama (worker, desde /dev/shm), sin --update-golden.

## Done When

_Name the observable condition that makes the task complete._

Una tarea cuyas references citan runtime/foo/tests/test_x.py (existente) tiene evidencia de tests; también la tiene una que cita un .py declarado en files. Siguen rechazados: rutas absolutas, rutas con .. que salen del root, archivos inexistentes, .py dentro de .venv, site-packages o node_modules y cadenas que solo parecen evidencia, cada caso con un test en tests/test_closeout_test_paths.py. tests/test_closeout_gates.py, test_cli, test_output_goldens y test_cli_help_examples quedan verdes sin cambiar expectativas. Hay una entrada en CHANGELOG.
