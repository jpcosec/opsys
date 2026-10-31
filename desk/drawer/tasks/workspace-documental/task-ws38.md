---
id: WS38
status: candidate
owner_repo: deskops
depends_on:
- WS37
- WS31
requires:
- G_HUMAN_DELEGATE
---

# Publicar capítulos verificados de delegación

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

docs/workspace-user-manual.md; desk/atoms/ vinculados

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Añadir instrucciones runtime y revisión trazable, con lo que funciona y fallos demostrados.

## Aceptación

Capturas y operaciones reales; mantención de contratos y autorización documentadas.

## Dependencias

Tareas: WS37, WS31. Gates: G_HUMAN_DELEGATE. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
