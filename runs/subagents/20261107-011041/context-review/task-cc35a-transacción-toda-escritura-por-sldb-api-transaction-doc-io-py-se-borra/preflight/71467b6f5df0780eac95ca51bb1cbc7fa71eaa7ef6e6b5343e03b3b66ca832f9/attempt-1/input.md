FILE:desk/tasks/task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra.md
---
id: task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
- task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb
- task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests
pills: []
files:
- deskops/doc_io.py
- deskops/doc_access.py
- deskops/services/
- deskops/cli/commands/message.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/repo.py
- deskops/runtime/scion.py
- deskops/lifecycle.py
- deskops/workspace.py
- deskops/bootstrap.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35a: Transacción - toda escritura por sldb.api.transaction; doc_io.py se borra

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35a del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3: parte (1), transacción, del agregado CC35 (L, partido en la rev 3), en PF3, árbol T3.5. Depende de CC30, CC36 y CC38, los tres en main. Gate: G_GD24 (sldb.api.transaction y apply_batch), satisfied.

## Goal

_Describe the concrete result this task must produce._

Toda escritura de deskops pasa por sldb.api.transaction (GD24), con expected_source_hash en los updates, y deskops/doc_io.py desaparece: su transacción propia y sus envoltorios de llamadas a sldb se reemplazan por sldb.api. message send/ack escriben dentro de la transacción, sin rollback manual. Un fallo a mitad de una operación compuesta revierte todo.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/doc_io.py (borrado), deskops/doc_access.py, deskops/services/, deskops/cli/commands/message.py, desk.py y repo.py, deskops/runtime/scion.py, deskops/lifecycle.py, deskops/workspace.py, deskops/bootstrap.py (P4: solo el import y la llamada, a3), tests y CHANGELOG.md. Fuera: selectores (CC35b), referencias entrantes (CC35c), tags/reemplazo (CC35d), escrituras en sldb, formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 3, CC35a, hijo del agregado CC35). SCOPE: Parte (1) del scope de CC35. Todo caller de doc_io.DocTransaction usa sldb.api.transaction (GD24) con expected_source_hash en los updates; message send/ack escribe por la transacción, sin rollback manual; doc_io.py se borra. Las líneas se fijan al promover, sobre main con CC30, CC36 y CC38 integrados.

