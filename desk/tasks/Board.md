---
sldb:
  by: agent
  at: '2026-11-10T21:32:07Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc33c-grafo-graph-y-drift-leen-sldb-graph-project-gd21-se-borran-la-construcción-propia-y-sus-rglob.md
- desk/tasks/task-cc35d-tags-y-reemplazo-namespaces-domain-tree-y-desk-replace-por-la-api-de-sldb-gd27-gd22.md
- desk/tasks/task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos.md
- desk/tasks/task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall.md
- desk/tasks/task-tareas-con-status-terminal-heredado-y-history-vacía-desks-pre-cc31-desk-update-las-migra-y-doctor-de.md
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

- CC33c: Grafo - graph y drift leen sldb graph project (GD21); se borran la construcción propia y sus rglob [draft] - deskops graph build|neighbors|missing|reflect y drift leen el grafo de proyecto de sldb (GD21) con la configuración de desk_graph.py; se borran snapshot.py como construcción propia, el rglob de checks.py y los de self_reflection.py; neighbors y missing dan lo mismo que el oráculo v1 y después tests/graph_oracle_v1/ se borra.
- CC35d: Tags y reemplazo - namespaces, domain tree y desk replace por la API de sldb (GD27, GD22) [draft] - tag-namespaces.yaml se sincroniza al store por la API de sldb; require_domain_parents y DomainTree.check/tree pasan a la validación y tag_tree de GD27; axis_folder_relpath pasa a tag_folder; services/replace.py pasa a sldb replace_text con la misma guarda de conteo.
- CC33b: Reglas de cierre - RuleDocs por tipo sobre task_completes y reglas de campo; se borran los hechos y gates viejos [draft] - El cierre de cada tipo de tarea lo decide una RuleDoc semilla on_transition sobre task_completes que exige los recibos evidence de CC33a; las reglas de campo son RuleDocs alert; se borran __closeout_evidence__, closeout_evidence_verified, pill_graduation_verified y _add_closeout_facts; los chequeos de CC38 asignados a CC33 pasan a RuleDoc o quedan con razón.
- advance y doctor ante semillas del ciclo de vida anteriores a CC31: doctor las reporta y advance falla nombrando la arista sin efecto sets [draft] - deskops doctor reporta las semillas managed del ciclo de vida desactualizadas y sugiere desk update --apply; deskops advance falla antes de escribir, con un mensaje que nombra la arista sin efecto sets.
- Tareas con status terminal heredado y history vacía (desks pre-CC31): desk update las migra y doctor/desk update no caen por un documento inválido [draft] - deskops desk update --apply migra las tareas heredadas según la tabla de d1 y reporta las que no puede decidir; doctor y desk update reportan los documentos inválidos uno por uno sin caer.
