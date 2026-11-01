## REFORMULACION  
**Propósito:** agrupar la entrega de autoría y operación manual segura: edición por campos, guardado fuente, intake/trabajo, evidencia y cierre por handoff.  
**Resultado:** paquete verificable cuyos hijos producen contrato, API/precondición, UI y acta humana integrada.  
**Repo dueño:** `deskops`.  
**Límites:** agregado no ejecutable; no autoriza tareas ni añade aristas; no implementa UI/API ni acepta deltas; los gates pendientes son intencionales; Scion queda fuera; no hay commit ni closeout HTTP automáticos.

## AMBIGUEDADES  
ninguna.

## DRY-RUN  
PK05 no se ejecuta: termina cuando terminan sus hijos. Un ejecutor futuro leería `dag.yaml`, guía, brief/alcance/decisiones, contratos WS12 y manifiesto WS40; no modificaría archivos propios. Crearía tareas de promoción solo para hijos `ready`, respetando gates y solapamientos.

Orden hipotético: WS12 publica `contratos/operaciones.md`. Con WS12, WS45 inventaría/prueba la precondición y emite `G_PAYLOAD_PRECONDITION`; WS20 verifica/completa raw-source y emite `G_SOURCE`. Después, con WS12 y `G_PAYLOAD_PRECONDITION`, WS19 integra campos/conflicto y sus hijos. Con WS19 y, en editable, WS20/`G_SOURCE`, WS21 integra fuente/render. WS25 hace captura/triage; WS27 requiere WS13+WS12; WS26 requiere WS22+WS12; WS42 requiere WS19+WS24+WS12; WS28 requiere WS27+WS12. Finalmente WS30 recibe salidas de WS17/21/22/23/24/25/26/28/42.

Cambios previstos: solo en los `output_scope` de los hijos —contratos, inventario/pruebas sldb, vistas/tests graph_ui y acta WS30—, no en PK05. Errores: contrato, API, dato o gate faltante detiene el hijo, registra hueco con repo dueño y no crea sustituto; fallo de conflicto/buffer/protegidos abre tarea en el nodo causal. Validación integrada: acta humana WS30 sobre UF02–05 y navegación, con paths/hashes, evidencia declarada/encontrada/verificada y cierre confirmado por Deskops/commit externo; `G_HUMAN_READ` antes de mutaciones UI.

## FUTURO  
WS12 fija la representación de la precondición; WS45 emite su veredicto; WS20 emite `G_SOURCE`; el responsable P01 acepta deltas; WS30 produce el acta humana; WS16/G_HUMAN_READ habilita uso UI; Deskops/CLI confirma el cierre. Nada de eso se decide aquí.
