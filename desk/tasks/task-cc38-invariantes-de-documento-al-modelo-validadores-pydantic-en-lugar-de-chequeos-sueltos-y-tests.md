---
id: task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_model_validators.py
- tests/test_model_validators.py
- pytest tests/test_domain_tree.py
- tests/test_domain_tree.py
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
- 4a1aae81d47bcee934224c2ce0504a1a3a15d1df
- desk/atoms/atom-una-invariante-de-un-solo-documento-vive-como-validador-de-su-modelo.md
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
pills: []
files:
- deskops/models/
- deskops/domain_tree.py
- deskops/atom_tags.py
- deskops/services/atoms.py
- deskops/services/
- deskops/doc_access.py
- deskops/specs/compiler.py
- deskops/cli/commands/doctor.py
- tests/test_atom_tags.py
- tests/test_desk_paths.py
- tests/test_cli.py
- tests/test_output_goldens.py
- tests/
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC38: Invariantes de documento al modelo - validadores pydantic en lugar de chequeos sueltos y tests

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC38 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 2 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PF2. Depende de: CC30 (entregado en wt/cc30, pendiente de integración). Gates requeridos: ninguno. Aplica DK6: una invariante de UN documento es un validador pydantic del modelo, que sldb aplica en toda vía de escritura; una invariante entre documentos es una RuleDoc.

## Goal

_Describe the concrete result this task must produce._

Cada chequeo de UN documento que hoy vive fuera del modelo (domain_tree, atom_tags, atoms validate, doctor y el inventario que dejó CC30) pasa a un validador pydantic de su modelo en deskops/models/ y el chequeo viejo se borra en el mismo paso; los chequeos entre documentos quedan inventariados y asignados a CC32 o CC33; los tests prueban que el modelo, sldb fields update y sldb docs update rechazan el payload malo. Sin cambio de gramática ni de texto de error: goldens idénticos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/models/ (validadores), deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/ (atoms y los que llamaban los chequeos), deskops/doc_access.py (solo para quitar chequeos movidos), deskops/cli/commands/doctor.py, los tests que los cubren y CHANGELOG.md. Fuera: reglas entre documentos (solo se inventarían para CC32/CC33); consistencia del ciclo de vida de TaskDoc (CC37); escrituras en sldb; formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 2, CC38). SCOPE: Principio del dueño (DK6): una invariante de UN documento es un validador pydantic del modelo (field_validator / model_validator), que sldb aplica en toda vía de escritura (deskops, sldb fields update, sldb docs update, /save, transacción; roundtrip en sldb api/documents/payload_save_steps.py:62); una invariante ENTRE documentos es una RuleDoc de sldb; el test solo prueba que el modelo o la regla rechaza el caso malo. (1) Inventario, en el TaskDoc, de los chequeos de un documento que hoy viven fuera del modelo o solo en tests. Puntos de partida: domain_tree.py (_check_crossroad, _check_protoatom, _check_atom), atom_tags.validate_atom_tag_namespaces, doctor._check_documents, validate_atoms, y los tests que arman un payload inválido y esperan un error del servicio (grep fijado en el TaskDoc). (2) Clasificación de cada uno: un documento → validador del modelo dueño en deskops/models/; entre documentos → RuleDoc, asignada a CC32 (activación) o CC33 (cierre y campos) en el inventario, que la implementan; lo que lea un archivo fuera del documento (p. ej. tag-namespaces.yaml) se clasifica como entre documentos. (3) Cada chequeo de un documento pasa al modelo y el chequeo viejo se borra en el mismo paso (DK3); los servicios y doctor que lo llamaban dejan de hacerlo y reportan el error de validación del modelo con el mismo texto de error que antes (goldens). (4) Tests: los que armaban un payload inválido contra el servicio pasan a probar que el modelo rechaza ese payload, y para un caso por modelo, que sldb fields update y sldb docs update lo rechazan también. No toca la consistencia del ciclo de vida de TaskDoc (status ↔ current_node ↔ history): la hace CC37 con el mismo mecanismo.

ACCEPTANCE: Inventario en el TaskDoc con cada chequeo, su clasificación (modelo | RuleDoc en CC32 | RuleDoc en CC33) y su destino; cada chequeo clasificado como de un documento existe como validador en deskops/models/ y su función vieja ya no existe (grep de los nombres del inventario en deskops/ vacío salvo los asignados a CC32/CC33); por cada validador nuevo, un test que construye el modelo con el payload malo y espera ValidationError; para un modelo de atom y uno de crossroad, sldb fields update con un valor que viola el validador es rechazado en una copia del desk; deskops doctor sin hallazgos nuevos en los 6 desks y los desks existentes cargan sin errores de validación nuevos (o el TaskDoc lista los documentos inválidos encontrados y los corrige vía deskops); goldens de ayuda y salida idénticos; los tests de los archivos tocados verdes; CHANGELOG.

