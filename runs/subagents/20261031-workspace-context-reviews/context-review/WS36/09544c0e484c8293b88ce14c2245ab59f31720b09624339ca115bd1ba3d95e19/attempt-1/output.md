## REFORMULACION
Propósito: integrar en el workspace la delegación e intervención humanas invocando solo el adaptador WS34 para dispatch/reply y registrando decisiones humanas mediante WS33.2, con actor y evidencia visibles. Resultado: vista de ejecución en `graph_ui` con operaciones vinculadas al intento, confirmación, errores honestos ante falta de API/permisos y tests. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/execution/` y `tests/`. Límites: no crear API propia, no simular ni autoaprobar; la ruta al adaptador WS34 debe estar autorizada por contrato WS12; gates pendientes bloquean ejecución.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS36, vecinos WS34/WS35/WS37/WS33.2 y gates. Cambios previstos: cablear la vista de ejecución contra el adaptador WS34; registrar decisiones vía WS33.2; mostrar actor/evidencia; cubrir respuesta vinculada, confirmación y ausencia de API/permisos con tests. Dependencias: WS34 y WS35; gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT; contrato WS12; evidencia WS33.1/WS33.2. Validaciones futuras: tests del nodo, recibo per_delta de G_UI_WRITE, contrato G_WRITE_CONTRACT, gates externos y validación con agente real en WS37. Sin ejecutar nada.

## FUTURO
WS12 produce el contrato técnico de la operación de registro; WS34 entrega el adaptador dispatch/reply; WS33.1/WS33.2 producen evidencia y decisión; el humano/externo resuelve G_EXEC, G_SCION y G_UI_WRITE; WS37 valida con agente real. La promoción fijará archivos, pills y textos exactos.
