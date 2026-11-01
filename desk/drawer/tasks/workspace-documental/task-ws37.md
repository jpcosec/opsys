---
id: WS37
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS36
- WS30
requires:
- G_EXEC
- G_SCION
---

# Validar delegación con agente real

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

runs/subagents/workspace-documental-acceptance/delegacion/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

UF06 real: pregunta/intervención/corrección/evidencia/decisión y cierre por el handoff de WS28, con actor humano.

## Aceptación

G_SCION/G_EXEC y protocolo de validacion-humana.md (guion, acta en runs/subagents/workspace-documental-acceptance/delegacion/); no sustituir integración por mocks ni completed por aprobación. No bloquea WS31.

## Dependencias

Tareas: WS36, WS30. Gates: G_EXEC, G_SCION. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS37/29fa5c3ef663b690138fff4ed26a98027ccbe3098d2d51c7740d69e731ccbbba/attempt-2']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
