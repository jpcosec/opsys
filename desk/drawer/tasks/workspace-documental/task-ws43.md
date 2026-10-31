---
id: WS43
status: candidate
owner_repo: deskops
node_role: delivery
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

Aplicar entradas/índices authored validados en Taller al deskops real, por operaciones autorizadas y preservando registry como inventario derivable. Enlazar repos conocidos por identidad/origen y su entrada existente; no modificar repos hermanos ni imponer nuevos modelos. Registrar conocimiento durable en átomos antes de docs. Repos a enlazar = todos los de `deskops list repositories`: enlazar no escribe en ellos. Escribir una entrada dentro de otro repo requiere su tarea y acuerdo de alcance. Contrato = contratos/navegacion.md (WS11, transitivo).

## Aceptación

P09 y contrato fijan ubicación/modelo opcional; los acuerdos durables aplicados al mapa (Pxx aceptadas y contratos navegacion.md/operaciones.md de WS11/WS12) quedan en átomos enlazados desde él. El participante que fija P08 recorre Markdown y UI real, links/roots verificables (root = alias/root autorizado por el contrato de navegación; un enlace es verificable si resuelve a un path existente del repo enlazado), commit por `deskops closeout commit`, acta deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md y commit; no publicar solo ejemplo como si fuera ecosistema real y el mapa publicado corresponde a las entradas/índices validados en Taller. Escribir una entrada en un proyecto adicional requiere su tarea de repo y acuerdo de alcance.

## Dependencias

Tareas: WS17, WS30. Gates: G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS43/0a10feb9fdb122c06e668909e323edb316631df2ecc44c36d5b18cb853d6f6c7/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
