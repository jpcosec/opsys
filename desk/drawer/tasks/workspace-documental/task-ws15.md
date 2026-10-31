---
id: WS15
status: candidate
owner_repo: graph_ui
depends_on:
- WS13
requires:
- G_UI_READ
---

# Mostrar errores de lectura y modo degradado

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Referencia rota, documento ausente, modelo no importable, backend caído y fuente no editable; error localizado sin borrar historial ni fingir vacío. UF10: proyecto sin desk muestra orientación, destino explícito e init CLI; nunca inicializar por GET. Tras init externo real, refrescar lectura. Incluye errores de instalación/CDN como límites visibles.

## Aceptación

Leer Markdown existente cuando soporte permita, informar límites reales, recuperar conexión sin perder contexto. CDN actual diagnosticado; empaquetado offline queda fuera.

## Dependencias

Tareas: WS13. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