ACCEPTANCE: grep -rn "doc_io\|DocTransaction" deskops/ vacío; un fallo inyectado a mitad de atoms merge revierte el atom, los referrers y el índice (hash de archivos y sldb stores check iguales antes y después); una escritura con expected_source_hash viejo falla con el mensaje de conflicto de deskops; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/doc_io.py (borrado), deskops/doc_access.py, deskops/services/, deskops/cli/commands/message.py, deskops/runtime/scion.py, tests/, CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-07, coordinador del plan):
a1 (inventario en main 4e79fbac): deskops/doc_io.py tiene 319 líneas. Lo usan, con número de líneas: deskops/bootstrap.py (8), deskops/cli/commands/desk.py (6), deskops/cli/commands/message.py (4), deskops/cli/commands/repo.py (4), deskops/doc_access.py (4), deskops/lifecycle.py (2), deskops/runtime/scion.py (2), deskops/services/atoms.py (10), deskops/services/closure.py (2), deskops/services/drawer.py (4), deskops/services/issues.py (4), deskops/services/replace.py (2), deskops/services/retire.py (2), deskops/services/review.py (3), deskops/services/tasks.py (2), deskops/workspace.py (7). Además de DocTransaction (:250) y _RootTransaction (:174), doc_io envuelve llamadas a sldb: track/untrack (:121-130), is_tracked (:86), register_model (:131), link_store_alias (:136), inherit_model_from (:140), init_store_at (:144), init_relations_in (:148), update_store_indexes_in (:152) y remove_model_from (:156).
a2 (alcance del grep de aceptación): «grep -rn "doc_io\|DocTransaction" deskops/ vacío» cubre todo doc_io, no solo la transacción. Cada envoltorio pasa a una llamada directa a sldb.api: transaction para escribir y create/update/delete/track/untrack/register_model/etc. con su nombre en sldb. No se crea un módulo nuevo que repita doc_io con otro nombre. Si una llamada necesita lógica propia de deskops (por ejemplo, el pythonpath por defecto del desk), puede vivir en deskops/doc_access.py como función con esa lógica y el informe la lista.
a3 (files fuera del output_scope del dag): para vaciar el grep entran también deskops/lifecycle.py, deskops/workspace.py, deskops/bootstrap.py, deskops/cli/commands/desk.py, deskops/cli/commands/repo.py, deskops/services/review.py, deskops/services/__init__.py y deskops/services/replace.py. bootstrap.py es P4 (brief, «No toca P4»): en P4 solo se cambia el import y la llamada de doc_io por su equivalente de sldb.api, sin cambiar la lógica.
a4 (expected_source_hash): cada lectura-modificación-escritura de un documento trackeado en los servicios lee el source hash al leer el documento (sldb lo da en el estado o la referencia del documento) y lo pasa como expected_source_hash al update dentro de la transacción. Las creaciones no llevan guarda. Si sldb lanza ConflictError, deskops lo traduce al mensaje de a5.
a5 (mensaje de conflicto de deskops; hoy no existe): «Error: <ruta relativa> changed since deskops read it; nothing was written. Re-run the command.» en stderr, exit 1, sin traza. Ningún golden lo fija; un test lo fija.
a6 (fallo inyectado en atoms merge): el test hace monkeypatch de una llamada que ocurre a mitad del merge, después de escribir el átomo destino y antes de reescribir los referrers, y la hace lanzar. Antes y después compara el sha256 de todos los archivos de desk/ y .sldb/core/ del desk temporal y la salida de sldb stores check, que deben ser iguales.
a7 (message send/ack): cli/commands/message.py escribe la nota (create) y el ack (update con guarda) dentro de sldb.api.transaction. Se borra el rollback manual que hoy hace a mano.
a8 (verificación en 6 desks; lección de CC31): deskops doctor sobre copias de los 6 desks con main y con la rama, comparando hallazgos. deskops se ejecuta con un cwd neutro (fuera de las copias), para que PYTHONPATH decida qué código se importa: python -m deskops con el cwd dentro de una copia del repo de deskops importa el paquete copiado. Hay plantilla del coordinador en ~/proyectos/SLDB_1/coord2-ccconfig/cc31/coord/n7c.sh.
a9 (fuera): selectores (CC35b), referencias entrantes (CC35c) y tags/reemplazo (CC35d). Este nodo no cambia la forma de resolver documentos ni de reescribir referencias: solo con qué se escribe.

## Validation

_List the checks required before this task can close._

- grep -rn 'doc_io\|DocTransaction' deskops/ vacío (a2)
- Fallo inyectado a mitad de atoms merge: sha256 de desk/ y .sldb/core/ y sldb stores check iguales antes y después (test, a6)
- Update con expected_source_hash viejo falla con el mensaje de conflicto de a5 (test)
- message send/ack dentro de la transacción, sin rollback manual (test)
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests de los archivos tocados (test_doc_io se reescribe o se borra con su módulo), test_atoms_*, test_message_cli, test_retire_cli, test_issue_cli, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- deskops doctor sin hallazgos nuevos en los 6 desks, con cwd neutro (a8)
- wc -l antes y después por archivo tocado
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

grep -rn "doc_io\|DocTransaction" deskops/ vacío; un fallo inyectado a mitad de atoms merge revierte el atom, los referrers y el índice (hash de archivos y sldb stores check iguales antes y después); una escritura con expected_source_hash viejo falla con el mensaje de conflicto de deskops; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

