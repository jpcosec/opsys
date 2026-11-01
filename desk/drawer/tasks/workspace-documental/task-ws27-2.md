---
id: WS27.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS27
depends_on:
- WS13
- WS12
requires:
- G_UI_READ
---

# Mostrar evidencia declarada, encontrada y verificada

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/evidence/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Evidencia junto a la TaskDoc. Sin modelo de comentarios nuevo. WS12 fija correspondencia por tipo de evidencia declarada TaskDoc (no inferencia por extensión en renderer), artefactos soporte y salida pública de closeout verify; declarada/encontrada/gates/summary se muestran según reporte real. Verificada refiere al resultado del gate de la TaskDoc/tipo, no prueba independiente del artefacto. Reporte ausente/fallo de comando es no verificable con error, nunca verificado.

## Aceptación

Mostrar declarada/encontrada/verificada y abrir su soporte; una evidencia ausente se ve como ausente; declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos, sin colapsarlos. Declarada = closeout_evidence de la TaskDoc; encontrada = artefactos resolubles en las references/files de la TaskDoc; verificada = resultado de `deskops closeout verify`. Abrir soporte = abrir el artefacto en el lector si es Markdown dentro del workspace; fuera de ese caso se muestra la ruta y se declara no soportado (alcance.md).

## Dependencias

Tareas: WS13, WS12. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS27.2/cbbdaf6677d7674159d199262d3ee409687ceab985dfddf98b64ec56750d2f71/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
