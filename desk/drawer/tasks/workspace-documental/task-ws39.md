---
id: WS39
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS12
- WS16
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar inspección y edición de modelos existente

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

shell/dialogs.js; views/models/; tests/; runs/subagents/workspace-documental-acceptance/modelos/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Hacer navegables Schema/editar clases ya disponibles desde documento/contexto; usar draft/validate/promote de sldb. No reimplementar modelos.

## Aceptación

UF09 inspección y mutación en store temporal real de prueba; comprobar los efectos y errores que declara el contrato WS12; no habilitar promover si API/autoridad falta. Extensión posterior al lector básico. Guardar acta de prueba humana en graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md con el participante que fija P08 y resultado; G_HUMAN_MODEL debe pasar antes de marcar disponible en el manual que publica WS31 el capítulo 15 (Personalizar modelos) del índice de borradores/manual.md.

## Dependencias

Tareas: WS12, WS16. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS39/0ea47b78a26f267f4a3e63e7e18252bbfed6ec558417e20e02973e7f64cced82/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
