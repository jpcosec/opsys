---
id: WS43
status: candidate
owner_repo: deskops
depends_on:
- WS17
- WS30
requires:
- G_HUMAN_MANUAL
- G_PRODUCT
- G_WRITE_CONTRACT
---

# Publicar navegación documental del desk real

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

desk/README.md; mapa de ecosistema/índices según P09 y WS11; átomos de acuerdos durables

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Aplicar entradas/índices authored validados en Taller al deskops real, por operaciones autorizadas y preservando registry como inventario derivable. Enlazar repos conocidos por identidad/origen y su entrada existente; no modificar repos hermanos ni imponer nuevos modelos. Registrar conocimiento durable en átomos antes de docs.

## Aceptación

P09 y contrato fijan ubicación/modelo opcional. Persona designada recorre Markdown y UI real, links/roots verificables, acta deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md y commit; no publicar solo ejemplo como si fuera ecosistema real. Cada proyecto adicional requiere su tarea de repo y acuerdo de alcance.

## Dependencias

Tareas: WS17, WS30. Gates: G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
