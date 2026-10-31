## REFORMULACION
**Propósito:** fijar WS34 como agregado de implementación que expone un adaptador público restringido para despacho y respuesta Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.

**Resultado:** agregado no ejecutable; se completa cuando WS34.1 y WS34.2 cumplen su aceptación. Su salida es la suma de las salidas de ambos hijos.

**Repo:** `deskops` (`output_base: deskops:repository_root/`), con `task_file` y promoción no autorizada.

**Límites:** solo adaptador autorizado; no shell arbitrario, no duplicar transporte, no sustituir broker. Los gates `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT` siguen pendientes o no verificados; dependencias declaradas: WS33, WS12 y los dos hijos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura y bloques DAG de WS34 y sus hijos; el `task_file` referido no viene incluido en el input. Sin ejecución.

**Cambios previstos:** ninguno en esta revisión. Si se promoviera, las salidas previstas son las de WS34.1/WS34.2 (`runtime/`, `cli/commands/runtime.py` o API definida, `tests/`), bajo `deskops`.

**Dependencias:** WS33 aporta referencias e identidad de intento; WS12, contrato de escritura y política del coordinador; WS34.1/WS34.2, implementación y evidencia. `G_SCION` depende de WS44; `G_EXEC`, de autorización humana externa; `G_WRITE_CONTRACT`, de WS12.

**Validaciones futuras:** probe Scion de WS44, autorización humana de `G_EXEC`, contrato de WS12, demostración con agente real de aceptación/fallo y respuesta vinculada al intento, preflight y autorización de promoción.

## FUTURO
WS07/humano resuelve gates y designa operador Scion; WS44 produce `G_SCION`; WS12 produce `G_WRITE_CONTRACT`; WS34.1/WS34.2 ejecutan y evidencian; WS36 consume el adaptador; un humano autoriza ejecución y promoción. Nada de esto se decide en esta revisión.