OUTPUT_SCOPE: deskops/models/, deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/, deskops/cli/commands/doctor.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-06, coordinador del plan):
p1 (base): CC38 depende de CC30, entregado en wt/cc30 (5f8dff78) y pendiente de integración. El worktree de CC38 sale de origin/main cuando CC30 esté integrado; si el coordinador de proyecto autoriza antes, sale de wt/cc30. Las rutas y líneas de este TaskDoc son de wt/cc30 5f8dff78: los helpers de documentos viven en deskops/doc_access.py y la verificación de cierre en services/closure.py.
p2 (puntos de partida fijados): deskops/domain_tree.py (_check_crossroad :280, _check_protoatom :296, _check_atom :317, _domain_errors); deskops/atom_tags.py (validate_atom_tag_namespaces :131); deskops/services/atoms.py (validate_atoms :201 y _validate_atom_path); deskops/cli/commands/doctor.py (_check_documents :71, _unreadable); y la sección «Inventario para CC38» de runs/subagents/cc30-worker-report.md (rama wt/cc30): doc_access.write_doc y doc_access.edit_artifact_field, el parseo de frontmatter a mano (doc_access.frontmatter_id, _task_route_summary, workspace._frontmatter_task_type), ClosureService._declares_materialization_sources y _generated_artifact_source_finding, reference_points_to_atom y _reference_points_to_existing_route, tasks.registered_task_types y doc_access._tracked_task_paths.
p3 (grep de tests fijado): grep -rnE "pytest\.raises\((ValueError|ValidationError)" tests/ (20 aciertos en 6 archivos en wt/cc30: test_cli, test_scion_runtime, test_review_doc, test_desk_paths, test_atom_tags, test_specs). Cada acierto que arma un payload inválido de UN documento contra un servicio entra al inventario. Los demás se listan como descartados, con su razón en una línea.
p4 (criterio de clasificación): (a) es de un documento si se decide solo con los campos del payload de ese documento; (b) es entre documentos (RuleDoc: CC32 si gobierna la activación o el avance, CC33 si gobierna el cierre o campos referenciados) si necesita otro documento, otro archivo (tag-namespaces.yaml, crossroads, el árbol de desk/), la ruta o el nombre del archivo, o el store; (c) no es invariante de dominio y no se mueve si es mecánica de escritura o lectura del store (ruido estructural, campos ilegibles por el modelo, parseo de frontmatter): se registra como «fuera de DK6» con su razón. Un chequeo mixto se parte: lo de un documento va al modelo y el resto al inventario de CC32/CC33.
p5 (mismo texto de error): el validador produce el mismo texto que el chequeo viejo. Donde el texto sale por la CLI (atoms validate, domain check, doctor), los goldens deben quedar idénticos. Si un texto cambia por el envoltorio de ValidationError, el servicio extrae el mensaje del validador, no reescribe el chequeo.
p6 (prueba de sldb): «sldb fields update» y «sldb docs update» se prueban en una copia del desk bajo /dev/shm (fixture de test o desk temporal), nunca sobre un desk real: un caso para un AtomDoc y uno para un CrossroadDoc, con el comando que rechaza y su salida en la Validation. Si sldb no aplica el validador del modelo en alguna de esas vías, se registra como hipótesis en el TaskDoc, se manda nota a sldb (deskops message send --to sldb; si el registro con /home/jp lo impide, se deja anotado para el coordinador) y no se suple con Python.
p7 (desks existentes): antes y después se corre «deskops doctor --root <desk>» y una carga por modelo (sldb stores check) en los 6 desks. Un documento existente que el validador nuevo rechace se lista en el TaskDoc y se corrige con deskops (edit/retire), nunca a mano. Si la corrección exige una decisión del dueño, el nodo se bloquea y se avisa.
p8 (fuera): la consistencia status ↔ current_node ↔ history de TaskDoc es de CC37; las reglas entre documentos solo se inventarían y asignan, no se implementan (CC32/CC33).

PRECISIONES DEL PREFLIGHT (review-task-cc38-...-preflight-1, 2026-11-06):
p9 (texto de error sin chequeo previo): un chequeo que solo vivía en un test no tiene texto viejo; su validador da un mensaje de una línea, en inglés como los demás errores de deskops, que nombra el campo, el valor y la regla. Ningún golden lo fija. p5 se aplica solo a los chequeos que tenían texto.
p10 (grep de aceptación): el grep de los nombres del inventario en deskops/ debe quedar vacío salvo los asignados a CC32/CC33 y los clasificados «fuera de DK6» (p4c). Esos siguen en el código y el inventario los lista con su razón en una línea.
p11 («el store» en p4b): un chequeo depende del store si consulta otro documento trackeado, el índice del store o el estado de tracking (si un documento está trackeado, si su hash cambió, si está movido). Leer el propio payload del documento a través del store no cuenta: eso sigue siendo de un documento.
p12 (fuente del inventario de CC30): runs/subagents/cc30-worker-report.md está en la rama wt/cc30 y llega a main con la integración de CC30. Si el worktree de CC38 no lo tiene, se lee con git show origin/wt/cc30:runs/subagents/cc30-worker-report.md. No se copia al desk.
p13 (matriz de p6): cuatro casos, AtomDoc y CrossroadDoc × «sldb fields update» y «sldb docs update». Cada uno, con el comando, el payload inválido y la salida de rechazo, en la Validation o en el informe del worker.

