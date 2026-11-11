---
sldb:
  by: agent
  at: '2026-11-11T14:47:02Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc35c-referencias-entrantes-referrers-y-rewrite-references-dentro-de-la-transacción-menciones-en-pro.md
- desk/tasks/task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece.md
- desk/tasks/task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo.md
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

- CC35c: Referencias entrantes - referrers y rewrite_references dentro de la transacción; menciones en prosa como MentionPattern [draft] - atoms delete/split/merge, retire, drawer remove y closeout buscan y reescriben las referencias entrantes con referrers y rewrite_references de sldb dentro de la misma transacción; las menciones en prosa se ven por los MentionPattern de la configuración de grafo; se borran las búsquedas propias.
- CC34: Vistas de la UI como ViewDoc servidas por sldb; desk_view.py desaparece [draft] - deskops view board|task|drawer|inbox sale de sldb.api.run_view sobre ViewDocs semilla del paquete, con el mismo JSON que hoy salvo revision; graph_ui lee esas vistas sin importar DeskView; desk_view.py y sus helpers se borran.
- CC35d resto: dominios, namespaces y tag_folder por la API de tags de sldb (GD27 con value bare y tag_models) [draft] - domain_tree, atom_tags y los chequeos de namespaces y padres de dominio pasan a la API de tags de sldb (declaración, reglas, tag_tree, tag_folder); se borran require_domain_parents, _domain_errors y validate_atom_tag_namespaces; goldens idénticos.
