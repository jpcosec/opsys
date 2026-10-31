---
id: WS26
status: candidate
owner_repo: graph_ui
depends_on:
- WS12
- WS22
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar autoría y contexto de tareas

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/task/; endpoints; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Autoría explícita desde candidato, evidencia declarada, dependencias y contexto/pill binding; promoción solo cuando el contrato resuelve commits previos por canal autorizado. Incluir enrutamiento explícito en Board y representación de capa lista por dependencias/no solapamiento; sin confundir Board route con ejecución. El canal de promoción debe respetar commits previos y estado real.

## Aceptación

UF04 con TaskDoc/Board reales; nunca editar status para avanzar. Si operación Git no tiene contrato/manual owner, mantener acción read-only/handoff explícito y gate humano no pasa hasta resolver.

## Dependencias

Tareas: WS12, WS22. Gates: G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
