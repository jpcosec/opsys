## REFORMULACION

**Propósito:** encargo de planificación del nodo WS24 para integrar conocimiento y grafo local en graph_ui, reutilizando el gráfico actual y un documento genérico para átomos, protoátomos, crossroads, materializaciones y pills, con clasificación y vecindad.

**Resultado:** delta de lectura en las vistas de grafo/Context del workspace, con navegación ida/vuelta y backlinks derivados de la API de grafo de sldb; no un renderer nuevo por clase.

**Repo dueño:** `graph_ui`. **Límites:** depende de WS13 y WS18; requiere `G_UI_READ` (pendiente, resuelto por WS11); promoción `not_authorized`; sin duplicado paralelo; output_scope acotado a `frontends/mindmap/views/workspace/graph/; Context; tests/`.

## AMBIGUEDADES

1. **“crossroads”**: «Reutilizar gráfico actual y documento genérico para átomos/protoátomos/crossroads/materializaciones/pills». No aparece definido en brief.md ni en el glosario. Obligaría a inventar qué entidad es y cómo se representa.

2. **“documento genérico”**: «documento genérico para átomos/protoátomos…». El glosario define “Documento” y “Vista de trabajo”, pero no este componente. Obligaría a inventar qué contrato o componente existente se reutiliza.

3. **Referencia normativa ausente**: «Backlinks = relaciones entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md». Ese archivo no consta en el input ni se identifica nodo que lo produzca. Obligaría a inventar la semántica de backlinks y la capacidad real de la API.

4. **Aceptación no comprobable**: «soporte no modelado visible». No define qué cuenta como “soporte no modelado” ni qué evidencia demuestra “visible”. Obligaría a inventar el criterio de aceptación.

5. **“tarea actual”**: «preservar Code local de tarea actual» y «Code local = proyección Code del ticket workspace». No se identifica la tarea concreta entre las draft de graph_ui. Obligaría a inventar el destino de integración.

## DRY-RUN

**Lecturas:** dag.yaml WS24; brief, alcance, decisiones, cobertura, reconciliación; contratos vecinos WS13/WS18 solo como referencia; `auditoria/infraestructura.md` (ausente en el input).

**Cambios previstos:** delta de lectura en vista de grafo/Context y tests; reutilización del gráfico y documento genérico; backlinks desde API de grafo; conservación de Code local.

**Dependencias:** WS13 (agregado lector), WS18 (ViewDoc/NotationDoc), `G_UI_READ` pendiente; WS11/WS12 de forma transitiva.

**Validaciones futuras:** acta `G_UI_READ`; navegación ida/vuelta y backlinks; soporte no modelado; pruebas sobre store temporal real; validación humana WS30. Nada ejecutado.

## FUTURO

WS11 produce la aceptación `G_UI_READ`; WS13.1–13.3 entregan el lector; WS18 declara proyecciones; WS07 identifica al responsable de graph_ui; WS30 registra validación humana; el dueño del repo promueve la tarea tras preflight. Las decisiones P01/P04/P07/P08/P09 y la política de escritura quedan para actores humanos.
