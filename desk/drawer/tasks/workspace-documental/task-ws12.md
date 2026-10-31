---
id: WS12
status: candidate
owner_repo: deskops
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

Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI.

## Aceptación

G_WRITE_POLICY verificado; registrar capability exacta para cada acción. No asumir lock UI protege escritores CLI. Toda operación sin contrato queda no disponible. WS07 ya aprobó principios, WS12 produce whitelist final. Contrato para campos/knowledge/intake puede cerrar sin esperar closeout: operaciones de autoría/cierre quedan bloqueadas por G_CLOSEOUT hasta evidencia; no se las etiqueta disponibles. Aceptar deltas de escritura por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable. Con read_only, G_SLDB_WRITE no es prerrequisito ni se anuncia como aprobado. La verificación del contrato clasifica APIs como existentes/comprobadas o faltantes, no exige implementar WS20 para cerrar WS12: la capacidad raw-source faltante se diseña y queda gated por G_SOURCE.

## Dependencias

Tareas: WS11, WS08. Gates: G_WRITE_POLICY. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
