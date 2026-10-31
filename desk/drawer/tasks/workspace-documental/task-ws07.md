---
id: WS07
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS06
requires: []
---

# Resolver decisiones de producto y escritura

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

El humano dueño del producto confirma o corrige P01–P09 de decisiones.md, leyendo validacion-humana.md para P08, y `baseline_proposal` de dag.yaml (propuesta de línea base, no aprobación del plan completo); registrar alternativas, fecha y evidencia de cada decisión. Designar con identidad explícita a responsable de graph_ui, sldb y spec2viz para aceptar deltas; se puede designar al solicitante, no suponerlo. Registrar source_mode=editable o read_only en parámetros del DAG y reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí; un cambio de nodos sigue la regla de alcance.md. Designar explícitamente también al operador responsable del ramal Scion y registrar qué acceso read-only tiene, con identidad registrada por el solicitante en P01; no requiere configurar/ejecutar Scion ni concede permiso G_EXEC.

## Aceptación

No inventar aprobación. Gates G_PRODUCT y G_WRITE_POLICY solo pasan por registro explícito. Redacción de alternativas puede avanzar mientras esperan. No cerrar sin registro de designación de responsables graph_ui/sldb/spec2viz y operador Scion, con su acceso read-only, en P01 (puede ser el propio solicitante si lo confirma), con actor humano/fecha; P01 no equivale a autorización de ejecución.

## Dependencias

Tareas: WS06. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS07/1b2854385a147a5b7dec115acba52559eab4cfce22c68d25f59cdf6e12584efa/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
