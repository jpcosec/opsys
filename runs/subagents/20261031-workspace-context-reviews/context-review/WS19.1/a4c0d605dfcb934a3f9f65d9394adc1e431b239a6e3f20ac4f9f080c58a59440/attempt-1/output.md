## REFORMULACION
**Propósito:** fijar el encargo de edición de campos en el workspace reutilizando editores y API, con revisión CAS y conflicto visible.  
**Resultado:** delta en `graph_ui` (`frontends/mindmap/views/workspace/fields/` y `tests/`) que permite guardar/recargar un dato real, conserva el texto local ante una escritura obsoleta y excluye campos workflow-protegidos.  
**Repo:** `graph_ui`.  
**Límites:** mutación solo en desk y modo manual exclusivo P03; otros modos read-only; sin cambios de contrato; sin ejecución; promoción no autorizada.

## AMBIGUEDADES
1. «Delta sobre ticket draft de edición». No se identifica el ticket/Board receptor concreto; obligaría a inventar cuál es el ticket existente y su alcance exacto, pese a que `integration_mode` alude a un ticket draft.
2. «conflicto visible (mensaje de rechazo con el texto local conservado)» frente a la aceptación «una escritura obsoleta no pierde texto local». La aceptación no exige comprobar que el conflicto sea visible; obligaría a inventar el criterio de visibilidad y la evidencia que lo demuestra (sin fijar aquí textos de pantalla).

## DRY-RUN
**Lecturas:** nodo WS19.1, contratos de WS12/WS16, guía, brief, alcance, decisiones, reconciliación y gates.  
**Cambios previstos:** componentes de campos y pruebas en `graph_ui`; consumo de endpoints WS12 sin modificarlos.  
**Dependencias:** contrato/whitelist y capacidades de WS12; acta humana de WS16; gates `G_UI_WRITE`, `G_WRITE_CONTRACT`, `G_HUMAN_READ`; P03/P04.  
**Validaciones futuras:** guardar/recargar dato real; escritura CAS obsoleta conserva texto local; campos protegidos no editables; otros modos read-only; preflight de promoción. Sin ejecutar.

## FUTURO
WS12 produce whitelist, capabilities y resuelve gates de escritura; WS16 produce acta humana; WS07 designa responsables y registra P03/P04; WS19.2 cubre relaciones; la promoción fija archivos, pruebas y textos; el humano aprueba gates; WS19 cierra cuando ambos hijos cumplen.
