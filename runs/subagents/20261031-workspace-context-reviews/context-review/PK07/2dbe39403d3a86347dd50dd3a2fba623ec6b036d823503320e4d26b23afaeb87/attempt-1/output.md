## REFORMULACION
Propósito: agrupar como macroencargo dos extensiones independientes, Changes y modelos, sin convertirlas en prerrequisito del lector o manual básico. Resultado sustantivo: paquete con dos entregas evidenciadas: WS29 integra Changes e impacto comprobable; WS39 integra inspección/edición de modelos existentes. No es resultado el gate `context_review`. Repo dueño: deskops; hijos en graph_ui. Límites: la agrupación no ejecuta, no autoriza tareas ni añade aristas; WS29 no repara automáticamente; WS39 no reimplementa modelos ni habilita promover sin API/autoridad; no se presume CST/Kimun; el manual solo etiqueta cada extensión según evidencia.

## AMBIGUEDADES
1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». No se define artefacto, responsable ni prueba de esa “integración”, y WS29/WS39 no comparten salida ni arista. Obliga a inventar si integrar significa validación conjunta, mera coexistencia en el workspace o etiquetado del manual.

## DRY-RUN
Hipotético: WS29 y WS39 no dependen entre sí; orden posible WS29→WS39 o paralelo, sin transferencia entre hermanos. WS29 recibe de WS15 errores/modo degradado y de WS24 lectura/vecindad; produce delta Changes, pruebas con store temporal y enlaces a comandos de diagnóstico. WS39 recibe contrato WS12 y lector WS13; produce entrada Context→Schema, edición/validación por API, prueba UF09 y acta humana. Integración: cada extensión se registra y etiqueta en workspace/manual por su evidencia; no hay artefacto WS29→WS39. Validación integrada futura: ejecutar ambos flujos sobre store temporal, comprobar mutación, impacto a 1 hop y diagnóstico enlazado, y edición/validación con acta; revisar que el manual no atribuya CST/Kimun.

## FUTURO
Ejecución de hijos y sus pruebas; acta humana de WS39/G_HUMAN_MODEL; publicación o etiquetado del manual por WS31; gates G_UI_READ, G_UI_WRITE y G_WRITE_CONTRACT, más recepción por delta. Nada de esto es ambigüedad.
