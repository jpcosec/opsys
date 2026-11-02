---
id: WS47
status: candidate
owner_repo: sldb
node_role: delivery
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT
---

# Proteger contenido no declarado en la edición por campos de /save

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `sldb`. Tamaño relativo: S.

inventario y pruebas focalizadas; src/sldb/api/documents/ y src/sldb/cli/serve/ solo para la guarda; tests/

Base explícita: `sldb:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Productor planificado de la guarda de conservación de contenido no declarado (HO-07 del contrato WS12, sección 6.7), distinta de la precondición de WS45 (igualdad de payload por expected) y de la protección de campos del adaptador de la UI. Canal elegido por el contrato, la edición por campos que termina en save_document_payload (POST /save update y update de graph_ui local). Primero inventario con ruta, símbolo y commit de refuse_structural_noise y refuse_undeclared_frontmatter, que create_document y track_document_file ya aplican al Markdown que se crea, y de la guarda de deskops edit sobre el archivo previo; la guarda de este nodo inspecciona el archivo previo y el efecto de reescribirlo, no solo el render nuevo, y reutiliza ese criterio antes de crear otro. No amplía WS45, no cambia la creación, no resuelve el gap de prevalidación de update capturado en el inbox de sldb (si toca el mismo código, las ediciones van en serie) y no se sustituye con un workaround de Deskops.

## Aceptación

Pruebas reales focalizadas en sldb sobre el canal elegido, tras recibo G_SLDB_WRITE para este delta. La guarda inspecciona el archivo previo y el efecto de reescribirlo, no solo el render nuevo, con un piso de detección, que son las comprobaciones de la guarda de deskops edit (_write_doc) leídas en fuente, que no se rebaja y que solo se amplía si el inventario lo justifica; refuse_structural_noise y refuse_undeclared_frontmatter se reutilizan donde apliquen. La aceptación declara qué pérdida detecta, qué casos no detecta y qué casos quedan deshabilitados; un residuo declarado no aprueba una pérdida conocida dentro del alcance que el nodo pretende habilitar. Un update con expected vigente que perdería contenido no declarado del archivo se rechaza con error observable y sin cambios; un update seguro, cuyo render no pierde contenido (incluido un documento limpio), se aplica; un expected obsoleto sigue dando 409; la creación no cambia. Sin merge ni restauración, y sin prometer editar todo documento con ruido. Hasta que pasen, WS19.1, WS19.2 y el recorrido directo de WS26.1 no habilitan la edición de documentos con contenido no declarado. Este nodo es plan; no afirma que exista ni que esté implementado o aceptado.

## Dependencias

Tareas: WS12. Gates: G_SLDB_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; no ejecutar. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
