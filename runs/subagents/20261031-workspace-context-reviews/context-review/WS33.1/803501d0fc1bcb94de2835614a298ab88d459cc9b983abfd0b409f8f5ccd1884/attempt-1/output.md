REFORMULACION
Propósito: vincular mensajes y resultados de Scion a un intento existente, con deduplicación y procedencia. Resultado: backend documental en deskops (`runtime/` con adaptador definido por contrato, modelos/reportes y tests) que importa de forma repetible sin duplicar ni atribuir una conversación completa a un intento; lo no resoluble queda como hueco de procedencia. Repo dueño: deskops. Límites: no UI, no dispatch/reply, no tablas Scion, no inventar contrato; depende de WS32 y requiere G_SCION y G_WRITE_CONTRACT; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
No es agregado. Un ejecutor futuro, tras recibir WS32 y los gates, leería `dag.yaml`/WS33.1, `task_file`, contrato WS12, inventario WS05 y evidencia WS44 sobre ids/campos, además de `runtime/scion.py`, modelos/reportes y tests existentes. Cambios previstos: adaptador de importación en `runtime/` según contrato; modelo/reporte de vínculos y huecos; pruebas de importación repetida. Consumiría G_SCION (API pública verificada) y G_WRITE_CONTRACT (operación, campos, efectos); WS32 aporta identidad/cierre. Si falta contrato, id de intento o API, se detendría y registraría hueco con dueño, sin sustituto. Errores esperados: mensaje con varios intentos o sin intento resoluble → no vínculo y hueco; duplicado → no nueva fila; fuente sin id → hueco. Validación: repetir la misma importación no duplica mensajes/resultados, no atribuye conversación completa, conserva procedencia y no toca tablas Scion; tests con contrato real.

FUTURO
WS12 fija la operación pública y campos; WS05/WS44 comprueban API e ids; WS32 produce identidad de intento/cierre; WS33.2 registra decisión humana; el TaskDoc de promoción fija archivos, pills y evidencia; el operador Scion y la resolución de G_SCION/G_WRITE_CONTRACT corresponden a otros nodos o a decisión humana.
