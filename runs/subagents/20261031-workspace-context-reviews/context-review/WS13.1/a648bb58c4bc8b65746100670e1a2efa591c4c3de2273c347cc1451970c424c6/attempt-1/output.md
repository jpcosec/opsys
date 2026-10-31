## REFORMULACION
Propósito: comprobar si WS13.1 se entiende como encargo de planificación para un lector de documento/fuente solo lectura, contexto, enlaces y Code local con foco compartido. Resultado: nodo `implementation` en `graph_ui`, como delta o ticket conciliado sobre el workspace `a1b2b22`, con salida en `views/workspace/document/`, rutas del contrato WS11 y tests. Repo dueño: `graph_ui`. Límites: solo lectura; sin índices nuevos ni workspace independiente; no exigir conocer IDs; `G_UI_READ` pendiente; promoción no autorizada.

## AMBIGUEDADES
1. «La selección por documento/nodo fija el foco del documento abierto: seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten, sin abrir otra copia.» Obliga a inventar si el foco es el documento activo o el elemento/nodo seleccionado dentro de él, y si la selección de un nodo debe propagarse entre texto, graph y Code. El contrato vecino suministrado define el foco como elemento dentro del documento, no como documento abierto; «sin abrir otra copia» tampoco fija la unidad de copia.

2. «output_scope: frontends/mindmap/views/workspace/document/; rutas de lectura definidas por el contrato WS11; tests/» frente a «panel de contexto […] y Code local». Obliga a inventar si el panel y la alternancia Code se implementan dentro de `document/` o si se modifican piezas existentes fuera de ese directorio, y si tocarlas excede el alcance.

3. «Si el acta de WS11 eligió integrar el workspace integrado a1b2b22, su cierre/evidencia sustituye este delta; reutilizar la base implementada a1b2b22 sin dar por aceptado el delta ampliado.» Obliga a inventar qué evidencia sustituye exactamente al delta y si basta verificar `a1b2b22` o debe probarse igualmente la aceptación ampliada; la condición de cierre no es comprobable por sí sola.

## DRY-RUN
Lecturas: nodo WS13.1 y aristas WS11/WS13; guía, brief, alcance, decisiones, cobertura y reconciliación; contrato WS11 y `vistas.md` de WS09 (pendientes); base `a1b2b22`. Cambios previstos: implementar o conciliar en `graph_ui` documento/fuente, contexto, enlaces y Code local, más tests. Dependencias: WS11 (contrato de navegación y acta `G_UI_READ` por delta), WS09 transitiva, `G_PRODUCT`, matriz WS06/WS12 y regla de no duplicar. Validaciones futuras: Markdown sin modelo legible, identidad/relaciones/origen, enlaces, alternancia texto/graph/Code y foco compartido; acta WS11; contraste con `a1b2b22`. Sin ejecutar.

## FUTURO
WS11 produce contrato y acta; WS06/WS12 deciden ticket o delta y evitan duplicación; la promoción fija TaskDoc, archivos y pruebas; WS16/WS30 validan; la persona designada P01 acepta el delta.
