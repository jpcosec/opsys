## REFORMULACION

**Propósito:** WS26 integra autoría explícita desde candidato, evidencia, dependencias, contexto/pills, enrutamiento en Board y representación de capa lista.

**Resultado:** es un `aggregate` no ejecutable; se cumple cuando WS26.1 y WS26.2 cumplen su aceptación.

**Repo:** `graph_ui`.

**Límites:** no confunde Board route con ejecución; no implementa promoción nueva; solo invoca una operación completa admitida por WS12 o deja handoff. Los gates son por delta; `G_HUMAN_READ` habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas de API.

## AMBIGUEDADES

Ninguna. El nodo declara propósito, resultado agregado, repo, límites, dependencias y aceptación comprobable mediante sus hijos. Los detalles de archivos, textos y pruebas quedan delegados a promoción/TaskDoc y a los hijos, conforme a la guía.

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura y definición de WS26 con sus hijos. Los bloques `edge` de WS12/WS22 se usan solo como contratos referenciados; no se revisan.

**Cambios previstos:** ninguno; no se ejecuta ni promueve nada.

**Dependencias:** WS12 aporta contrato de operaciones/escritura; WS22 aporta representación de Board; WS26.1 y WS26.2 producen las salidas agregadas. Gates requeridos: `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, con evaluación por delta.

**Validaciones futuras:** aceptación de WS26.1 y WS26.2; recibos por delta de `G_UI_WRITE`/`G_WRITE_CONTRACT`; preflight de promoción limitado a tarea, archivos, pills, átomos y evidencia. No hay validación ejecutable propia de WS26.

## FUTURO

WS26.1 y WS26.2 implementan autoría/contexto y enrutamiento/capa lista. WS12 produce el contrato técnico aplicable; WS22, la representación de Board. El receptor humano P01 emite actas por delta en el repo dueño. WS30 valida autoría/revisión manual. La promoción de WS26 queda sujeta a autorización y preflight por otro nodo o decisión humana.
