## REFORMULACION

**Propósito:** agrupar dos extensiones independientes del workspace documental, con evidencia propia y sin convertirlas en prerrequisito del lector o manual básico.

**Resultado sustantivo:** dos deltas integrados en `graph_ui`: (1) Changes con impacto comprobable —mutación real, documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, sin reparación automática—; (2) inspección/edición de modelos existentes desde documento/contexto, con pruebas API y acta humana propia. El manual debe etiquetar cada extensión según evidencia, sin presumir CST/Kimun.

**Repo dueño:** PK07 en `deskops`; hijos en `graph_ui`. **Límites:** PK07 no ejecuta, no añade aristas ni autoriza tareas; sus hijos no bloquean lector/manual básico.

## AMBIGUEDADES

1. «Manual etiqueta cada extra según evidencia» — PK07 no identifica qué nodo produce ese manual, dónde se verifica el etiquetado ni qué hacer si falta. Obligaría a inventar productor, dueño y comprobación.
2. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» — «integración indicada» no se concreta en el nodo; los hijos se declaran independientes. Obligaría a inventar un artefacto o prueba de integración conjunta no definidos.

## DRY-RUN

- **Orden:** hijos independientes, sin arista entre sí; pueden avanzar en paralelo. WS29 espera lectura/vecindad de WS15/24; WS39 espera contrato WS12 y lector WS13.
- **WS29:** lee store temporal real y API de grafo; produce vista Changes, relaciones a 1 hop, errores agrupados y enlaces a comandos documentados, más tests.
- **WS39:** lee contrato WS12, panel Context de WS13 y editor existente inventariado; produce integración Schema/editor, tests y acta humana en la ruta indicada.
- **Transferencia:** no hay artefacto conjunto entre ambos; cada extensión entrega evidencia propia.
- **Validación futura:** mutación e inspección en store temporal; verificación de efectos/errores según WS12; acta UF09; etiquetado del manual según evidencia. No se ejecuta ahora.

## FUTURO

WS15/24 y WS12/13 producen entradas; WS31 publica el capítulo de manual; el participante P08 firma el acta; la recepción de gates y la decisión de disponibilidad corresponden a actores humanos y nodos receptores, no a PK07.
