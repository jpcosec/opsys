---
id: WS31
status: candidate
owner_repo: deskops
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL
---

# Publicar manual documental básico probado

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

docs/workspace-user-manual.md; desk/atoms/ vinculados

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Publicar navegación, edición, captura, trabajo manual y revisión demostradas; actualizar índice/capturas/limitaciones.

## Aceptación

Cada instrucción tiene evidencia vigente; etiquetas, links y atom->doc verificados. Scion solo capítulo marcado propuesto hasta WS38. Para capítulos que mencionen personalización o impacto, comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta; no bloquear manual básico por esos extras.

## Dependencias

Tareas: WS30, WS10, WS43. Gates: G_HUMAN_MANUAL. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
