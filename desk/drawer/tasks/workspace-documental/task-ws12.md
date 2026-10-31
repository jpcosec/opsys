---
id: WS12
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY
---

# Cerrar contrato de operaciones y escritura

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

contratos/operaciones.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y dueño, no se diseña uno aquí.

## Aceptación

G_WRITE_POLICY verificado; registrar capability exacta (operación, canal, efectos) para cada mutación o lectura Git que usen WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS32, WS34, WS36, WS39 y WS42. No asumir lock UI protege escritores CLI. Toda operación sin contrato queda no disponible. Requiere principios ya aprobados por humano en WS07 (G_WRITE_POLICY); WS12 produce la whitelist final. Contrato para campos/knowledge/intake puede cerrar sin esperar closeout: operaciones de autoría de tareas/cierre quedan bloqueadas por G_CLOSEOUT hasta evidencia; no se las etiqueta disponibles. Aceptar el delta de escritura (operaciones de la whitelist sobre los scope_nodes de G_UI_WRITE) por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable. Tras WS07 source_mode ya no vale pending, porque G_PRODUCT exige registrarlo. Con read_only, G_SLDB_WRITE no es prerrequisito ni se anuncia como aprobado. La verificación del contrato clasifica APIs como existentes/comprobadas o faltantes, no exige implementar WS20 para cerrar WS12: la capacidad raw-source faltante se especifica como requisito (operación y efectos) y queda gated por G_SOURCE; su diseño e implementación pertenecen a WS20.

## Dependencias

Tareas: WS11, WS08. Gates: G_WRITE_POLICY. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS12/722f2e73e7ea1d3fbeb6ad7d7a494a65946b7196e3180ab5a2e60936142b881b/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
