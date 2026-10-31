---
id: WS45
status: candidate
owner_repo: sldb
node_role: delivery
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT
---

# Verificar o completar la precondición de escritura de payload

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `sldb`. Tamaño relativo: M.

inventario y pruebas focalizadas; src/sldb/api/documents/ y src/sldb/cli/serve/ solo si al ejecutar falta capacidad; tests/

Base explícita: `sldb:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Productor planificado, independiente de source_mode y de raw-source (WS20 conserva raw-source). Distingue tres cosas, sin negar la capacidad optimista real ni inferir frescura por CLI; before-image por valor existente (`expected`, HTTP 409, C-40), token publicado (`version`/`content_hash`, C-38) y comparación o escritura pública con precondición compartida, aún no probada. Primero reutilizar; inventario con path, símbolo y commit de la capacidad existente en sldb frente al contrato WS12 (representación de la precondición, operaciones y escritores alcanzados); luego pruebas reales focalizadas; código solo si al ejecutar falta capacidad, con tarea propia en sldb. No fuerza CAS en toda CLI ni elige un algoritmo de hash por inercia, y no mezcla UI ni productor condicional alguno. P03 no cambia.

## Aceptación

Inventario entregado y, para cada operación y escritor que el contrato WS12 alcance, una prueba real focalizada que muestra que una precondición obsoleta se rechaza sin cambios, una vigente se aplica y el rechazo es observable por el llamante. Si la capacidad existe, esas pruebas bastan y no se duplica código; si es parcial, se completa solo lo faltante y se vuelve a probar todo el contrato, tras recibo G_SLDB_WRITE para este delta. G_PAYLOAD_PRECONDITION se satisface solo con esa evidencia verificable. Este nodo es plan; no afirma que exista ni que esté implementado o aceptado.

## Dependencias

Tareas: WS12. Gates: G_SLDB_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; no ejecutar. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
