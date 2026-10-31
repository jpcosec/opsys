## REFORMULACION
**Propósito:** agrupar, sin ejecución propia, dos extensiones independientes del workspace documental: Changes/impacto (WS29) y modelos existentes (WS39), para que cada una aporte evidencia propia y el manual las etiquete según evidencia real, sin presumir CST/Kimun.

**Resultado:** paquete planificado con WS29 —mutación real en store temporal, impacto entrante/saliente a 1 hop, hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, sin reparación automática— y WS39 —inspección/edición de Schema vía API existente, entrada desde Context, validación y acta humana—. PK07 no ejecuta: completa cuando sus hijos cumplen y la integración indicada se verifica.

**Repo:** PK07 pertenece a `deskops`; ambos hijos a `graph_ui`.

**Límites:** no añade aristas ni autoriza tareas; ninguna extensión bloquea lector/manual básico; no reimplementa modelos, no repara automáticamente, no presume CST/Kimun; no autoriza dispatch/Scion.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
No hay arista entre WS29 y WS39: el orden hipotético es paralelo, sujeto a sus dependencias. WS29 espera WS15/WS24; recibe lectura, errores/modo degradado y vecindad; produce vista Changes, pruebas sobre store temporal y evidencia de mutación/impacto. WS39 espera WS12/WS13; recibe contrato de operaciones/escritura y panel Context; produce acceso a Schema, editor existente, pruebas y acta humana. No hay artefacto que pase de WS29 a WS39 ni viceversa.

Integración: el manual etiqueta cada extensión según evidencia; validación por pruebas de WS29, prueba UF09/acta de WS39 y G_HUMAN_MODEL, sin exigir aceptación conjunta ni bloquear lector/manual básico. No se ejecuta nada.

## FUTURO
Recepciones técnicas por delta, gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT` y `G_HUMAN_MODEL`, acta humana con participante P08, publicación/etiquetado del manual por WS31 y cualquier autorización de implementación o Scion. Nada de ello se decide en este nodo.
