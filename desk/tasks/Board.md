---
sldb:
  by: agent
  at: '2026-11-11T23:36:05Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo.md
- desk/tasks/task-closeout-resolved-by-cierra-una-tarea-que-el-modelo-rechaza-leyendo-su-frontmatter-como-retire-y-sup.md
- desk/tasks/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com.md
- desk/tasks/task-closeout-resolved-by-acepta-referencias-calificadas-por-repo-repo-sha-repo-ruta-de-test-verificadas.md
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
- closeout resolved-by cierra una tarea que el modelo rechaza leyendo su frontmatter, como retire y supersede (huecos de legacy, parte 1) [draft] - deskops closeout resolved-by de una tarea que el modelo rechaza la cierra por CLI, con el mismo commit, los mismos trailers (Closeout-Mode: resolved-by) y las mismas compuertas de ref y test que una tarea válida, leyéndola por frontmatter como supersede; con store y otra tarea inválida en el mismo modelo, rechaza antes de escribir y nombra sldb H2 y la vía manual.
- deskops edit task (y edit de cualquier artefacto) no guarda el párrafo placeholder de la plantilla como contenido: una edición con el texto de la sección no lo duplica [draft] - Una edición por CLI de un campo de sección deja exactamente un placeholder de plantilla (el ancla) en el archivo, venga o no el placeholder dentro del valor. La edición es idempotente: el mismo valor dos veces deja el mismo archivo.
- closeout resolved-by acepta referencias calificadas por repo (<repo>:<sha>, <repo>:<ruta de test>) verificadas contra un repo registrado, para cerrar una task.code cuyo código vive en otro repo [draft] - deskops closeout resolved-by cierra una tarea con --ref <repo>:<sha> y --test <repo>:<ruta>, donde <repo> es un repo del registro del ecosistema (deskops repo register), verificando en ese repo que el commit es ancestro de su HEAD y que el test existe y es un archivo de tests; con el mismo commit de cierre y los mismos trailers, que guardan la referencia calificada tal cual.