PRECISIONES DEL COLD-BUNDLE (review-task-cc38-...-bundle-1, 2026-11-06):
p14 (chequeo mixto): la parte de un documento pasa al validador y se borra de la función vieja en el mismo paso. La parte entre documentos queda en el código, en la misma función reducida a esa parte (sin renombrar), hasta que CC32/CC33 la reemplace. El inventario la lista con el nodo asignado y el grep de p10 la exime.
p15 (texto ya fijado por un test): si un test existente fija el texto de un chequeo (p. ej. match="Unknown atom tag namespace"), ese chequeo tiene texto viejo y p5 lo obliga a conservarlo. p9 vale solo para chequeos sin texto en ningún test ni golden.
p16 (ValueError frente a ValidationError): cada chequeo movido tiene al menos un test nuevo que construye el modelo con el payload malo y espera pydantic.ValidationError. Los tests existentes que prueban la vía del servicio con pytest.raises(ValueError) se conservan si siguen verdes (ValidationError es subclase de ValueError) y no se migran. Se migran solo los que arman el payload para probar la invariante y no el servicio.
p17 (sldb docs update): los cuatro casos de p13 bloquean, también «sldb docs update». Si una vía de sldb no aplica el validador, rige p6 (hipótesis y nota a sldb, sin suplir con Python) y el nodo se entrega con esa vía marcada como hipótesis abierta, no como verde.

DESVÍOS AUTORIZADOS DURANTE LA EJECUCIÓN (coordinador del plan, 2026-11-06; aprobados por el coordinador de proyecto):
d1 (regresión de CC30): tests/test_domain_tree.py fallaba en main 93cc1943 (4 tests), porque domain_tree.py llamaba ops._write_new_doc, _track_created_document y _remove_created_file, que la fachada de CC30 ya no expone. CC38 lo corrige dentro de deskops/domain_tree.py llamando a doc_access directamente.
d2 (files ampliado): deskops/specs/compiler.py entra en files. El chequeo de un documento 'Task title cannot be empty' (compiler.py:44; lo fija tests/test_specs.py:73) pasa al validador de TaskDoc.title con el mismo texto (p5) y se quita de compiler.py. El KeyError por title ausente en el payload crudo es forma de la entrada, no del modelo: se queda y se inventaría como fuera de DK6.

## Validation

_List the checks required before this task can close._

- Inventario en el TaskDoc (implementation_path, sección INVENTARIO) con cada chequeo, su clasificación según p4 y su destino
- grep de los nombres de función del inventario clasificados como de un documento en deskops/ vacío
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests nuevos de validadores (un ValidationError por validador), tests/test_atom_tags.py, los tests de domain tree y atoms validate, tests/test_cli.py, tests/test_output_goldens.py y tests/test_cli_help_examples.py (sin --update-golden)
- sldb fields update y sldb docs update rechazan un AtomDoc y un CrossroadDoc inválidos en una copia del desk bajo /dev/shm (p6), con comando y salida
- deskops doctor y sldb stores check en los 6 desks antes y después sin hallazgos nuevos, o documentos inválidos listados y corregidos vía deskops (p7)
- CHANGELOG
- RESULTADO (coordinador de proyecto, 2026-11-06, squash 4a1aae81 sobre origin/main, después de renombrar por CLI los 82 átomos con '_' de spec2viz b16c021 y graph_ui 62bc9f8, autorizado por el overlord): model_validators 14, specs 5, model_contract_snapshot 2 (contratos sin cambio, sin migración), domain_tree 5, atom_folder_axis 13, atoms_cli 4, atom_tags 5, desk_view 9+1 skipped, scaffold_golden 3, cli_help_examples 11, operator_manual 1, output_goldens 7: todos verdes, de a uno. Corrige las regresiones de CC30 en domain_tree, atom_folder_axis y operator_manual. Inventario: 9 chequeos entre documentos para CC33 y 0 para CC32. task.refactor: queda abierta por goldens no verificable (opción a del overlord).

## Done When

_Name the observable condition that makes the task complete._

Inventario en el TaskDoc con cada chequeo, su clasificación (modelo | RuleDoc en CC32 | RuleDoc en CC33) y su destino; cada chequeo clasificado como de un documento existe como validador en deskops/models/ y su función vieja ya no existe (grep de los nombres del inventario en deskops/ vacío salvo los asignados a CC32/CC33); por cada validador nuevo, un test que construye el modelo con el payload malo y espera ValidationError; para un modelo de atom y uno de crossroad, sldb fields update con un valor que viola el validador es rechazado en una copia del desk; deskops doctor sin hallazgos nuevos en los 6 desks y los desks existentes cargan sin errores de validación nuevos (o el TaskDoc lista los documentos inválidos encontrados y los corrige vía deskops); goldens de ayuda y salida idénticos; los tests de los archivos tocados verdes; CHANGELOG.
