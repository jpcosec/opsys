REFORMULACION
Propósito: integrar en la vista de ejecución de `graph_ui` la delegación e intervención humanas, invocando solo el adaptador WS34 para dispatch/reply y registrando decisiones con WS33.2. Resultado: vista de ejecución y tests que prueben respuesta vinculada al intento, confirmación, actor humano y evidencia enlazada. Repo dueño: `graph_ui`; salida acotada a `frontends/mindmap/views/workspace/execution/`, ruta fina autorizada por WS12 y `tests/`. Límites: no autoaprobación ni simulación, no sustituir el adaptador, gates y contrato pendientes, y ninguna ejecución en esta revisión.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS36, bloques de WS34/WS35/WS37 y gates. No se detecta dato que obligue a inventar resultado, aceptación, repo, actor o dependencia.

Cambios previstos: ninguno; esta revisión no modifica el nodo ni ejecuta código.

Dependencias: WS34 es agregado y termina con WS34.1/WS34.2; WS35 cubre la lectura de ejecución y trazabilidad. WS33 y WS12 quedan transitivamente cubiertos por WS34/WS35. WS33.1/WS33.2 se nombran como fuente de resultados y decisiones; si faltan, aplica la regla común de detenerse y registrar el hueco.

Validaciones futuras: comprobar que el adaptador WS34 confirma dispatch/reply y vincula el intento; que WS33.2 permite registrar decisiones con actor; que G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT estén resueltos antes de ejecutar; que los tests cubran respuesta, revisión con actor/evidencia y error visible por ausencia de API o permisos, sin autoaprobación.

FUTURO
WS37 valida la delegación con agente real y acta humana. WS07 designa al operador Scion y WS44 produce G_SCION; WS12 produce G_UI_WRITE/G_WRITE_CONTRACT. Las propuestas Pxx siguen pendientes de decisión humana y no se resuelven aquí.
