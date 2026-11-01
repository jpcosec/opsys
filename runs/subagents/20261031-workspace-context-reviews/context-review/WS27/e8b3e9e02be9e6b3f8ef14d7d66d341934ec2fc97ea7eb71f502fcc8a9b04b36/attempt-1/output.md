## REFORMULACION
**Propósito:** revisar WS27 como encargo de planificación agregado que integra la revisión de cambios y evidencia.
**Resultado:** agregado no ejecutable; se completa cuando WS27.1 y WS27.2 cumplen su aceptación. Sus dependientes siguen dependiendo de WS27.
**Repo dueño:** `graph_ui`.
**Límites:** no ejecuta por sí mismo ni añade alcance; su salida es la agregación de las salidas de WS27.1 y WS27.2. Requiere `G_UI_READ` por delta y no debe inferir cierre por commit; la reconciliación queda pendiente de aceptación del nodo/delta.

## AMBIGUEDADES
Ninguna. El nodo se entiende como agregado: propósito, repo, hijos, dependencias, salida y aceptación están delimitados. No obliga al ejecutor de WS27 a inventar resultado, aceptación ni límites; el detalle operativo pertenece a WS27.1/WS27.2 y a su promoción.

## DRY-RUN
- **Lecturas:** `dag.yaml` (WS27, WS13, WS12, WS27.1, WS27.2, gates), guía de revisión, brief, alcance, decisiones y cobertura.
- **Cambios previstos:** ninguno propio; WS27 no se ejecuta como tarea. Solo agrega resultados de sus hijos.
- **Dependencias:** WS13 y WS12, más WS27.1 y WS27.2 como hijos/dependencias.
- **Validaciones futuras:** aceptación de WS27.1 y WS27.2; recibos `G_UI_READ` por delta concreto; revisión de reconciliación. No se ejecuta nada.

## FUTURO
WS27.1 produce el diff Git read-only; WS27.2 produce la evidencia declarada/encontrada/verificada. El receptor humano P01 emite, si procede, el acta de recepción por delta en el repo dueño. WS28 y WS35 consumen WS27 según sus dependencias. La reconciliación y el estado de aceptación los decide el proceso humano/receptor, no este nodo.
