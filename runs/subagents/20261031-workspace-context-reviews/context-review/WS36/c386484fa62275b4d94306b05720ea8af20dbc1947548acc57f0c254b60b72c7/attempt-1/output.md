## REFORMULACION
**Propósito:** integrar en `graph_ui` la delegación e intervención humanas sobre ejecución Scion. **Resultado:** dispatch/reply mediante el adaptador WS34 y registro de decisión con WS33.2, con revisión de actor humano y evidencia enlazada; errores por ausencia de API/permisos visibles y probados. **Repo dueño:** `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador WS34 autorizada por WS12, y `tests/`. **Límites:** invocar solo el adaptador WS34 para dispatch/reply; no autoaprobación ni simulación; requires y gates pendientes; promoción no autorizada. No se ejecuta nada.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** nodo WS36 en `dag.yaml`, guía, brief, alcance, decisiones y cobertura; contratos vecinos WS34, WS35 y WS33.2, y gates G_EXEC/G_SCION/G_UI_WRITE/G_WRITE_CONTRACT, solo como referencia. **Cambios previstos:** implementación futura en `graph_ui` dentro de `output_scope`, sin ejecutar ni promover. **Dependencias:** WS34 y WS35; WS33.2 como contexto de revisión y registro de decisión; WS12 como fuente del contrato de operación. **Validaciones futuras:** tests de respuesta vinculada al intento y operación confirmada; revisión con actor humano y evidencia WS33.1/WS33.2; error visible ante ausencia de API/permisos; no autoaprobación ni simulación. WS37 validará con agente real.

## FUTURO
WS12 debe fijar el contrato de operación; WS34 expone el adaptador; WS33.2 registra la decisión humana; WS37 ejecuta la validación real. G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT los resuelven el humano/operador o el receptor del delta. La promoción y el TaskDoc fijarán archivos, textos y pruebas concretas.
