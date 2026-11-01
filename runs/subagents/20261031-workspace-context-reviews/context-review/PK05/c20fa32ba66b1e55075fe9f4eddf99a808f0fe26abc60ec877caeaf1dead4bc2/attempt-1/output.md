## REFORMULACION

**Propósito:** agrupar la Entrega M: autoría manual segura, intake/trabajo y revisión/cierre mediante handoff verificable. **Resultado:** paquete integrado —contrato de operaciones, edición de campos con conflicto, guardado fuente reversible, precondición de payload, captura/triage, autoría y Board, diff/evidencia, cierre por handoff, operaciones de conocimiento— validado por una aceptación humana WS30. **Repo dueño:** deskops para el paquete de planificación; las implementaciones pertenecen a graph_ui y sldb según cada hijo. **Límites:** agrupación sin ejecución propia ni tareas nuevas; no autoriza implementación, actas ni permisos; no hay commit ni closeout HTTP; mutaciones UI esperan G_HUMAN_READ; Scion queda fuera.

## AMBIGUEDADES

ninguna

## DRY-RUN

PK05 no se ejecuta: termina cuando terminan sus hijos. Hipotéticamente:

1. **WS12** publica `contratos/operaciones.md` (whitelist, precondición, efectos) y alimenta a WS19, WS20, WS45, WS25, WS26, WS27, WS28 y WS42.
2. **WS45** consume WS12, entrega inventario y pruebas focalizadas, y produce G_PAYLOAD_PRECONDITION para WS19/WS21. **WS20** consume WS12 y produce G_SOURCE para WS21 editable.
3. **WS19** espera WS12 y ese gate; sus hijos entregan edición/relaciones y alimentan WS21, WS42 y WS30. **WS25** entrega captura/triage. **WS27** (tras WS13+WS12) entrega diff/evidencia a WS28.
4. **WS26** espera WS22 externo y WS12; sus hijos entregan autoría/Board. **WS42** espera WS19+WS24 externo+WS12 y entrega operaciones de conocimiento. **WS21** espera WS19, el gate y, en editable, G_SOURCE.
5. **WS28** espera WS27+WS12 y entrega verificación/handoff de cierre. **WS30** recibe WS17/21/22/23/24/25/26/28/42 y ejecuta la aceptación humana UF02–05 y navegación.

Si falta contrato, API o permiso, se detiene y registra el hueco sin sustituto; la operación queda no disponible. Validación integrada: roundtrip/conflicto/protegidos, rechazo observable de precondición obsoleta, guardado sin commit, evidencia distinta, cierre confirmado por Deskops/commit y acta WS30.

## FUTURO

WS16 produce G_HUMAN_READ; WS17/22/23/24 aportan entradas externas; el receptor P01 emite actas por delta; WS30 produce el acta humana. La promoción fija TaskDocs, archivos y escenarios; commits, closeout y recibos G_SLDB_WRITE/G_UI_WRITE/G_WRITE_CONTRACT ocurren fuera de este nodo.
