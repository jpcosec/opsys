## REFORMULACION

Propósito: integrar en el workspace una búsqueda navegable sobre texto, campos y semántica, usando la API pública existente. Resultado: resultados que enlazan identidad y contexto, con estados de búsqueda vacía, error y degradación diferenciados. Repo dueño: `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`. Límites: no usar parser propio; no cargar todo el grafo en cada tecla; depende de WS13 y del gate `G_UI_READ`; promoción no autorizada.

## AMBIGUEDADES

1. «Usar find público, no parser propio».
   No se identifica qué API `find` concreta debe usarse, quién la produce ni qué hacer si no existe. Obliga a inventar el contrato, sus parámetros y su semántica de resultados.

2. «Teclado y abrir/volver conservan consulta y foco».
   No define qué recorridos ni qué límites de persistencia cuentan para aceptar la conservación. Obliga a inventar los escenarios comprobables y el criterio de éxito.

3. «Búsqueda vacía/error/degradación diferenciados».
   No delimita qué condiciones producen cada estado ni qué diferencia observable se exige. Obliga a inventar estados de UI y criterios de comprobación.

## DRY-RUN

Lecturas previstas: `dag.yaml#node:WS14`, `dag.yaml#gates` y las fuentes suministradas del plan. No se prevén cambios: este nodo es candidato y su promoción está `not_authorized`. Dependencias: WS13 (agregado) y `G_UI_READ` pendiente, lo cual es intencional. Validaciones futuras: comprobar que la búsqueda usa la API pública acordada, que los resultados preservan identidad/contexto, que los estados vacío/error/degradación son distinguibles y que teclado/abrir-volver mantienen consulta y foco sin recargar el grafo completo.

## FUTURO

WS11 debe resolver `G_UI_READ` y registrar la aceptación del responsable de `graph_ui`; la promoción debe precisar archivos, TaskDoc, átomos y evidencia. La existencia o ausencia de la API `find` debe aclararse en el contrato o en el nodo predecesor correspondiente, no inferirse aquí.
