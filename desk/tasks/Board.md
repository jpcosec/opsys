---
sldb:
  by: agent
  at: '2026-11-12T03:38:00Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo.md
- desk/tasks/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com.md
- desk/tasks/task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas.md
- desk/tasks/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper.md
- desk/tasks/task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo.md
- desk/tasks/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de.md
- desk/tasks/task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- context-review
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- CC35d resto: dominios, namespaces y tag_folder por la API de tags de sldb (GD27 con value bare y tag_models) [draft] - domain_tree, atom_tags y los chequeos de namespaces y padres de dominio pasan a la API de tags de sldb (declaración, reglas, tag_tree, tag_folder); se borran require_domain_parents, _domain_errors y validate_atom_tag_namespaces; goldens idénticos.
- deskops edit task (y edit de cualquier artefacto) no guarda el párrafo placeholder de la plantilla como contenido: una edición con el texto de la sección no lo duplica [draft] - Una edición por CLI de un campo de sección deja exactamente un placeholder de plantilla (el ancla) en el archivo, venga o no el placeholder dentro del valor. La edición es idempotente: el mismo valor dos veces deja el mismo archivo.
- closeout resolved-by acepta referencias calificadas por repo (<repo>:<sha>, <repo>:<ruta de test>) verificadas contra un repo registrado, para cerrar una task.code cuyo código vive en otro repo [draft] - deskops closeout resolved-by cierra una tarea con --ref <repo>:<sha> y --test <repo>:<ruta>, donde <repo> es un repo del registro del ecosistema (deskops repo register), verificando en ese repo que el commit es ancestro de su HEAD y que el test existe y es un archivo de tests; con el mismo commit de cierre y los mismos trailers, que guardan la referencia calificada tal cual.
- Los tests de deskops leen la ruta del sldb hermano de la variable de entorno SLDB_SRC, con un helper común [draft] - Un solo helper común resuelve la ruta de sldb para los tests: lee la variable de entorno SLDB_SRC y, si no está definida, usa la ruta hermana de hoy; los 18 archivos lo usan y ninguno repite la línea fija.
- deskops quita las guardas que esquivaban H1-H3 de sldb: cerrar por CLI dos tareas inválidas del mismo modelo y reparar un desk que tiene un documento inválido [draft] - Con sldb corregido, deskops cierra por CLI dos o más tareas inválidas del mismo modelo (retire, supersede, resolved-by), y desk update --apply sobre un desk con documentos inválidos hace todas las reparaciones sin saltarse ninguna, mientras la migración de estados heredados y el listado de las tareas inválidas se quedan.
- add task y el doctor sugieren task.external (o una tarea espejo) cuando los files o las referencias de una tarea apuntan a otro repo [draft] - Al crear una tarea cuyos files apuntan a otro repo, add task lo avisa con una línea (no bloquea) que nombra el repo y sugiere task.external o una tarea espejo en el desk de ese repo; y el doctor lista como alerta, sin cambiar su código de salida, las tareas existentes con esa forma que no son task.external.
- deskops view board en menos de 2,5 s: construir una vez por corrida lo que hoy se rehace por tarjeta (transiciones, closeout, grafo del desk) y abrir el store menos veces [draft] - deskops view board, con el store construido y en un proceso nuevo, tarda 2,5 s o menos (mediana de 3, layout del benchmark de H11) y su salida es idéntica a la de hoy; lo que se construye una vez por corrida se comparte entre las tarjetas.
